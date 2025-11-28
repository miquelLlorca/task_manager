import streamlit as st
from datetime import datetime
from uuid import uuid4
from data import *
from views import *


CALENDAR = "Calendar"
KANBAN = "Kanban"
BACKLOG = "Backlog"

st.set_page_config(page_title="Task Manager", layout="centered")
st.title("Task Manager")

events = load_events()
categories = load_categories()


view = st.sidebar.radio(
    "View",
    [CALENDAR, KANBAN, BACKLOG],
    index=0
)

TASK_STATUSES = ["TODO", "IN PROGRESS", "DONE"]
DEFAULT_COLOR = "#4CAF50"  # default green

with st.expander("➕ Add New Task", expanded=view==CALENDAR):
    # --- Add task UI ---
    task_name = st.text_input("Task name")
    category_name = st.selectbox("Category", options=[c['name'] for c in categories])
    description = st.text_input("Description")

    status = st.selectbox("Status", TASK_STATUSES)
    all_day = st.checkbox("All day task", value=True)

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start date", value=datetime.now())
    with col2:
        end_date = st.date_input("End date", value=start_date)

    # If all day, force start = end
    if all_day:
        end_date = start_date

    color = st.color_picker("Task color (for calendar)", value=get_color_from_category(categories, category_name))
    no_date = st.checkbox("No deadline / backlog task", value=False)

    if st.button("Add Task"):
        if not task_name.strip():
            st.error("Task name required")
        else:
            new_task = {
                "id": str(uuid4()),
                "title": task_name.strip(),
                'description': description,
                'category':category_name,
                "status": status,
                "allDay": all_day,
                "color": color,
                "start": None if no_date else start_date.isoformat(),
                "end": None if no_date else end_date.isoformat()
            }
            events.append(new_task)
            save_events(events)
            st.success(f"✔ Task '{task_name}' added")
            st.rerun()


with st.expander("➕ Add New Category", expanded=False):
    category_name = st.text_input("Category name")
    color = st.color_picker("Category color", value=DEFAULT_COLOR)
    if(st.button('Create Category')):
        categories.append({
            'name': category_name, 'color':color
        })
        save_categories(categories)

if(view==CALENDAR):

    calendar_view(events)
elif(view == "Kanban"):
    kanban_view(events)
elif(view == "Backlog"):
    backlog_view(events)
