from .base_model import BaseModel, db

from .voter_candidate import voter_candidate

class Voter(BaseModel):
    __tablename__ = 'voter'
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    location = db.Column(db.String(100), nullable=False)

    votes = db.relationship("Candidate", 
                            secondary=voter_candidate,
                            backref=db.backref('voters', lazy=True)
            )

    serialize_rules = ('location',)

    def to_dict(self):
        res = super().to_dict()
        res['total_votes'] = len(self.votes)
        return res
