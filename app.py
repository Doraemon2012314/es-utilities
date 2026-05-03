import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-key')
CORS(app)

GITHUB_DATA_URL = "https://raw.githubusercontent.com/Doraemon2012314/es-utilities/main/data.json"

def fetch_data():
    try:
        r = requests.get(GITHUB_DATA_URL, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None

@app.route('/api/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/api/stats')
def stats():
    data = fetch_data()
    if not data:
        return jsonify({"error": "GitHub fetch failed"}), 503
    points = data.get("time_points", [])
    total = len(points)
    active = len([p for p in points if p.get("minutes", 0) > 20])
    passed = len([p for p in points if p.get("minutes", 0) >= 100])
    return jsonify({
        "total_staff": total,
        "active_this_week": active,
        "total_hours": sum(p.get("minutes", 0) for p in points),
        "pass_rate": round(passed / total * 100) if total else 0,
        "active_rate": round(active / total * 100) if total else 0
    })

@app.route('/api/timepoints')
def timepoints():
    data = fetch_data()
    return jsonify({"points": data.get("time_points", []) if data else []})

@app.route('/api/leaderboard')
def leaderboard():
    data = fetch_data()
    return jsonify({"leaderboard": data.get("leaderboard", []) if data else []})

@app.route('/api/timelogs')
def timelogs():
    data = fetch_data()
    return jsonify({"logs": data.get("timelogs", []) if data else []})

@app.route('/api/staff')
def staff():
    data = fetch_data()
    return jsonify({"staff": data.get("staff", []) if data else []})
