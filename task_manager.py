import streamlit as st
import json




#Run: streamlit run task_manager.py




#Functions streamlit
def priority_color(priority):
    if priority == 'High':
        return 'red'
    elif priority == 'Medium':
        return 'orange'
    else: #low
        return 'green'


#Functions json
def save_tasks():
    tasks_data = {
        'daily_tasks': st.session_state.daily_tasks,
        'weekly_tasks': st.session_state.weekly_tasks,
        'monthly_tasks': st.session_state.monthly_tasks
    }
    with open('tasks.json','w') as f:
        json.dump(tasks_data, f, default=str)

def load_tasks():
    try:
        with open('tasks.json', 'r') as f:
            tasks_data = json.load(f)
            return tasks_data
    except FileNotFoundError:
        #If file doesn't exist. return empty lists
        return {
            'daily_tasks': [],
            'weekly_tasks': [],
            'monthly_tasks': []
        }

#Browser and config
st.set_page_config(page_title='Task Manager', page_icon='📝', layout='wide')

#Main Page
st.title('📝 Task Manager')
st.markdown('Tracking Daily Tasks')
st.markdown('---')

#Initialize session state for storing tasks
# Load saved tasks when app starts
if 'daily_tasks' not in st.session_state:
    saved_data = load_tasks()
    st.session_state.daily_tasks = saved_data['daily_tasks']
    st.session_state.weekly_tasks = saved_data['weekly_tasks']
    st.session_state.monthly_tasks = saved_data['monthly_tasks']

col1, col2, col3 = st.columns(3)

with col1:
    st.header('Daily Tasks')
    #Adding Task section
    st.subheader('➕ Add New Task')
    with st.form('daily_form'):
        task_desc = st.text_input('Task Description')
        task_date = st.date_input('Date')
        priority = st.selectbox('Priority',['High','Medium','Low'])
        submitted = st.form_submit_button('Add Task')
    if submitted:
        task = {
            'description': task_desc,
            'date': task_date,
            'priority': priority,
            'completed': False,
        }
        st.session_state.daily_tasks.append(task)
        st.success('Task added!')
        save_tasks()
    st.markdown('---')
    st.subheader('📋 Task List')
    if st.button("🗑️ Clean Completed", key="clear_daily"):
        st.session_state.daily_tasks = [task for task in st.session_state.daily_tasks if not task['completed']]
        save_tasks()
        st.rerun()

    for i,task in enumerate(st.session_state.daily_tasks):
        col_check, col_info, col_delete = st.columns([1,5,1]) #Adds an addition column per number

        with col_check:
            completed = st.checkbox('Done', value=task['completed'], key=f'daily_{i}')
            st.session_state.daily_tasks[i]['completed'] = completed
            save_tasks()

        with col_info:
            if task['completed']:
                st.markdown(f'<s>{task['description']}</s>', unsafe_allow_html=True)
            else:
                st.write(f"**{task['description']}**")
            color = priority_color(task['priority'])
            st.markdown(f"📅 {task['date']} | Priority: <span style='color:{color}'>{task['priority']}</span>",unsafe_allow_html=True)

        with col_delete:
            if st.button('🗑️', key=f'delete_daily_{i}'):
                st.session_state.daily_tasks.pop(i)
                save_tasks()
                st.rerun()


with col2:
    st.header('Weekly Tasks')
    st.subheader('➕ Add New Task')
    with st.form('weekly_form'):
        task_desc = st.text_input('Task Description')
        task_date = st.date_input('Date')
        priority = st.selectbox('Priority', ['High', 'Medium', 'Low'])
        submitted = st.form_submit_button('Add Task')
    if submitted:
        task = {
            'description': task_desc,
            'date': task_date,
            'priority': priority,
            'completed': False,
        }
        st.session_state.weekly_tasks.append(task)
        st.success('Task added!')
        save_tasks()
    st.markdown('---')

    st.subheader('📋 Task List')
    if st.button("🗑️ Clean Completed", key="clear_weekly"):
        st.session_state.weekly_tasks = [task for task in st.session_state.weekly_tasks if not task['completed']]
        save_tasks()
        st.rerun()


    for i, task in enumerate(st.session_state.weekly_tasks):
        col_check, col_info, col_delete = st.columns([1, 5, 1])  # Adds an addition column per number

        with col_check:
            completed = st.checkbox('Done', value=task['completed'], key=f'weekly_{i}')
            st.session_state.weekly_tasks[i]['completed'] = completed
            save_tasks()

        with col_info:
            if task['completed']:
                st.markdown(f'<s>{task['description']}</s>', unsafe_allow_html=True)
            else:
                st.write(f"**{task['description']}**")
            color = priority_color(task['priority'])
            st.markdown(f"📅 {task['date']} | Priority: <span style='color:{color}'>{task['priority']}</span>",unsafe_allow_html=True)

        with col_delete:
            if st.button('🗑️', key=f'delete_weekly_{i}'):
                st.session_state.weekly_tasks.pop(i)
                save_tasks()
                st.rerun()

with col3:
    st.header('Monthly Tasks')
    st.subheader('➕ Add New Task')
    with st.form('monthly_form'):
        task_desc = st.text_input('Task Description')
        task_date = st.date_input('Date')
        priority = st.selectbox('Priority', ['High', 'Medium', 'Low'])
        submitted = st.form_submit_button('Add Task')
    if submitted:
        task = {
            'description': task_desc,
            'date': task_date,
            'priority': priority,
            'completed': False,
        }
        st.session_state.monthly_tasks.append(task)
        st.success('Task added!')
        save_tasks()
    st.markdown('---')

    st.subheader('📋 Task List')
    if st.button("🗑️ Clean Completed", key="clear_monthly"):
        st.session_state.monthly_tasks = [task for task in st.session_state.monthly_tasks if not task['completed']]
        save_tasks()
        st.rerun()
    for i, task in enumerate(st.session_state.monthly_tasks):
        col_check, col_info, col_delete = st.columns([1, 5, 1])  # Adds an addition column per number

        with col_check:
            completed = st.checkbox('Done', value=task['completed'], key=f'monthly_{i}')
            st.session_state.monthly_tasks[i]['completed'] = completed
            save_tasks()

        with col_info:
            if task['completed']:
                st.markdown(f'<s>{task['description']}</s>', unsafe_allow_html=True)
            else:
                st.write(f"**{task['description']}**")
            color = priority_color(task['priority'])
            st.markdown(f"📅 {task['date']} | Priority: <span style='color:{color}'>{task['priority']}</span>",unsafe_allow_html=True)
        with col_delete:
            if st.button('🗑️', key=f'delete_monthly_{i}'):
                st.session_state.monthly_tasks.pop(i)
                save_tasks()
                st.rerun()
