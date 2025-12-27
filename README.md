# MusicVault

MusicVault is a smart, offline-first music management and playback application. This repository contains the source code for the desktop application, which acts as the authoritative source for a user's music library.

## Getting Started

### Prerequisites

- Python 3.8+
- `ffmpeg` (for running the test suite)

On Debian-based systems, you can install `ffmpeg` with:
```bash
sudo apt-get update && sudo apt-get install -y ffmpeg
```

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd musicvault
   ```

2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

To run the desktop application, execute the `main.py` script:
```bash
python main.py
```

### Running Tests

To run the unit tests, use the following command from the project root:
```bash
python -m unittest discover tests
```
