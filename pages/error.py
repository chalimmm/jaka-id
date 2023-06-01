import json
import requests
from streamlit_lottie import st_lottie

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def app(code:int):
    lottie_link = {
        307 : "assets/error307.json",
        404 : "assets/error404.json"
    }
    
    lottie_file = load_lottiefile(lottie_link[code])
    # lottie_file = load_lottieurl("lottie_link")

    st_lottie(
        lottie_file,
        speed=1,
        reverse=False,
        loop=True,
        quality="high", # medium ; high
        renderer="svg", # canvas
        height=600,
        width=None,
        key=1,
    )