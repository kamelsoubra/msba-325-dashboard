# Run the dashboard with Streamlit

This version serves the same dashboard inside Streamlit, preserving its vanilla JavaScript filters, SVG charts, hover and tap tooltips, branding and dark mode. Controls are inside the embedded dashboard. Its data is embedded by Python instead of fetched over HTTP. The static version remains available in public/index.html.

## Local setup

Open a terminal in the project folder:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python prepare.py
.venv\Scripts\python -m streamlit run app.py
```

Open http://localhost:8501 if Streamlit does not open it automatically. Press Ctrl+C in the terminal to stop. On macOS or Linux, replace `.venv\Scripts\python` with `.venv/bin/python`.

## Files to keep together

app.py, requirements.txt, prepare.py, data/Coffee Shop Sales.csv, public/index.html and public/agg.json. The current OSB logo is included at public/assets/osb-current.png, and the team names are in public/index.html. The dashboard adapts to phone screens with stacked KPIs and scrollable hourly charts. See README.md for phone access on the same Wi-Fi or through a hosted link.

The app uses the already validated aggregate data. Run prepare.py again after editing the CSV, then reload the app. The cache checks file modification timestamps.

## Hosting

Streamlit requires a running Python server. Netlify drag-and-drop and GitHub Pages can host the static version, but cannot execute app.py. For the Streamlit version, use Streamlit Community Cloud with app.py as the entrypoint and requirements.txt in the repository. Include the prepared public/agg.json so the cloud app can load immediately.
