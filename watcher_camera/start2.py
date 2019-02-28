import face_recognition
import cv2
import time


def check_images(images, known_encoding):
    batch_of_face_locations = face_recognition.batch_face_locations(
            images, 
            number_of_times_to_upsample=0, 
            batch_size=len(images))

    for frame_number_in_batch, face_locations in enumerate(batch_of_face_locations):
        face_encodings = face_recognition.face_encodings(images[frame_number_in_batch], face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encoding, face_encoding)

            if True in matches:
                print("ciri")
            else:
                print("unknown")


def start_capturing():
    batch_size = 30
    frames = []
    frame_count = 0

    image = face_recognition.load_image_file("images/ciri1.jpg")
    encoding = face_recognition.face_encodings(image)

    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()

        if not ret:
            break

        frame = frame[:, :, ::-1]
        frames.append(frame)
        frame_count += 1

        if len(frames) == batch_size:
            check_images(frames, encoding)

            frames = []

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start_capturing()
