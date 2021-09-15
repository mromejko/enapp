import click
from flask.cli import cli, with_appcontext
from api.models import Client, Station, DailyEnergyConsumption, ReportStatus
from api.extensions import db

@cli.command('seeder', help="DB seeder")
@with_appcontext
def seeder():
    click.secho("Creating dummy data...", fg='green')

    client = Client(name="Client_one")
    db.session.add(client)

    station1 = Station(name="Enelion_01")
    station2 = Station(name="Enelion_02")
    station3 = Station(name="Enelion_03")

    station_objects = [station1, station2, station3]
    client.stations.extend(station_objects)

    station1.bills.extend([
        DailyEnergyConsumption(energy=123.44, created_at="2021-01-12 10:00:00"),
        DailyEnergyConsumption(energy=4127.12, created_at="2021-02-13 15:30:00"),
    ])

    station2.bills.extend([
        DailyEnergyConsumption(energy=724.41, created_at="2021-03-19 10:30:00"),
        DailyEnergyConsumption(energy=1248.00, created_at="2021-03-22 15:00:00"),
        DailyEnergyConsumption(energy=10.00, created_at="2021-03-30 10:00:00"),
    ])

    station3.bills.extend([
        DailyEnergyConsumption(energy=8514.00, created_at="2021-01-09 15:12:00"),
        DailyEnergyConsumption(energy=9541.77, created_at="2021-01-12 17:40:00"),
    ])

    db.session.commit()

    click.secho("Creating report statuses...", fg='green')
    _create_report_statuses()

    click.secho("DONE!", fg='green')

def _create_report_statuses():
    objects = [
        ReportStatus(name='In progress'),
        ReportStatus(name='Done'),
        ReportStatus(name='Rejected')
    ]

    db.session.bulk_save_objects(objects)
    db.session.commit()