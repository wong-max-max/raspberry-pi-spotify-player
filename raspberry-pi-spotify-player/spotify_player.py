#!/usr/bin/env python3
"""
Raspberry Pi Spotify Player
Searches for artists, lets you select one, then plays continuously
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import random
import sys
import os

# Spotify API credentials - you'll need to fill these in
SPOTIPY_CLIENT_ID = 'YOUR_CLIENT_ID'
SPOTIPY_CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

class SpotifyPlayer:
    def __init__(self):
        """Initialize Spotify connection"""
        scope = "user-read-playback-state,user-modify-playback-state,user-read-currently-playing"
        
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET,
            redirect_uri=SPOTIPY_REDIRECT_URI,
            scope=scope
        ))
        
        print("Connected to Spotify successfully.")
    
    def search_artists(self, query):
        """Search for artists by name"""
        results = self.sp.search(q=query, type='artist', limit=10)
        return results['artists']['items']
    
    def display_artists(self, artists):
        """Display artist search results"""
        print("\n" + "="*60)
        print("Search Results:")
        print("="*60)
        
        for i, artist in enumerate(artists, 1):
            followers = artist['followers']['total']
            genres = ', '.join(artist['genres'][:3]) if artist['genres'] else 'No genres listed'
            print(f"{i}. {artist['name']}")
            print(f"   Followers: {followers:,} | Genres: {genres}")
            print()
        
        print("="*60)
    
    def get_artist_top_tracks(self, artist_id):
        """Get an artist's top tracks"""
        results = self.sp.artist_top_tracks(artist_id)
        return results['tracks']
    
    def get_artist_albums(self, artist_id):
        """Get all tracks from an artist's albums"""
        all_tracks = []
        
        # Get albums
        albums = self.sp.artist_albums(artist_id, limit=50)
        
        for album in albums['items']:
            # Get tracks from each album
            tracks = self.sp.album_tracks(album['id'])
            for track in tracks['items']:
                all_tracks.append(track['uri'])
        
        return all_tracks
    
    def create_playback_queue(self, artist_id, artist_name):
        """Create a shuffled queue of artist's music"""
        print(f"\nLoading tracks from {artist_name}...")
        
        # Get top tracks and album tracks
        top_tracks = self.get_artist_top_tracks(artist_id)
        album_tracks = self.get_artist_albums(artist_id)
        
        # Combine URIs
        track_uris = [track['uri'] for track in top_tracks]
        track_uris.extend(album_tracks)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_tracks = []
        for uri in track_uris:
            if uri not in seen:
                seen.add(uri)
                unique_tracks.append(uri)
        
        print(f"Loaded {len(unique_tracks)} tracks")
        return unique_tracks
    
    def get_active_device(self):
        """Get the currently active Spotify device"""
        devices = self.sp.devices()
        
        if not devices['devices']:
            print("\nNo active Spotify devices found.")
            print("Please open Spotify on this device or another device first.")
            return None
        
        # Find active device or use first available
        active = next((d for d in devices['devices'] if d['is_active']), None)
        if not active:
            active = devices['devices'][0]
        
        print(f"Using device: {active['name']}")
        return active['id']
    
    def start_playback(self, track_uris, device_id=None):
        """Start playing tracks"""
        try:
            # Shuffle the tracks
            shuffled = track_uris.copy()
            random.shuffle(shuffled)
            
            # Start playback with first 100 tracks (Spotify API limit)
            self.sp.start_playback(device_id=device_id, uris=shuffled[:100])
            
            # Enable repeat
            self.sp.repeat('context', device_id=device_id)
            
            # Enable shuffle
            self.sp.shuffle(True, device_id=device_id)
            
            print("Playback started successfully.")
            return True
        except Exception as e:
            print(f"Error starting playback: {e}")
            return False
    
    def monitor_playback(self, track_uris, device_id):
        """Monitor playback and keep it running"""
        print("\n" + "="*60)
        print("Playback Monitor Active")
        print("="*60)
        print("Press Ctrl+C to stop")
        print("You can now disconnect - playback will continue.\n")
        
        last_track_id = None
        error_count = 0
        
        while True:
            try:
                # Check current playback
                current = self.sp.current_playback()
                
                if current and current['is_playing']:
                    track = current['item']
                    
                    # Display track info if it changed
                    if track['id'] != last_track_id:
                        artists = ', '.join([a['name'] for a in track['artists']])
                        print(f"Now playing: {track['name']} - {artists}")
                        last_track_id = track['id']
                        error_count = 0  # Reset error count on success
                
                elif current and not current['is_playing']:
                    # Playback paused, restart it
                    print("Playback paused, restarting...")
                    shuffled = track_uris.copy()
                    random.shuffle(shuffled)
                    self.sp.start_playback(device_id=device_id, uris=shuffled[:100])
                    self.sp.repeat('context', device_id=device_id)
                    self.sp.shuffle(True, device_id=device_id)
                
                else:
                    # No playback at all
                    print("No playback detected, starting...")
                    shuffled = track_uris.copy()
                    random.shuffle(shuffled)
                    self.sp.start_playback(device_id=device_id, uris=shuffled[:100])
                    self.sp.repeat('context', device_id=device_id)
                    self.sp.shuffle(True, device_id=device_id)
                
                # Wait before checking again
                time.sleep(30)
                
            except spotipy.exceptions.SpotifyException as e:
                error_count += 1
                if error_count > 5:
                    print(f"Too many errors, stopping: {e}")
                    break
                print(f"Spotify error (attempt {error_count}/5): {e}")
                time.sleep(60)  # Wait longer on errors
                
            except KeyboardInterrupt:
                print("\n\nStopping playback monitor...")
                break
            
            except Exception as e:
                error_count += 1
                print(f"Unexpected error (attempt {error_count}/5): {e}")
                if error_count > 5:
                    break
                time.sleep(60)

