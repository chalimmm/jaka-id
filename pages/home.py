import streamlit as st
import json
import requests
from streamlit_lottie import st_lottie
from pages import error

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def goto(page):
    st.session_state['menu'] = page

def app():
    c1, c2 = st.columns(2)
    
    with c2:
        lottie_file = load_lottiefile("assets/schedule.json")  # replace link to local lottie file

        st_lottie(
            lottie_file,
            speed=1,
            reverse=False,
            loop=True,
            quality="high", # small; medium ; high
            renderer="svg", # svg; canvas
            height=None,
            width=None,
            key="lottie-schedule",
        )
    
    with c1:
        body = st.container()       
        for i in range(5):
            body.write(' ')
        body.title("JAKA")
        body.markdown("""
        <p class='info'>Jadwal Aman, Kuliah Aman.</p>
        <hr style="height:4px;border:none;
        color:#f72585;background-color:#f72585">
        """, unsafe_allow_html=True)
        
        about_text = """
        <p class='info'>JAKA is built to make Universitas Indonesia student's course scheduling
        easier, faster, seamless, and more intuitive than ever.</p>"""
        body.markdown(about_text, unsafe_allow_html=True)
        for i in range(2):
            body.write(' ')
        
        st.button("Start Now!", key='start-now', on_click=goto, args=['Login'])
