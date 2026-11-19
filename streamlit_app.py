import json
import streamlit as st
import streamlit.components.v1 as components

from script_data import SCRIPT_CUES
from movie_ui import MOVIE_HTML_HEAD
from movie_cast import MOVIE_JS_PART1
from movie_props import MOVIE_PROPS_JS
from movie_act1 import MOVIE_ACT1_JS
from movie_act2 import MOVIE_ACT2_JS

st.set_page_config(
    page_title="The Scholar's Rebellion | Comic Movie",
    page_icon="💥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        #MainMenu, header, footer {visibility: hidden;}
        .block-container {
            padding: 0.4rem 0.8rem 0rem 0.8rem !important;
            max-width: 100% !important;
        }
        body, .stApp { background-color: #090d16; }
    </style>
    """,
    unsafe_allow_html=True,
)

cues_js = f"const DIALOGUE_CUES = {json.dumps(SCRIPT_CUES)};\n"
full_html = (
    MOVIE_HTML_HEAD
    + cues_js
    + MOVIE_JS_PART1
    + MOVIE_PROPS_JS
    + MOVIE_ACT1_JS
    + MOVIE_ACT2_JS
)
components.html(full_html, height=795, scrolling=False)
