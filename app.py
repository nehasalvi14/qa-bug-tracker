import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# =========================================================
# QA CORE NEXUS - STABLE BACKEND
# Flask + In-Memory Database
# Compatible with existing index.html
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
import json

DB_FILE = os.path.join(BASE_DIR, 'database.json')

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "projects": [],
        "test_cases": [],
        "bugs": [],
        "activity_logs": []
    }

def save_db():
    with open(DB_FILE, 'w') as f:
        json.dump(db, f, indent=4)

db = load_db()

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates")
)

CORS(app)

app.config["JSON_SORT_KEYS"] = False


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def now_text():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def next_id(items):
    if not items:
        return 1
    return max(item.get("id", 0) for item in items) + 1


def add_activity(user, action):
    db["activity_logs"].insert(
        0,
        {
            "id": next_id(db["activity_logs"]),
            "user": user or "QA Team",
            "action": action,
            "timestamp": "Just now",
            "created_at": now_text()
        }
    )


def get_json():
    return request.get_json(silent=True) or {}


def find_by_id(collection, item_id):
    return next(
        (item for item in collection if item.get("id") == item_id),
        None
    )


# =========================================================
# IN-MEMORY DATABASE
# =========================================================

db = {

    # -----------------------------------------------------
    # USERS
    # -----------------------------------------------------

    "users": [
        {
            "id": 1,
            "username": "admin",
            "email": "admin@qanexus.com",
            "password": "admin",
            "role": "QA Head"
        },
        {
            "id": 2,
            "username": "nishit",
            "email": "nishit@qanexus.com",
            "password": "password123",
            "role": "QA Head"
        },
        {
            "id": 3,
            "username": "priya",
            "email": "priya@qanexus.com",
            "password": "password123",
            "role": "QA Tester"
        },
        {
            "id": 4,
            "username": "aditya",
            "email": "aditya@qanexus.com",
            "password": "password123",
            "role": "Developer"
        },
        {
            "id": 5,
            "username": "client",
            "email": "client@qanexus.com",
            "password": "password123",
            "role": "Client"
        }
    ],

    # -----------------------------------------------------
    # PROJECTS
    # -----------------------------------------------------

    "projects": [
        {
            "id": 1,
            "name": "E-Commerce Platform",
            "code": "ECOMM",
            "status": "Ongoing",
            "progress": 75,
            "team_details": "Nishit Dubey (QA Head), Aditya Joshi (Developer)",
            "outcome": "A scalable online shopping cart with seamless payment gateway integration and real-time order tracking."
        },
        {
            "id": 2,
            "name": "Banking Mobile App",
            "code": "BANK",
            "status": "Done",
            "progress": 100,
            "team_details": "Priya Nair (QA Tester), Rahul Deshmukh (Developer)",
            "outcome": "Secure mobile banking portal with biometric authentication and zero high-severity defects."
        }
    ],

    # -----------------------------------------------------
    # SPRINTS
    # -----------------------------------------------------

    "sprints": [
        {
            "id": 1,
            "sprint_code": "SPR-001",
            "name": "Sprint 14",
            "project": "E-Commerce Platform",
            "goal": "Checkout & Payment Improvements",
            "start_date": "2026-09-01",
            "end_date": "2026-09-14",
            "status": "Active",
            "sprint_lead": "Nishit Dubey"
        },
        {
            "id": 2,
            "sprint_code": "SPR-002",
            "name": "Sprint 13",
            "project": "E-Commerce Platform",
            "goal": "Cart & Product Improvements",
            "start_date": "2026-08-18",
            "end_date": "2026-08-31",
            "status": "Completed",
            "sprint_lead": "Priya Nair"
        }
    ],

    # -----------------------------------------------------
    # BUGS
    # -----------------------------------------------------

    "bugs": [
        {
            "id": 1,
            "bug_code": "BUG-1001",
            "title": "Payment Gateway 504 Timeout Error",
            "project": "E-Commerce Platform",
            "sprint": "Sprint 14",
            "severity": "Critical",
            "priority": "High",
            "status": "Open",
            "description": "Checkout process fails on payment gateway redirection under peak loads.",
            "steps": "1. Add items to cart\n2. Proceed to checkout\n3. Select Credit Card payment\n4. Click Pay Now",
            "expected_result": "Payment confirmation page should load within 3 seconds.",
            "actual_result": "Server responds with 504 Gateway Timeout error screen.",
            "assigned_tester": "Priya Nair",
            "assigned_developer": "Aditya Joshi",
            "comments": [
                {
                    "author": "Priya Nair",
                    "text": "Issue reproduced during peak-load testing.",
                    "time": "1 hour ago"
                }
            ],
            "audit_history": [
                {
                    "action": "Bug created",
                    "user": "Priya Nair",
                    "time": "Today"
                },
                {
                    "action": "Assigned to Aditya Joshi",
                    "user": "Nishit Dubey",
                    "time": "Today"
                }
            ]
        },

        {
            "id": 2,
            "bug_code": "BUG-1002",
            "title": "Profile Avatar Upload Crop Bug",
            "project": "E-Commerce Platform",
            "sprint": "Sprint 14",
            "severity": "Medium",
            "priority": "Medium",
            "status": "In Progress",
            "description": "User profile avatar gets stretched when uploading non-square PNG images.",
            "steps": "1. Go to settings\n2. Upload rectangular avatar\n3. Click save",
            "expected_result": "Image should automatically crop to square aspect ratio.",
            "actual_result": "Image gets horizontally stretched.",
            "assigned_tester": "Nishit Dubey",
            "assigned_developer": "Rahul Deshmukh",
            "comments": [],
            "audit_history": [
                {
                    "action": "Bug created",
                    "user": "Nishit Dubey",
                    "time": "Yesterday"
                }
            ]
        }
    ],

    # -----------------------------------------------------
    # TEST CASES
    # -----------------------------------------------------

    "test_cases": [
        {
            "id": 1,
            "test_code": "TC-1001",
            "title": "Verify Login with Valid Credentials",
            "module": "Authentication",
            "project": "E-Commerce Platform",
            "sprint": "Sprint 14",
            "priority": "High",
            "preconditions": "User account exists in system.",
            "steps": "1. Open login modal\n2. Enter valid email and password\n3. Click Login",
            "expected_result": "User should be logged in and redirected to dashboard.",
            "actual_result": "User successfully logged in with toast notification.",
            "assigned_tester": "Priya Nair",
            "test_result": "Passed"
        },

        {
            "id": 2,
            "test_code": "TC-1002",
            "title": "Verify Password Reset Token Expiry",
            "module": "Authentication",
            "project": "E-Commerce Platform",
            "sprint": "Sprint 14",
            "priority": "Medium",
            "preconditions": "Reset token generated.",
            "steps": "1. Request password reset\n2. Wait 15 minutes\n3. Click reset link",
            "expected_result": "Link should display 'Token Expired' message.",
            "actual_result": "Link allows password update even after expiry.",
            "assigned_tester": "Nishit Dubey",
            "test_result": "Failed"
        }
    ],

    # -----------------------------------------------------
    # TEAM
    # -----------------------------------------------------

    "team": [
        {
            "id": 1,
            "name": "Nishit Dubey",
            "role": "QA Head",
            "department": "Tech / QA",
            "status": "Active",
            "assigned_projects": "E-Commerce Platform",
            "assigned_tasks": 4
        },

        {
            "id": 2,
            "name": "Priya Nair",
            "role": "QA Tester",
            "department": "Quality Assurance",
            "status": "Active",
            "assigned_projects": "E-Commerce Platform, Banking Mobile App",
            "assigned_tasks": 6
        },

        {
            "id": 3,
            "name": "Aditya Joshi",
            "role": "Developer",
            "department": "Backend Engineering",
            "status": "Away",
            "assigned_projects": "E-Commerce Platform",
            "assigned_tasks": 3
        },

        {
            "id": 4,
            "name": "Amitabh Banerjee",
            "role": "Client",
            "department": "Product Management",
            "status": "Active",
            "assigned_projects": "Banking Mobile App",
            "assigned_tasks": 0
        }
    ],

    # -----------------------------------------------------
    # REPORTS
    # -----------------------------------------------------

    "reports": [
        {
            "id": 1,
            "title": "Sprint 14 Defect Audit",
            "project": "E-Commerce Platform",
            "generated_by": "Nishit Dubey",
            "date": "2026-09-28",
            "summary": "Audited 12 defects logged during payment integration phase. Critical bugs isolated."
        }
    ],

    # -----------------------------------------------------
    # ACTIVITY LOGS
    # -----------------------------------------------------

    "activity_logs": [
        {
            "id": 1,
            "user": "Nishit Dubey",
            "action": "assigned BUG-1001 to Aditya Joshi",
            "timestamp": "2 minutes ago",
            "created_at": now_text()
        },
        {
            "id": 2,
            "user": "Priya Nair",
            "action": "created Sprint 14",
            "timestamp": "1 hour ago",
            "created_at": now_text()
        }
    ]
}


