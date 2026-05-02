from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app, origins=["https://es-utilities.netlify.app"])

# Connect to database (you'll need to share the database file)
# For production, use a cloud database like Supabase or shared SQLite via GitHub

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/api/stats', methods=['GET'])
def stats():
    # Your stats logic here
    return jsonify({"total_staff": 0, "active_this_week": 0})

# Add your other endpoints (/api/timepoints, /api/leaderboard, etc.)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
