from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import sys

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='dist', **kwargs)

class ResilientServer(ThreadingHTTPServer):
    allow_reuse_address = True

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 4173
    server = ResilientServer(('127.0.0.1', port), Handler)
    print(f'Serving HTTP on 127.0.0.1 port {port} (http://127.0.0.1:{port}/) ...', flush=True)
    server.serve_forever()