# =========================================================
# HOME
# =========================================================

@app.route("/")
def index():
    return render_template("index.html")


# =========================================================
# AUTHENTICATION
# =========================================================

@app.route("/api/auth/register", methods=["POST"])
def register():

    data = get_json()

    username = str(data.get("username", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))
    role = str(data.get("role", "QA Tester")).strip()

    if not username or not email or not password:
        return jsonify({
            "error": "Username, email and password are required."
        }), 400

    for user in db["users"]:

        if user["username"].lower() == username.lower():
            return jsonify({
                "error": "Username already exists!"
            }), 400

        if user["email"].lower() == email:
            return jsonify({
                "error": "Email already exists!"
            }), 400

    new_user = {
        "id": next_id(db["users"]),
        "username": username,
        "email": email,
        "password": password,
        "role": role
    }

    db["users"].append(new_user)

    add_activity(
        username,
        f"created a new {role} account"
    )

    return jsonify({
        "message": "Registration successful!",
        "user": new_user
    }), 201


@app.route("/api/auth/login", methods=["POST"])
def login():

    if request.is_json:
        data = request.get_json(silent=True) or {}
    else:
        data = request.form.to_dict()

    login_id = (
        data.get("username")
        or data.get("email")
        or data.get("login")
        or ""
    ).strip()

    password = str(data.get("password", ""))

    if not login_id or not password:
        return jsonify({
            "error": "Username/email and password are required."
        }), 400

    for user in db["users"]:

        if (
            (
                user["username"].lower() == login_id.lower()
                or
                user["email"].lower() == login_id.lower()
            )
            and
            user["password"] == password
        ):

            add_activity(
                user["username"],
                "logged into QA Core Nexus"
            )

            return jsonify({
                "message": "Login successful!",
                "user": user
            }), 200

    return jsonify({
        "error": "Invalid credentials!"
    }), 401


