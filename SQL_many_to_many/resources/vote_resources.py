from flask_restful import Resource
from flask import request
from models.voter_candidate import voter_candidate
from models.candidate import Candidate
from utils import cal_app, find_winner
from extension import db

class VoteResource(Resource):
    def post(self):
        data =  request.get_json()
        vote = voter_candidate.insert().values(**data)

        db.session.execute(vote)
        db.session.commit
        return {
            'message': 'Vote recorded'
        }, 201

    def get(self):
        votes = db.session.query(voter_candidate).all()
        app_perc = cal_app(votes)
        winner_id, max_app = find_winner(app_perc)

        if winner_id:
            win = Candidate.query.get(winner_id)
            return {
                'winner': win.name,
                'approval_percentage': max_app
            }, 200
        
        return {
            "message": "No winner could be determined"
        }, 404
    