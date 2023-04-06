# Import the dependencies.
from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

app = Flask(__name__)

#################################################
# Database Setup
#################################################

# create engine to hawaii.sqlite
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

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return(
        f"<center><h2>Welcome to my Hawaii Climate Local API!</h2></center>"
        f"<center><h3>Select from one of the available routes:</h3></center>"
        f"<center>/api/v1.0/precipitation</center>"
        f"<center>/api/v1.0/stations</center>"
        f"<center>/api/v1.0/tobs</center>"
        f"<center>/api/v1.0/start/end</center>"
    )

##find routes for data and return as jsons
@app.route("/api/v1.0/precipitation")
def precip():
    prevYr = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >=prevYr).all()

    session.close()
    ##create dict w/date as key and precp as the value
    precipitation = {date: prcp for date, prcp in results}
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    #shows a list of the stations, then perform query to get names of the stations
    results = session.query(Station.station).all()
    session.close()

    stationList = list(np.ravel(results))

    return jsonify(stationList)

@app.route("/api/v1.0/tobs")
def temps():
    prevYr = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    ##create dict to get prev year temps
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').\
                        filter(Measurement.date >= prevYr).all()                   
    session.close()

    tempsList = list(np.ravel(results))
    return jsonify(tempsList)

##routes for start and end 
@app.route ("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def dateStats(start=None, end=None):

    selection = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    if not end:
        startDate = dt.datetime.strptime(start, "%m%d%Y")
        results = session.query(*selection).filter(Measurement.date >= startDate).all()

        session.close()

        tempsList = list(np.ravel(results))

        return jsonify(tempsList)

    else:
        startDate = dt.datetime.strptime(start,"%m%d%Y" )
        endDate = dt.datetime.strptime(end,"%m%d%Y" )

        results = session.query(*selection).filter(Measurement.date >= startDate).\
            filter(Measurement.date <= endDate).all()

        session.close()

        tempslist = list(np.ravel(results))


##launch app
if __name__ == '__main__':
    app.run(debug =True)



#################################################
# Flask Setup
#################################################





