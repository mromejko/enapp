from api.extensions import db

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    stations = db.relationship('Station', lazy='dynamic', backref='owner')
    reports = db.relationship('Report', lazy='dynamic', backref='client')