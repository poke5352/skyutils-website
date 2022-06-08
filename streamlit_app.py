import streamlit as st
from config import page_config, PAGE_TITLE, ICON, SIGNATURE_KEY
import importlib
import json
import extra_streamlit_components as stx
from cryptography.fernet import Fernet

st.set_page_config(layout="wide", page_title=PAGE_TITLE, page_icon=ICON)

if 'login_data' not in st.session_state:
    st.session_state['login_data'] = None


@st.cache(allow_output_mutation=True)
def get_manager():
    return stx.CookieManager()


cookie_manager = get_manager()


def login():
    global st
    try:
        value = cookie_manager.get_all()["login_data"]
        fernet_key = Fernet(SIGNATURE_KEY)
        decrypted = json.loads(fernet_key.decrypt(
            value.encode("utf-8")).decode())
        st.session_state.login_data = decrypted
    except:
        st.session_state.login_data = None


if True:
    query_params = st.experimental_get_query_params()
    if query_params == {}:
        raise Exception("Use Main Page")
    nav_params = query_params['nav'][0]
    if nav_params in page_config:
        style = """
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>"""
        page_file = page_config[nav_params]["page_file"]

        login()

        module = "pages." + page_file
        page_module = importlib.import_module(module)
        st.markdown(style, unsafe_allow_html=True)
        page_module.app()
    else:
        raise Exception("Use Main Page")
