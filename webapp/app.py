from pathlib import Path
from flask import Flask, jsonify, render_template
from core.config import load_config
from core.lab import run_lab
from database.db import Database

ROOT = Path(__file__).resolve().parents[1]

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    cfg = load_config(ROOT / "config/config.json")
    db = Database(ROOT / "data/lab.db")
    db.initialize()

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/summary")
    def summary():
        counts, severities = db.stats()
        return jsonify({
            "counts": counts,
            "severity": {row["severity"]: row["n"] for row in severities},
        })

    @app.get("/api/incidents")
    def incidents():
        return jsonify([dict(row) for row in db.incidents()])

    @app.get("/api/events")
    def events():
        return jsonify([dict(row) for row in db.recent_events(30)])

    @app.get("/api/rules")
    def rules():
        return jsonify(cfg["detection"])

    @app.post("/api/lab/run")
    def run():
        run_lab(cfg, db)
        return jsonify({"ok": True})

    return app
