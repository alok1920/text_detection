from __future__ import annotations
import os
from pathlib import Path

from flask import Flask, request, jsonify, render_template

# Aloow importing from project root (so we can reuse detector/)
import sys
ROOT = Path(__file__).resolve().parent.parent # one level up from webapp/
sys.path.append(str(ROOT))

from detector.runner import DetectText

app = Flask(__name__)

detector = DetectText()

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/detect")
def api_detect():

    data = request.get_json(force=True)
    data_url = data.get("image")
    if not data_url:
        return jsonify({"error": "missing image"}), 400
    
    img_bgr = DetectText.from_data_url(data_url)

    res = detector.run_on_image(img_bgr)
    return jsonify(res)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
