# Search Engine

A Google-like search engine built with Python Flask and SQLite.

![Search Engine](https://img.shields.io/badge/Python-Flask-blue) ![Database](https://img.shields.io/badge/Database-SQLite-green)

## Features

- Google-like search interface
- Full-text search with inverted index
- Relevance-based ranking
- 20 pre-indexed sample articles
- REST API for search

## Quick Start (Local)

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python python_server/app.py
```

Open http://localhost:5000

## Deploy to Render

See [DEPLOY.md](DEPLOY.md) for step-by-step instructions.

## Project Structure

```
search-engine/
├── frontend/
│   ├── index.html      # Search page
│   ├── style.css       # Styling
│   └── script.js       # Search logic
├── python_server/
│   └── app.py          # Flask server + search engine
├── data/               # SQLite database
├── requirements.txt    # Dependencies
├── Procfile           # Render config
└── runtime.txt        # Python version
```

## API

**Search:** `POST /api/search`
```json
{"query": "python", "page": 1, "limit": 10}
```

**Add Document:** `POST /api/index`
```json
{"title": "...", "content": "...", "url": "...", "category": "..."}
```

**Stats:** `GET /api/stats`

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python Flask
- **Database:** SQLite
- **Hosting:** Render

## License

MIT
