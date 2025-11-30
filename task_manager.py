import os
import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
from streamlit import rerun


#Browser Config ---------------------------------------------------
st.set_page_config(page_title='Task Manager', page_icon='📝',layout='wide')

#SideBar -------------------------------------------------------
with st.sidebar:
    st.header('Filter')
    filter_select = st.selectbox("Tasks",['All Tasks', 'Completed','Incomplete'])
try:
    #Sheety API -------------------------------------------------------
    SHEETY_API = os.getenv("SHEETY_API")
    AUTH_USER = os.getenv("AUTH_USER")
    AUTH_PASS = os.getenv("AUTH_PASS")
except(KeyError,FileNotFoundError):
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    SHEETY_API = os.getenv("SHEETY_API")
    AUTH_USER = os.getenv("AUTH_USER")
    AUTH_PASS = os.getenv("AUTH_PASS")


if not all([SHEETY_API,AUTH_USER,AUTH_PASS]):
    st.error("Missing API Credentials, Please Check your .env File")
    st.stop()

#Functions --------------------------------------------------------

def create_local_task(task_desc,task_date,category_desc,priority):
    task = {
        'description': task_desc,
        'date': task_date,
        'category': category_desc,
        'priority': priority,
        'completed': False
    }
    return task

def export_task_to_sheety(task):
    sheety_data = {
        'sheet1':{
        'description': task['description'],
        'date': str(task['date']),
        'category': task['category'],
        'priority': task['priority'],
        'completed': task['completed']
    }
    }
    try:
        response = requests.post(
            url=SHEETY_API,
            json=sheety_data,
            auth=HTTPBasicAuth(AUTH_USER,AUTH_PASS)
        )
        st.write(f'Status: {response.status_code}')
        st.write(f'Response: {response.text}')
        return response.json()
    except Exception as e:
        st.write(f'Exception : {e}')
        return None

def import_task_from_sheety():
    try:
        response = requests.get(
            url=SHEETY_API,
            auth=HTTPBasicAuth(AUTH_USER,AUTH_PASS))
        data = response.json()
        tasks_sheety = data.get('sheet1', [])
        return tasks_sheety
    except Exception as e:
        st.error(f'Error loading tasks: {e}')
        return []

def edit_sheety_task(task_id, task):
    sheety_data = {
        'sheet1': {
            'description': task['description'],
            'date': str(task['date']),
            'category': task['category'],
            'priority': task['priority'],
            'completed': task['completed']
        }
    }
    try:
        response = requests.put(
            url=f'{SHEETY_API}/{task_id}',
            json=sheety_data,
            auth=HTTPBasicAuth(AUTH_USER,AUTH_PASS)
        )
    except Exception as e:
        st.error(f'Error loading tasks: {e}')
        return []

def delete_sheety_task(task_id):
    try:
        response = requests.delete(
            url=f'{SHEETY_API}/{task_id}',
            auth=HTTPBasicAuth(AUTH_USER, AUTH_PASS)
        )
    except Exception as e:
        st.error(f'Error deleting tasks: {e}')
        return False

def priority_color(priority):
    if priority == 'High':
        return 'red'
    elif priority == 'Medium':
        return 'yellow'
    else:
        return 'green'

#Task Manager Display ---------------------------------------------
st.title('Task Manager')
st.markdown("---")

#Initialize Task Section --------------------------------------------
st.header('My Task')
st.subheader('➕ Add New Task')


#Task Form -----------------------------------------------------------
with st.form('task_form'):
    task_desc = st.text_input('Task Description')
    task_date = st.date_input('Date', format="MM/DD/YYYY")
    category_desc = st.text_input('Category')
    priority = st.selectbox('Priority',['High','Medium','Low'])
    submitted = st.form_submit_button('Add Task')
if submitted:
    task = create_local_task(task_desc, task_date, category_desc, priority)
    export_task_to_sheety(task)
    st.success('Task Added!')


#Task List Displayed -------------------------------------------------
st.markdown('---')
st.subheader('📋 Task List')

#Import Tasks from Sheety
tasks = import_task_from_sheety()
print(tasks)

#Initializing Session state for Editing
if 'editing_task_id' not in st.session_state:
    st.session_state.editing_task_id = None

#Initialize delete state
if 'delete_task_id' not in st.session_state:
    st.session_state.delete_task_id = None

#Filter Tasks
if filter_select == 'Completed':
    tasks = [t for t in tasks if t.get('completed', False)]
elif filter_select == 'Incomplete':
    tasks = [t for t in tasks if t.get('completed', True)]


#Display Tasks
if tasks:
    for task in tasks:
        task_id = task.get('id')

        if st.session_state.delete_task_id == task_id:
            success = delete_sheety_task(task_id)
            st.session_state.delete_task_id = None
            st.rerun()

        if st.session_state.editing_task_id == task_id:
            #EDIT Task Mode
            st.markdown(f'### ✏️ Editing Task')
            with st.form(f'edit_form_{task_id}'):
                edit_desc = st.text_input('Task Description', value=task.get('description',''))
                edit_date = st.date_input('Date',value=task.get('date',''),format="MM/DD/YYYY")
                edit_category = st.text_input('Category',value=task.get('category',''))
                edit_priority = st.selectbox('Priority',['High','Medium','Low'],
                                             index=['High','Medium','Low'].index(task.get('priority','Low')))
                edit_completed = st.checkbox('Completed', value=task.get('completed',False))

                col1,col2 = st.columns(2)
                with col1:
                    save_button = st.form_submit_button('💾 Save Changes')
                with col2:
                    cancel_button = st.form_submit_button('❌ Cancel')

            if save_button:
                updated_task = {
                    'description':edit_desc,
                    'date': edit_date,
                    'category':edit_category,
                    'priority':edit_priority,
                    'completed':edit_completed
                }
                edit_sheety_task(task_id,updated_task)
                st.session_state.editing_task_id = None
                st.rerun()

            if cancel_button:
                st.session_state.editing_task_id = None
                st.rerun()

        else:
            #Display Mode
            col_check, col_info, col_action, col_delete = st.columns([1,5,1,1])

            with col_check:
                completed = task.get('completed', False)
                if st.checkbox('Done', value=completed, key=f'checkbox_{task_id}'):
                    if not completed:
                        task['completed'] = True
                        edit_sheety_task(task_id,task)
                        st.rerun()
                else:
                    if completed:
                        task['completed'] = False
                        edit_sheety_task(task_id,task)
                        st.rerun()

            with col_info:
                if task['completed']:
                    st.markdown(f'<s>{task.get('description')}</s>', unsafe_allow_html=True)
                else:
                    st.write(f'**{task.get('description')}** ')
                color = priority_color(task.get('priority', 'Low'))
                st.markdown(f'📅 {task['date']} '
                            f'Category: {task['category']} | '
                            f"Priority: <span style='color:{color};'>{task.get('priority', '')}</span>", unsafe_allow_html=True)

            with col_action:
                if st.button('✏️', key=f'edit_{task_id}', help='Edit task'):
                    st.session_state.editing_task_id = task_id
                    st.rerun()

            with col_delete:
                if st.button('❌', key=f'delete_{task_id}', help='Delete task'):
                    st.session_state.delete_task_id = task_id
                    st.rerun()


            st.markdown('---')

else:
    st.info('No tasks to display')




