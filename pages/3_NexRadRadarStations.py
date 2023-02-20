import folium 
import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
from Util.DbUtil import DbUtil


if 'email' not in st.session_state:
    st.session_state.email = ''

if 'logout_disabled' not in st.session_state:
    st.session_state.logout_disabled = True

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

###################################################################################
# Side Bar
with st.sidebar:
    user = "Not Logged In" if st.session_state.email == "" else st.session_state.email
    st.write(f'Current User: {user}')
    logout_submit = st.button('LogOut', disabled=st.session_state.logout_disabled)
    if logout_submit:
        for key in st.session_state.keys():
            if key == 'login_disabled' or key == 'logout_disabled' or key == 'register_disabled':
                st.session_state[key] = not st.session_state[key]
            else:
                st.session_state[key] = ''
        st.session_state.login_disabled = False
        st.session_state.register_disabled = False
        st.experimental_rerun()
###################################################################################


# data = pd.read_csv('nexrad-stations.csv')


util = DbUtil('metadata.db')
conn = util.conn

data = pd.read_sql_query(f'select * from nexrad_lat_long', conn)

st.title("NexRad Radar Stations")
if not st.session_state.email == "":
    st.subheader("The data here contains locations of current and archived radar stations. The map denotes these specified stations by a blue pin.")
    st.caption("Note: You can find information like the station name and city in which station is located by hovering over the points.")

    # Select only Columns that are needed. First 2 column will be used for plotting others can be used for labelling.
    map_loc = data[["LAT", "LONG", "station", "city"]]

    # Passing the latitude and longitutde value to plot it on map
    map = folium.Map(location=[map_loc.LAT.mean(), map_loc.LONG.mean()], zoom_start=14, control_scale=True)

    # Adding the points to the map by itterating through the dataframe
    for index, location_info in map_loc.iterrows():
        folium.Marker([location_info["LAT"], location_info["LONG"]],
        popup=[location_info["LAT"], location_info["LONG"]],
        tooltip=[location_info["LAT"], location_info["LONG"], "Station: " + location_info["station"], "City: " + location_info["city"]]).add_to(map)

    st_data = st_folium(map, width=725)

    util.conn.close()
else:
    st.write('Please Login!')
