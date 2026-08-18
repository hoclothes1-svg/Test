import asyncio
import threading
from playwright.async_api import async_playwright
from flask import Flask, render_template_string

app = Flask(__name__)
found_m3u8_url = ""

# --- بەشی یەکەم: دۆزەرەوەی لینکەکە ---
async def find_m3u8(target_url):
    global found_m3u8_url
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True) # بە شاراوەیی کار دەکات
        page = await browser.new_page()

        print(f"[*] Searching for link in: {target_url}")

        async def handle_request(request):
            global found_m3u8_url
            if ".m3u8" in request.url and "chunk" not in request.url:
                found_m3u8_url = request.url
                print(f"\n[+] Link Found: {found_m3u8_url}")

        page.on("request", handle_request)
        
        try:
            await page.goto(target_url, wait_until="networkidle", timeout=60000)
            await asyncio.sleep(5) # کات بۆ باربوونی تەواوی ڤیدیۆکە
        except Exception as e:
            print(f"[-] Error during search: {e}")
        
        await browser.close()

# --- بەشی دووەم: وێب سێرڤەر بۆ نمایشکردنی ڤیدیۆکە ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Cyber AI - High Performance Player</title>
    <link href="https://vjs.zencdn.net/7.20.3/video-js.css" rel="stylesheet" />
    <style>
        body { background-color: #0f0f0f; color: white; font-family: sans-serif; text-align: center; }
        .container { margin-top: 50px; }
        .video-js { margin: 0 auto; border: 2px solid #00ff00; box-shadow: 0 0 20px rgba(0,255,0,0.2); }
    </style>
</head>
<body>
    <div class="container">
        <h1>Live Stream Player</h1>
        <p>Source: {{ url }}</p>
        <video id="player" class="video-js vjs-default-skin vjs-16-9" controls preload="auto">
            <source src="{{ url }}" type="application/x-mpegURL">
        </video>
    </div>

    <script src="https://vjs.zencdn.net/7.20.3/video.min.js"></script>
    <script>
        var player = videojs('player', {
            autoplay: true,
            fluid: true,
            html5: { vhs: { overrideNative: true, enableLowInitialPlaylist: true } }
        });
        
        // ڕێگری لە پچڕان: ئەگەر هەڵە ڕوویدا دووبارە پەیوەندی دەکاتەوە
        player.on('error', function() {
            console.log("Reconnecting...");
            player.src({ src: "{{ url }}", type: 'application/x-mpegURL' });
            player.play();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    if found_m3u8_url:
        return render_template_string(HTML_TEMPLATE, url=found_m3u8_url)
    return "<h1>Searching for link... Please refresh in 10 seconds.</h1>"

def run_flask():
    app.run(port=5000)

# --- بەشی سێیەم: ڕاکردنی هەردوو بەشەکە پێکەوە ---
if __name__ == "__main__":
    target = input("Enter the Website URL: ")
    
    # دەستپێکردنی سێرڤەر لە Threadێکی جیاواز
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # دەستپێکردنی گەڕان بۆ لینکەکە
    asyncio.run(find_m3u8(target))

    print("\n[!] Web Server is running at: http://127.0.0.1:5000")
    print("[*] Press Ctrl+C to stop.")
    
    while True: # هێشتنەوەی بەرنامەکە بە کراوەیی
        pass
