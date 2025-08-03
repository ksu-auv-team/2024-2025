# db_manager.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify
from db_manager import db

def commit_to_db(instance):
    """
    Add instance to DB and commit.
    """
    try:
        db.session.add(instance)
        db.session.commit()
        return {"status": "success"}
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"status": "error", "message": str(e)}
