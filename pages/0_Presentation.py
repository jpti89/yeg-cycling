import streamlit as st
import pandas as pd
#from streamlit.hello.utils import source_data_table

st.set_page_config(page_title="YEG Cycling & Pedestrian")

tab1, tab2, tab3, tab4 = st.tabs(["Introduction", "Source Data", "Development Enviroment","Limitations"])

with tab1:
    st.markdown("# YEG Cycling & Pedestrian Web APP")
    st.write(
        """As students at the University of Alberta, situated in Edmonton, we recognize the challenge 
        of excessive car dependency. Commuting as pedestrians and cyclists between our residence, 
        the university, and various destinations, we've discovered an abundance of openly 
        available data within Edmonton.   
        Leveraging this data, we've crafted powerful visualizations, particularly focusing on our commuting p
        references."""
    )
    
    st.write(
        """Our web application, accessible at https://yeg-cycling.streamlit.app/, is designed to empower 
        pedestrians and cyclists, with valuable insights into their commuting experiences 
        across Edmonton."""
    )

    st.write("""Developed entirely in Python, we've utilized Streamlit, an open-source framework tailored 
        for creating interactive data science applications and visualizations."""
    )

    st.write("""Our main App welcoming functionality is a geo-spatial visual to the available data, 
             such that our users can identify and recognize these data points on a daily basis.   
             This is presented in a completely interactive and highly user customizable geospatial 
             Python library, called Kepler.GL.  
            We also gave the user more control of filtering and selecting data outside the visualization, 
             with date sliders, and filtering data in order to see pedestrian or cyclists data points.
            """
            )


with tab2:
    st.markdown("## Source Data")
    st.write(
        """The dataset provided by the City of Edmonton, available at https://data.edmonton.ca, our application 
        dynamically retrieves live data through its REST API.   
        The dataset, originally titled "Bike and Pedestrian Counts (Eco Counter)," commenced on February 6, 2019, 
        initially monitoring a handful of locations within the city. Over time, until today, it has expanded 
        to encompass 51 monitoring spots, predominantly concentrated in Edmonton's central region along the scenic 
        North Saskatchewan River."""
    )
    st.write(
        """
    Currently comprising over 6.48 million rows of data across 20 columns, each row identifies one monitor location, 
    and the calculated amount of people walking or cycling through that point, in a 15 minute window time frame.   
    We mainly use the columns of Geolocation, TimeStamp, cyclist and pedestrians count in our visualization.
"""
    )
    d = {'Column Name': [
                'Row ID',
                'Counter Location Description',
                'Log Time Interval (minutes)',
                'Log Timstamp',
                'Counter Configuration',
                'Direction of Travel',
                'Pedestrian Count EBD',
                'Pedestrian Count WBD',
                'Pedestrian Count NBD',
                'Pedestrian Count SBD',
                'Total Pedestrian Count',
                'Cyclist Count EBD',
                'Cyclist Count WBD',
                'Cyclist Count NBD',
                'Cyclist Count SBD',
                'Total Cyclist Count',
                'Combined Total Count',
                'Latitude',
                'Longitude',
                'Location',
            ], 
            'Description': [
                'A unique value for the row of data, used to prevent the duplication of data.',
                'A brief description of where the counter is located in the city.',
                'The number of minutes that is counted before the values are recorded.',
                'The actual date and time of when the data was recorded.',
                'The configuration of the counter. It could be Cyclist Only counter, or a Cyclist and Pedestrian counter.',
                'The direction of travel that is recorded for the counter.',
                'The number of pedestrians counted that were travelling in an east bound direction (EBD).',
                'The number of pedestrians counted that were travelling in a west bound direction (WBD).',
                'The number of pedestrians counted that were travelling in a north bound direction (NBD).',
                'The number of pedestrians counted that were travelling in a south bound direction (SBD).',
                'The total number of pedestrians counted at this location (i.e. counts in both directions added together).',
                'The number of cyclists counted that were travelling in an east bound direction (EBD).',
                'The number of cyclists counted that were travelling in a west bound direction (WBD).',
                'The number of cyclists counted that were travelling in a north bound direction (NBD).',
                'The number of cyclists counted that were travelling in a south bound direction (SBD).',
                'The total number of cyclists counted at this location (i.e. counts in both directions added together).',
                'The total number of pedestrians and cyclists counted at this location.',
                'Latitude of the point\'s centre of the where the counter is located.',
                'Longitude of the point\'s centre of the where the counter is located.',
                'Concatenation of latitude and longitude for mapping purposes.',
            ],
            'Type': [
                'Plain Text',
                'Plain Text',
                'Plain Text',
                'Date & Time',
                'Plain Text',
                'Plain Text',
                'Number',
                'Number',
                'Number',
                'Number',
                'Number',
                'Number',
                'Number',
                'Number',
                'Number',
                'Number',
                'Number',
                'Number',
                'Number',
                'Location'
                    ]}
    df = pd.DataFrame(data=d)
    st.table(df)

with tab3:
    st.markdown("## Development Environment")
    st.write(
        """The web platform Streamlit has the following limits and shared resources for its free tier:  
        - CPU: 0.078 cores minimum, 2 cores maximum  
        - Memory: 690MB minimum, 2.7GBs maximum  
        - Storage: No minimum, 50GB maximum"""
    )
    st.markdown("## Network Configuration")
    st.write(
        """The network configuration for this project involves accessing the City of Edmonton's data through 
        its REST API, fetching data points related to pedestrian and cyclist counts, and visualizing them on 
        a web application hosted on a platform like Streamlit."""
    )   

    
with tab4:
    st.markdown("## Limitations")
    st.write(
        """
    - Data Availability: Our project relies heavily on the availability and quality of data provided by the City of Edmonton. 
    Limited or inconsistent data could impact the accuracy and reliability of the visualizations and insights generated by the application.
    - Scope and Scale: While the project successfully analyzes data from 51 monitoring spots in Edmonton, it may not capture the full extent 
    of pedestrian and cyclist activity in the city.
    - Technical Constraints: The web application's performance may be affected by technical constraints such as limited computing resources, 
    especially considering the constraints of the free tier of the Streamlit platform.  
    Handling large datasets and real-time data retrieval may pose challenges in terms of processing power and memory.
    """
    )