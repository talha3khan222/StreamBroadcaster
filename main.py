from Utils.StreamBroadcaster import StreamBroadcaster
import cv2
from multiprocessing import Process, freeze_support, Pool
import subprocess


def get_command(stream_url, stream_id):
    command = ["support",
               "-i", stream_url,
               "-c:v", "libx264",
               "-preset", "veryfast",
               "-b:v", "500k",
               "-maxrate", "500k",
               "-bufsize", "1000k",
               "-c:a", "aac",
               "-b:a", "128k",
               "-f", "flv", "rtmp://streaming.deutics.com/live/" + stream_id]

    return command


def run_ffmpeg(command):
    subprocess.run(command)


def broadcast_streams(streams_list):
    commands = []
    for index, stream_url in enumerate(streams_list):
        commands.append(get_command(stream_url, "stream"+str(index)))

    # Create a pool of worker processes and execute the FFmpeg commands
    with Pool(processes=len(streams_list)) as pool:
        pool.map(run_ffmpeg, commands)


def push_stream(stream_data):
    cap = cv2.VideoCapture(stream_data["source_url"])

    width, height = int(cap.get(3)), int(cap.get(4))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    sb = StreamBroadcaster(width=width, height=height, fps=fps, stream_key=stream_data["stream_key"])

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("frame read failed")
            break

        # cv2.imshow('Frame' + stream_data["stream_key"], frame)
        # if cv2.waitKey(1) == ord('q'):
        #     break

        try:
            pass
            sb.send_frame(frame)
        except Exception as e:
            print(stream_data["stream_key"], "Stream Broadcasting Stopped", e)
            break

    cap.release()
    sb.close_broadcasting_pipe()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    freeze_support()

    f = open("urls.txt", 'r')
    lines = f.readlines()
    urls_list = []
    for line in lines:
        urls_list.append(line.rstrip('\n'))

    f.close()

    print(urls_list)

    streams_data = []

    for index, url in enumerate(urls_list):
        streams_data.append({"source_url": int(url) if url.isnumeric() else url,
                             "stream_key": "stream" + str(index)})

    with Pool(processes=len(streams_data)) as pool:
        pool.map(push_stream, streams_data)

    # "rtsp://getptz:a10alb8q9jz8jJiD@93.122.231.135:9554/ISAPI/Streaming/channels/102"