# =========================================================
# PROJECTS
# =========================================================

@app.route("/api/projects", methods=["GET", "POST"])
def handle_projects():

    if request.method == "GET":
        return jsonify(db["projects"])

    data = get_json()

    name = str(data.get("name", "")).strip()

    if not name:
        return jsonify({
            "error": "Project name is required."
        }), 400

    new_project = {
        "id": next_id(db["projects"]),
        "name": name,
        "code": data.get(
            "code",
            f"PRJ-{next_id(db['projects']):03d}"
        ),
        "status": data.get("status", "Ongoing"),
        "progress": int(data.get("progress", 0)),
        "team_details": data.get(
            "team_details",
            "Unassigned"
        ),
        "outcome": data.get(
            "outcome",
            "No outcome specified yet."
        )
    }

    db["projects"].append(new_project)

    add_activity(
        data.get("created_by", "QA Team"),
        f"created project {name}"
    )

    return jsonify(new_project), 201


@app.route("/api/projects/<int:pid>", methods=["GET", "PATCH", "PUT", "DELETE"])
def project_detail(pid):

    project = find_by_id(db["projects"], pid)

    if not project:
        return jsonify({
            "error": "Project not found"
        }), 404

    if request.method == "GET":
        return jsonify(project)

    if request.method == "DELETE":

        deleted_name = project["name"]

        db["projects"].remove(project)

        add_activity(
            "QA Team",
            f"deleted project {deleted_name}"
        )

        return jsonify({
            "message": "Project deleted successfully"
        })

    data = get_json()

    if "name" in data:
        project["name"] = data["name"]

    if "code" in data:
        project["code"] = data["code"]

    if "status" in data:
        project["status"] = data["status"]

    if "progress" in data:
        try:
            project["progress"] = max(
                0,
                min(100, int(data["progress"]))
            )
        except:
            pass

    if "team_details" in data:
        project["team_details"] = data["team_details"]

    if "outcome" in data:
        project["outcome"] = data["outcome"]

    add_activity(
        data.get("updated_by", "QA Team"),
        f"updated project {project['name']}"
    )

    return jsonify(project)


