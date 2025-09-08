mmocr_detect/
├─ detector/
│  ├─ __init__.py
│  ├─ config.py          # all knobs live here (model name, device, thresholds, paths)
│  └─ runner.py          # small “DetectText” class that wraps MMOCR and postprocess
├─ scripts/
│  ├─ infer_image.py     # CLI: run on a single image or folder
│  └─ visualize.py       # CLI: draw polygons and save result
└─ outputs/
   ├─ preds.jsonl        # one line per input {file, polys, scores}
   └─ vis/               # rendered images with overlays

Layout 2
textcam_flask/
├─ app.py                      # Flask app; creates global detector; exposes routes
├─ detector/                   # re-use from Stage 1 (symlink/copy)
│  ├─ config.py
│  └─ runner.py
├─ templates/
│  └─ index.html               # video element + overlay canvas
└─ static/
   └─ app.js     


   🧪 How to run and test
From project root:
export FLASK_APP=webapp/app.py
python webapp/app.py
Open http://localhost:5000.
Click Start → browser asks camera permission → you should see boxes appear over text in view.

virtual env == mmocr-webapp

Now in a new machine/repo:
python -m venv venv
source venv/bin/activate   # (or .\venv\Scripts\activate on Windows)
pip install -r requirements.txt
