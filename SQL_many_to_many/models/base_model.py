from uuid import uuid4
from datetime import datetime
from extension import db

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    update_at = db.Column(db.DateTime, default=datetime.utcnow)

    serialize_rules = ()

    def to_dict(self):
        return {
            c.name: getattr(self, c.name) for c in self.__table__.columns if c.name not in self.serialize_rules
            }