# =========================================================
# SPRINTS
# =========================================================

@app.route("/api/sprints", methods=["GET", "POST"])
def handle_sprints():

    if request.method == "GET":
        return jsonify(db["sprints"])

    data = get_json()

    name = str(data.get("name", "")).strip()

    if not name:
        return jsonify({
            "error": "Sprint name is required."
        }), 400

    new_sprint = {
        "id": next_id(db["sprints"]),
        "sprint_code": f"SPR-{next_id(db['sprints']):03d}",
        "name": name,
        "project": data.get(
            "project",
            "E-Commerce Platform"
        ),
        "goal": data.get("goal", ""),
        "start_date": data.get("start_date", ""),
        "end_date": data.get("end_date", ""),
        "status": data.get("status", "Planned"),
        "sprint_lead": data.get(
            "sprint_lead",
            "QA Team"
        )
    }

    db["sprints"].append(new_sprint)

    add_activity(
        new_sprint["sprint_lead"],
        f"created {name}"
    )

    return jsonify(new_sprint), 201


@app.route("/api/sprints/<int:sid>", methods=["GET", "PATCH", "PUT", "DELETE"])
def sprint_detail(sid):

    sprint = find_by_id(db["sprints"], sid)

    if not sprint:
        return jsonify({
            "error": "Sprint not found"
        }), 404

    if request.method == "GET":
        return jsonify(sprint)

    if request.method == "DELETE":

        name = sprint["name"]

        db["sprints"].remove(sprint)

        add_activity(
            "QA Team",
            f"deleted {name}"
        )

        return jsonify({
            "message": "Sprint deleted successfully"
        })

    data = get_json()

    allowed_fields = [
        "name",
        "project",
        "goal",
        "start_date",
        "end_date",
        "status",
        "sprint_lead"
    ]

    for field in allowed_fields:
        if field in data:
            sprint[field] = data[field]

    add_activity(
        data.get("updated_by", "QA Team"),
        f"updated {sprint['name']}"
    )

    return jsonify(sprint)


# =========================================================
# BUGS
# =========================================================

@app.route("/api/bugs", methods=["GET", "POST"])
def handle_bugs():

    if request.method == "GET":
        return jsonify(db["bugs"])

    data = get_json()

    title = str(data.get("title", "")).strip()

    if not title:
        return jsonify({
            "error": "Bug title is required."
        }), 400

    bug_id = next_id(db["bugs"])

    new_bug = {
        "id": bug_id,
        "bug_code": f"BUG-{1000 + bug_id}",
        "title": title,
        "project": data.get(
            "project",
            "E-Commerce Platform"
        ),
        "sprint": data.get(
            "sprint",
            "Sprint 14"
        ),
        "severity": data.get(
            "severity",
            "Medium"
        ),
        "priority": data.get(
            "priority",
            "Medium"
        ),
        "status": data.get(
            "status",
            "New"
        ),
        "description": data.get(
            "description",
            ""
        ),
        "steps": data.get(
            "steps",
            ""
        ),
        "expected_result": data.get(
            "expected_result",
            ""
        ),
        "actual_result": data.get(
            "actual_result",
            ""
        ),
        "assigned_tester": data.get(
            "assigned_tester",
            "Unassigned"
        ),
        "assigned_developer": data.get(
            "assigned_developer",
            "Unassigned"
        ),
        "comments": [],
        "audit_history": [
            {
                "action": "Bug created",
                "user": data.get(
                    "created_by",
                    "QA Team"
                ),
                "time": "Just now"
            }
        ]
    }

    db["bugs"].append(new_bug)

    add_activity(
        data.get("created_by", "QA Team"),
        f"created {new_bug['bug_code']} - {title}"
    )

    return jsonify(new_bug), 201


