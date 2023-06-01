import streamlit as st
import json
import requests
from streamlit_lottie import st_lottie
from firebase_admin import firestore

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

def Settings():
    st.markdown("<center><h1 style='text-align: center;'>What Do You Want To Do?</h1></center>", unsafe_allow_html=True)
    
    #st.info('Actions: '+str(st.session_state['actions']))
    c1, a1, c2, a2, c3 = st.columns((2, 1, 2, 1, 2))
    
    with c1:
        lottie_file = load_lottiefile("assets/create.json")

        st_lottie(
            lottie_file,
            speed=1,
            reverse=False,
            loop=True,
            quality="high", # small; medium ; high
            renderer="svg", # svg; canvas
            height=None,
            width=None,
            key="lottie-create-schedule",
        )
        st.button('Create Schedule', on_click=goto, args=['Create Schedule'])
        
    with c2:
        lottie_file = load_lottiefile("assets/modify.json")

        st_lottie(
            lottie_file,
            speed=1,
            reverse=False,
            loop=True,
            quality="high", # small; medium ; high
            renderer="svg", # svg; canvas
            height=None,
            width=None,
            key="lottie-modify-schedule",
        )
        st.button('Modify Schedule', on_click=goto, args=['Modify Schedule'])
        
    with c3:
        lottie_file = load_lottiefile("assets/delete.json")

        st_lottie(
            lottie_file,
            speed=1,
            reverse=False,
            loop=True,
            quality="high", # small; medium ; high
            renderer="svg", # svg; canvas
            height=None,
            width=None,
            key="lottie-delete-schedule",
        )
        st.button('Delete Schedule', on_click=goto, args=['Delete Schedule'])

def View():
    st.subheader('Your Schedule(s)')
    
    with st.spinner('Please Wait...'):    
        db = firestore.client()
        st.session_state['plans'] = db.collection('users').document(st.session_state['username']).collection('plan').get()
    
    if st.session_state['plans']:
        for plan in st.session_state['plans']:
            schedule = plan.to_dict()
            with st.expander('Schedule on '+plan.id):
                st.write(schedule)
    else:
        st.write('Kamu belum memiliki jadwal, Create Schedule pada menu Settings')

def database(cmd, timestamp):
    if cmd == 'Modify':
        st.session_state['selectedCourse'] = []
        for plan in st.session_state['plans']:
            if plan.id == timestamp:
                st.session_state['timestamp'] = timestamp
                schedules = plan.to_dict()
                st.write(schedules)
                for sched in schedules:
                    st.session_state['selectedCourse'].append(sched + " - " + st.session_state['courses'][sched]['Nama'])
                break
        st.session_state['menu'] = 'Create Schedule'
    elif cmd == 'Delete':
        for plan in st.session_state['plans']:
            if plan.id == timestamp:
                with st.spinner('Please Wait...'):    
                    db = firestore.client()
                    db.collection('users').document(st.session_state['username']).collection('plan').document(timestamp).delete()
                break

def Modify():
    headerTxt, nextBtn = st.columns([4, 1])
    headerTxt.header('Select Schedule')
    st.write("---")
    
    with st.spinner('Please Wait...'):    
        db = firestore.client()
        st.session_state['plans'] = db.collection('users').document(st.session_state['username']).collection('plan').get()
    
    if len(st.session_state['plans']) > 0:
        option = []
        for plan in st.session_state['plans']:
            option.append(plan.id)
        timestamp = st.selectbox("Type or scroll to search", options=option)
        nextBtn.button("Next", on_click=database, args=['Modify', timestamp])
    else:
        st.write('Kamu belum memiliki jadwal, Create Schedule pada menu Settings')
        nextBtn.markdown('''
        <a href='javascript:alert("You do not have any schedule to modify");'>
            <div class="customButton">
                <button>
                    Next
                </button>
            </div>
        </a>
        ''', unsafe_allow_html=True)

def Delete():
    headerTxt, nextBtn = st.columns([4, 1])
    headerTxt.header('Select Schedule')
    st.write("---")
    top = st.container()
    View()
    if len(st.session_state['plans']) > 0:
        option = []
        for plan in st.session_state['plans']:
            option.append(plan.id)
        timestamp = top.selectbox("Type or scroll to search", options=option)
        nextBtn.button("Delete", on_click=database, args=['Delete', timestamp])
    else:
        nextBtn.markdown('''
        <a href='javascript:alert("You do not have any schedule to delete");'>
            <div class="customButton">
                <button>
                    Delete
                </button>
            </div>
        </a>
        ''', unsafe_allow_html=True)