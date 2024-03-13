# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
import plotly.express as px
import pandas as pd
from sodapy import Socrata
import datetime
from keplergl import KeplerGl
from streamlit_keplergl import keplergl_static
#datetime.datetime.strptime

LOGGER = get_logger(__name__)

client = Socrata("data.edmonton.ca",
                '0QYjRL0AGkE3yWTOhXlgpGpzA',
                username="torresir@ualberta.ca",
                password="=4F^!k8}%%:6f}W")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("tq23-qn4m", limit=2000)

def run():
    st.set_page_config(
        page_title="YEG Cycling & Pedestrian",
        page_icon="🚴🚶",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    st.write("# Welcome to YEG CYCLING & PEDESTRIANS!🚴🚶")

    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)

    df = results_df.drop(['log_time_interval_minutes', 
                      'direction_of_travel', 
                      'pedestrian_count_ebd',
                      'pedestrian_count_wbd',
                      'pedestrian_count_nbd',
                      'pedestrian_count_sbd',
                      'cyclist_count_ebd',
                      'cyclist_count_wbd',
                      'cyclist_count_nbd',
                      'cyclist_count_sbd',
                      'combined_total_count',
                      ':@computed_region_7ccj_gre3',
                      ':@computed_region_ecxu_fw7u',
                      ':@computed_region_izdr_ja4x',
                      ':@computed_region_5jki_au6x',
                      ':@computed_region_mnf4_kaez',
                      ':@computed_region_eq8d_jmrp',
                      'location',
                      'counter_configuration',
                     ] , axis=1)
    
    df["total_cyclist_count"] = pd.to_numeric(df["total_cyclist_count"], downcast="float")
    df["total_pedestrian_count"] = pd.to_numeric(df["total_pedestrian_count"], downcast="float")
    df["latitude"] = pd.to_numeric(df["latitude"], downcast="float")
    df["longitude"] = pd.to_numeric(df["longitude"], downcast="float")
    df['log_timstamp'] = pd.to_datetime(df['log_timstamp'])
    
    start_time = st.slider(
        "Start date of data",
        #value = datetime.datetime.now,
        min_value = datetime.datetime(2024,1,1,0,0),
        max_value = datetime.datetime(2024,3,20,0,0),
        step = datetime.timedelta(minutes=15),
        format = "MM/DD/YY - hh:mm")
    st.write("Start time:", start_time)

    df = df[(df['log_timstamp'] >= start_time)]
    df['log_timstamp'] = df['log_timstamp'].astype(str)



    option = st.selectbox(
    'Would you like to see the data from Cyclist or Pedestrians?',
    ('Cyclist', 'Pedestrians'))
    st.write('You selected:', option)

    config = {
        "version": "v1",
        "config": {
            "mapState": {
                "bearing": 0,
                "latitude": 53.55014 ,
                "longitude": -113.46871,
                "pitch": 0,
                "zoom": 10,
            }
        },
    }

    map_1 = KeplerGl(height=1000)
    map_1.config = config

    if option == 'Cyclist':
        df['total_cyclist_count_to_date'] = df.groupby('counter_location_description')['total_cyclist_count'].transform('sum')
        df = df.drop(['total_cyclist_count','total_pedestrian_count','log_timstamp','row_id'] , axis=1)
        map_1.add_data(data=df, name='counter_location')

    elif option == 'Pedestrians':
        df['total_pedestrian_count_to_date'] = df.groupby('counter_location_description')['total_pedestrian_count'].transform('sum')
        df = df.drop(['total_pedestrian_count', 'total_cyclist_count','log_timstamp','row_id'] , axis=1)
        map_1.add_data(data=df, name='counter_location')
    

    keplergl_static(map_1)




if __name__ == "__main__":
    run()
