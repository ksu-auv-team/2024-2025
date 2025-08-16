from . import db

class Input(db.Model):
    __tablename__ = "inputs"
    id          = db.Column(db.Integer, primary_key=True)
    step_index  = db.Column(db.Integer, nullable=False)
    x           = db.Column(db.Float,   nullable=False)
    y           = db.Column(db.Float,   nullable=False)
    z           = db.Column(db.Float,   nullable=False)
    yaw         = db.Column(db.Float,   nullable=False)
    s1          = db.Column(db.Float,   nullable=False)
    s2          = db.Column(db.Float,   nullable=False)
    s3          = db.Column(db.Float,   nullable=False)
    arm         = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "step_index": self.step_index,
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "yaw": self.yaw,
            "s1": self.s1,
            "s2": self.s2,
            "s3": self.s3,
            "arm": self.arm
        }

    def __repr__(self):
        return f"<Input step_index={self.step_index}, x={self.x}, y={self.y}, z={self.z}, yaw={self.yaw}, s1={self.s1}, s2={self.s2}, s3={self.s3}, arm={self.arm}>"
