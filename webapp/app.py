from __future__ import annotations
import os
from pathlib import Path

from flask import Flask, request, jsonify, render_template

# Aloow importing from project root (so we can reuse detector/)
import sys
ROOT = Path(__file__).resolve().parent.parent # one level up from webapp/
sys.path.append(str(ROOT))
'''
render_template serves templates/index.html.
We push the project root into sys.path so from detector.runner import DetectText will work when you run python webapp/app.py.
'''

# Importing detector & create the Flask app
from detector.runner import DetectText # now import works

app = Flask(__name__)

# create ONE global detector (load models once, reuse for all requests)
detector = DetectText()

# Home page route
@app.get("/")
def index():
    return render_template("index.html")

# detection API route
@app.post("/api/detect")
def api_detect():

    data = request.get_json(force=True) #parse json body
    data_url = data.get("image")
    if not data_url:
        return jsonify({"error": "missing image"}), 400
    
    # convert data url -> OpenCV BGR image
    img_bgr = DetectText.from_data_url(data_url)

    # run detector (return dict with boxes + input_size)
    res = detector.run_on_image(img_bgr)
    return jsonify(res)
'''
The browser sends a base64 image string; we decode and run detection.
Response is JSON: { "boxes": [...], "input_size": {...} }.
'''

# App entry point
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)