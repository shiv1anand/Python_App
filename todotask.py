import streamlit as st

st.title("📝 To-Do List App")

# Agar session me "tasks" nahi hai toh empty list banao
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Task input box
new_task = st.text_input("Enter a new task:")

# Add button
if st.button("➕ Add Task"):
    if new_task:
        st.session_state.tasks.append(new_task)
        st.success(f"✅ '{new_task}' added!")
    else:
        st.warning("⚠️ Please enter a task.")

st.subheader("📋 Your Tasks:")

# Show all tasks
if st.session_state.tasks:
    for i, task in enumerate(st.session_state.tasks):
        col1, col2 = st.columns([4, 1])  # layout
        col1.write(f"- {task}")
        if col2.button("❌ Delete", key=i):
            st.session_state.tasks.pop(i)
            st.rerun()
else:
    st.info("No tasks yet. Add some!")