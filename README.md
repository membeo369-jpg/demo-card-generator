# Demo Card Studio v3

Standalone Flask web app for creating clearly marked fictional demo/mockup cards.

## Features
- Live HTML/CSS preview
- Upload portrait image
- Edit school/demo organization, name, program, demo ID, year
- Multiple visual themes
- Download card as PNG in the browser
- Permanent visible `SAMPLE / NOT VALID` watermark
- Railway-ready

## Railway

Push these files to your GitHub repository.

Start command:

```bash
gunicorn app:app --bind 0.0.0.0:$PORT
```

A `railway.json` file is included, so Railway can also detect the start command automatically.

After deployment:
1. Railway service -> Settings
2. Networking / Public Networking
3. Generate Domain
4. Open the generated URL

## Structure

```text
app.py
requirements.txt
Procfile
railway.json
templates/
  index.html
```
