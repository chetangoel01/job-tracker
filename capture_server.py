#!/usr/bin/env python3
import http.server
import json
import socketserver
import urllib.parse
from datetime import datetime
from pathlib import Path

ROOT = Path('/Users/chetan/Desktop/job-tracker')
MD_FILE = ROOT / 'job-tracker.md'

def append_to_markdown(company: str, role: str, url: str, source: str | None = None) -> None:
    """Append a new Inbox item as a Markdown table row.

    The table schema matches the Pipeline table:
    | status | company | role | link | source | applied_on | last_touch | next_action | follow_up_on | notes |
    For Inbox items, we fill: status=Inbox, link=[link](URL), source, last_touch=captured timestamp.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    source_text = source or ''

    # Escape vertical bars in free-text fields to avoid breaking the table
    def esc(text: str) -> str:
        return (text or '').replace('|', '\\|').strip()

    company_cell = esc(company)
    role_cell = esc(role)
    link_cell = f"[link]({url})" if url else ''

    # Compose a table row matching the header columns
    new_line = (
        f"| Inbox | {company_cell} | {role_cell} | {link_cell} | {source_text} |  | {timestamp} |  |  |  |\n"
    )

    contents = MD_FILE.read_text(encoding='utf-8')
    separator = '' if contents.endswith('\n') else '\n'
    MD_FILE.write_text(contents + separator + new_line, encoding='utf-8')

class Handler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        try:
            length = int(self.headers.get('content-length', '0'))
            raw = self.rfile.read(length)
            ctype = self.headers.get('content-type', '')
            if 'application/json' in ctype:
                data = json.loads(raw.decode('utf-8') or '{}')
            else:
                data = urllib.parse.parse_qs(raw.decode('utf-8'))
                data = {k: v[0] if isinstance(v, list) else v for k, v in data.items()}

            company = (data.get('company') or '').strip()
            role = (data.get('role') or '').strip()
            url = (data.get('url') or '').strip()
            source = (data.get('source') or '').strip()

            if not url:
                self.send_response(400)
                self._cors(); self.end_headers()
                self.wfile.write(b'Missing url')
                return

            if not company:
                # Best-effort from URL host
                try:
                    host = urllib.parse.urlparse(url).hostname or ''
                    company = host.replace('www.', '')
                except Exception:
                    company = ''

            if not role:
                role = ''

            append_to_markdown(company, role, url, source)

            self.send_response(200)
            self._cors(); self.end_headers()
            self.wfile.write(b'OK')
        except Exception as e:
            self.send_response(500)
            self._cors(); self.end_headers()
            self.wfile.write(str(e).encode('utf-8'))

    def log_message(self, format, *args):
        return  # keep quiet

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'text/plain; charset=utf-8')

def run(default_port: int = 8765):
    candidate_ports = [default_port, 8766, 8787, 8888]
    last_err = None
    for port in candidate_ports:
        try:
            with socketserver.TCPServer(('127.0.0.1', port), Handler) as httpd:
                print(f'Capture server running at http://127.0.0.1:{port}')
                httpd.serve_forever()
                return
        except OSError as e:
            last_err = e
            continue
    raise SystemExit(f'Failed to bind to any port in {candidate_ports}: {last_err}')

if __name__ == '__main__':
    run()


