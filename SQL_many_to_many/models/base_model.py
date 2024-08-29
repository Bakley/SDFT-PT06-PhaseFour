from uuid import uuid4
from datetime import datetime
from extension import db

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    update_at = db.Column(db.DateTime, default=datetime.utcnow)

    serialize_rules = ()

    from datetime import datetime

    def to_dict(self):
        """Convert the model instance to a dictionary, converting datetime fields to strings."""
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()  # Convert datetime to ISO format string
        return data
