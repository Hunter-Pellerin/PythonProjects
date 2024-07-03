from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from threading import Thread
import imutils
import sys
import cv2
from time import sleep

stream = None

class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if self.path.endswith('/stream.mjpg'):
            self._setupImageCanvas()
            while True:
                self._writeStreamToServer()
                sleep(0.1)

        elif self._checkForHomePath:
            self._setupHTML()

    def _writeStreamToServer(self):
        try:
            frame = stream.read()
            if (frame.all() != None):
                self._writeFrame(frame)
        except Exception as e:
            raise e

    def _writeFrame(self, frame):
        retval, memBuffer = cv2.imencode(".jpg", frame)
        self.wfile.write("--jpgboundary\r\n".encode())
        self.end_headers()
        self.wfile.write(bytearray(memBuffer))

    def _checkForHomePath(self):
        return self.path.endswith('.html') or self.path == "/"

    def _setupImageCanvas(self):
        self.send_response(20)
        self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
        self.end_headers()

    def _setupHTML(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<html><head></head><body>')
        self.wfile.write(b'<img src="http://localhost:9090/stream.mjpg" height="240px" width="320px"/>')
        self.wfile.write(b'</body></html>')

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

class ImageStream:
    def __init__(self):
        self.frame = None
        self.isStreamEnabled = False

    def start(self):
        self.isStreamEnabled = True
        return self

    def update(self, img):
        self.frame = img

    def read(self):
        return self.frame

    def stop(self):
        self.isStreamEnabled = False

class WebcamVideoStream:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                self.stream.release()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True


def start():
    global stream
    ip = 'localhost'

    try:
        stream = ImageStream()
        server = ThreadedHTTPServer((ip, 9090), CamHandler)
        print("starting server")
        target = Thread(target=server.serve_forever,args=()).start()

    except KeyboardInterrupt:
        sys.exit()
