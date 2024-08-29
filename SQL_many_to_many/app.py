from flask import Flask
from flask_restful import Api
from config import Config
from extension import db, api, migrate
import click

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

    from models.voter import Voter
    from models.voter_candidate import VoterCandidate
    from models.candidate import Candidate

    # with app.app_context():
    #     # Initialize your models and other components
    #     db.create_all()
    # # add reseource to endpoint

    @app.cli.command(name='create_tables')
    def create_tables():
        db.create_all()
        print("Tables created successfully.")

    
    app.cli.add_command(create_tables)


    return app

if __name__ == "__main__":
    # Create tables

    app = create_app()
    app.run(debug=True)

