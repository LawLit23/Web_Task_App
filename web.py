import streamlit as st
import functions
import os

# Load todos
todos = functions.get_todos()


def add_todo():
    """Add a new task to the list."""
    if st.session_state["new_todo"]:  # Ensure input is not empty
        todo = st.session_state["new_todo"] + "\n"
        todos.append(todo)
        functions.write_todos(todos)
        st.session_state["new_todo"] = ""  # Clears input field


def complete_task():
    """Remove completed tasks from the list."""
    completed_indexes = [index for index, todo in enumerate(
        todos) if st.session_state.get(f"todo_{index}")]
    # Reverse to avoid index shift issues
    for index in reversed(completed_indexes):
        todos.pop(index)
    functions.write_todos(todos)
    # Reset state for the removed tasks
    for index in completed_indexes:
        del st.session_state[f"todo_{index}"]


# App Title
st.title("Lawrence's Daily Task Manager")
st.subheader("Add and manage your daily tasks:")

# Display checkboxes for tasks with unique keys
for index, todo in enumerate(todos):
    st.checkbox(todo.strip(), key=f"todo_{index}")

# Button to complete selected tasks
if st.button("Complete Selected Tasks"):
    complete_task()
    st.rerun()  # Refresh app to update the list of tasks

# Input field to add new tasks
st.text_input(label="Enter new task", placeholder="Add new tasks...",
              on_change=add_todo, key="new_todo")
