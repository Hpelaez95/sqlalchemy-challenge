# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect the tables
Base=automap_base()
Base.prepare(autoload_with=engine)
Base.classes.keys()

# Save references to each table
Measurement=Base.classes.measurement
Station=Base.classes.station

# Create our session (link) from Python to the DB

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List All available api routes"""
    return(f"Available Rouds: <br/>"
           f"/api/v1.0/precipitation<br>"
           f"/api/v1.0/stations<br>"
           f"/api/v1.0/tobs<br>"
           f"/api/v1.0/start<br>"
           f"api/v1.0/start/end")





@app.route("/api/v1.0/precipitation")
def precipitation():

    latest_date = dt.date(2017,8,23)
    year_ago = latest_date- dt.timedelta(days=365)

    session= Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date>= year_ago).all()

    session.close()

    all_precipitation = []
    for date,prcp in results:
        prcp_dict={}
        prcp_dict[date] = prcp
        all_precipitation.append(prcp_dict)

    return jsonify(all_precipitation)

    


@app.route("/api/v1.0/stations")
def stations(): 

    session=Session(engine)
    results = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    session.close()
    all_stations=[]
    for id,station,name,latitude,longitude, elevation in results:
        station_dict={}
        station_dict['id']=id
        station_dict['station']=station
        station_dict['name']=name
        station_dict['latitude']=latitude
        station_dict['longitude']=longitude
        station_dict['elevation']=elevation
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs(): 

    latest_date = dt.date(2017,8,23)
    year_ago = latest_date- dt.timedelta(days=365)

    session=Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).filter_by(station = 'USC00519281').\
    filter(Measurement.date >= year_ago).all()
    session.close()

    all_temps = []
    for date, tobs in results:
        tobs_dict={}
        tobs_dict['date']=date
        tobs_dict['tobs']=tobs
        all_temps.append(tobs_dict)
    return jsonify(all_temps)




@app.route("/api/v1.0/<start>")
def temp_start(start):
    session=Session(engine)
    """to calculate TMIN, TAVG, and TMAX for all the dates
    Need an argument as Start_date: A date format as %Y-%m-%d"""

    results=session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()
    session.close()
    temptobs={}
    temptobs['Min_Temp']=results[0][0]
    temptobs['Avg_Temp']=results[0][1]
    temptobs['Max_temp']=results[0][2]
    return jsonify(temptobs)






@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session=Session(engine)
    """to calculate TMIN, TAVG, and TMAX for all the dates
    Need an argument as Start_date: A date format as %Y-%m-%d
    and an end date as %Y-%m-%d """

    results=session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    temptobs={}
    temptobs['Min_Temp']=results[0][0]
    temptobs['Avg_Temp']=results[0][1]
    temptobs['Max_temp']=results[0][2]
    return jsonify(temptobs)



if __name__ == '__main__':
    app.run(debug=True)