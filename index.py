### IMPORT LIBRARIES AND PAGES ###
import streamlit as st
from pages import home, login, error, schedule, dashboard

### FIREBASE CONNECT ###
import firebase_admin
from firebase_admin import credentials

if not firebase_admin._apps:
    cred = credentials.Certificate('pages/serviceAccountKey.json') 
    firebase_admin.initialize_app(cred)

### INIT SESSION STATE ###
if 'menu'           not in st.session_state : st.session_state['menu']           = 'Home'
if 'auth'           not in st.session_state : st.session_state['auth']           = False
if 'courses'        not in st.session_state : st.session_state['courses']        = {}
if 'username'       not in st.session_state : st.session_state['username']       = 'username'
if 'selectedCourse' not in st.session_state : st.session_state['selectedCourse'] = []

### PAGE STYLING ###
st.set_page_config(
        page_title = "JAKA",
        layout = "wide",
        page_icon = "https://i.ibb.co/yP2wjhW/jaka-02.png",
        initial_sidebar_state = "collapsed"
    )
css_style = """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;800&display=swap" rel="stylesheet">
    <style>
        #MainMenu, footer, .edgvbvh6, .ehezqtx2 {visibility:hidden;} 
        div.stButton > button {
            background-color: #f72585;
            border-radius: 50px;
            display: inline-block;
            border: none;
            transition: all 0.4s ease 0s;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-transform: uppercase;
            text-decoration: none;
            display: inline-block;
            font-family: 'Montserrat';
            font-weight: 700;
            margin: 4px 2px;
            cursor: pointer;
            width: 100%;
        }
        div.stButton > button:hover {
            background-color: #f8f8f8;
            box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 10px 20px 0 rgba(0,0,0,0.19);
        }
        .customButton > button {
            background-color: #3a0ca3;
            border-radius: 50px;
            display: inline-block;
            border: none;
            transition: all 0.4s ease 0s;
            color: #ffffff;
            padding: 15px 32px;
            text-align: center;
            text-transform: uppercase;
            text-decoration: none;
            display: inline-block;
            font-family: 'Montserrat';
            font-weight: 700;
            margin: 4px 2px;
            width: 100%;
        }
        .customButton > button:hover {
            background-color: #f8f8f8;
            color: #3a0ca3;
            box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 10px 20px 0 rgba(0,0,0,0.19);
        }
        .navTxt {
            font-family: 'Montserrat';
            font-size: 24px;
            font-weight: 600;
            padding-top: 20px;
            padding-bottom: 5px;
            background-color: #f8f8f8;
            position: fixed;
            top: 0;
            right: 50px;
            width: 25%;
            height: 75px;
            z-index:99999;
            opacity: 0.95;
        }
        .navImg {
            padding-top: 25px;
            background-color: #f8f8f8;
            top: 0;
            position: fixed;
            width: 100%;
            height: 75px;
            z-index:99990;
            opacity: 0.95;
        }
        h1 { font-family: 'Montserrat';font-size: 55px; font-weight: 900; }
        h2,h3,h4,h5 { font-family: 'Montserrat'; }
        .judul { font-family: 'Montserrat'; font-size: 35px; font-weight: 710; }
        .info { font-family: 'Montserrat'; font-size: 25px; }
        p { font-family: 'Montserrat'; font-size: 16px; }
        a:link { font-family: 'Montserrat'; color: #3a0ca3; text-decoration:none; }
        a:hover { color: #f72585; text-decoration:none; }
        img:hover { opacity: 0.5; }
        label { font-family: 'Montserrat';font-size: 20px; font-weight: 600; }
        div.streamlit-expanderHeader {
            font-family: 'Montserrat';
            font-size: 20px;
            font-weight: 600;
            background-color: #f72585;
            color: #ffffff;
        }
        li > div[aria-expanded="true"] > svg[title="Expand"] {
            color: #ffffff;
        }
        li > div[aria-expanded="true"], div.streamlit-expanderHeader:hover {
            background-color: #ffffff;
            color: #f72585;
        }
        div.streamlit-expanderContent {
            font-family: 'Montserrat';
            font-size: 20px;
            background-color: #ffffff;
        }
        label[data-baseweb="radio"] > div.st-e6.st-dn.st-bt.st-ae.st-af.st-ag.st-ah.st-ai.st-aj{
            box-sizing: border-box;
            width: 100%
            height: 50px;
            display: block;
            background: transparent;
            border-radius: 5px;
            padding: 1rem;
            margin-top: -1rem;
            margin-right: 0.5rem;
            margin-left: -0.5rem;
            margin-bottom: -1rem;
            position: relative;
            font-family: 'Montserrat';
            font-size: 16px;
            font-weight: 600;
        }
        label[data-baseweb="radio"] > div > div {
            display: none;
        }
        label[data-baseweb="radio"] > div.st-az {
            width: 5px;
            height: 50px;
            background: #3a0ca3;
            border-radius: 1px;
        }
        label[data-baseweb="radio"] > div.st-et, label[data-baseweb="radio"] > div.st-eu, label[data-baseweb="radio"] > div.st-ev, label[data-baseweb="radio"] > div.st-ew, label[data-baseweb="radio"] > div.st-ex {
            width: 30px;
            height: 50px;
            background: #f72585;
            border-radius: 1px;
        }
    </style>
    """
