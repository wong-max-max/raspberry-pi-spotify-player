#!/bin/bash
# Installation script for Raspberry Pi Spotify Player

echo "Raspberry Pi Spotify Player - Installation"
echo "==========================================="
echo ""

# Check if running on Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/cpuinfo 2>/dev/null && ! grep -q "BCM" /proc/cpuinfo 2>/dev/null; then
    echo "Warning: This doesn't appear to be a Raspberry Pi."
    echo "Continuing anyway..."
    echo ""
fi

# Update system
echo "[1/4] Updating system packages..."
sudo apt-get update -qq

# Install Python dependencies
echo "[2/4] Installing Python..."
sudo apt-get install -y python3 python3-pip

# Install spotipy
echo "[3/4] Installing Spotify library..."
pip3 install spotipy --break-system-packages

# Create directory
echo "[4/4] Setting up application..."
mkdir -p ~/spotify-player
cp spotify_player.py ~/spotify-player/
chmod +x ~/spotify-player/spotify_player.py

echo ""
echo "Installation complete."
echo ""
echo "Next steps:"
echo "1. Get Spotify API credentials from https://developer.spotify.com/dashboard"
echo "2. Edit ~/spotify-player/spotify_player.py with your credentials"
echo "3. Run: cd ~/spotify-player && python3 spotify_player.py"
echo ""
echo "See README.md for detailed instructions."
echo ""
