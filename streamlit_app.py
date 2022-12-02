import streamlit as st
import streamlit.components.v1 as components
# import streamlit_authenticator as stauth

# streamlit_app.py

def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        with st.form("sign-in1"):
            # First run, show inputs for username + password.
            st.text_input("Username", key="username")
            st.text_input(
                "Password", type="password", key="password"
            )

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            password_entered()
        
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        with st.form("sign-in2"):
            # First run, show inputs for username + password.
            st.text_input("Username", key="username")
            st.text_input(
                "Password", type="password", key="password"
            )

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            password_entered()
    else:
        # Password correct.
        return True

st.title("Cup Adventure")
if check_password():
    st.write(f'Welcome *Fred*')

# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days'],
#     config['preauthorized']
# )

# with open('../config.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)

# name, authentication_status, username = authenticator.login('Login', 'main')

# if authentication_status:
#     authenticator.logout('Logout', 'main')
#     st.title("Cup Adventure")
#     st.write(f'Welcome *{name}*')
#     st.write(config['credentials'])
# elif authentication_status == False:
#     st.error('Username/password is incorrect')
# elif authentication_status == None:
#     st.warning('Please enter your username and password')

# from PIL import Image
# image = Image.open(r"images\banner.jpg")

# st.image(image)
# st.image("images\logo.jpg")
# st.image(r"images\banner.jpg")

# st.subheader("Previous Code")
# HTMLFile = open('hack.html', 'r', encoding='utf-8')
# sourceCode = HTMLFile.read()
# components.html(sourceCode)

# st.subheader("Website Code")
# HTMLFile = open('final_form_website.html', 'r', encoding='utf-8')
# sourceCode = HTMLFile.read()
# components.html(sourceCode)