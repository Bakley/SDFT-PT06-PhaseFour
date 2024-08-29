from flask_restful import Resource, reqparse
from flask import jsonify
from models.candidate import Candidate
from sqlalchemy.exc import SQLAlchemyError
from extension import db

class CandidateResource(Resource):
    # Parser for handling POST and PUT requests
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='Name cannot be blank')
    parser.add_argument('manifesto', type=str, required=True, help='Manifesto cannot be blank')
    parser.add_argument('party', type=str, required=True, help='Party cannot be blank')
    parser.add_argument('region', type=str, required=True, help='Region cannot be blank')

    def get(self, candidate_id):
        # Retrieve a candidate by ID
        candidate = Candidate.query.get(candidate_id)
        if candidate is None:
            return {'message': 'Candidate not found'}, 404

        return candidate.to_dict(), 200

    def post(self):
        # Create a new candidate
        args = self.parser.parse_args()

        candidate = Candidate(
            name=args['name'],
            manifesto=args['manifesto'],
            party=args['party'],
            region=args['region']
        )

        try:
            db.session.add(candidate)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'Error creating candidate', 'error': str(e)}, 500

        return candidate.to_dict(), 201

    def put(self, candidate_id):
        """
        Update and existing candidate resource

        Replace the entire resource with a new representation
        """

        candidate = Candidate.query.get(candidate_id)
        if candidate is None:
            return {'message': 'Candidate not found'}, 404

        args = self.parser.parse_args()

        candidate.name = args['name']
        candidate.manifesto = args['manifesto']
        candidate.party = args['party']
        candidate.region = args['region']

        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'Error updating candidate', 'error': str(e)}, 500

        return jsonify(candidate.to_dict()), 200

    def patch(self, candidate_id):
        """
        Retrieve the candidate object or return 404 if not found

        Apply partial updates to a resource
        """
        candidate = Candidate.query.get(candidate_id)
        if candidate is None:
            return {'message': 'Candidate not found'}, 404

        # Parse arguments, only update provided fields
        args = self.parser.parse_args()

        # Use a dictionary to map the fields
        fields_to_update = {key: value for key, value in args.items() if value is not None}

        # Using dictionary unpacking and getattr to update only if the value has changed
        try:
            for field, value in fields_to_update.items():
                if getattr(candidate, field) != value:
                    setattr(candidate, field, value)

            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'Error updating candidate', 'error': str(e)}, 500

        return jsonify(candidate.to_dict()), 200


    def delete(self, candidate_id):
        # Soft delete a candidate by marking them as deleted
        candidate = Candidate.query.get(candidate_id)
        if candidate is None:
            return {'message': 'Candidate not found'}, 404

        try:
            db.session.delete(candidate)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'Error deleting candidate', 'error': str(e)}, 500

        return '', 204

# Register the resource with Flask-RESTful
# api.add_resource(CandidateResource, '/candidates/<string:candidate_id>')
