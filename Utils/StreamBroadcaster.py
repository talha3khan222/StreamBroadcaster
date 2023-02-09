import cv2
import subprocess
import copy
from Utils.GoogleDriveDownloader import download_file_from_google_drive


class StreamBroadcaster:
    def __init__(self, width=640, height=480, fps=30, stream_key="stream1"):
        self._executable_path = "../support.exe"

        # downloader = GoogleDriveDownloader()
        download_file_from_google_drive(id="1Vz-6phclxoqS1hBGBRfLjhxj16L_G8ux", destination=self._executable_path)

        self._streaming_server_url = "rtmp://streaming.deutics.com/live/{}"

        self._command_template = ['support', '-y', '-f', 'rawvideo', '-vcodec', 'rawvideo', '-pix_fmt', 'bgr24', '-s',
                                  "{}x{}".format(width, height), '-r', str(fps), '-i', '-', '-c:v', 'libx264',
                                  '-pix_fmt', 'yuv420p', '-preset', 'ultrafast', '-f', 'flv',
                                  self._streaming_server_url.format(stream_key)]

        self._broadcasting_pipe = subprocess.Popen(self._command_template, stdin=subprocess.PIPE, shell=True)

    def send_frame(self, frame):
        self._broadcasting_pipe.stdin.write(frame.tobytes())

