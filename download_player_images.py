"""
Download player face images from CSV for 2022 only and save them locally
Uses concurrent downloads for maximum speed
"""
import pandas as pd
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import time
from threading import Lock

# Global counters with thread lock
stats_lock = Lock()
stats = {
    'successful': 0,
    'failed': 0,
    'skipped': 0,
    'total': 0,
    'start_time': None
}

# Create directory for images
images_dir = Path("player_images")
images_dir.mkdir(exist_ok=True)

def download_image(url):
    """Download a single image"""
    if not pd.notna(url) or not str(url).startswith('http'):
        return 'invalid'
    
    try:
        # Extract filename from URL
        # URL format: https://cdn.sofifa.net/players/158/023/22_120.png
        filename = url.split('/')[-3] + '_' + url.split('/')[-2] + '_' + url.split('/')[-1]
        filepath = images_dir / filename
        
        # Skip if already downloaded
        if filepath.exists():
            return 'skipped'
        
        # Download image
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return 'success'
        else:
            return 'failed'
    
    except Exception as e:
        return 'failed'

def update_progress():
    """Display real-time progress"""
    elapsed = time.time() - stats['start_time']
    completed = stats['successful'] + stats['failed'] + stats['skipped']
    remaining = stats['total'] - completed
    
    if completed > 0:
        rate = completed / elapsed
        eta_seconds = remaining / rate if rate > 0 else 0
        eta_minutes = int(eta_seconds / 60)
        eta_seconds = int(eta_seconds % 60)
    else:
        rate = 0
        eta_minutes = 0
        eta_seconds = 0
    
    percentage = (completed / stats['total'] * 100) if stats['total'] > 0 else 0
    
    # Create progress bar
    bar_length = 40
    filled = int(bar_length * completed / stats['total']) if stats['total'] > 0 else 0
    bar = '█' * filled + '░' * (bar_length - filled)
    
    # Clear line and print progress
    sys.stdout.write('\r' + ' ' * 120)  # Clear line
    sys.stdout.write(f'\r[{bar}] {percentage:.1f}% | {completed}/{stats["total"]} | '
                    f'✓ {stats["successful"]} ✗ {stats["failed"]} ⊘ {stats["skipped"]} | '
                    f'{rate:.1f} img/s | ETA: {eta_minutes}m {eta_seconds}s')
    sys.stdout.flush()

# Load data - only 2022
print("Loading FIFA 2022 data...")
df = pd.read_csv('fifa_players_15_22_clean.csv', low_memory=False)
df_2022 = df[df['year'] == 2022]

# Get unique player face URLs for 2022
print("Finding unique player images for 2022...")
unique_urls = df_2022['player_face_url'].dropna().unique().tolist()
stats['total'] = len(unique_urls)
stats['start_time'] = time.time()

print(f"Found {stats['total']} unique player images to download")
print("Starting concurrent download...\n")

# Download images concurrently
max_workers = 50  # Concurrent download threads
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    # Submit all download tasks
    future_to_url = {executor.submit(download_image, url): url for url in unique_urls}
    
    # Process completed downloads
    for future in as_completed(future_to_url):
        result = future.result()
        
        with stats_lock:
            if result == 'success':
                stats['successful'] += 1
            elif result == 'failed':
                stats['failed'] += 1
            elif result == 'skipped':
                stats['skipped'] += 1
            
            update_progress()

# Final newline
print(f"\n\nDownload complete!")
print(f"✓ Successful: {stats['successful']}")
print(f"✗ Failed: {stats['failed']}")
print(f"⊘ Skipped (already exists): {stats['skipped']}")
print(f"Total images: {stats['successful'] + stats['skipped']}")
print(f"Time taken: {time.time() - stats['start_time']:.1f} seconds")
