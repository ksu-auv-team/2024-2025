# This module contains the business logic for managing database operations.
# libs/db_manager/logic.py
from flask import current_app
from marshmallow import Schema, fields, ValidationError
from .models import db
from .models.inputs import Input
from .models.outputs import Output
# import other sensor models as needed: IMU, Sonar, etc.


class Error(Exception):
    pass


class NotFound(Error):
    status_code = 404


class DuplicateStep(Error):
    status_code = 409


class InputSchema(Schema):
    step_index = fields.Int(required=True)
    direction = fields.Float(required=True)
    force = fields.Float(required=True)


class OutputSchema(Schema):
    step_index = fields.Int(required=True)
    command = fields.Str(required=True)
    status = fields.Str(required=True)


input_schema = InputSchema()
inputs_schema = InputSchema(many=True)
output_schema = OutputSchema()
outputs_schema = OutputSchema(many=True)


def create_input(payload: dict) -> dict:
    data = input_schema.load(payload)
    existing = Input.query.filter_by(step_index=data["step_index"]).first()
    if existing:
        raise DuplicateStep(f"Input with step_index {data['step_index']} already exists")
    obj = Input(**data)
    db.session.add(obj)
    db.session.commit()
    current_app.logger.debug(f"Created {obj!r}")
    return obj.to_dict()


def create_inputs_batch(payloads: list) -> list:
    # Validate full list first
    data = inputs_schema.load(payloads)
    existing_steps = {i.step_index for i in Input.query.filter(Input.step_index.in_([d["step_index"] for d in data])).all()}
    if existing_steps:
        raise DuplicateStep(f"Duplicate step_indexes in DB: {sorted(existing_steps)}")
    objs = [Input(**d) for d in data]
    db.session.bulk_save_objects(objs)
    db.session.commit()
    current_app.logger.info(f"Inserted batch of {len(objs)} Inputs")
    return inputs_schema.dump(data)


def get_input_by_step(step_index: int) -> dict:
    obj = Input.query.filter_by(step_index=step_index).first()
    if not obj:
        raise NotFound(f"No Input found at step_index={step_index}")
    return obj.to_dict()


def get_latest_input() -> dict:
    obj = Input.query.order_by(Input.id.desc()).first()
    if not obj:
        raise NotFound("No Input rows found")
    return obj.to_dict()


def list_inputs(offset=0, limit=100) -> list:
    q = Input.query.order_by(Input.step_index.asc()).offset(offset).limit(limit)
    return inputs_schema.dump(q.all())


def create_output(payload: dict) -> dict:
    data = output_schema.load(payload)
    existing = Output.query.filter_by(step_index=data["step_index"]).first()
    if existing:
        raise DuplicateStep(f"Output with step_index {data['step_index']} already exists")
    obj = Output(**data)
    db.session.add(obj)
    db.session.commit()
    current_app.logger.debug(f"Created {obj!r}")
    return obj.to_dict()


def get_latest_output() -> dict:
    obj = Output.query.order_by(Output.id.desc()).first()
    if not obj:
        raise NotFound("No Output rows available")
    return obj.to_dict()


def list_outputs(offset=0, limit=100) -> list:
    return outputs_schema.dump(Output.query.order_by(Output.step_index.asc()).offset(offset).limit(limit).all())
