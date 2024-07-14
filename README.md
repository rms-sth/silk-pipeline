# Silk Data Pipeline

## Setup

1. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

2. Set environment variables for API URLs and tokens:
    ```sh
    export QUALYS_API_URL="YOUR_QUALYS_API_URL"
    export QUALYS_API_TOKEN="YOUR_QUALYS_API_TOKEN"
    export CROWDSTRIKE_API_URL="YOUR_CROWDSTRIKE_API_URL"
    export CROWDSTRIKE_API_TOKEN="YOUR_CROWDSTRIKE_API_TOKEN"
    export MONGODB_URI="YOUR_MONGODB_URI"
    ```

3. Run the application:
    ```sh
    python main.py
    ```

## Dependencies
- Python 3.10
- httpx
- motor
- matplotlib
- flake8
- black
- isort

## Usage
The application fetches hosts data from Qualys and Crowdstrike APIs, normalizes the data, deduplicates the hosts, stores them in MongoDB, and generates visualizations.

## Visualizations
- Distribution of hosts by operating system (`hosts_by_os.png`)
- Old hosts vs newly discovered hosts (`old_vs_new_hosts.png`)
