import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
from pyvis.network import Network
from datetime import datetime
from firebase_admin import firestore

def goto(page):
    st.session_state['menu'] = page

def updateCourse():
    if 'selected' in st.session_state:
        st.session_state['selectedCourse'] = st.session_state['selected']

def Course():
    courses = st.session_state['courses']
    
    headerTxt, nextBtn = st.columns([4, 1])
    headerTxt.header('Select Course(s)')
    
    st.write("---")
    
    filter, status = st.columns([4, 1])
    
    listCourse = []
    
    with filter:
        for course in courses:
            listCourse.append(course + " - " + courses[course]['Nama'])
        st.multiselect('Type or scroll to search', options = listCourse, default = st.session_state['selectedCourse'], key = 'selected', on_change = updateCourse)
    
    sks = 0
    for course in st.session_state['selectedCourse']:
        sks += int(course[-14:-13])
    
    status.metric(label = "SKS", value = sks, delta = (24 - sks))
    
    st.write("---")
    with st.expander("Selected Course", expanded=True):
        for selected in st.session_state['selectedCourse']:
            st.write(selected)
    
    with nextBtn:
        st.write(" ")
        if sks in range(1, 25):
            st.button('Next', on_click = goto, args = ['Choose Schedule'])
        else:
            st.markdown('''
            <a href='javascript:alert("Please select the schedule and make sure it does not exceed the number of your maximum credits!");'>
                <div class="customButton">
                    <button>
                        Next
                    </button>
                </div>
            </a>
            ''', unsafe_allow_html=True)

def checkSchedule(raw):
    checkResult = True
    nx_graph = nx.Graph()

    schedule = []

    day = { 'Senin': '1',
            'Selasa': '2',
            'Rabu': '3',
            'Kamis': '4',
            'Jumat': '5' }
    
    for data in raw:
        d, t = data[1].split(", ")
        
        s, f = t.split("-")
        
        s = s.split(".")
        s = "".join(s)
        s = int(day[d] + s)

        f = f.split(".")
        f = "".join(f)
        f = int(day[d] + f)

        schedule.append((s, data[0]))
        schedule.append((f, data[0]))

    schedule.sort()
    conflict = {}

    for i in range(len(schedule)):
        conflict[schedule[i][1]] = []
    
    n = len(schedule)
    for i in range(n):
        curr = schedule[i]
        if i < (n-1):
            temp = schedule[i+1]
            if temp[1] == curr[1]:
                pass
            elif curr[0]/10000 == temp[0]/10000:
                checkResult = False
                print(curr, temp)
                if curr[1] in conflict.get(curr[1]):
                    conflict[curr[1]].remove(curr[1])
                else:
                    conflict[curr[1]].append(curr[1])
                    conflict[curr[1]].append(temp[1])
    
    # DRAW CONFLICT GRAPH
    for temp in conflict:
        if temp in conflict[temp]:
            conflict[temp].remove(temp)
        if conflict[temp]:
            nx_graph.add_node(temp, size=20)
            for x in conflict[temp]:
                nx_graph.add_node(x, size=20)
                nx_graph.add_edge(temp, x)

    nt = Network("350px", "280px",notebook=True,heading='')
    nt.from_nx(nx_graph)
    nt.show('test.html')

    with st.sidebar.container():
        HtmlFile = open("test.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read() 
        components.html(source_code, height = 900,width=900)
        
    return checkResult

def saveSchedule():
    db = firestore.client()
    
    if 'selectedCourse' in st.session_state:
        temp = st.session_state['selectedCourse']
    
        if 'timestamp' not in st.session_state:
            timestamp = datetime.now()
            st.session_state['timestamp'] = timestamp.strftime("%d-%m-%Y %H:%M:%S")
        
        schedule = {}
        
        for course in temp:
            courseCode = course[:11].strip()
            kelas = st.session_state['courses'][courseCode]['Kelas']
            if st.session_state[courseCode] == 'Rekomendasi JAKA':
                schedule[courseCode] = kelas
            for i in range(len(kelas)):
                if kelas[i]['Nama'] == st.session_state[courseCode]:
                    schedule[courseCode] = [kelas[i]]
                    break
            del st.session_state[courseCode]
            
        del st.session_state['selectedCourse']
        
        with st.spinner('Updating Database'):
            db.collection('users').document(st.session_state['username']).collection('plan').document(st.session_state['timestamp']).set(schedule)
        
        st.success('Successfully added schedule on ' + st.session_state['timestamp'])
        st.session_state['menu'] = 'View Schedule'

def Class():
    headerTxt, backBtn, checkBtn = st.columns([4, 1, 1])
    headerTxt.header('Select Class')
    
    if 'selectedCourse' in st.session_state:
        temp = st.session_state['selectedCourse']
    st.write("---")
    
    raw = []
    
    for courseName in temp:
        courseCode = courseName[:10].strip()
        with st.expander(courseName, True):
            data = st.session_state['courses'][courseCode]['Kelas']
            opt, sched = st.columns([1, 2])
            for i in range(2):
                sched.write(" ")
            
            indexClass = 0
            option = []
            
            if len(data) > 1:
                option = ['Rekomendasi JAKA']                        
                    
                if courseCode not in st.session_state:
                    st.session_state[courseCode] = 'Rekomendasi JAKA'
            else:
                st.session_state[courseCode] = data[0]['Nama']
            
            jadwal = []
            
            for kelas in data:
                temp = kelas['Nama']
                option.append(temp)
                for jam in kelas['Jadwal']:
                    jadwal.append((courseCode, jam))
            print(jadwal)
            indexClass = option.index(st.session_state[courseCode])
            
            if indexClass or len(data) == 1:
                idx = indexClass - 1 if len(data) > 1 else 0
                sched.write("##### **Detail Kelas**")
                sched.write("⌛ "+" ⌛ ".join(data[idx]['Jadwal']))
                sched.write("🚪 "+data[idx]['Ruang'])
                sched.write('🎓 '+' 🎓 '.join(data[idx]['Dosen']))
                for jam in data[idx]['Jadwal']:
                    raw.append((courseCode, jam))
            else:
                sched.write(" ")
                sched.write("##### **Silakan pilih kelas atau serahkan ke JAKA**")
                raw.extend(jadwal)
            
            opt.radio(' ', options=option, key=courseCode, index=indexClass) 
    
    status = st.sidebar.container()
    status.write(" ")
    
    noConflict = checkSchedule(raw)
    
    with backBtn:
        st.write(" ")
        st.button('Back', on_click=goto, args=['Create Schedule'])
    
    with checkBtn:
        st.write(" ")    
        if noConflict:
            status.success("Tidak ada konflik jadwal")
            st.button('Save', on_click=saveSchedule)
        else:
            status.error("Ada jadwal yang konflik")
            st.markdown("""
            <a href="javascript:document.getElementsByClassName('css-1ydp377 edgvbvh6')[1].click();">
                <div class="row-widget customButton">
                    <button>
                        Save
                    </button>
                </div>
            </a>
            """, unsafe_allow_html=True)
