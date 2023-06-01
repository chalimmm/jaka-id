import streamlit as st
from pages import scraping

def goto(page):
    st.session_state['menu'] = page

def relogin():
    st.session_state['auth'] = False

def app():
    st.markdown("""
    <h1 style='text-align: center;'>
        JAKA
    </h1>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <center>
        <p style='text-align: center;'>
            Login using your SSO-UI account.
        </p>
    </center>
    """, unsafe_allow_html=True)

    empty, center, empty = st.columns([1, 2, 1])
    with center:
        status = st.container()
        
        u = st.text_input('Username', help="Enter your SSO UI account's username", max_chars=30)
        p = st.text_input('Password', help="Enter your SSO UI account's password", type='password')
        with st.expander("JAKA's Privacy Policy"):
            st.write("""
                #### **With using JAKA, You agreed to comply with our Privacy Policy, in which they are as follows.**\n
                1. JAKA uses login information, such as the username and password of Universitas Indonesia's Signle-Sign-On account to enrter SIAK-NG.\n
                2. That login information will be used for the authentication process, which is to ensure that every party that does the process is an active student in Universitas Indonesia.\n
                3. Other than being used for the authentication process, your login information will also be used for data scraping from the schedule page in SIAK-NG so that it can be processed by JAKA for the students to arrange their course plan from the retreived data.\n
                4. JAKA DOES NOT save users' login information in any form.\n
                5. JAKA IS NOT responsible for its users' failure in choosing a schedule in SIAK-NG based on JAKA's recommendation.\n
                6. JAKA treats all users in the same way, in which it means that every single one of its users will have a maximum of 24 possible credits for the term. So, each user has to know their respective maximum credits to be taken for the term.\n
            """)
        isAgree = st.checkbox("I have read JAKA's Privacy Policy.")
        
        loginBtn = st.container()
        
        if u and p and isAgree:
            if st.session_state['auth']:
                loginBtn.write(" ")
                loginBtn.button('Login', on_click=goto, args=['Dashboard'])
            else:
                try:
                    st.session_state['auth'] = scraping.app(u, p)
                    if st.session_state['auth']:
                        st.session_state['username'] = u
                        status.success('Authenticated, hai '+u)
                        loginBtn.write(" ")
                        loginBtn.button('Login', on_click=goto, args=['Dashboard'])
                    else:
                        status.error('Wrong username or password')
                except:
                    status.error('Authentication Failed')
        else:
            loginBtn.markdown("""
            <a href='javascript:alert("Authenticated User Only! Please, check the User Agreement!");'>
                <div class="row-widget customButton">
                    <button>
                        Login
                    </button>
                </div>
            </a>
            """, unsafe_allow_html=True)
            status.warning('Masukkan username dan password')
            st.stop()
