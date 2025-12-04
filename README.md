# Raspberry Pi Spotify Player

A Python application that enables continuous playback of a selected artist on Spotify through a Raspberry Pi.

## Features

- Interactive artist search with detailed results
- Continuous playback of artist's complete discography
- Automatic restart on interruption
- Compatible with Spotify Free and Premium
- Runs independently after initial setup
- Optional systemd integration for auto-start

## Requirements

- Raspberry Pi (any model with network capability)
- Spotify account
- Internet connection
- Active Spotify playback device (phone, computer, or speaker)

## Installation

### 1. Transfer Files

Copy all files to your Raspberry Pi:

```bash
scp install.sh spotify_player.py spotify-player.service pi@raspberrypi.local:~
```

### 2. Run Installation

SSH into your Pi and execute:

```bash
cd ~
chmod +x install.sh
./install.sh
```

This installs Python dependencies and sets up the application directory.

### 3. Obtain Spotify API Credentials

1. Navigate to https://developer.spotify.com/dashboard
2. Log in with your Spotify account
3. Click "Create app"
4. Configure:
   - App name: Any descriptive name
   - App description: Personal use
   - Redirect URI: `http://localhost:8888/callback` (must be exact)
5. Save and access Settings
6. Copy Client ID and Client Secret

### 4. Configure Application

Edit the configuration file:

```bash
nano ~/spotify-player/spotify_player.py
```

Update credentials:

```python
SPOTIPY_CLIENT_ID = 'your_client_id_here'
SPOTIPY_CLIENT_SECRET = 'your_client_secret_here'
```

Save with Ctrl+X, Y, Enter.

## Usage

### Starting Playback

1. Open Spotify on any device to establish an active session
2. Run the application:

```bash
cd ~/spotify-player
python3 spotify_player.py
```

3. On first run, authorize the application through the browser prompt
4. Enter an artist name when prompted
5. Select from search results (1-10)
6. Playback begins automatically

The application monitors playback every 30 seconds and restarts if interrupted.

### Stopping Playback

Press Ctrl+C in the terminal, or:

```bash
pkill -f spotify_player.py
```

## Optional: Systemd Integration

To enable automatic startup on boot:

```bash
sudo cp ~/spotify-player.service /etc/systemd/system/
sudo systemctl enable spotify-player.service
sudo systemctl start spotify-player.service
```

View logs:

```bash
sudo journalctl -u spotify-player.service -f
```

## Technical Details

**Architecture:**
- Uses Spotify Web API via spotipy library
- Retrieves artist's top tracks and full discography
- Implements shuffle and repeat through Spotify Connect
- Monitors playback state via polling

**Power Consumption:**
- Raspberry Pi Zero W: ~0.5W
- Raspberry Pi 4: ~3W

## Troubleshooting

**No active devices found**
- Ensure Spotify is open and playing on at least one device

**Connection errors**
- Verify Client ID and Secret are correct
- Confirm Redirect URI matches exactly: `http://localhost:8888/callback`

**Module errors**
```bash
pip3 install spotipy --break-system-packages
```

**Playback interruptions**
- Check network stability
- Spotify Free accounts may have additional limitations

## Alternative: Raspotify

For native Spotify Connect support on the Pi:

```bash
curl -sL https://dtcooper.github.io/raspotify/install.sh | sh
```

This makes the Pi appear as a Spotify Connect speaker.

## Notes

This application is intended for personal use. Artificial streaming or manipulation of play counts violates Spotify's Terms of Service and may result in account suspension.
