# from .base_model import db

# # Association table for the many-to-many relationship between voters and candidates
# voter_candidate = db.Table('voter_candidate',
#     db.Column('voter_id', db.String, db.ForeignKey('voter.id')),
#     db.Column('candidate_id', db.String, db.ForeignKey('candidate.id')),
#     db.Column('score', db.Integer, nullable=False),  # Stores the rating given by the voter
#     db.Column('voted_at', db.DateTime, default=db.func.now())
# )

from uuid import uuid4
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from .base_model import db

# Association class with additional columns
class VoterCandidate(db.Model):
    __tablename__ = 'voter_candidate'
    voter_id = db.Column(db.String, db.ForeignKey('voter.id'), primary_key=True)
    candidate_id = db.Column(db.String, db.ForeignKey('candidate.id'), primary_key=True)
    score = db.Column(db.Integer, nullable=False)  # Stores the rating given by the voter
    voted_at = db.Column(db.DateTime, default=db.func.now())  # Stores when the vote was cast

    # Relationships
    voter = db.relationship('Voter', back_populates='voter_candidates')
    candidate = db.relationship('Candidate', back_populates='voter_candidates')
