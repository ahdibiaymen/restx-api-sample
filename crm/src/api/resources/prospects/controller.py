from flask_restx import Resource, abort
from src import exceptions
from src.api.resources.namespaces import NAMESPACES
from src.api.resources.prospects.parsers import filter_prospects, new_prospect
from src.api.resources.prospects.serializers import (
    prospect_serializer,
    standard_serializer,
)
from src.api.resources.prospects.service import ProspectService

prospects_ns = NAMESPACES["Prospects"]


@prospects_ns.route("")
class Prospects(Resource):
    @prospects_ns.response(200, "Success")
    @prospects_ns.response(400, "Bad request")
    @prospects_ns.response(401, "Unauthorized")
    @prospects_ns.response(404, "Not found")
    @prospects_ns.response(500, "Internal server error")
    @prospects_ns.expect(filter_prospects, validate=True)
    @prospects_ns.marshal_with(prospect_serializer)
    def get(self):
        """List all prospects (with/without FILTERS)"""
        args = filter_prospects.parse_args()
        prospect_service = ProspectService(**args)
        prospects = prospect_service.get_prospects()
        return prospects

    @prospects_ns.response(200, "Success")
    @prospects_ns.response(400, "Bad request")
    @prospects_ns.response(401, "Unauthorized")
    @prospects_ns.response(404, "Not found")
    @prospects_ns.response(500, "Internal server error")
    @prospects_ns.expect(new_prospect, validate=True)
    @prospects_ns.marshal_with(standard_serializer)
    def post(self):
        """Create new prospect
        LEAD_choices=("REFERRAL",
             "WEBSITE",
             "SOCIAL_MEDIA",
             "EVENT",
             "ADVERTISING",
             "EMAIL",
             "SALES_OUTREACH",
             "PARTNERSHIP",
             "OTHER"),

         STATUS_choices=("NEW_LEAD",
         "CONTACTED",
         "QUALIFIED",
         "PROPOSAL_SENT",
         "NEGOTIATING",
         "CLOSED_WON",
         "CLOSED_LOST",
         "ON_HOLD",
         "DISQUALIFIED",
         "OTHER"),
        """
        args = new_prospect.parse_args()
        prospect_service = ProspectService()
        try:
            prospect = prospect_service.create_new_prospect(args)
        except exceptions.AlreadyExist:
            abort(406, "Prospect Already exists")
        else:
            if prospect:
                http_response = {
                    "status": "success",
                    "message": "NEW_PROSPECT_CREATED",
                }
            else:
                http_response = {
                    "status": "fail",
                    "message": "FAILED_TO_CREATE_PROSPECT",
                }
            return http_response
