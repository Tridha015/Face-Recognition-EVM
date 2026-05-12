import cv2
import os


if not os.path.exists('known_faces'):
    os.makedirs('known_faces')

cap = cv2.VideoCapture(0)

name = input("Enter Voter Name: ")

print("Press 's' to capture photo and register.")

while True:
    success, img = cap.read()
    cv2.imshow("Register Voter", img)
    
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite(f'known_faces/{name}.jpg', img)
        print(f"Voter {name} Registered Successfully!")
        break

cap.release()
cv2.destroyAllWindows()
