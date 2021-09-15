from api.extensions import db
from datetime import datetime

class DailyEnergyConsumption(db.Model):
    __tablename__ = 'daily_energy_consumptions'
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey('stations.id'), nullable=False)
    energy = db.Column(db.Numeric(precision=9, scale=2), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