st.markdown(css_style, unsafe_allow_html=True)

### CALLBACK FUNCTION ###
def goto(page):
    st.session_state['menu'] = page

### HEADER SECTION ###
logoSide, titleSide = st.sidebar.columns((1, 2))
logoSide.markdown('''
    <center>
    <a href="javascript:document.getElementsByClassName('css-1ydp377 edgvbvh6')[2].click();">
        <img src="https://i.ibb.co/yP2wjhW/jaka-02.png" alt="Logo JAKA" style="width:50px;height:50px;"/>
    </a>
    </center>
    ''', unsafe_allow_html=True)
titleSide.markdown("""
    <p class='judul' align='center'>
        <a href="javascript:document.getElementsByClassName('css-1ydp377 edgvbvh6')[2].click();">
            JAKA
        </a>
    </p>
    """, unsafe_allow_html=True)
logoMain, textMain = st.columns((1, 4))
if st.session_state['auth'] and st.session_state['menu'] != 'Login':
    logoMain.markdown('''
    <div class='navImg'> 
        <a href="javascript:document.getElementsByClassName('css-1ydp377 edgvbvh6')[1].click();">
            <img src="https://i.ibb.co/yP2wjhW/jaka-02.png" alt="Logo JAKA" style="width:50px;height:50px;"/>
        </a>
    </div>
    ''', unsafe_allow_html=True)
    st.sidebar.markdown("""
    <h4 align='center'>
        <a href="javascript:document.getElementsByClassName('css-1ydp377 edgvbvh6')[2].click();">
            Hai, """+st.session_state['username']+""" 
        </a>
    </h4>
    """, unsafe_allow_html=True)
    textMain.markdown("""
    <div align='right' class='navTxt'>
        <a href="javascript:document.getElementsByClassName('css-1ydp377 edgvbvh6')[2].click();">
            """+st.session_state['menu']+""" 
        </a>
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.button('Dashboard', on_click=goto, args=['Dashboard'])
    st.sidebar.button('Settings', on_click=goto, args=['Settings'])
    st.sidebar.markdown("""
    <a href='javascript:if(confirm("Are you sure to logout?")) window.location.reload(true);'>
        <div class="customButton">
            <button>
                Logout
            </button>
        </div>
    </a>
    """, unsafe_allow_html=True)
elif st.session_state['menu'] == 'Home':
    logoMain.markdown('''
    <div class='navImg'>
        <a href="javascript:window.location.reload(true);">
            <img src="https://i.ibb.co/yP2wjhW/jaka-02.png" alt="Logo JAKA" style="width:50px;height:50px;"/>
        </a>
    </div>
    ''', unsafe_allow_html=True)
    textMain.markdown("""
    <div align='right' class='navTxt'>
        <a href="javascript:document.getElementsByClassName('css-1wwkvaf edgvbvh1')[0].click();">
            Login 
        </a>
    </div>
    """, unsafe_allow_html=True)
else:
    logoMain.markdown('''
    <div class='navImg'>
        <a href="javascript:window.location.reload(true);">
            <img src="https://i.ibb.co/yP2wjhW/jaka-02.png" alt="Logo JAKA" style="width:50px;height:50px;"/>
        </a>
    </div>
    ''', unsafe_allow_html=True)

### PAGE CONTROLLER ###
if st.session_state['auth']:
    if st.session_state['menu'] == 'Settings':
        dashboard.Settings()
    elif st.session_state['menu'] == 'Create Schedule':
        schedule.Course()
    elif st.session_state['menu'] == 'Modify Schedule':
        dashboard.Modify()
    elif st.session_state['menu'] == 'Delete Schedule':
        dashboard.Delete()
    elif st.session_state['menu'] == 'Choose Schedule':
        schedule.Class()
    else:
        dashboard.View()
else:
    if st.session_state['menu'] == 'Home':
        home.app()
    elif st.session_state['menu'] == 'Login':
        login.app()
    else:
        error.app(307)