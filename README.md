````
# 📸 Live Text Detection Web App

A simple Flask + JavaScript project that shows real-time text detection directly in your browser.  
Open the page, allow camera access, and watch as boxes appear over text.

---

## 🚀 Quickstart

1. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate
````

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Run the Flask app:

   ```
   python webapp/app.py
   ```

4. Open your browser at:
   👉 [http://localhost:5000](http://localhost:5000)

---

## ✨ Features

* Live camera preview in the browser
* Server-side text detection API
* Boxes and confidence scores drawn in real-time
* Start/Stop controls, FPS counter, and status display

---

## 📂 Project Structure

```
webapp/
├─ app.py              # Flask backend
├─ templates/
│  └─ index.html       # Webpage UI
└─ static/
   └─ app.js           # Camera + overlay logic
requirements.txt
```

---

## 📜 License

This project is open-sourced under the MIT License. Feel free to use and adapt!

```

---

👉 Would you like me to also add **some nice badges** (Python version, Flask, License) at the top to make it look more “GitHub-ready”?
```
