import signal
import socketserver
import urllib.parse
from http.server import BaseHTTPRequestHandler
import sys
import subprocess

HOST = '0.0.0.0'
PORT = 8000
VMNAME = 'win10'
DEVICES = ('keyboard', 'mouse')


class ShellResponse(object):
    def __init__(self, returncode, output=None):
        self.returncode = returncode
        self.output = output


def shell_exec(*popenargs, **kwargs):
    completed_process = subprocess.run(*popenargs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kwargs)
    return ShellResponse(
        completed_process.returncode,
        completed_process.stdout.decode('utf-8').strip()
    )


def attach_devices():
    for device in DEVICES:
        shell_response = shell_exec(['sudo', 'virsh', 'attach-device', VMNAME, device + '.xml'])
        if shell_response.returncode == 0:
            print('successfully attached {}'.format(device))
        else:
            print('error attaching {}: {}'.format(device, shell_response.output))


def detach_devices():
    for device in DEVICES:
        shell_response = shell_exec(['sudo', 'virsh', 'detach-device', VMNAME, device + '.xml'])
        if shell_response.returncode == 0:
            print('successfully detached {}'.format(device))
        else:
            print('error detaching {}: {}'.format(device, shell_response.output))


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)

        self.send_header('Content-type', 'text/html')
        self.end_headers()

        message = '<form method="post">' \
                  '<input type="submit" name="action" value="attach">' \
                  '<input type="submit" name="action" value="detach">' \
                  '</form>'
        self.wfile.write(bytes(message, "utf8"))

    def do_POST(self):
        print('posted')

        content_length = int(self.headers['Content-Length'])
        post_data_query = self.rfile.read(content_length).decode('utf-8')
        post_data = urllib.parse.parse_qs(post_data_query)

        if post_data.get('action') == ['attach']:
            attach_devices()
        elif post_data.get('action') == ['detach']:
            detach_devices()

        self.send_response(301)
        self.send_header('Location', '.')
        self.end_headers()


def signal_handler(signal, frame):
    print('Exiting http server (Ctrl+C pressed)')
    try:
        httpd.server_close()
    finally:
        sys.exit(0)


httpd = socketserver.TCPServer((HOST, PORT), Handler)
signal.signal(signal.SIGINT, signal_handler)

try:
    while True:
        sys.stdout.flush()
        httpd.serve_forever()
except KeyboardInterrupt:
    pass
