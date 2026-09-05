# Demo Student Card Generator

Standalone web app for generating clearly marked demo/mock student cards.

## Local
```bash
pip install -r requirements.txt
python app.py
```

Open http://localhost:8080

## Railway
1. Push this folder to GitHub.
2. Railway -> New Project -> Deploy from GitHub.
3. Railway will install `requirements.txt`.
4. Start command:
   `gunicorn app:app --bind 0.0.0.0:$PORT`

No database or environment variables are required.

All generated cards contain a prominent `SAMPLE / NOT VALID` watermark.
