"""Script to download static files for the frontend."""

from pathlib import Path

import requests

# Create static directory if it doesn't exist
static_dir = Path("frontend/static")
static_dir.mkdir(parents=True, exist_ok=True)

# URLs for static files
STATIC_FILES = {
    "tailwind.min.css": (
        "https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css"
    ),
    "htmx.min.js": ("https://unpkg.com/htmx.org@1.9.10/dist/htmx.min.js"),
    "hyperscript.min.js": (
        "https://unpkg.com/hyperscript.org@0.9.12/dist/_hyperscript.min.js"
    ),
}


def download_file(url: str, filename: str) -> None:
    """Download a file from a URL and save it to the static directory.

    Args:
        url: URL to download from
        filename: Name to save the file as
    """
    response = requests.get(url)
    response.raise_for_status()

    file_path = static_dir / filename
    file_path.write_bytes(response.content)
    print(f"Downloaded {filename}")


def main() -> None:
    """Download all static files."""
    for filename, url in STATIC_FILES.items():
        try:
            download_file(url, filename)
        except Exception as e:
            print(f"Error downloading {filename}: {e}")


if __name__ == "__main__":
    main()
