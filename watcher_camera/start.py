import face_recognition
import cv2


video_capture = cv2.VideoCapture(0)

image = face_recognition.load_image_file("images/ciri1.jpg")
encoding = face_recognition.face_encodings(image)

process_this_frame = True
face_locations = []

while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    rgb_small_frame = small_frame[:, :, ::-1]

    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame,
            face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(encoding, face_encoding)
            name = "Unknown"

            print(matches)
            if True in matches:
                name = "Ciri"

            face_names.append(name)

    process_this_frame = not process_this_frame

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(
            frame,
            (left, bottom - 35),
            (right, bottom),
            (0, 0, 255),
            cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(
            frame,
            name,
            (left + 6, bottom - 6),
            font,
            1.0,
            (255, 255, 255),
            1)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
