"""Render the ZuluLens timeline animation to MP4.

Opens index.html?record in a headless browser, steps the animation one frame at a time
and pipes each screenshot into ffmpeg. No icons or play button are shown.

Usage (needs Python with `playwright` installed, plus ffmpeg):
    python export_video.py                 # 16:9, 1920x1080
    python export_video.py --size square   # 1080x1080
    python export_video.py --size vertical # 1080x1920
    python export_video.py --theme dark --fps 30
"""
import argparse, functools, http.server, os, subprocess, threading
from playwright.sync_api import sync_playwright

SIZES = {  # CSS viewport and scale; output pixels = viewport x scale
    'wide': (1280, 720, 1.5),
    'square': (720, 720, 1.5),
    'vertical': (720, 1280, 1.5),
}

def serve(folder):
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args): pass
    handler = functools.partial(Quiet, directory=folder)
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--size', choices=SIZES, default='wide')
    ap.add_argument('--fps', type=int, default=60)
    ap.add_argument('--theme', choices=['light', 'dark'], default='light')
    ap.add_argument('--hold-start', type=float, default=0.6, help='seconds to hold on 2000')
    ap.add_argument('--hold-end', type=float, default=3.0, help='seconds to hold on Oct 2026')
    ap.add_argument('--scale', type=float, default=None, help='pixel scale (1.5 = 1080p square; 3 = 2160x2160)')
    ap.add_argument('--out', default=None)
    a = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    w, h, scale = SIZES[a.size]
    if a.scale: scale = a.scale
    out = a.out or os.path.join(here, 'video', f'ZuluLens_timeline_{a.size}_{a.theme}_{int(w * scale)}.mp4')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    srv = serve(here)
    url = f'http://127.0.0.1:{srv.server_address[1]}/index.html?record'

    ff = subprocess.Popen([
        'ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(a.fps), '-i', '-',
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'slow', '-movflags', '+faststart', out,
    ], stdin=subprocess.PIPE)

    ticks = max(1, round(60 / a.fps))  # the live page runs one layout step per 60 fps frame
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception:  # Playwright's own browser not installed: use Google Chrome instead
            browser = p.chromium.launch(channel='chrome')
        page = browser.new_page(viewport={'width': w, 'height': h}, device_scale_factor=scale)
        page.goto(url)
        page.wait_for_function('window.rec && document.getElementById("canvas").width > 0')
        page.wait_for_timeout(500)
        if a.theme == 'dark':
            page.evaluate("document.getElementById('theme').click()")  # button is hidden in record mode
        page.evaluate('rec.start()')
        page.add_style_tag(content='*{caret-color:transparent!important}')

        def shot():
            ff.stdin.write(page.screenshot(type='png'))

        frames = 0
        for _ in range(round(a.hold_start * a.fps)):
            page.evaluate(f'rec.step(0, {ticks})'); shot(); frames += 1
        done = False
        while not done:
            done = page.evaluate(f'rec.step({1 / a.fps}, {ticks})'); shot(); frames += 1
        for _ in range(round(a.hold_end * a.fps)):
            page.evaluate(f'rec.step(0, {ticks})'); shot(); frames += 1
        browser.close()

    ff.stdin.close(); ff.wait(); srv.shutdown()
    print(f'{out}  ({frames} frames, {frames / a.fps:.1f}s, {int(w * scale)}x{int(h * scale)})')

if __name__ == '__main__':
    main()
