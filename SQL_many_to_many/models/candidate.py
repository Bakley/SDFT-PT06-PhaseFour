from .base_model import BaseModel, db
from .voter_candidate import VoterCandidate

class Candidate(BaseModel):
    __tablename__ = 'candidate'

    name = db.Column(db.String(80), nullable=False)
    manifesto = db.Column(db.Text, nullable=False)
    party = db.Column(db.String(50), nullable=False)
    region = db.Column(db.String(80), nullable=False)
    voter_candidates = db.relationship('VoterCandidate',
                            back_populates='candidate'
            )

    serialize_rules = ('manifesto', 'party')

    def to_dict(self):
        data = super().to_dict()
        # res['total_votes'] = len(self.votes)
        # res['approval_percentage'] = self.calc_app_per()
        return data
    
    def calc_app_per(self):
        total_votes = len(self.votes)
        if total_votes == 0:
            return 0
        
        approve_votes = len([vote for vote in self.votes if vote.score > 0])
        return (approve_votes/total_votes) * 100
    