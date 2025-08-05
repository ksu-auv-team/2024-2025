from . import db

class Input(db.Model):
    __tablename__ = 'inputs'
    id = db.Column(db.Integer, primary_key=True)
    step_index = db.Column(db.Integer, nullable=False)
    direction = db.Column(db.String(50), nullable=False)
    force = db.Column(db.Float, nullable=False)
    s1 = db.Column(db.Float, nullable=False)
    s2 = db.Column(db.Float, nullable=False)
    s3 = db.Column(db.Float, nullable=False)
    arm = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "step_index": self.step_index,
            "direction": self.direction,
            "force": self.force,
            "s1": self.s1,
            "s2": self.s2,
            "s3": self.s3,
            "arm": self.arm
        }

    def __repr__(self):
        return f"<Input step={self.step_index}, direction={self.direction}>"
