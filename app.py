import numpy as np 
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session 
from sqlalchemy import create_engine, func



from flask import Flask, jsonify


engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)


Measurement = Base.classes.measurement 
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    print("idk what im doing")
    return (
        "Available routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/<start><br/>"
        "/api/v1.0/<start>/<end>"


    )

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Station.station).all()
    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)



@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    rec_year_sev = dt.date(2017,8,18)-dt.timedelta(days = 365)
    rec_yr_sev = rec_year_sev.strftime("%Y-%m-%d")

    q4 = session.query(Measurement.date, Measurement.tobs)\
    .filter(Measurement.station == Station.station)\
    .filter(Station.id == 7)\
    .filter(Measurement.date >= rec_yr_sev)\
    .order_by(Measurement.date.asc()).all()

    all_tobs = []
    for date, tobs in q4:
        obs = {}
        obs["date"] = date
        obs["tobs"] = tobs
        all_tobs.append(obs)
    
    return jsonify(all_tobs)

    session.close()


@app.route("/api/v1.0/<start>")
def f(start):
    session=Session(engine)

    q3 = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
    .filter(Station.station == Measurement.station)\
    .filter(Station.id == 7).filter(Measurement.date >= start).all()

    session.close()
    
   
    return jsonify(float((q3[0][0])), float(q3[0][1]), float(q3[0][2]))


@app.route("/api/v1.0/<start>/<end>")
def g(start,end):

    session = Session(engine)

    qq = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
    .filter(Station.station == Measurement.station)\
    .filter(Station.id == 7).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close
    return jsonify(float((qq[0][0])), float(qq[0][1]), float(qq[0][2]))

if __name__ == "__main__":
    app.run(debug=True)
