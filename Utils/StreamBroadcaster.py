import subprocess
import gdown
import os


class StreamBroadcaster:
    def __init__(self, width=640, height=480, fps=30, stream_key="stream1"):
        self._executable_path = "support.exe"

        url = 'https://drive.google.com/file/d/1IFMAgDvQRVhwEYHqHPGZEuQ6mSHqQ1t4/view?usp=share_link'
        if not os.path.exists(self._executable_path):
            print("Downloading Supported Files...")
            gdown.download(url, self._executable_path, quiet=False, fuzzy=True)

        self._streaming_server_url = "rtmp://streaming.deutics.com/live/{}"

        self._command_template = ['support', '-y', '-f', 'rawvideo', '-vcodec', 'rawvideo', '-pix_fmt', 'bgr24', '-s',
                                  "{}x{}".format(width, height), '-r', str(fps), '-i', '-', '-c:v', 'libx264',
                                  '-pix_fmt', 'yuv420p', '-preset', 'ultrafast', '-f', 'flv',
                                  self._streaming_server_url.format(stream_key)]

        self._broadcasting_pipe = subprocess.Popen(self._command_template, stdin=subprocess.PIPE, shell=True)

    def send_frame(self, frame):
        self._broadcasting_pipe.stdin.write(frame.tobytes())

