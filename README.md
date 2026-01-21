# Simple SoundCloud Playlist Downloader
Downloads tracks from public SoundCloud playlists into a local folder so Spotify can pick them up as Local Files.

## Install Dependencies
`pip install -r requirements.txt`

## Configure
Edit `config.json` and add your public playlist URLs under `playlists`.
Set `output_dir` to the folder you want the MP3s saved to.

## Run
`python3 main.py`

## Spotify Local Files
In the Spotify desktop app, go to Settings and add `output_dir` under Local Files so the downloaded tracks appear.

## Cron (Monthly)
Edit `cron.txt` and set `REPO_DIR` (and `PYTHON` if needed). Then install it:
`(crontab -l 2>/dev/null; cat cron.txt) | crontab -`
Cron only runs when your Mac is on and awake; missed runs are not backfilled.

## Notes
If SoundCloud returns 401, set `SOUNDCLOUD_CLIENT_ID` and retry.