@app.route("/api/bugs/<int:bid>", methods=["GET", "PATCH", "PUT", "DELETE"])
def bug_detail(bid):

    bug = find_by_id(db["bugs"], bid)

    if not bug:
        return jsonify({
            "error": "Bug not found"
        }), 404

    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------

    if request.method == "GET":
        return jsonify(bug)

    # -----------------------------------------------------
    # DELETE
    # -----------------------------------------------------

    if request.method == "DELETE":

        bug_code = bug["bug_code"]

        db["bugs"].remove(bug)

        add_activity(
            "QA Team",
            f"deleted {bug_code}"
        )

        return jsonify({
            "message": "Bug deleted successfully"
        })

    # -----------------------------------------------------
    # UPDATE
    # -----------------------------------------------------

    data = get_json()

    editable_fields = [
        "title",
        "project",
        "sprint",
        "severity",
        "priority",
        "status",
        "description",
        "steps",
        "expected_result",
        "actual_result",
        "assigned_tester",
        "assigned_developer"
    ]

    changes = []

    for field in editable_fields:

        if field in data:

            old_value = bug.get(field)
            new_value = data[field]

            if old_value != new_value:
                bug[field] = new_value
                changes.append(field)

    if changes:

        user = data.get(
            "updated_by",
            "QA Team"
        )

        bug.setdefault(
            "audit_history",
            []
        )

        bug["audit_history"].insert(
            0,
            {
                "action": "Updated: " + ", ".join(changes),
                "user": user,
                "time": "Just now"
            }
        )

        add_activity(
            user,
            f"updated {bug['bug_code']}"
        )

    return jsonify(bug)


# =========================================================
# BUG STATUS WORKFLOW
# =========================================================

@app.route("/api/bugs/<int:bug_id>/status", methods=["POST", "PATCH"])
def update_bug_status(bug_id):

    bug = find_by_id(db["bugs"], bug_id)

    if not bug:
        return jsonify({
            "error": "Bug not found"
        }), 404

    data = get_json()

    new_status = data.get("status")

    allowed_statuses = [
        "New",
        "Open",
        "In Progress",
        "Resolved",
        "Retest",
        "Closed"
    ]

    if new_status not in allowed_statuses:
        return jsonify({
            "error": "Invalid bug status.",
            "allowed_statuses": allowed_statuses
        }), 400

    old_status = bug.get("status")

    bug["status"] = new_status

    user = data.get(
        "updated_by",
        "QA Team"
    )

    bug.setdefault(
        "audit_history",
        []
    )

    bug["audit_history"].insert(
        0,
        {
            "action": f"Status changed: {old_status} → {new_status}",
            "user": user,
            "time": "Just now"
        }
    )

    add_activity(
        user,
        f"changed {bug['bug_code']} status from {old_status} to {new_status}"
    )

    return jsonify({
        "success": True,
        "status": new_status,
        "bug": bug
    })


# =========================================================
# BUG COMMENTS
# =========================================================

