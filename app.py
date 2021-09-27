import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# data = engine.execute("SELECT * FROM measurement")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return ('''
        Available Routes:<br/>
        <a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a><br/>
        <a href="/api/v1.0/stations">/api/v1.0/stations</a><br/>
        <a href="/api/v1.0/tobs">/api/v1.0/tobs</a><br/>
        <a href="/api/v1.0/start">/api/v1.0/&#x3C;start&#x3E;</a><br/>
        'Enter date in browser as YYYY-MM-DD format for both start and end'<br/>
        <a href="/api/v1.0/start/end">/api/v1.0/&#x3C;start&#x3E/&#x3C;end&#x3E;</a><br/>
        '''
    )


@app.route("/api/v1.0/precipitation")
def get_precipitation():

    session = Session(engine)

    data = engine.execute("SELECT date FROM measurement ORDER BY date DESC LIMIT 1")
    datez = [list(x) for x in data]
    most_recent_date = datez[0][0]
    last_twelve_months_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)

    prec_data = session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date >= last_twelve_months_date).all()

    session.close()

    prcp_data = []
    for date, prcp in prec_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)


@app.route("/api/v1.0/stations")
def get_stations():

    session = Session(engine)

    station_results = session.query(Station.id,Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation).all()

    session.close()

    stations_data = []
    for id, station, name, latitude, longitude, elevation in station_results:
        station_dict = {}
        station_dict["id"] = id
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        stations_data.append(station_dict)

    return jsonify(stations_data)


@app.route("/api/v1.0/tobs")
def get_tobs():

    session = Session(engine)

    data = engine.execute("SELECT date FROM measurement ORDER BY date DESC LIMIT 1")
    datez = [list(x) for x in data]
    most_recent_date = datez[0][0]
    last_twelve_months_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)

    active_stations = session.query(Measurement.station, func.count(Measurement.station)).\
                    group_by(Measurement.station).\
                    order_by(func.count(Measurement.station).desc()).all()
    most_active_station = active_stations[0][0]

    temperature = session.query(Measurement.station, Measurement.tobs).\
                filter(Measurement.station == most_active_station).\
                filter(Measurement.date >= last_twelve_months_date).all()

    session.close()

    tobs_data = []
    for station, tobs in temperature:
        tobs_dict = {}
        tobs_dict["station"] = station
        tobs_dict["tobs"] = tobs
        tobs_data.append(tobs_dict)

    return jsonify(tobs_data)


@app.route("/api/v1.0/<start>")
def get_start(start):
    ret = {}
    ret = start
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    print(type(start))
    print(type(start_date))

    session = Session(engine)

    data = engine.execute("SELECT date FROM measurement ORDER BY date DESC LIMIT 1")
    datez = [list(x) for x in data]
    most_recent_date = datez[0][0]

    query_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
        func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    
    TMIN = query_results[0][0]
    TAVG = query_results[0][1]
    TMAX = query_results[0][2]

    session.close()

    return jsonify(TMIN,TAVG,TMAX)


@app.route("/api/v1.0/<start>/<end>")
def get_start_end(start,end):
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')

    session = Session(engine)

    query_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
        func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()
    
    TMIN = query_results[0][0]
    TAVG = query_results[0][1]
    TMAX = query_results[0][2]

    session.close()

    return jsonify(TMIN,TAVG,TMAX)


if __name__ == '__main__':
    app.run(debug=True)