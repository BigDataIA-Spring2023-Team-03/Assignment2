import streamlit as st
import json
import requests

#########################################
# Pages:
st.set_page_config(
    page_title="DAMG7245_Spring2023 Group 03",
    page_icon="👋",
)

# st.sidebar.success("Select a page above.")

# Initialize username in session state
# Session State also supports the attribute based syntax 
if 'key' not in st.session_state:
    st.session_state.username = 'Not Logged in!'



#########################################
# # API TESTING:
# response = requests.get(url = 'http://127.0.0.1:8000/hello')
# st.write(response.json())

# # S3_Transfer API
# data = {
#   "action": "test",
#   "src_bucket": "noaa-goes18",
#   "dest_bucket": "damg7245",
#   "dest_folder": "assignment1",
#   "prefix": "ABI-L1b-RadC/2023/001/00/",
#   "files_selected": "OR_ABI-L1b-RadC-M6C01_G18_s20230010001170_e20230010003544_c20230010003582.nc"
# }
# st.write(type(data))
# response = requests.post(url = 'http://127.0.0.1:8000/s3_transfer', json=data)
# st.write(response.json())
# dest_url = response.json().get('Destination s3 URL')
# st.write(f'dest_url: {dest_url}')



###################################################################################
# Login Form
with st.form(key="Login"):
    username = st.text_input("Username", 'Username')
    password = st.text_input("Password", 'Password')
    # Executes FastAPI to check Login
    login_status = st.form_submit_button("Login")

# st.write(login_status)

# Use login_status from the FastAPI response to provide follow-up options
if username == 'Username' or password == 'Password':
    st.warning('Please enter your username and password')
    # Register new User
    new_user = st.button("Create New Account")
# fastapi response for correct username, password
elif login_status:
    st.write(f'Welcome {username}!')
    st.title('Use SEVIRDataFetcher to get Data!')
    # create streamlit session for user if correct
    st.session_state.username = username
# fastapi response for incorrect username, password
elif login_status is False:
    st.error('Username/password is incorrect')
    # Register new User
    new_user = st.button("Create New Account")


###################################################################################
# New User
try:
    if new_user:
        # Login Form
        with st.form(key="Create"):
            username = st.text_input("Username", 'Username')
            email = st.text_input("Email", 'Email')
            password = st.text_input("Password", 'Password')
            # Executes FastAPI to create account
            create_status = st.form_submit_button("Create Account")
except:
    new_user = None


###################################################################################
# Side Bar
with st.sidebar:
    username = 'test' 
    st.write(f'Current User: {st.session_state.username}')