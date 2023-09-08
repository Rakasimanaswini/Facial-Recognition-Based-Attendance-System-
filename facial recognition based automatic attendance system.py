import face_recognition
import cv2
import datetime

# 1. Prepare the dataset
known_faces = []
known_names = []

# Assuming you have images named as "person_name.jpg" in a "dataset" folder
image_files = ['dataset/alice.jpg', 'dataset/bob.jpg'] # ... add all your image filenames here

for image_file in image_files:
    image = face_recognition.load_image_file(image_file)
    encoding = face_recognition.face_encodings(image)[0]
    known_faces.append(encoding)
    known_names.append(image_file.split("/")[-1].split(".")[0])

attendance = {}

# 2. Start webcam and recognize faces
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    rgb_frame = frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        
        name = "Unknown"
        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]

            # Mark attendance (with time)
            if name not in attendance:
                attendance[name] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

    cv2.imshow('Video', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

# 3. Save the attendance to a file
with open("attendance.csv", "w") as file:
    file.write("Name,Time\n")
    for name, time in attendance.items():
        file.write(f"{name},{time}\n")

print("Attendance saved to attendance.csv!")
Facial recognition-based attendance system  Facial recognition-based attendance system  Facial recognition-based attendance system   
