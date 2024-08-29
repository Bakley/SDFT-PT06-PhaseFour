from flask import Flask
from flask_restful import Api
from config import Config
from extension import db, api, migrate

# apps models
from resources.vote_resources import VoteResource
from resources.candidate_resources import CandidateResource



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    migrate.init_app(app, db)
    api = Api(app)

    api.add_resource(VoteResource, "/voters", "/voters/<string:voter_id>")
    api.add_resource(CandidateResource, "/candidates", "/candidates/<string:candidate_id>")

    from models import voter, candidate, voter_candidate

    with app.app_context():
    #     # Initialize your models and other components
        db.create_all()
    # add reseource to endpoint



    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
