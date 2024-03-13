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
#datetime.datetime.strptime

LOGGER = get_logger(__name__)

def run():
    st.set_page_config(
        page_title="YEG Cycling",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    st.write("# Welcome to YEG CYCLING!")

    client = Socrata("data.edmonton.ca",
                  '0QYjRL0AGkE3yWTOhXlgpGpzA',
                  username="torresir@ualberta.ca",
                  password="=4F^!k8}%%:6f}W")

    # First 2000 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    results = client.get("tq23-qn4m", limit=10)

    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)

    df = results_df.drop(['log_time_interval_minutes', 
                      'direction_of_travel', 
                      'pedestrian_count_ebd',
                      'pedestrian_count_wbd',
                      'pedestrian_count_nbd',
                      'pedestrian_count_sbd',
                      'total_pedestrian_count',
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
    df["latitude"] = pd.to_numeric(df["latitude"], downcast="float")
    df["longitude"] = pd.to_numeric(df["longitude"], downcast="float")
    df['log_timstamp'] = pd.to_datetime(df['log_timstamp'])

    fig = px.scatter_mapbox(
    df,
    lat="latitude",
    lon="longitude",
    hover_name="counter_location_description",
    hover_data=["log_timstamp", "total_cyclist_count"],
    color_discrete_sequence=["fuchsia"],
    zoom=11,
    height=300,
    )

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    #fig.update_layout(mapbox_bounds={"west": -180, "east": -50, "south": 20, "north": 90})
    fig.show()
    


if __name__ == "__main__":
    run()
