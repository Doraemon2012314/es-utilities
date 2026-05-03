import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-secret-change-me')
CORS(app, origins=["https://es-utilities.netlify.app", "https://135246.netlify.app"])

GITHUB_DATA_URL = "https://raw.githubusercontent.com/Doraemon2012314/es-utilities/main/data.json"

def fetch_github_data():
    """Fetch data.json from GitHub. Returns dict or None."""
    try:
        resp = requests.get(GITHUB_DATA_URL, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        app.logger.error(f"GitHub fetch failed: {e}")
        return None

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/api/stats', methods=['GET'])
def stats():
    data = fetch_github_data()
    if not data:
        return jsonify({"error": "Cannot fetch data from GitHub"}), 503
    points = data.get("time_points", [])
    total_staff = len(points)
    total_hours = sum(p.get("minutes", 0) for p in points)
    active = len([p for p in points if p.get("minutes", 0) > 20])
    passed = len([p for p in points if p.get("minutes", 0) >= 100])
    pass_rate = round(passed / total_staff * 100) if total_staff else 0
    active_rate = round(active / total_staff * 100) if total_staff else 0
    return jsonify({
        "total_staff": total_staff,
        "active_this_week": active,
        "total_hours": total_hours,
        "pass_rate": pass_rate,
        "active_rate": active_rate
    })

@app.route('/api/timepoints', methods=['GET'])
def timepoints():
    data = fetch_github_data()
    if not data:
        return jsonify({"error": "Cannot fetch data from GitHub"}), 503
    return jsonify({"points": data.get("time_points", [])})

@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    data = fetch_github_data()
    if not data:
        return jsonify({"error": "Cannot fetch data from GitHub"}), 503
    return jsonify({"leaderboard": data.get("leaderboard", [])})

@app.route('/api/timelogs', methods=['GET'])
def timelogs():
    data = fetch_github_data()
    if not data:
        return jsonify({"error": "Cannot fetch data from GitHub"}), 503
    return jsonify({"logs": data.get("timelogs", [])})

@app.route('/api/staff', methods=['GET'])
def staff():
    data = fetch_github_data()
    if not data:
        return jsonify({"error": "Cannot fetch data from GitHub"}), 503
    return jsonify({"staff": data.get("staff", [])})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
