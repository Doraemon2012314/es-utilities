import os
from flask import Flask, jsonify
from flask_cors import CORS
import requests
import traceback

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-key-change-in-production')
CORS(app, origins=["https://es-utilities.netlify.app"])

GITHUB_DATA_URL = "https://raw.githubusercontent.com/Doraemon2012314/es-utilities/main/data.json"

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

def fetch_github_data():
    """尝试从 GitHub 获取数据，失败时返回 None。"""
    try:
        resp = requests.get(GITHUB_DATA_URL, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        app.logger.error(f"GitHub fetch failed: {e}")
        return None

@app.errorhandler(Exception)
def handle_exception(e):
    """统一处理未捕获的异常。"""
    app.logger.error(f"Unhandled Exception: {e}\n{traceback.format_exc()}")
    return jsonify({"error": "Internal Server Error"}), 500

@app.route('/api/stats', methods=['GET'])
def stats():
    data = fetch_github_data()
    if not data:
        return jsonify({"error": "Failed to fetch data from GitHub"}), 503
    # ... 在这里处理 data 并返回 ...
