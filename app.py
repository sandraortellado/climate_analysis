import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)


@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        "<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start date<br/>"
        f"/api/v1.0/start date/end date<br/>"
        "<br/>"
        "Format for dates: YYYY-MM-DD"
    )

@app.route("/api/v1.0/precipitation")
def precipitation_json():
    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date > '2016-08-23').all()

    # Convert list of tuples into normal list
    prcp_dict = dict(results)

    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations_json():
    results = session.query(Measurement.station).group_by(Measurement.station).all()
    station_list=list(np.ravel(results))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs_json():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).filter(Measurement.date > '2016-08-23').all()
    tobs_list = list(np.ravel(results))
    return jsonify(tobs_list)

@app.route(f"/api/v1.0/<start_date>")
def start_json(start_date):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    start_list = list(np.ravel(results))
    return jsonify(start_list)

@app.route(f"/api/v1.0/<start_date>/<end_date>")
def startend_json(start_date, end_date):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    start_end_list = list(np.ravel(results))
    return jsonify(start_end_list)
    


if __name__ == "__main__":
    app.run(debug=True)