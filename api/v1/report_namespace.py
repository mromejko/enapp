from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from api.models import Client, Report, ReportStatus
from api.extensions import db
from api.rabbit import send_message

report_ns = Namespace("reports", description="Report routes")

report_request_model = report_ns.model(
    "ReportRequest", {
        "client_id": fields.Integer(description="Client ID", required=True)
    }
)

report_response_model = report_ns.model(
    "ReportsRequestResponse", {
        "message": fields.String(description="Request response")
    }
)

@report_ns.route('/')
@report_ns.response(201, 'Report request sent')
@report_ns.response(404, 'Client not found')
@report_ns.response(400, 'Bad request')
class ReportClass(Resource):
    @report_ns.expect(report_request_model)
    @report_ns.marshal_with(report_response_model, code=201)
    def post(self):
        data = request.json

        if not data:
            report_ns.abort(400, message="Payload is empty")

        if 'client_id' not in data:
            report_ns.abort(400, message="Key client_id not found")

        if not isinstance(data['client_id'], int):
            report_ns.abort(400, message="client_id is not integer")

        _client = Client.query.get(data['client_id'])

        if not _client:
            report_ns.abort(404, message="Client not found")

        # creating report request

        in_progress_status = ReportStatus.query.filter(ReportStatus.name == "In progress").first()

        _report = Report(
            client=_client,
            status=in_progress_status
        )

        db.session.add(_report)
        db.session.commit()

        send_message({"request": "client.report", "client_id": _client.id, "report_id": _report.id})

        return {"message": "OK"}, 201