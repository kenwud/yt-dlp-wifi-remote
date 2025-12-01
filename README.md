# yt-dlp-wifi-remote

Passes links from your phone to yt-dlp on PC with a simple web interface over wifi

## Screenshot of web interface
<img width="499" height="730" alt="yt-dlp-remote-ss" src="https://github.com/user-attachments/assets/dbeb5e5e-ff9b-468b-8c93-4c5d9ae47dec" />

## Features

- 🎯 Simple one-button interface accessible from any device on your network
- 📱 Perfect for sending videos from your phone to your PC
- 🎚️ Quality selector (Best/1080p/720p/480p/Audio Only)
- ⚡ Lightweight Flask server
- 🌐 Works on local network - no internet required after initial setup (internet is still required for the pc to access the video you want to download)

## Prerequisites

- **Python 3.7+** - [Download here](https://www.python.org/downloads/)
- **yt-dlp** - [Download latest release](https://github.com/yt-dlp/yt-dlp/releases)
- **Flask** - Installed via requirements.txt (see below)
- **ffmpeg** (Optional but recommended) - For merging video/audio formats


## Platform Support

Works on Windows, Mac, and Linux.

**Note for Mac/Linux users:** Use forward slashes in paths:
```python
DOWNLOAD_FOLDER = "/home/username/downloads"
YTDLP_PATH = "yt-dlp"  # usually already in PATH
```


## Installation

1. **Clone or download this repository**
```bash
   git clone https://github.com/kenwud/yt-dlp-wifi-remote.git
   cd yt-dlp-wifi-remote
```

2. **Install Python dependencies**
```bash
   pip install -r requirements.txt
```

3. **Download yt-dlp** and place it in a folder, or install it system-wide

4. **Edit the script configuration**
   
   Open `server.py` and modify lines 9-10:
```python
   DOWNLOAD_FOLDER = r"C:\path\to\your\download\folder"
   YTDLP_PATH = r"C:\path\to\yt-dlp.exe"  # or just "yt-dlp" if in PATH
```

5. **Find your PC's IP address**
```bash
   ipconfig          # Windows
   ifconfig          # Mac/Linux
```
   Look for your IPv4 address (e.g., `192.168.1.123`)

## Usage

1. **Start the server**
   just double click the server.py
   or
```bash
   python server.py
```

2. **Access from your phone**
   - Open your phone's browser
   - Go to `http://YOUR_PC_IP:5000`
   - Bookmark it for quick access!

3. **Download videos**
   - Paste a YouTube URL
   - Select quality
   - Hit Download
   - Video saves to your configured folder

## Tips

- Keep the server running whenever you want to download videos
- Both devices must be on the same WiFi network
- Bookmark the page on your phone's home screen for one-tap access

Recommended folder structure:
yt-dlp-remote/
├── server.py
├── requirements.txt
├── yt-dlp.exe
├── ffmpeg.exe
└── downloads/ (create this folder)


## Troubleshooting

**Can't connect from phone?**
- Make sure both devices are on the same WiFi
- Check your PC's firewall isn't blocking port 5000
- Verify you're using the correct IP address

**Downloads failing?**
- Update yt-dlp: `yt-dlp -U`
- Check that your paths in the script are correct
- Ensure you have write permissions to the download folder

## License

MIT License - feel free to modify and use however you want!

## Contributing

Pull requests welcome! Feel free to add features or improvements.
