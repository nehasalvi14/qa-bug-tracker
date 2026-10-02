import os
import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))
CORS(app)

# In-Memory Database initialized with complete default seed data + Sprints & Activity Logs
db = {
    "users": [
        {"id": 1, "username": "admin", "email": "admin@qanexus.com", "password": "admin", "role": "QA Head"},
        {"id": 2, "username": "nishit", "email": "nishit@qanexus.com", "password": "password123", "role": "QA Head"},
        {"id": 3, "username": "priya", "email": "priya@qanexus.com", "password": "password123", "role": "QA Tester"},
        {"id": 4, "username": "aditya", "email": "aditya@qanexus.com", "password": "password123", "role": "Developer"},
        {"id": 5, "username": "client", "email": "client@qanexus.com", "password": "password123", "role": "Client"}
    ],
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
            "team_details": "Priya Nair (QA Tester), Rahul Deshmukh (Dev)",
            "outcome": "Secure mobile banking portal with biometric authentication and zero high-severity defects."
        }
    ],
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
            "assigned_developer": "Aditya Joshi"
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
            "assigned_developer": "Rahul Deshmukh"
        }
    ],
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
    "activity_logs": [
        {
            "id": 1,
            "user": "Nishit Dubey",
            "action": "assigned BUG-1001 to Aditya Joshi",
            "timestamp": "2 minutes ago"
        },
        {
            "id": 2,
            "user": "Priya Nair",
            "action": "created Sprint 14",
            "timestamp": "1 hour ago"
        }
    ]
}

# ---------------------------------------------------------
# ROUTES & REST API ENDPOINTS
# ---------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')

