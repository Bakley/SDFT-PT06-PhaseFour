from .base_model import BaseModel, db
from .voter_candidate import voter_candidate

class Candidate(BaseModel):
    __tablename__ = 'candidate'

    name = db.Column(db.String(80), nullable=False)
    manifesto = db.Column(db.Text, nullable=False)
    party = db.Column(db.String(50), nullable=False)
    region = db.Column(db.String(80), nullable=False)
    votes = db.relationship('Voter', 
                            secondary=voter_candidate,
                            backref=db.backref('candidates', lazy=True)
            )

    serialize_rules = ('manifesto', 'party')

    def to_dict(self):
        res = super().to_dict()
        res['total_votes'] = len(self.votes)
        res['approval_percentage'] = self.calc_app_per()
        return res
    
    def calc_app_per(self):
        total_votes = len(self.votes)
        if total_votes == 0:
            return 0
        
        approve_votes = len([vote for vote in self.votes if vote.score > 0])
        return (approve_votes/total_votes) * 100
    