from .base_model import BaseModel, db
from .voter_candidate import VoterCandidate

class Voter(BaseModel):
    __tablename__ = 'voter'
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    location = db.Column(db.String(100), nullable=False)

    voter_candidates = db.relationship("VoterCandidate",
                            back_populates='voter'
            )

    serialize_rules = ('location',)

    def to_dict(self):
        res = super().to_dict()
        # res['total_votes'] = len(self.votes)
        return res
