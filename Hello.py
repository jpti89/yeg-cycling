import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
from sodapy import Socrata
import datetime
from keplergl import KeplerGl
from streamlit_keplergl import keplergl_static
from plotly_calplot import calplot
from streamlit.hello.utils import show_code

LOGGER = get_logger(__name__)

@st.cache_data
def load_data():
    client = Socrata("data.edmonton.ca",
                '0QYjRL0AGkE3yWTOhXlgpGpzA',
                username="torresir@ualberta.ca",
                password="=4F^!k8}%%:6f}W")

    # First 2000 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    results = client.get("tq23-qn4m", limit=250000)
    results = pd.DataFrame.from_records(results)
    return results

def run():
    st.set_page_config(
        page_title="YEG Cycling & Pedestrian",
        page_icon="🚴🚶",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    st.write("# Welcome to YEG CYCLING & PEDESTRIANS!🚴🚶")

    option = st.selectbox(
    'Would you like to see the data from Cyclist or Pedestrians?',
    ('Cyclist', 'Pedestrians'))

    start_time = st.slider(
        "Start and End date of data to visualize",
        value= (datetime.datetime(2024,1,1,0,0), datetime.datetime(2024,3,19,0,0)),
        min_value = datetime.datetime(2023,1,1,0,0),
        max_value = datetime.datetime(2024,3,20,0,0),
        step = datetime.timedelta(minutes=15),
        format = "MM/DD/YY - hh:mm")

    results_df = load_data()

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

    df = df[df['log_timstamp'].between(*start_time, inclusive='both')]


    df['log_timstamp'] = df['log_timstamp'].astype(str)

    map_1 = KeplerGl(height=800)

    with open('./Data/Neighbourhood Boundaries 2019_20240320.geojson', 'r') as f:
        boundaries = f.read()
    

    if option == 'Cyclist':
        
        with open('./Data/Bike Routes_20240320.geojson', 'r') as f:
            routes = f.read()

        with open('./Data/Bike_Racks__Post_and_Ring__and_Bulk_20240320.csv', 'r') as f:
            racks = f.read()

        df['total_cyclist_count_to_date'] = df.groupby('counter_location_description')['total_cyclist_count'].transform('sum')
        df2 = df.drop(['total_cyclist_count','total_pedestrian_count','log_timstamp','row_id'] , axis=1)
        map_1.add_data(data=df2, name='counter_location')
        #map_1.add_data(data=racks, name='racks')
        map_1.add_data(data=routes, name='routes')
        #map_1.add_data(data=boundaries, name='boundaries')

        
        keplergl_static(map_1, center_map=True)

        df_day=df
        df_day['log_timstamp'] = pd.to_datetime(df_day['log_timstamp'])

        df_day = df.groupby([pd.Grouper(key='log_timstamp', freq='D')
        ]).sum().reset_index()
        df_day = df_day.drop(['latitude', 'longitude'] , axis=1)
        fig = calplot(df_day, x="log_timstamp", y="total_cyclist_count", dark_theme=False, years_title=True,name="total_cyclist_count",
              showscale=True, cmap_max=5000, cmap_min=0,month_lines_width=2, month_lines_color="#666")
        st.plotly_chart(fig,use_container_width = True)

    elif option == 'Pedestrians':
        with open('./Data/LRT Routes_20240320.geojson', 'r') as f:
            lrt_routes = f.read()

        df['total_pedestrian_count_to_date'] = df.groupby('counter_location_description')['total_pedestrian_count'].transform('sum')
        df2 = df.drop(['total_pedestrian_count', 'total_cyclist_count','log_timstamp','row_id'] , axis=1)
        map_1.add_data(data=df2, name='counter_location')
        map_1.add_data(data=lrt_routes, name='lrt_routes')
        #map_1.add_data(data=boundaries, name='geojson')
        keplergl_static(map_1, center_map=True)

        df_day=df
        df_day['log_timstamp'] = pd.to_datetime(df_day['log_timstamp'])

        df_day = df.groupby([pd.Grouper(key='log_timstamp', freq='D')
        ]).sum().reset_index()
        df_day = df_day.drop(['latitude', 'longitude'] , axis=1)
        fig = calplot(df_day, x="log_timstamp", y="total_pedestrian_count", dark_theme=False, years_title=True,name="total_pedestrian_count",
              showscale=True, cmap_max=12000, cmap_min=0,month_lines_width=2, month_lines_color="#666")
        st.plotly_chart(fig,use_container_width = True)
    

if __name__ == "__main__":
    run()
    show_code(run)
