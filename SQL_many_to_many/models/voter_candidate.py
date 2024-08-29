from .base_model import db

# Association table for the many-to-many relationship between voters and candidates
voter_candidate = db.Table('voter_candidate',
    db.Column('voter_id', db.String, db.ForeignKey('voter.id'), primary_key=True),
    db.Column('candidate_id', db.String, db.ForeignKey('candidate.id'), primary_key=True),
    db.Column('score', db.Integer, nullable=False),  # Stores the rating given by the voter
    db.Column('voted_at', db.DateTime, default=db.func.now())
)
