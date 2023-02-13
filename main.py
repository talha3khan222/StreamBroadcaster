from Utils.StreamBroadcaster import StreamBroadcaster
import cv2


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    cap = cv2.VideoCapture(0)

    sb = StreamBroadcaster(width=640, height=480, fps=30, stream_key="stream1")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("frame read failed")
            break

        # YOUR CODE FOR PROCESSING FRAME HERE
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break

        try:
            sb.send_frame(frame)
        except Exception as e:
            print(e)

