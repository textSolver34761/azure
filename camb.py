import cv2 as cv

capture = cv.VideoCapture(0)
if not capture.isOpened():
    print('Unable to open: ')
    exit(0)
while True:
    bool, frame = capture.read()
    if(bool == True):
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imshow('live', frame)
        if(cv.waitKey(20) == ord('x')):
            break
capture.release()
cv.destroyAllWindows()