@app.route("/api/bugs/<int:bug_id>/comments", methods=["GET", "POST"])
def post_bug_comment(bug_id):

    bug = find_by_id(db["bugs"], bug_id)

    if not bug:
        return jsonify({
            "error": "Bug not found"
        }), 404

    bug.setdefault(
        "comments",
        []
    )

    if request.method == "GET":
        return jsonify(bug["comments"])

    data = get_json()

    comment_text = str(
        data.get("comment", "")
    ).strip()

    if not comment_text:
        return jsonify({
            "error": "Comment cannot be empty."
        }), 400

    author = data.get(
        "author",
        "Neha Salvi"
    )

    new_comment = {
        "author": author,
        "text": comment_text,
        "time": "Just now"
    }

    bug["comments"].append(
        new_comment
    )

    bug.setdefault(
        "audit_history",
        []
    )

    bug["audit_history"].insert(
        0,
        {
            "action": "Added a comment",
            "user": author,
            "time": "Just now"
        }
    )

    add_activity(
        author,
        f"commented on {bug['bug_code']}"
    )

    return jsonify({
        "success": True,
        "comment": new_comment
    }), 201


# =========================================================
# TEST CASES
# =========================================================

@app.route("/api/test-cases", methods=["GET", "POST"])
def handle_test_cases():

    if request.method == "GET":
        return jsonify(db["test_cases"])

    data = get_json()

    title = str(
        data.get("title", "")
    ).strip()

    if not title:
        return jsonify({
            "error": "Test case title is required."
        }), 400

    tc_id = next_id(
        db["test_cases"]
    )

    new_test_case = {
        "id": tc_id,
        "test_code": f"TC-{1000 + tc_id}",
        "title": title,
        "module": data.get(
            "module",
            "General"
        ),
        "project": data.get(
            "project",
            "E-Commerce Platform"
        ),
        "sprint": data.get(
            "sprint",
            "Sprint 14"
        ),
        "priority": data.get(
            "priority",
            "Medium"
        ),
        "preconditions": data.get(
            "preconditions",
            ""
        ),
        "steps": data.get(
            "steps",
            ""
        ),
        "expected_result": data.get(
            "expected_result",
            ""
        ),
        "actual_result": data.get(
            "actual_result",
            ""
        ),
        "assigned_tester": data.get(
            "assigned_tester",
            "Unassigned"
        ),
        "test_result": data.get(
            "test_result",
            "Not Run"
        )
    }

    db["test_cases"].append(
        new_test_case
    )

    add_activity(
        data.get(
            "created_by",
            "QA Team"
        ),
        f"created {new_test_case['test_code']}"
    )

    return jsonify(
        new_test_case
    ), 201


@app.route("/api/test-cases/<int:tcid>", methods=["GET", "PATCH", "PUT", "DELETE"])
def tc_detail(tcid):

    test_case = find_by_id(
        db["test_cases"],
        tcid
    )

    if not test_case:
        return jsonify({
            "error": "Test Case not found"
        }), 404

    if request.method == "GET":
        return jsonify(test_case)

    if request.method == "DELETE":

        code = test_case["test_code"]

        db["test_cases"].remove(
            test_case
        )

        add_activity(
            "QA Team",
            f"deleted {code}"
        )

        return jsonify({
            "message": "Test case deleted successfully"
        })

    data = get_json()

    editable_fields = [
        "title",
        "module",
        "project",
        "sprint",
        "priority",
        "preconditions",
        "steps",
        "expected_result",
        "actual_result",
        "assigned_tester",
        "test_result"
    ]

    changed = []

    for field in editable_fields:

        if field in data:

            if test_case.get(field) != data[field]:

                test_case[field] = data[field]
                changed.append(field)

    if changed:

        add_activity(
            data.get(
                "updated_by",
                "QA Team"
            ),
            f"updated {test_case['test_code']}"
        )

    return jsonify(test_case)


# =========================================================
# TEAM
# =========================================================

