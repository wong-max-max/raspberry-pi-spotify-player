# Quick Start Guide

## Setup (5 minutes)

### 1. Copy to Raspberry Pi
```bash
scp *.py *.sh *.service *.md pi@raspberrypi.local:~
```

### 2. Install
```bash
ssh pi@raspberrypi.local
./install.sh
```

### 3. Get Spotify Credentials
- Visit https://developer.spotify.com/dashboard
- Create app with redirect URI: `http://localhost:8888/callback`
- Copy Client ID and Secret

### 4. Configure
```bash
nano ~/spotify-player/spotify_player.py
```
Replace `YOUR_CLIENT_ID` and `YOUR_CLIENT_SECRET` with actual values.

### 5. Run
```bash
cd ~/spotify-player
python3 spotify_player.py
```

## Usage

1. Ensure Spotify is running on any device
2. Run the script
3. Enter artist name
4. Select result (1-10)
5. Playback begins

## Commands

```bash
# Run player
python3 spotify_player.py

# Stop player
Ctrl+C

# Enable auto-start
sudo systemctl enable spotify-player.service

# View logs
sudo journalctl -u spotify-player.service -f
```

## Common Issues

**No devices found**: Open Spotify on a device first

**Module error**: `pip3 install spotipy --break-system-packages`

**Playback stops**: Check internet connection

See README.md for detailed documentation.
