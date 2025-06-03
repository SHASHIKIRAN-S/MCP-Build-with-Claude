# MCP Leave Tracker Server

A FastMCP-based server application for managing student leave requests. This application provides a simple and efficient way to handle leave submissions, approvals, and tracking for students.

## Features

- Submit leave requests with date and reason
- View leave history for individual students
- Filter leave requests by status (pending, approved, rejected)
- Update leave request status
- View all leave requests across students
- Test data generation for demonstration purposes

## Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd mcp-server
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On Unix or MacOS
source .venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Required Packages

Create a `requirements.txt` file with the following dependencies:

```
fastmcp>=1.0.0
python-dateutil>=2.8.2
typing-extensions>=4.5.0
```

## Project Structure

```
mcp-server/
├── main.py           # Main server implementation
├── README.md         # Project documentation
├── pyproject.toml    # Project configuration
├── requirements.txt  # Package dependencies
└── .venv/           # Virtual environment directory
```

## Usage

1. Start the server:
```bash
python main.py
```

2. Available Tools:

- `submit_leave(student_id: str, date: str, reason: str)`: Submit a new leave request
- `get_leave_history(student_id: str, status: Optional[str])`: View leave history for a student
- `get_all_leave_requests()`: Get all leave requests in the system
- `update_leave_status(student_id: str, date: str, new_status: str)`: Update leave request status

## Data Format

### Leave Request Structure
```python
{
    "date": "YYYY-MM-DD",
    "reason": str,
    "status": "pending" | "approved" | "rejected",
    "timestamp": "ISO-8601 timestamp"
}
```

## Development

The project uses Python 3.10+ and follows standard Python coding conventions. To contribute:

1. Create a new branch for your feature
2. Make your changes
3. Submit a pull request

