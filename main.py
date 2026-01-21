import json
import os
import re
from urllib.parse import urljoin
from urllib.request import Request, urlopen
try:
    import certifi
except ImportError:
    certifi = None

if certifi and not os.environ.get("SSL_CERT_FILE"):
    os.environ["SSL_CERT_FILE"] = certifi.where()

from sclib import SoundcloudAPI, Track, Playlist

CLIENT_ID_RE = re.compile(r'client_id["\']?\s*[:=]\s*["\']([a-zA-Z0-9]+)["\']')
SCRIPT_SRC_RE = re.compile(r'<script[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)


def _fetch_text(url):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req) as response:
        return response.read().decode("utf-8", errors="replace")


def _find_client_id(text):
    match = CLIENT_ID_RE.search(text)
    return match.group(1) if match else None


def _scrape_client_id():
    base_url = "https://soundcloud.com"
    page_text = _fetch_text(base_url)
    client_id = _find_client_id(page_text)
    if client_id:
        return client_id
    for src in SCRIPT_SRC_RE.findall(page_text):
        if "cookielaw.org" in src:
            continue
        script_text = _fetch_text(urljoin(base_url, src))
        client_id = _find_client_id(script_text)
        if client_id:
            return client_id
    return None

CONFIG_PATH = "./config.json"


def _load_config(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


config = _load_config(CONFIG_PATH)
output_dir = config.get("output_dir", "./test-album")
playlists = config.get("playlists", [])
if isinstance(playlists, str):
    playlists = [playlists]
if not playlists:
    raise RuntimeError("No playlists found in config.json.")

client_id = os.environ.get("SOUNDCLOUD_CLIENT_ID") or _scrape_client_id()
api = SoundcloudAPI(client_id=client_id) if client_id else SoundcloudAPI()
os.makedirs(output_dir, exist_ok=True)
for playlist_url in playlists:
    try:
        playlist = api.resolve(playlist_url)
    except TypeError:
        raise RuntimeError(
            "SoundCloud returned 401/unauthorized. Set SOUNDCLOUD_CLIENT_ID and retry."
        ) from None

    if not isinstance(playlist, Playlist):
        raise RuntimeError(f"Failed to resolve playlist: {playlist_url}")

    for track in playlist.tracks:
        filename = f'{output_dir}/{track.artist} - {track.title}.mp3'
        with open(filename, 'wb+') as file:
            track.write_mp3_to(file)
