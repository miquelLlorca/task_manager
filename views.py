import streamlit as st
from data import *

import json
from uuid import uuid4
from streamlit_calendar import calendar


def calendar_view(events):
    # --- Calendar (editable) ---
    state = calendar(
        events=events,
        options={
            "initialView": "dayGridMonth",
            "firstDay": 1,
            "editable": True,
            "selectable": True,
        },
        key="task_calendar"
    )

    # --- Handle drag (eventDrop) updates ---
    if state and state.get("eventChange"):
        dropped = state["eventChange"]["event"]  # dict from FullCalendar about moved event
        # Try to get a reliable id and new start
        event_id = dropped.get("id") or dropped.get("extendedProps", {}).get("id")
        new_start_raw = dropped.get("startStr") or dropped.get("start") or dropped.get("start_time") or dropped.get("date")
        new_start = to_date_str(new_start_raw)
        print(new_start_raw)

        # find matching event in session_state
        updated = False
        if event_id:
            for ev in events:
                if str(ev.get("id")) == str(event_id):
                    ev["start"] = new_start
                    # if event had an 'end' and calendar returned end info, update it too
                    new_end_raw = dropped.get("endStr") or dropped.get("end")
                    if new_end_raw:
                        ev["end"] = to_date_str(new_end_raw)
                    updated = True
                    break

        # fallback: match by title if no id available
        if not updated:
            title = dropped.get("title")
            for ev in events:
                if ev.get("title") == title:
                    ev["start"] = new_start
                    new_end_raw = dropped.get("endStr") or dropped.get("end")
                    if new_end_raw:
                        ev["end"] = to_date_str(new_end_raw)
                    updated = True
                    break

        if updated:
            save_events(events)
            st.success(f"Event saved: {title if 'title' in locals() else event_id} → {new_start}")
        else:
            st.warning("Moved event could not be matched to stored events.")

    # --- show raw events for debug (optional) ---
    # st.subheader("Stored events (session)")
    # st.write(events)
    # print(events)


KANBAN_COLUMNS = ["TODO", "IN PROGRESS", "DONE"]

def kanban_view(events):
    st.header("Task Columns")

    cols = st.columns(len(KANBAN_COLUMNS))
    for i, col_name in enumerate(KANBAN_COLUMNS):
        with cols[i]:
            st.subheader(col_name)
            for ev in events:
                if ev.get("status", "TODO") == col_name:
                    st.write(f"- {ev['title']}")
                    
                    # Move buttons
                    if i > 0:
                        if st.button("←", key=f"{ev['id']}-back"):
                            ev["status"] = KANBAN_COLUMNS[i-1]
                            save_events(events)
                            st.rerun()
                    if i < len(KANBAN_COLUMNS)-1:
                        if st.button("→", key=f"{ev['id']}-fwd"):
                            ev["status"] = KANBAN_COLUMNS[i+1]
                            save_events(events)
                            st.rerun()

                    # Optional delete button
                    if st.button("🗑️", key=f"{ev['id']}-del"):
                        events = [e for e in events if e["id"] != ev["id"]]
                        save_events(events)
                        st.rerun()


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

def backlog_view(events):
    st.header("Backlog (No Deadline)")
    backlog = [ev for ev in events if not ev.get("start")]

    if not backlog:
        st.info("No tasks without deadlines.")
        return

    for ev in backlog:
        st.write(f"📝 {ev['title']}")