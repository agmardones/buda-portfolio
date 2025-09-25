# Buda Portfolio

A FastAPI service for calculating cryptocurrency portfolio values using Buda.com price data.

You can watch it live at: https://buda-portfolio.onrender.com
Docs: https://buda-portfolio.onrender.com/docs

## Features

- Portfolio value calculation
- Multi-currency support
- Buda.com price integration
- Health check endpoint

## Quick Start

### Run the application
```bash
uv run fastapi dev src/main.py
```

### Run tests
```bash
uv run pytest
```

## API Endpoints

- `GET /health` - Health check
- `POST /portfolio/value` - Calculate portfolio value

## Requirements

- Python 3.12+
- uv package manager
