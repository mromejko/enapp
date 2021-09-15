from api.extensions import db

class Station(db.Model):
    __tablename__ = 'stations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)

    bills = db.relationship('DailyEnergyConsumption', lazy='dynamic', backref='station')

    def __str__(self):
        return self.name