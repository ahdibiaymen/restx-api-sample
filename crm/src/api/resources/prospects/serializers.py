from flask_restx import fields
from src.api.resources.namespaces import NAMESPACES

prospects_ns = NAMESPACES["Prospects"]

prospect_fields = {
    "id": fields.Integer(),
    "name": fields.String(),
    "email": fields.String(),
    "company": fields.String(),
    "phone_number": fields.String(),
    "lead_source": fields.String(),
    "status": fields.String(),
    "notes": fields.String(),
    "created_date": fields.DateTime(),
}

prospect_serializer = prospects_ns.model(
    "ProspectGetSerializer", prospect_fields
)

standard_fields = {"status": fields.String(), "message": fields.String()}

standard_serializer = prospects_ns.model("StandardSerializer", standard_fields)
