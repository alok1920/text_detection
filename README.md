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