@app.route("/api/team", methods=["GET", "POST"])
def handle_team():

    if request.method == "GET":
        return jsonify(db["team"])

    data = get_json()

    name = str(
        data.get("name", "")
    ).strip()

    role = str(
        data.get("role", "")
    ).strip()

    department = str(
        data.get("department", "")
    ).strip()

    if not name or not role:
        return jsonify({
            "error": "Name and role are required."
        }), 400

    member_id = next_id(
        db["team"]
    )

    new_member = {
        "id": member_id,
        "name": name,
        "role": role,
        "department": department or "General",
        "status": data.get(
            "status",
            "Active"
        ),
        "assigned_projects": data.get(
            "assigned_projects",
            "None"
        ),
        "assigned_tasks": int(
            data.get(
                "assigned_tasks",
                0
            )
        )
    }

    db["team"].append(
        new_member
    )

    add_activity(
        data.get(
            "created_by",
            "QA Team"
        ),
        f"added team member {name}"
    )

    return jsonify(
        new_member
    ), 201


@app.route("/api/team/<int:mid>", methods=["GET", "PATCH", "PUT", "DELETE"])
def team_member_detail(mid):

    member = find_by_id(
        db["team"],
        mid
    )

    if not member:
        return jsonify({
            "error": "Team member not found"
        }), 404

    if request.method == "GET":
        return jsonify(member)

    if request.method == "DELETE":

        name = member["name"]

        db["team"].remove(
            member
        )

        add_activity(
            "QA Team",
            f"removed team member {name}"
        )

        return jsonify({
            "message": "Team member deleted successfully"
        })

    data = get_json()

    fields = [
        "name",
        "role",
        "department",
        "status",
        "assigned_projects",
        "assigned_tasks"
    ]

    for field in fields:

        if field in data:

            if field == "assigned_tasks":

                try:
                    member[field] = int(
                        data[field]
                    )
                except:
                    member[field] = 0

            else:
                member[field] = data[field]

    add_activity(
        data.get(
            "updated_by",
            "QA Team"
        ),
        f"updated team member {member['name']}"
    )

    return jsonify(member)


# =========================================================
# REPORTS
# =========================================================

@app.route("/api/reports", methods=["GET", "POST"])
def handle_reports():

    if request.method == "GET":
        return jsonify(db["reports"])

    data = get_json()

    title = str(
        data.get("title", "")
    ).strip()

    if not title:
        return jsonify({
            "error": "Report title is required."
        }), 400

    report_id = next_id(
        db["reports"]
    )

    new_report = {
        "id": report_id,
        "title": title,
        "project": data.get(
            "project",
            "E-Commerce Platform"
        ),
        "generated_by": data.get(
            "generated_by",
            "QA Lead"
        ),
        "date": datetime.now().strftime(
            "%Y-%m-%d"
        ),
        "summary": data.get(
            "summary",
            ""
        )
    }

    db["reports"].append(
        new_report
    )

    add_activity(
        new_report["generated_by"],
        f"generated report {title}"
    )

    return jsonify(
        new_report
    ), 201


@app.route("/api/reports/<int:rid>", methods=["GET", "PATCH", "PUT", "DELETE"])
def report_detail(rid):

    report = find_by_id(
        db["reports"],
        rid
    )

    if not report:
        return jsonify({
            "error": "Report not found"
        }), 404

    if request.method == "GET":
        return jsonify(report)

    if request.method == "DELETE":

        title = report["title"]

        db["reports"].remove(
            report
        )

        add_activity(
            "QA Team",
            f"deleted report {title}"
        )

        return jsonify({
            "message": "Report deleted successfully"
        })

    data = get_json()

    fields = [
        "title",
        "project",
        "generated_by",
        "summary"
    ]

    for field in fields:

        if field in data:
            report[field] = data[field]

    add_activity(
        data.get(
            "updated_by",
            "QA Team"
        ),
        f"updated report {report['title']}"
    )

    return jsonify(report)


# =========================================================
# ACTIVITY LOGS
# =========================================================

@app.route("/api/activity-logs", methods=["GET"])
def get_activity_logs():

    return jsonify(
        db["activity_logs"]
    )


