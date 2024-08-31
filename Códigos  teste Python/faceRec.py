#import the necessary modules
import freenect
import cv2
import numpy as np

face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def get_depth():
    depth, _ = freenect.sync_get_depth()
    return depth * 0.001

def faceDist(x, y):
    depth = get_depth()
    # print(type(depth))
    x = int(x / 2048 * 255)
    y = int(y / 2048 * 255)
    # print(type(int(x)))
    center = depth[x, y]
    print(f'Distance at center face: {center:.2f} meters')

def detect_bounding_box(vid):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    for (x, y, w, h) in faces:
        cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)
        # center = [(x + w/2),(y + h/2)]
        if type(faces) is np.ndarray:
            faceDist((x + w/2), (y + h/2))
            print(f"Positions are :",(x + w/2),", ", (y + h/2))
    return faces

while True:

    array,_ = freenect.sync_get_video()
    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)

    faces = detect_bounding_box(
        array
    )  # apply the function we created to the video frame

    cv2.imshow(
        "My Face Detection Project", array
    )  # display the processed frame in a window named "My Face Detection Project"
    # print(type(faces))

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

#array.release()
cv2.destroyAllWindows()