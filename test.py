import multiprocessing
import cv2
import subprocess as sp


def push_stream(rtmp_url, width, height, fps):
    capture = cv2.VideoCapture(0)
    width, height = int(capture.get(3)), int(capture.get(4))
    fps = int(capture.get(cv2.CAP_PROP_FPS))

    command = ['support',
               '-y',
               '-f', 'rawvideo',
               '-vcodec', 'rawvideo',
               '-pix_fmt', 'bgr24',
               '-s', f'{width}x{height}',
               '-r', str(fps),
               '-i', '-',
               '-c:v', 'libx264',
               '-pix_fmt', 'yuv420p',
               '-preset', 'ultrafast',
               '-f', 'flv',
               rtmp_url]

    p = sp.Popen(command, stdin=sp.PIPE)

    # Replace this with your code to capture frames

    while True:
        ret, frame = capture.read()
        if not ret:
            break
        frame = cv2.resize(frame, (width, height))
        p.stdin.write(frame.tobytes())

    p.stdin.close()
    p.wait()


if __name__ == '__main__':
    # Define the RTMP URLs and stream parameters for each stream
    stream1_url = 'rtmp://streaming.deutics.com/live/stream1'
    stream1_width = 640
    stream1_height = 480
    stream1_fps = 30

    stream2_url = 'rtmp://example.com/stream2'
    stream2_width = 1280
    stream2_height = 720
    stream2_fps = 60

    # Spawn a separate process for each stream
    p1 = multiprocessing.Process(target=push_stream, args=(stream1_url, stream1_width, stream1_height, stream1_fps))
    #p2 = multiprocessing.Process(target=push_stream, args=(stream2_url, stream2_width, stream2_height, stream2_fps))

    # Start the processes
    p1.start()
    #p2.start()

    # Wait for the processes to finish
    p1.join()
    #p2.join()
