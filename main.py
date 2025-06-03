<<<<<<< HEAD
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


=======
# server.py

from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import random

# Initialize MCP server
mcp = FastMCP("LeaveTracker")

# Leave reasons and statuses
reasons = ["Fever", "Cold", "Family trip", "Medical checkup", "Headache", "Travel", "Sick", "Doctor appointment", "Sports event", "Personal"]
statuses = ["pending", "approved", "rejected"]

# In-memory "database"
leave_db: Dict[str, List[Dict]] = {}

# Generate test data
student_ids = [f"stu{str(i).zfill(3)}" for i in range(1, 26)]
base_date = datetime(2025, 5, 1)
record_count = 0

while record_count < 100:
    for student_id in student_ids:
        if record_count >= 100:
            break
        leave_date = base_date + timedelta(days=random.randint(0, 14))
        leave_entry = {
            "date": leave_date.strftime("%Y-%m-%d"),
            "reason": random.choice(reasons),
            "status": random.choice(statuses),
            "timestamp": datetime.now().isoformat()
        }
        leave_db.setdefault(student_id, []).append(leave_entry)
        record_count += 1

print(f"Generated {record_count} leave records for {len(leave_db)} students.")

# Tool to submit a leave request
@mcp.tool()
def submit_leave(student_id: str, date: str, reason: str) -> str:
    """Submit a leave request for a student"""
    try:
        datetime.strptime(date, "%Y-%m-%d")  # Validate format
    except ValueError:
        return "Invalid date format. Use YYYY-MM-DD."

    for entry in leave_db.get(student_id, []):
        if entry["date"] == date:
            return f"Leave already submitted for {date}."

    leave_entry = {
        "date": date,
        "reason": reason,
        "status": "pending",
        "timestamp": datetime.now().isoformat()
    }
    leave_db.setdefault(student_id, []).append(leave_entry)
    return f"Leave submitted for {student_id} on {date}."

# Tool to view student's leave history
@mcp.tool()
def get_leave_history(student_id: str, status: Optional[str] = None) -> List[Dict]:
    """Get leave history for a student, optionally filtered by status"""
    history = leave_db.get(student_id, [])
    if status:
        return [entry for entry in history if entry["status"] == status]
    return history

# Tool to get all requests
@mcp.tool()
def get_all_leave_requests() -> Dict[str, List[Dict]]:
    """Get all leave requests across students"""
    return leave_db

# Tool to update leave status
@mcp.tool()
def update_leave_status(student_id: str, date: str, new_status: str) -> str:
    """Approve or reject a leave request"""
    valid_statuses = {"approved", "rejected", "pending"}
    if new_status not in valid_statuses:
        return f"Invalid status. Choose from {valid_statuses}."

    for entry in leave_db.get(student_id, []):
        if entry["date"] == date:
            entry["status"] = new_status
            return f"Leave on {date} for {student_id} marked as {new_status}."
    return f"No leave found for {student_id} on {date}."

# Greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    return f"Hello, {name}!"

def main():
    print("Hello from mcp-server!")

if __name__ == "__main__":
    main()
>>>>>>> 301e0d6ed47d90f17c4215fb8b1908ef0bb6085d
