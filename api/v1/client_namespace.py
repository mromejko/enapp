from flask_restx import Namespace, Resource, fields
from api.models import Client, Report, ReportStatus, Station

client_ns = Namespace("clients", description="Client routes")

client_list_model = client_ns.model("ClientList", {
    'id': fields.Integer(readonly=True, description='Station ID'),
    'name': fields.String(readonly=True, description='Station name')
})

client_model = client_ns.model('Client', {
    'id': fields.Integer(readonly=True, description='Client ID'),
    'name': fields.String(readonly=True, description='Client name'),
})

station_model = client_ns.model("Station", {
    'id': fields.Integer(readonly=True, description='Station ID'),
    'name': fields.String(readonly=True, description='Station name')
})

report_nested_model = client_ns.model("ReportItem", {
    "id": fields.Integer(readonly=True, description='Report ID'),
    "status": fields.String(readonly=True, description='Report status'),
    "created_at": fields.DateTime(readonly=True, description='Created at'),
    "updated_at": fields.DateTime(readonly=True, description='Updated at')
})

report_list_model = client_ns.model("ClientReportList", {
    "client_name": fields.String(readonly=True, description='Client name'),
    "reports": fields.Nested(report_nested_model, as_list=True, description="Report list")
})

report_model = client_ns.model("Report", {
    "id": fields.Integer(readonly=True, description='Report ID'),
    "report": fields.String(readonly=True, description='Energy report'),
    "created_at": fields.DateTime(readonly=True, description='Created at'),
    "updated_at": fields.DateTime(readonly=True, description='Updated at')
})

energy_model = client_ns.model("EnergyList", {
    'id': fields.Integer(readonly=True, description='Station ID'),
    'energy': fields.String(readonly=True, description='Energy value'),
    'created_at': fields.String(readonly=True, description='Created at')
})

@client_ns.route('/')
class ClientList(Resource):
    @client_ns.marshal_list_with(client_list_model)
    def get(self):
        clients = Client.query.all()
        return clients

@client_ns.route('/<int:id>')
@client_ns.response(404, 'Client not found')
@client_ns.param('id', 'Client ID')
class ClientClass(Resource):
    @client_ns.marshal_with(client_model)
    def get(self, id):
        client = Client.query.get(id)
        if not client:
            client_ns.abort(404, message="Client not found")

        return client

@client_ns.route('/<int:id>/reports')
@client_ns.response(404, 'Client not found')
@client_ns.param('id', 'Client ID')
class ClientReportList(Resource):
    @client_ns.marshal_with(report_list_model)
    def get(self, id):
        client = Client.query.get(id)
        if not client:
            client_ns.abort(404, message="Client not found")

        _client_reports = client.reports.all()

        _result = dict()
        _report_list = list()

        for _report in _client_reports:
            _item = dict()
            _item['id'] = _report.id
            _item['status'] = _report.status
            _item['created_at'] = _report.created_at
            _item['updated_at'] = _report.updated_at
            _report_list.append(_item)

        _result['client_name'] = client.name
        _result['reports'] = _report_list

        return _result


@client_ns.route('/<int:id>/reports/<int:report_id>')
@client_ns.response(404, 'Report not found or in progress')
@client_ns.param('id', 'Client ID')
@client_ns.param('report_id', 'Report ID')
class ClientReportClass(Resource):
    @client_ns.marshal_with(report_model)
    def get(self, id, report_id):

        client = Client.query.get(id)
        if not client:
            client_ns.abort(404, message="Client not found")

        _done_status = ReportStatus.query.filter(ReportStatus.name == "Done").first()

        _client_report = client.reports.filter(
            Report.id == report_id,
            Report.status == _done_status
        ).first()

        if not _client_report:
            client_ns.abort(404, message="Report not found or in progress")

        _result = dict()
        _result['id'] = _client_report.id
        _result['report'] = _client_report.data
        _result['created_at'] = _client_report.created_at
        _result['updated_at'] = _client_report.updated_at

        return _result

@client_ns.route('/<int:id>/stations')
@client_ns.response(404, 'Client not found')
@client_ns.param('id', 'Client ID')
class ClientStationList(Resource):
    @client_ns.marshal_list_with(station_model)
    def get(self, id):
        client = Client.query.get(id)
        if not client:
            client_ns.abort(404, message="Client not found")

        _stations = client.stations.all()

        _report_list = list()

        for _station in _stations:
            _item = dict()
            _item['id'] = _station.id
            _item['name'] = _station.name
            _report_list.append(_item)

        return _report_list

@client_ns.route('/<int:id>/stations/<int:station_id>')
@client_ns.response(404, 'Station not found')
@client_ns.param('id', 'Client ID')
@client_ns.param('station_id', 'Station ID')
class ClientStationClass(Resource):
    @client_ns.marshal_list_with(energy_model)
    def get(self, id, station_id):
        client = Client.query.get(id)
        if not client:
            client_ns.abort(404, message="Client not found")

        _station = client.stations.filter(Station.id == station_id).first()

        if not _station:
            client_ns.abort(404, message="Station not found")

        _bills = _station.bills.all()

        _result= list()

        for _bill in _bills:
            _item = dict()
            _item['id'] = _bill.id
            _item['energy'] = _bill.energy
            _item['created_at'] = _bill.created_at
            _result.append(_item)

        return _result