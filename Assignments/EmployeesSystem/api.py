import json
import ast
from http.server import BaseHTTPRequestHandler, HTTPServer

from EmployeesSystem.logic.ClientHandler import ClientHandler

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(bytes("Welcome to our web server", "utf-8"))

    def do_POST(self):
        self._set_headers()
        if self.path.split("?")[0] == '/check':
            self.do_check()
        return

    def do_check(self):
        content_len = int(self.headers.get('content-length', 0))
        if not content_len:
            self.send_error(404, "No data was given.")
            return
        data_dic = ast.literal_eval(self.rfile.read(content_len).decode('utf-8'))
        print("data dic:", data_dic)
        result = ClientHandler().check_employee_eligible(data_dic)
        if result.success:
            json_response = json.dumps({"eligible": True})
        else:
            if result.error == "This employee does not exist_ids in the system.":
                json_response = json.dumps({"eligible": False})
            else:
                self.send_error(404, result.error)
                return
        self.wfile.write(json_response.encode())


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")