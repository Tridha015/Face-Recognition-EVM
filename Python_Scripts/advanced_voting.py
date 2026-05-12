import sys
import os
import collections
import time

try:
    import pkg_resources
except ImportError:
    if not hasattr(collections, 'Mapping'):
        import collections.abc
        collections.Mapping = collections.abc.Mapping
    class FakePkgResources:
        def resource_filename(self, package_or_requirement, resource_name):
            import face_recognition_models
            return os.path.join(os.path.dirname(face_recognition_models.__file__), resource_name)
    sys.modules['pkg_resources'] = FakePkgResources()

env_path = '/Users/fabihalamisatridha/Desktop/Microprocessor/project/voting_env/lib/python3.13/site-packages'
if env_path not in sys.path:
    sys.path.insert(0, env_path)

import face_recognition
import cv2
import serial

VOTE_FILE = "voted_list.txt"
voted_voters = set()

if os.path.exists(VOTE_FILE):
    with open(VOTE_FILE, "r") as f:
        voted_voters = set(line.strip() for line in f if line.strip())

def save_vote_to_file(name):
    with open(VOTE_FILE, "a") as f:
        f.write(name + "\n")


try:
    arduino = serial.Serial(port='/dev/cu.usbmodem114201', baudrate=9600, timeout=1)
    print("✅ Arduino Connected!")
    time.sleep(2) 
except Exception as e:
    print(f"⚠️ Arduino Not Found: {e}")

known_face_encodings = []
known_face_names = []

print("🔄 Loading registered voters...")
if not os.path.exists("known_faces"):
    os.makedirs("known_faces")

for file in os.listdir("known_faces"):
    if file.endswith((".jpg", ".png", ".jpeg")):
        img = face_recognition.load_image_file(f"known_faces/{file}")
        encodings = face_recognition.face_encodings(img)
        if len(encodings) > 0:
            known_face_encodings.append(encodings[0])
            known_face_names.append(file.split(".")[0])
            print(f"✔️ Loaded: {file.split('.')[0]}")


cap = cv2.VideoCapture(0)
print("System Ready! Looking for faces...")

while True:
    success, frame = cap.read()
    if not success:
        break

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        status_msg = "Unknown Person"
        color = (0, 0, 255)

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

            if name in voted_voters:
                status_msg = f"{name} - ALREADY VOTED!"
                color = (0, 0, 255)
                print(f"❌ Access Denied: {name} has already voted!")
                
                if 'arduino' in locals() and arduino.is_open:
                    arduino.write(b'D') 
                time.sleep(3) 
            else:
                
                status_msg = f"Verified: {name}"
                color = (0, 255, 0) 
                print(f"🔓 Verified: {name}. Unlocking Machine...")
                
                if 'arduino' in locals() and arduino.is_open:
                    arduino.flushInput() 
                    arduino.write(b'U')
                
                
                vote_done = False
                print(f"⏳ Waiting for {name} to cast a vote on Arduino...")
                
                start_wait = time.time()
                while time.time() - start_wait < 20:
                    if 'arduino' in locals() and arduino.in_waiting > 0:
                        data = arduino.read().decode().strip()
                        if data == 'V':
                            vote_done = True
                            break
                    
                    cv2.waitKey(1) 
                    time.sleep(0.1)

                if vote_done:
                    voted_voters.add(name) 
                    save_vote_to_file(name) 
                    print(f"✅ Success: Vote Registered for {name}")
                    cv2.putText(frame, "VOTE RECORDED!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    print(f"⚠️ Timeout: {name} did not vote in time.")
                    cv2.putText(frame, "VOTE TIMEOUT!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
                cv2.imshow('AIUB Secure Voting System', frame)
                cv2.waitKey(1)
                time.sleep(2)

        top, right, bottom, left = [v * 4 for v in face_location]
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, status_msg, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow('AIUB Secure Voting System', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
if 'arduino' in locals():
    arduino.close()
