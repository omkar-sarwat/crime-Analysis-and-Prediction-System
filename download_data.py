import requests
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

def download_chicago_crime_data():
    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # URL for the Chicago Crime dataset
    url = "https://data.cityofchicago.org/api/views/ijzp-q8t2/rows.csv?accessType=DOWNLOAD"
    
    # File path to save the data
    file_path = os.path.join('data', 'chicago_crime_data.csv')
    
    print("Downloading Chicago Crime dataset...")
    
    # Configure retry strategy
    retry_strategy = Retry(
        total=3,  # number of retries
        backoff_factor=1,  # wait 1, 2, 4 seconds between retries
        status_forcelist=[500, 502, 503, 504]  # HTTP status codes to retry on
    )
    
    # Create a session with the retry strategy
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    
    try:
        # Download the file with a larger timeout
        response = session.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        # Get total file size
        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192
        downloaded = 0
        
        # Save the file with progress tracking
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    # Calculate and display progress
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        print(f"\rDownload progress: {progress:.1f}%", end='')
        
        print("\nDownload complete!")
        print(f"File saved to: {file_path}")
        print(f"File size: {os.path.getsize(file_path) / (1024*1024):.2f} MB")
        
    except requests.exceptions.RequestException as e:
        print(f"\nError downloading the file: {str(e)}")
        print("Please try again later or download manually from:")
        print("https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2")
    finally:
        session.close()

if __name__ == "__main__":
    download_chicago_crime_data() 