def main():
    """Main program flow"""
    print("="*60)
    print("Spotify Continuous Player for Raspberry Pi")
    print("="*60)
    print()
    
    # Check if credentials are set
    if SPOTIPY_CLIENT_ID == 'YOUR_CLIENT_ID':
        print("Error: Spotify API credentials not configured.")
        print("Please edit this file and add your Client ID and Secret.")
        print("See README.md for setup instructions.")
        sys.exit(1)
    
    # Initialize player
    try:
        player = SpotifyPlayer()
    except Exception as e:
        print(f"❌ Failed to connect to Spotify: {e}")
        sys.exit(1)
    
    # Search for artist
    while True:
        query = input("\nEnter artist name to search: ").strip()
        if not query:
            print("Please enter an artist name.")
            continue
        
        print(f"Searching for '{query}'...")
        artists = player.search_artists(query)
        
        if not artists:
            print("No artists found. Try again.")
            continue
        
        # Display results
        player.display_artists(artists)
        
        # Let user select
        while True:
            try:
                choice = input("Enter number (1-10) or 'n' for new search: ").strip().lower()
                
                if choice == 'n':
                    break
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(artists):
                    selected_artist = artists[choice_num - 1]
                    print(f"\nSelected: {selected_artist['name']}")
                    
                    # Load tracks
                    track_uris = player.create_playback_queue(
                        selected_artist['id'],
                        selected_artist['name']
                    )
                    
                    if not track_uris:
                        print("No tracks found for this artist.")
                        break
                    
                    # Get device
                    device_id = player.get_active_device()
                    if not device_id:
                        sys.exit(1)
                    
                    # Start playback
                    if player.start_playback(track_uris, device_id):
                        # Monitor continuously
                        player.monitor_playback(track_uris, device_id)
                    
                    return
                else:
                    print("Invalid number.")
            except ValueError:
                print("Please enter a number or 'n'.")
            except KeyboardInterrupt:
                print("\n\nExiting...")
                sys.exit(0)

if __name__ == "__main__":
    main()
