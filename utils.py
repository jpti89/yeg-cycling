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

import inspect
import textwrap
import pandas as pd
import streamlit as st


def show_code(demo):
    """Showing the code of the demo."""
    show_code = st.sidebar.checkbox("Show code", True)
    if show_code:
        # Showing the code of the demo.
        st.markdown("## Code")
        sourcelines, _ = inspect.getsourcelines(demo)
        st.code(textwrap.dedent("".join(sourcelines[1:])))

def source_data_table(df):
    """Source Data definition of columns."""
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
    return df