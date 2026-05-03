from flask import Flask, jsonify
from flask_cors import CORS
import requests
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow requests from your Netlify dashboard

# Your GitHub raw JSON URL
GITHUB_DATA_URL = "https://raw.githubusercontent.com/Doraemon2012314/es-utilities/main/data.json"

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/api/stats', methods=['GET'])
def stats():
    try:
        resp = requests.get(GITHUB_DATA_URL)
        data = resp.json()
        points = data.get("time_points", [])
        total_staff = len(points)
        total_hours = sum(p.get("minutes", 0) for p in points)
        active_staff = len([p for p in points if p.get("minutes", 0) > 20])
        passed = len([p for p in points if p.get("minutes", 0) >= 100])
        pass_rate = round(passed / total_staff * 100) if total_staff > 0 else 0
        active_rate = round(active_staff / total_staff * 100) if total_staff > 0 else 0
        return jsonify({
            "total_staff": total_staff,
            "active_this_week": active_staff,
            "total_hours": total_hours,
            "pass_rate": pass_rate,
            "active_rate": active_rate
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/timepoints', methods=['GET'])
def timepoints():
    try:
        resp = requests.get(GITHUB_DATA_URL)
        data = resp.json()
        return jsonify({"points": data.get("time_points", [])})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    try:
        resp = requests.get(GITHUB_DATA_URL)
        data = resp.json()
        return jsonify({"leaderboard": data.get("leaderboard", [])})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/timelogs', methods=['GET'])
def timelogs():
    try:
        resp = requests.get(GITHUB_DATA_URL)
        data = resp.json()
        return jsonify({"logs": data.get("timelogs", [])})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/staff', methods=['GET'])
def staff():
    try:
        resp = requests.get(GITHUB_DATA_URL)
        data = resp.json()
        return jsonify({"staff": data.get("staff", [])})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Optional: endpoint to trigger force export (can call your bot's /forceexport webhook if you set one up)
@app.route('/api/forceexport', methods=['POST'])
def force_export():
    # You could optionally forward this request to your bot if you add a webhook endpoint there.
    return jsonify({"success": False, "message": "Manual trigger not configured"}), 501

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
