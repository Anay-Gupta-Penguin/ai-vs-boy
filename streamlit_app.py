import json
import streamlit as st
import streamlit.components.v1 as components

from movie_art import MOVIE_HTML_PART1
from movie_scenes import MOVIE_JS_PART2
from script_data import SCRIPT_CUES

st.set_page_config(
    page_title="The Scholar's Rebellion — Comic Movie (6:30)",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
    .block-container {
        padding: 0.4rem 1rem 0rem 1rem !important;
        max-width: 1360px !important;
    }
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    .stApp {
        background-color: #090d16;
    }
</style>
""",
    unsafe_allow_html=True,
)

FULL_MOVIE_HTML = (
    MOVIE_HTML_PART1.replace("__DIALOGUE_JSON__", json.dumps(SCRIPT_CUES))
    + MOVIE_JS_PART2
)

components.html(FULL_MOVIE_HTML, height=600, scrolling=False)
