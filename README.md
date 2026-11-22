# Product Barcode Lookup

Terminal UI for looking up products by barcode, built with [Textual](https://textual.textualize.io/).

## Status

Environment scaffold only. Application code is not implemented yet, so the `barcode-tui`
command will start working once `src/barcode_tui/main.py` exposes a `main()` entry point.

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) — `winget install --id astral-sh.uv -e` (or `pip install uv`)

## Setup

```powershell
uv sync
Copy-Item .env.example .env
```

Then fill in the provider keys you actually use in `.env`. `uv sync` creates `.venv/`, resolves
dependencies into `uv.lock`, and installs this project in editable mode.

## Configuration

Configuration is loaded from `.env`, which is gitignored and must never be committed. Providers are
pluggable: enable them in priority order and configure each one through the same generic fields.

| Variable | Purpose |
| --- | --- |
| `BARCODE_PROVIDERS` | Comma-separated provider IDs, in lookup priority order |
| `PROVIDER_<ID>_API_KEY` | Provider credential (blank = unauthenticated) |
| `PROVIDER_<ID>_BASE_URL` | Override the provider endpoint (blank = provider default) |
| `PROVIDER_<ID>_TIMEOUT` | Request timeout in seconds (blank = `10`) |
| `PROVIDER_<ID>_USER_AGENT` | Optional User-Agent header |
| `BARCODE_CACHE_DIR` | Disk cache location (blank = memory-only, nothing written to disk) |
| `BARCODE_CACHE_TTL_SECONDS` | Cache entry lifetime in seconds (blank = `604800`, 7 days) |

Adding a provider requires a `PROVIDER_<ID>_*` block plus a class under
`src/barcode_tui/services/providers/`. The configuration loader, UI, caching, and error handling
stay unchanged.

Caching is in-memory by default: entries live for the duration of the process, expire after
`BARCODE_CACHE_TTL_SECONDS`, and nothing is written to disk. Set `BARCODE_CACHE_DIR` to a
writable directory to enable a persistent cache; it is then stored with `diskcache` using
`JSONDisk` (JSON-only values, no pickle), and the directory is created on first write.

## Development

```powershell
uv run barcode-tui                                  # launch the TUI (once main.py is implemented)
uv run textual run --dev src/barcode_tui/main.py    # run with devtools
uv run pytest                                       # tests
uv run ruff check .                                 # lint
uv run ruff format .                                # format
```

## Project layout

```
src/barcode_tui/
├── main.py              # Textual app + entry point
├── styles.tcss          # Textual CSS
├── services/
│   └── providers/       # one module per barcode provider
├── types/               # shared models
└── ui/                  # widgets and screens
```
