import cv2
from PIL import Image
from io import BytesIO
from api import alert


should_alert = False


def process_image(image):
    image = Image.open(image)
    image = image.convert('RGB')
    new = BytesIO()
    image.save(new, 'jpeg')

    return new


def process_video_frame(frame):
    ret, jpeg = cv2.imencode('.jpg', frame)

    if not ret:
        return

    frame = jpeg.tobytes()

    global should_alert
    if not should_alert:
        should_alert = True
        alert(['Ciri'], frame)

    return frame
