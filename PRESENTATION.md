# Krishi Saarthi presentation setup

This setup runs the existing React + Django project with a separate SQLite demo database. No Redis server or API keys are needed for the presentation path. Use Python **3.11 or 3.12** and Node **22.12+** (tested with Python 3.12 and Node 24).

## Install once

From the repository root on macOS/Linux:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cpu
.venv/bin/python -m pip install -r backend/requirements.txt
npm ci --prefix frontend
python3 present.py
```

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cpu
.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt
npm ci --prefix frontend
py present.py
```

The CPU PyTorch command is for Linux/Windows. On macOS install `torch==2.5.1 torchvision==0.20.1` from the default pip index instead. The first installation downloads several hundred MB; do it before presentation day.

## Start on presentation day

```bash
python present.py
```

Open **http://localhost:5173**. Sign in with:

- Username: `demo_farmer`
- Password: `DemoFarmer@2026`

Keep the terminal open. Ctrl+C stops the servers. The launcher uses frontend port 5173 and backend port 8765; it stops with a useful message if either is occupied. It migrates and seeds automatically, preserving edits on repeated starts. Sample data lives in `backend/demo.sqlite3`, separately from the regular `backend/db.sqlite3`. The sample account is not an administrator.

## Five-minute walkthrough

1. **Dashboard:** explain the weather card, vegetation trend, health estimate and reference MSP prices. Point out the presentation-mode banner.
2. **Active field:** switch between Ludhiana Rice Plot and Ludhiana Wheat Plot using the selector above the content. Open **My Field** to show the stored boundary.
3. **Field Report / Analytics:** show NDVI/EVI, area, time-series graphs and water/carbon estimates. These calculations use simulated satellite inputs in presentation mode.
4. **Field Log:** select a date, record an activity and show it on the calendar. Reload to demonstrate database persistence.
5. **Costs & Revenue / Profit & Loss:** each sample field starts with ₹22,000 costs and ₹45,000 sales. Add an expense and show the updated totals.
6. **Season Calendar / Inventory / Crop Rotation:** show the planned activity, stock and rule-based rotation suggestions.
7. **Chat:** ask “How should I irrigate?” The response explicitly identifies itself as preset demo guidance.

## What is real and what is simulated

| Capability | Presentation behavior |
| --- | --- |
| Login, field records, logs, expenses, revenue, calendar, inventory | Real Django API and SQLite persistence |
| Weather and satellite readings | Deterministic simulated data; banner and API source labels identify it |
| Chat | Preset guidance stored in real conversation records; no live AI call |
| Health, irrigation, carbon, yield and price estimates | Illustrative calculations / existing fallback heuristics, not validated predictions |
| Market prices | Repository's **2025–26 reference MSP** and indicative ranges, not current live mandi prices |
| Crop rotation | Rule-based suggestions, not an AI model |
| Pest image classification | Trained model weights are absent from this repository; unavailable results must not be presented as diagnoses |
| Live Gemini soil advice / plant validation | Requires a configured Gemini key; not part of the credential-free walkthrough |
| Map tiles, map search, directions | External providers; internet is required for basemaps/search. Saved field boundaries remain local |
| Language / voice | UI uses English fallback; browser voice support and permissions vary |

Do not describe demo outputs as real satellite observations or trained model results. The app's existing “AgriSmart” branding is retained; the repository/project is Krishi Saarthi.

## Live integrations (optional, separate from presentation)

Run the backend normally with `DEMO_MODE=False`, configure `backend/.env` with `GEE_PROJECT`, `GEMINI_API_KEY`, and `OPENWEATHER_API_KEY`, and authenticate Earth Engine. The trained files expected by `backend/ml_engine` must be supplied separately for CNN/LSTM inference. Set `REDIS_URL` only if a Redis server is running. Live services have not been verified without credentials or model weights.

For normal development use `python manage.py runserver` from `backend` and `npm run dev` from `frontend`; Vite proxies to port 8000 by default. Set `API_PROXY_TARGET` to override that backend target. Demo mode is explicitly opt-in and rejected with `DEBUG=False`.

## Verification

```bash
npm run check --prefix frontend
npm run build --prefix frontend
.venv/bin/python backend/manage.py test tests --noinput
```

On Windows substitute `.\.venv\Scripts\python.exe` for `.venv/bin/python`.

Browser checks cover login, refresh, dashboard navigation, the demo chat, and desktop/mobile layout. Backend regression tests cover sample-seed idempotency, real Knox-token access/revocation/expiry, isolation of users' fields and demo-versus-live behavior.

## Troubleshooting

- **Port already in use:** close the previous presentation terminal with Ctrl+C. Do not start duplicate servers.
- **Login fails:** use the exact credentials above. Seeding preserves an existing account's changed password.
- **Map is blank:** check internet access. The presentation's stored records and simulated metrics do not require external API credentials.
- **Want a clean rehearsal database:** stop the servers, back up `backend/demo.sqlite3`, then remove that demo file and restart. This discards only your demo edits.
- **Normal mode gives service unavailable:** configure the relevant credentials; demo mode is provided by `present.py`.

Repeat the browser smoke test while `python present.py` is running:

```bash
cd frontend
npx playwright install chromium
npm run test:e2e
```

If Chromium is already installed, set `CHROMIUM_PATH` to its executable instead of downloading a browser.
