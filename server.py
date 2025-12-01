from flask import Flask, request, render_template_string, jsonify
import subprocess
import os
from threading import Thread

app = Flask(__name__)

# CONFIGURATION - Change these to match your setup
DOWNLOAD_FOLDER = r"C:\Users\YourUsername\Downloads"  # Change this to your folder
YTDLP_PATH = "yt-dlp"  # If yt-dlp is in PATH, keep as is. Otherwise use full path like r"C:\path\to\yt-dlp.exe"

# Simple HTML interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>yt-dlp Remote</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background: #1a1a1a;
            color: #fff;
        }
        h1 {
            text-align: center;
            color: #4CAF50;
        }
        .container {
            background: #2d2d2d;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        input[type="text"], select {
            width: 100%;
            padding: 15px;
            font-size: 16px;
            border: 2px solid #444;
            border-radius: 5px;
            box-sizing: border-box;
            background: #1a1a1a;
            color: #fff;
            margin-bottom: 15px;
        }
        select {
            cursor: pointer;
        }
        button {
            width: 100%;
            padding: 15px;
            font-size: 18px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover {
            background: #45a049;
        }
        button:active {
            background: #3d8b40;
        }
        #status {
            margin-top: 20px;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
            font-weight: bold;
            display: none;
        }
        .success {
            background: #4CAF50;
            color: white;
        }
        .error {
            background: #f44336;
            color: white;
        }
        .info {
            background: #2196F3;
            color: white;
        }
    </style>
</head>
<body>
    <h1>📥 yt-dlp Remote</h1>
    <div class="container">
        <input type="text" id="url" placeholder="Paste video URL here" autofocus>
        
        <select id="quality">
            <option value="best">Best Quality (Default)</option>
            <option value="1080">1080p</option>
            <option value="720">720p</option>
            <option value="480">480p</option>
            <option value="audio">Audio Only (MP3)</option>
        </select>
        
        <button onclick="download()">Download</button>
        <div id="status"></div>
    </div>

    <script>
        function showStatus(message, type) {
            const status = document.getElementById('status');
            status.textContent = message;
            status.className = type;
            status.style.display = 'block';
        }

        function download() {
            const url = document.getElementById('url').value.trim();
            const quality = document.getElementById('quality').value;
            
            if (!url) {
                showStatus('Please paste a URL', 'error');
                return;
            }

            showStatus('Starting download...', 'info');
            
            fetch('/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({url: url, quality: quality})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showStatus('✓ Download started!', 'success');
                    document.getElementById('url').value = '';
                } else {
                    showStatus('✗ Error: ' + data.error, 'error');
                }
            })
            .catch(error => {
                showStatus('✗ Connection error', 'error');
            });
        }

        // Allow Enter key to submit
        document.getElementById('url').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                download();
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url', '').strip()
    quality = data.get('quality', 'best')
    
    if not url:
        return jsonify({'success': False, 'error': 'No URL provided'})
    
    # Build yt-dlp command based on quality selection
    if quality == 'audio':
        cmd = [YTDLP_PATH, '-x', '--audio-format', 'mp3', url]
    elif quality == 'best':
        cmd = [YTDLP_PATH, url]
    else:
        # For specific resolutions (1080, 720, 480)
        cmd = [YTDLP_PATH, '-f', f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]', url]
    
    # Run yt-dlp in background thread so the response is immediate
    def run_download():
        try:
            # Change to download directory
            os.chdir(DOWNLOAD_FOLDER)
            
            # Run yt-dlp with selected quality
            subprocess.run(cmd, check=True)
        except Exception as e:
            print(f"Download error: {e}")
    
    thread = Thread(target=run_download)
    thread.daemon = True
    thread.start()
    
    return jsonify({'success': True})

if __name__ == '__main__':
    print("=" * 50)
    print("yt-dlp Remote Server Starting...")
    print("=" * 50)
    print(f"Download folder: {DOWNLOAD_FOLDER}")
    print(f"\nAccess from your phone at:")
    print(f"  http://YOUR_PC_IP:5000")
    print("\nTo find your PC's IP:")
    print("  Run: ipconfig")
    print("  Look for 'IPv4 Address' under your network adapter")
    print("=" * 50)
    
    # Run server accessible from network
    app.run(host='0.0.0.0', port=5000, debug=False)
