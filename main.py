# main.py (Streamlit Frontend - MODIFIED)

import streamlit as st
import requests
import datetime
import sys
import os
from mcp.server.fastmcp import FastMCP

# Add project root (i.e., directory containing `mcp/`) to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))


# FastAPI backend URL
API_URL = "http://127.0.0.1:8000"

# --- API Helper Functions ---

def register_student(student_id, student_name):
    try:
        response = requests.post(f"{API_URL}/register_student", json={
            "student_id": student_id,
            "student_name": student_name
        })
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def submit_leave_request(student_id, date, reason):
    try:
        response = requests.post(f"{API_URL}/submit_leave", json={
            "student_id": student_id,
            "date": date,
            "reason": reason
        })
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_leave_history(student_id, status=None):
    try:
        url = f"{API_URL}/get_leave_history/{student_id}"
        if status:
            url += f"?status={status}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_ai_response(prompt, student_id=None):
    try:
        payload = {"prompt": prompt}
        if student_id:
            payload["student_id"] = student_id

        response = requests.post(f"{API_URL}/ai_query", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# --- Streamlit UI ---

st.set_page_config(
    page_title="Leave Management System",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📘 Leave Management System")

# --- Student Registration Section ---
st.header("🧑 Register New Student")
new_student_id = st.text_input("Student ID", key="reg_student_id")
new_student_name = st.text_input("Student Name", key="reg_student_name")

if st.button("Register Student"):
    if new_student_id and new_student_name:
        result = register_student(new_student_id, new_student_name)
        if "error" in result:
            st.error(f"Error: {result['error']}")
        else:
            st.success(result.get("message", "Student registered successfully!"))
    else:
        st.error("Please fill in both Student ID and Student Name.")

# --- Leave Submission Section ---
st.header("📝 Submit Leave Request")
student_id_submit = st.text_input("Student ID (Submit)", key="submit_student_id")
date_submit = st.date_input("Date (Submit)", datetime.date.today(), key="submit_date")
reason_submit = st.text_area("Reason for Leave (Submit)", key="submit_reason")

if st.button("Submit Leave Request"):
    if student_id_submit and reason_submit:
        result = submit_leave_request(student_id_submit, date_submit.strftime("%Y-%m-%d"), reason_submit)
        if "error" in result:
            st.error(f"Error submitting leave: {result['error']}")
        else:
            st.success(result.get("message", "Leave request submitted!"))
    else:
        st.error("Please fill in all fields for submission.")

st.markdown("---")

# --- Leave History by Student ID ---
st.header("📜 Get Leave History by Student ID")
student_id_history = st.text_input("Enter Student ID for History", key="history_student_id")
status_filter = st.selectbox("Filter by Status", options=["", "pending", "approved", "rejected"], key="history_status_filter")

if st.button("Get Leave History"):
    if student_id_history:
        history = get_leave_history(student_id_history, status_filter if status_filter else None)
        if "error" in history:
            st.error(f"Error fetching history: {history['error']}")
        elif isinstance(history, list) and len(history) > 0:
            st.subheader(f"Leave History for Student ID: {student_id_history}")
            history_data = [
                {
                    "Date": record.get('date', 'N/A'),
                    "Reason": record.get('reason', 'N/A'),
                    "Status": record.get('status', 'N/A')
                }
                for record in history
            ]
            st.table(history_data)
        else:
            st.info("No leave history found for this student ID or filter.")
    else:
        st.error("Please enter a Student ID to view history.")