# --- AUTHENTICATION ---
@app.route('/api/auth/register', methods=['POST'])
def register():
    payload = request.json
    for u in db['users']:
        if u['username'] == payload['username'] or u['email'] == payload['email']:
            return jsonify({"error": "User or Email already exists!"}), 400
    new_user = {
        "id": len(db['users']) + 1,
        "username": payload['username'],
        "email": payload['email'],
        "password": payload['password'],
        "role": payload['role']
    }
    db['users'].append(new_user)
    return jsonify({"message": "Registration successful!", "user": new_user}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    # Dono JSON aur Form requests ko safely handle karega
    payload = request.get_json(silent=True) or request.form
    login_id = payload.get('username')
    password = payload.get('password')
    
    for u in db['users']:
        if (u['username'] == login_id or u['email'] == login_id) and u['password'] == password:
            return jsonify({"message": "Login successful!", "user": u}), 200
            
    return jsonify({"error": "Invalid credentials!"}), 401
# --- PROJECTS ---
@app.route('/api/projects', methods=['GET', 'POST'])
def handle_projects():
    if request.method == 'POST':
        p = request.json
        new_p = {
            "id": len(db['projects']) + 1,
            "name": p['name'],
            "code": p.get('code', f"PRJ-{len(db['projects'])+1}"),
            "status": p.get('status', 'Ongoing'),
            "progress": int(p.get('progress', 0)),
            "team_details": p.get('team_details', 'Unassigned'),
            "outcome": p.get('outcome', 'No outcome specified yet.')
        }
        db['projects'].append(new_p)
        return jsonify(new_p), 201
    return jsonify(db['projects'])

@app.route('/api/projects/<int:pid>', methods=['PATCH', 'DELETE'])
def project_detail(pid):
    global db
    if request.method == 'DELETE':
        db['projects'] = [p for p in db['projects'] if p['id'] != pid]
        return jsonify({"message": "Project deleted successfully"})
    
    payload = request.json
    for p in db['projects']:
        if p['id'] == pid:
            if 'status' in payload: p['status'] = payload['status']
            if 'progress' in payload: p['progress'] = int(payload['progress'])
            return jsonify(p)
    return jsonify({"error": "Project not found"}), 404

# --- SPRINTS ---
@app.route('/api/sprints', methods=['GET', 'POST'])
def handle_sprints():
    if request.method == 'POST':
        s = request.json
        new_s = {
            "id": len(db['sprints']) + 1,
            "sprint_code": f"SPR-{len(db['sprints'])+1:03d}",
            "name": s['name'],
            "project": s['project'],
            "goal": s.get('goal', ''),
            "start_date": s['start_date'],
            "end_date": s['end_date'],
            "status": s.get('status', 'Planned'),
            "sprint_lead": s.get('sprint_lead', 'QA Team')
        }
        db['sprints'].append(new_s)
        
        # Add activity log
        db['activity_logs'].insert(0, {
            "id": len(db['activity_logs']) + 1,
            "user": s.get('sprint_lead', 'QA Team'),
            "action": f"created Sprint {s['name']}",
            "timestamp": "Just now"
        })
        return jsonify(new_s), 201
    return jsonify(db['sprints'])

@app.route('/api/sprints/<int:sid>', methods=['PATCH', 'DELETE'])
def sprint_detail(sid):
    global db
    if request.method == 'DELETE':
        db['sprints'] = [s for s in db['sprints'] if s['id'] != sid]
        return jsonify({"message": "Sprint deleted successfully"})
    
    payload = request.json
    for s in db['sprints']:
        if s['id'] == sid:
            if 'status' in payload: s['status'] = payload['status']
            if 'goal' in payload: s['goal'] = payload['goal']
            return jsonify(s)
    return jsonify({"error": "Sprint not found"}), 404

# --- BUGS ---
@app.route('/api/bugs', methods=['GET', 'POST'])
def handle_bugs():
    if request.method == 'POST':
        b = request.json
        new_b = {
            "id": len(db['bugs']) + 1,
            "bug_code": f"BUG-{1000 + len(db['bugs']) + 1}",
            "title": b['title'],
            "project": b['project'],
            "sprint": b.get('sprint', 'Sprint 14'),
            "severity": b.get('severity', 'Medium'),
            "priority": b.get('priority', 'Medium'),
            "status": b.get('status', 'New'),
            "description": b.get('description', ''),
            "steps": b.get('steps', ''),
            "expected_result": b.get('expected_result', ''),
            "actual_result": b.get('actual_result', ''),
            "assigned_tester": b.get('assigned_tester', 'Unassigned'),
            "assigned_developer": b.get('assigned_developer', 'Unassigned')
        }
        db['bugs'].append(new_b)
        return jsonify(new_b), 201
    return jsonify(db['bugs'])

@app.route('/api/bugs/<int:bid>', methods=['PATCH', 'DELETE'])
def bug_detail(bid):
    global db
    if request.method == 'DELETE':
        db['bugs'] = [b for b in db['bugs'] if b['id'] != bid]
        return jsonify({"message": "Bug deleted successfully"})
    
    payload = request.json
    for b in db['bugs']:
        if b['id'] == bid:
            if 'status' in payload: b['status'] = payload['status']
            if 'severity' in payload: b['severity'] = payload['severity']
            if 'assigned_developer' in payload: b['assigned_developer'] = payload['assigned_developer']
            return jsonify(b)
    return jsonify({"error": "Bug not found"}), 404

# --- TEST CASES ---
@app.route('/api/test-cases', methods=['GET', 'POST'])
def handle_test_cases():
    if request.method == 'POST':
        tc = request.json
        new_tc = {
            "id": len(db['test_cases']) + 1,
            "test_code": f"TC-{1000 + len(db['test_cases']) + 1}",
            "title": tc['title'],
            "module": tc['module'],
            "project": tc.get('project', 'E-Commerce Platform'),
            "sprint": tc.get('sprint', 'Sprint 14'),
            "priority": tc.get('priority', 'Medium'),
            "preconditions": tc.get('preconditions', ''),
            "steps": tc.get('steps', ''),
            "expected_result": tc.get('expected_result', ''),
            "actual_result": tc.get('actual_result', ''),
            "assigned_tester": tc.get('assigned_tester', 'Unassigned'),
            "test_result": tc.get('test_result', 'Not Run')
        }
        db['test_cases'].append(new_tc)
        return jsonify(new_tc), 201
    return jsonify(db['test_cases'])

@app.route('/api/test-cases/<int:tcid>', methods=['PATCH', 'DELETE'])
def tc_detail(tcid):
    global db
    if request.method == 'DELETE':
        db['test_cases'] = [t for t in db['test_cases'] if t['id'] != tcid]
        return jsonify({"message": "Test case deleted successfully"})
    
    payload = request.json
    for t in db['test_cases']:
        if t['id'] == tcid:
            if 'test_result' in payload: t['test_result'] = payload['test_result']
            return jsonify(t)
    return jsonify({"error": "Test Case not found"}), 404

# --- TEAM ---
@app.route('/api/team', methods=['GET', 'POST'])
def handle_team():
    if request.method == 'POST':
        m = request.json
        new_m = {
            "id": len(db['team']) + 1,
            "name": m['name'],
            "role": m['role'],
            "department": m['department'],
            "status": m.get('status', 'Active'),
            "assigned_projects": m.get('assigned_projects', 'None'),
            "assigned_tasks": int(m.get('assigned_tasks', 0))
        }
        db['team'].append(new_m)
        return jsonify(new_m), 201
    return jsonify(db['team'])

@app.route('/api/team/<int:mid>', methods=['DELETE'])
def delete_member(mid):
    global db
    db['team'] = [m for m in db['team'] if m['id'] != mid]
    return jsonify({"message": "Team member deleted successfully"})

# --- REPORTS ---
@app.route('/api/reports', methods=['GET', 'POST'])
def handle_reports():
    if request.method == 'POST':
        r = request.json
        new_r = {
            "id": len(db['reports']) + 1,
            "title": r['title'],
            "project": r['project'],
            "generated_by": r.get('generated_by', 'QA Lead'),
            "date": "2026-09-28",
            "summary": r['summary']
        }
        db['reports'].append(new_r)
        return jsonify(new_r), 201
    return jsonify(db['reports'])

@app.route('/api/reports/<int:rid>', methods=['DELETE'])
def delete_report(rid):
    global db
    db['reports'] = [r for r in db['reports'] if r['id'] != rid]
    return jsonify({"message": "Report deleted successfully"})

# --- ACTIVITY LOGS ---
@app.route('/api/activity-logs', methods=['GET'])
def get_activity_logs():
    return jsonify(db['activity_logs'])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)