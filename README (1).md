# BuildPlan India v3

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud
Upload `app.py`, `requirements.txt`, and `README.md` to the root of your GitHub repository. Select `app.py` as the main file, then deploy or reboot the app.

## Features
- Building type, built-up area per floor, floor count and location inputs
- Preliminary room-zoning drawing with PNG download
- Conceptual column/beam grid with PNG download
- Standalone textbook beam example with shear-force and bending-moment diagrams
- Indian standards and local rules checklist
- Rough quantity allowances and indicative cost scenario
- Downloadable project report and quantities CSV

## Limitations
This is an educational rule-based prototype, not a generative AI model or certified engineering tool. The floor plan and structural grid are conceptual. The beam analysis is not connected to the building model. Quantity factors and cost rates are assumptions. The app does not certify compliance with BIS standards, wind/seismic requirements, or Telangana/local authority rules. Do not use it for construction, tendering, or permits. A qualified architect and structural engineer must verify current standards/amendments, site jurisdiction, soil report, loads, drawings and calculations.
