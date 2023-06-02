import subprocess
import sys
import json
import streamlit as st

def app(u, p):
    placeholder = st.empty()
    placeholder.write("---")
    loading = placeholder.progress(0)
    with placeholder.container():
        with open("./courses.json", "w") as output:
            subprocess.call('docker run -e USERNAME="' + u + '" -e PASSWORD="' + p + '" scraping', shell=True, stdout=output, stderr=output)
            loading.progress(50)
        
        courses = {}

        with open("./courses.json", "r") as f:
            courses = json.load(f)

        print(courses)

        if courses == {}:
            loading.progress(100)
            placeholder.empty()
            return False

        loading.progress(100)
        st.session_state['courses'] = courses
        
        placeholder.empty()
        return True
