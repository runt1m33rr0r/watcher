import face_recognition
import cv2
import time


def draw_box(frame, face_locations, face_names):
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 1
        right *= 1
        bottom *= 1
        left *= 1

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


def detect():
    video_capture = cv2.VideoCapture(0)

    image = face_recognition.load_image_file("images/ciri1.jpg")
    encoding = face_recognition.face_encodings(image)

    face_locations = []
    face_names = []
    process_this_frame = True

    while True:
        ret, frame = video_capture.read()

        if not ret:
            break

        converted_frame = frame[:, :, ::-1]

        if process_this_frame:
            face_names = []

            face_locations = face_recognition.face_locations(converted_frame, model="cnn")
            face_encodings = face_recognition.face_encodings(converted_frame, face_locations)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(encoding, face_encoding)

                if True in matches:
                    face_names.append("ciri")
                else:
                    face_names.append("unknown")
            
        process_this_frame = not process_this_frame

        draw_box(frame, face_locations, face_names)

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    detect()