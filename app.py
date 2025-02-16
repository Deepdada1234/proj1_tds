from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import json
import os

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        """Handles POST requests for executing tasks."""
        if self.path.startswith("/run"):
            query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            task = query_components.get("task", [None])[0]

            if not task or not task.strip():
                self.respond(400, {"status": "error", "message": "Task description cannot be empty"})
                return

            # Simulate task execution
            response = {"status": "success", "message": f"Executed task: {task}"}
            self.respond(200, response)
        else:
            self.respond(404, {"status": "error", "message": "Endpoint not found"})

    def do_GET(self):
        """Handles GET requests for reading files."""
        if self.path.startswith("/read"):
            query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            path = query_components.get("path", [None])[0]

            if not path:
                self.respond(400, {"status": "error", "message": "File path parameter is required"})
                return

            if not os.path.isfile(path):
                self.respond(404, {"status": "error", "message": "File not found"})
                return

            try:
                with open(path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.respond(200, {"status": "success", "content": content})
            except Exception as e:
                self.respond(500, {"status": "error", "message": f"Error reading file: {str(e)}"})
        else:
            self.respond(404, {"status": "error", "message": "Endpoint not found"})

    def respond(self, status_code, response_data):
        """Helper function to send JSON responses."""
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode("utf-8"))

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    """Starts the HTTP server."""
    server_address = ("0.0.0.0", port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
