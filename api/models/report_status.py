from api.extensions import db

class ReportStatus(db.Model):
    __tablename__ = 'report_statuses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    reports = db.relationship('Report', lazy=True, backref='status')

    def __str__(self):
        return self.name