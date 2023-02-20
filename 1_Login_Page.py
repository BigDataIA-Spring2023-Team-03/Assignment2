import streamlit as st
import apis
from schemas import UserRegisterSchema, UserLoginSchema
import requests
import json
from streamlit_extras.switch_page_button import switch_page

#########################################
# Pages:
st.set_page_config(
    page_title="DAMG7245_Spring2023 Group 03",
    page_icon="👋",
)

if 'first_name' not in st.session_state:
    st.session_state.first_name = ''

if 'last_name' not in st.session_state:
    st.session_state.last_name = ''

if 'email' not in st.session_state:
    st.session_state.email = ''

if 'password' not in st.session_state:
    st.session_state.password = ''

# if 'email_login' not in st.session_state:
#     st.session_state.email_login = ''
#
# if 'password_login' not in st.session_state:
#     st.session_state.password_login = ''

if 'access_token' not in st.session_state:
    st.session_state.access_token = ''

if 'login_disabled' not in st.session_state:
    st.session_state.login_disabled = False

if 'logout_disabled' not in st.session_state:
    st.session_state.logout_disabled = True

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
# st.session_state.update(st.session_state)

# Initialize username in session state
# Session State also supports the attribute based syntax 
# if 'key' not in st.session_state:
#     st.session_state.username = 'Not Logged in!'



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
# with st.form(key="Login"):
#     username = st.text_input("Username", placeholder='Username')
#     password = st.text_input("Password", placeholder='Password', type = 'password')
#     # Executes FastAPI to check Login
#     login_status = st.form_submit_button("Login")
#
# # st.write(login_status)
#
# # Use login_status from the FastAPI response to provide follow-up options
# if username == 'Username' or password == 'Password':
#     st.warning('Please enter your username and password')
#     # Register new User
#     new_user = st.button("Create New Account")
# # fastapi response for correct username, password
# elif login_status:
#     st.write(f'Welcome {username}!')
#     st.title('Use SEVIRDataFetcher to get Data!')
#     # create streamlit session for user if correct
#     st.session_state.username = username
# # fastapi response for incorrect username, password
# elif login_status is False:
#     st.error('Username/password is incorrect')
#     # Register new User
#     new_user = st.button("Create New Account")


###################################################################################
# New User
# def submitted():
#     st.session_state.submitted = True
# def reset():
#     st.session_state.submitted = False
#
# try:
#     if new_user:
#         # Login Form
#         with st.form(key="Create"):
#             first_name = st.text_input("First Name", placeholder = 'First Name', key='first_name')
#             last_name = st.text_input("Last Name", placeholder = 'Last Name', key='last_name')
#             email = st.text_input("Email", placeholder = 'Email', key='email')
#             password = st.text_input("Password", placeholder = 'Password', type = "password", key='password')
#             submitted = st.form_submit_button("Create Account", on_click = submitted())
#
#
#         if 'submitted' in st.session_state:
#             if st.session_state.submitted == True:
#                 print("Submit button pressed")
#                 new_user = {
#                   "first_name": st.session_state.first_name,
#                   "last_name": st.session_state.last_name,
#                   "email": st.session_state.email,
#                   "password": st.session_state.password
#                 }
#                 # print(st.session_state)
#                 res = requests.post(url='http://localhost:8000/user/register', data=json.dumps(new_user))
#                 # st.sidebar.write(new_user)
#                 # reset()
# except:
#     new_user = None


###################################################################################
# Side Bar



email = st.text_input("Username", st.session_state.email, placeholder='Username')
password = st.text_input("Password", st.session_state.password, placeholder='Password', type = 'password')
login_submit = st.button('Login', disabled = st.session_state.login_disabled)

if login_submit:
    st.session_state.email = email
    st.session_state.password = password
    login_user = {
        'email': st.session_state.email,
        'password': st.session_state.password
    }
    res = requests.post(url='http://localhost:8000/user/login', data=json.dumps(login_user))
    if res and res.status_code == 200:
        # st.experimental_rerun()
        st.session_state.access_token = res.json()['access_token']
        st.session_state.login_disabled = True
        st.session_state.logged_in = True
        st.session_state.logout_disabled = False
        switch_page('sevirdatafetcher')

    elif res.status_code == 401:
        switch_page('registerpage')
    else:
        error = "<p style='font-family:sans-serif; color:Red; font-size: 20px;'>Error: User doesn't exist!</p>"
        st.markdown(error, unsafe_allow_html=True)


with st.sidebar:
    if st.session_state and st.session_state.logged_in and st.session_state.email:
        st.write(f'Current User: {st.session_state.email}')
    else:
        st.write('Current User: Not Logged In')

    logout_submit = st.button('LogOut', disabled = st.session_state.logout_disabled)
    if logout_submit:
        for key in st.session_state.keys():
            if key == 'login_disabled' or key == 'logout_disabled' or key == 'register_disabled':
                st.session_state[key] = not st.session_state[key]
            else:
                st.session_state[key] = ''
        st.session_state.login_disabled = False
        st.experimental_rerun()



