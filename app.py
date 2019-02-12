import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#flask Setup
app=Flask(__name__)


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        #f"/api/v1.0/start<br/>"
        f"/api/v1.0/tobs/start/end"
    )
#api end point precipitation
@app.route("/api/v1.0/precipitation")
def prcp():
    """Return a list of all precipitation observations"""
    # Query all prcp observations
    results = session.query(Measurement.prcp).all()
#query results into a dictionary
#date is the key and prcp is the value
    all_prcp = []
    for date in results:
        prcp_dict = {}
        prcp_dict["date"] = Measurment.date
        prcp_dict["prcp"] = Measurment.prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_passengers)

#api end point stations
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all station names"""
    # Query all passengers
    results = session.query(Station.name).all()

    # Convert list of tuples into normal list
    station_names = list(np.ravel(results))

    return jsonify(station_names)

#api end point temp
@app.route("/api/v1.0/tobs")
def temp():
#query for dates and tobs from a year from the last data point 2017-08-23
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results=session.query(Measurement.tobs, Measurement.date).filter(Measurement.date>=prev_year)

    last_year_tobs=list(np.ravel(results))
    return jsonify(last_year_tobs)

#min, avg, max temp stats from start date

@app.route("/api/v1.0/tobs/<start>")
@app.route("/api/v1.0/tobs/<start>/<end>")
def min_avg_max_temp_start_date_to_end_date(start=None, end=None):
    #return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        #filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

 # Select statement
   sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
   if not end:
       # calculate TMIN, TAVG, TMAX for dates greater than start
    results = session.query(*sel).filter(Measurement.date >= start).all()
       # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))
    #return jsonify(temps)
    # calculate TMIN, TAVG, TMAX with start and stop
    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))
    return jsonify(temps)

if __name__=='__main__':
    app.run()
