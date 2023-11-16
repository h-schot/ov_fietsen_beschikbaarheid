import os.path
import json
import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

url = "https://uzu34h3kfl.execute-api.eu-central-1.amazonaws.com/test/ov_fietsen"


def load_locations() -> dict:

    dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = os.path.join(dirname, "data/locatie_info.json")

    f = open(filename)

    data = json.load(f)
    locations = data["locaties"]
    location_mapper = {value["description"]: key for key, value in locations.items()}

    f.close()

    return location_mapper


def app(url):
    st.title('Verwachte OV fiets beschikbaarheid')
    
    locations = load_locations()
    station_name = st.selectbox("Station", locations.keys())
    # station_code = locations[station_name]
    station_code = station_name

    datum = st.date_input("Datum", datetime.today(), min_value=datetime.today(), max_value=datetime.today()+timedelta(days=14))
    datum = str(datum)

    tijd = st.time_input("Tijd", datetime.now())
    tijd = str(tijd)

    if st.button('Haal verwachte beschikbare fietsen op'):
        input_json = {"locatie":station_code,
                      "datum":datum,
                      "tijd":tijd}
        headers = {"x-api-key": "gLWQE1fApb4eOXoQ8Boyn90Sqo6AnPYG1chHvsIx"}
        response = requests.request("POST", url, headers=headers, json=input_json)
        st.write(response.text)

    else:
        return

app(url)

#https://share.streamlit.io/app/ovfiets-beschikbaarheid/
# https://kimthegreat7-tostiband-appapp-streamlit-ov-fietsen-iq2y3p.streamlit.app/