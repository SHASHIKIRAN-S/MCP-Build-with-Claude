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