# =========================================================
# DASHBOARD STATISTICS
# =========================================================
@app.route("/api/stats", methods=["GET"])
def get_stats_data():
    projects = db["projects"]
    bugs = db["bugs"]
    test_cases = db["test_cases"]
    
    resolved_bugs = sum(1 for b in bugs if b.get("status") == "Resolved")
    pending_bugs = len(bugs) - resolved_bugs
    
    return jsonify({
        "total_projects": len(projects),
        "total_bugs": len(bugs),
        "critical_bugs": sum(1 for b in bugs if b.get("severity") == "Critical"),
        "high_bugs": sum(1 for b in bugs if b.get("severity") == "High"),
        "medium_bugs": sum(1 for b in bugs if b.get("severity") == "Medium"),
        "low_bugs": sum(1 for b in bugs if b.get("severity") == "Low"),
        "pending_bugs": pending_bugs,
        "resolved_bugs": resolved_bugs,
        "total_test_cases": len(test_cases),
        "passed_test_cases": sum(1 for t in test_cases if t.get("status") == "Passed"),
        "overall_progress": round((resolved_bugs / len(bugs) * 100) if bugs else 0, 1)
    })

@app.route("/api/dashboard", methods=["GET"])
def dashboard():

    projects = db["projects"]
    bugs = db["bugs"]
    test_cases = db["test_cases"]

    total_bugs = len(bugs)

    critical_bugs = sum(
        1
        for b in bugs
        if b.get("severity") == "Critical"
    )

    pending_bugs = sum(
        1
        for b in bugs
        if b.get("status")
        in [
            "New",
            "Open",
            "In Progress",
            "Retest"
        ]
    )

    resolved_bugs = sum(
        1
        for b in bugs
        if b.get("status")
        in [
            "Resolved",
            "Closed"
        ]
    )

    severity_summary = {
        "Critical": 0,
        "High": 0,
        "Medium": 0,
        "Low": 0
    }

    for bug in bugs:

        severity = bug.get(
            "severity",
            "Medium"
        )

        if severity in severity_summary:
            severity_summary[severity] += 1

    status_summary = {
        "New": 0,
        "Open": 0,
        "In Progress": 0,
        "Resolved": 0,
        "Retest": 0,
        "Closed": 0
    }

    for bug in bugs:

        status = bug.get(
            "status",
            "New"
        )

        if status in status_summary:
            status_summary[status] += 1

    passed_tests = sum(
        1
        for tc in test_cases
        if tc.get("test_result") == "Passed"
    )

    overall_progress = 0

    if total_bugs > 0:
        overall_progress = round(
            (resolved_bugs / total_bugs) * 100
        )

    return jsonify({

        "total_projects": len(projects),

        "total_bugs": total_bugs,

        "critical_bugs": critical_bugs,

        "pending_bugs": pending_bugs,

        "resolved_bugs": resolved_bugs,

        "total_test_cases": len(test_cases),

        "passed_test_cases": passed_tests,

        "overall_progress": overall_progress,

        "severity_summary": severity_summary,

        "status_summary": status_summary

    })


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/api/health", methods=["GET"])
def health():

    return jsonify({
        "status": "ok",
        "application": "QA Core Nexus",
        "backend": "Flask",
        "database": "In-Memory",
        "projects": len(db["projects"]),
        "bugs": len(db["bugs"]),
        "test_cases": len(db["test_cases"]),
        "team_members": len(db["team"])
    })


# =========================================================
# ERROR HANDLERS
# =========================================================

@app.errorhandler(404)
def not_found(error):

    if request.path.startswith("/api/"):

        return jsonify({
            "error": "API endpoint not found",
            "path": request.path
        }), 404

    return error


@app.errorhandler(500)
def internal_error(error):

    if request.path.startswith("/api/"):

        return jsonify({
            "error": "Internal server error"
        }), 500

    return error


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    print("")
    print("=" * 55)
    print("        QA CORE NEXUS - BACKEND")
    print("=" * 55)
    print(f"Server running on port: {port}")
    print("Local URL: http://127.0.0.1:5000")
    print("Health:    http://127.0.0.1:5000/api/health")
    print("=" * 55)
    print("")

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )