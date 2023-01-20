import cv2
import numpy as np
from threading import *

class height:
    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    # Set the ArUco tag dictionary and parameters
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_7X7_250)
    parameters = cv2.aruco.DetectorParameters_create()
    parameters.minMarkerDistanceRate = 0.001
    parameters.minMarkerPerimeterRate=0.01
    parameters.cornerRefinementMethod=cv2.aruco.CORNER_REFINE_SUBPIX
    cap.set(cv2.CAP_PROP_FPS,120)

    # Define the marker length (in meters)
    markerLength = 0.1

    # Define the camera matrix and distortion coefficients
    cameraMatrix = np.array([[1.14725359e+04, 0.00000000e+00, 3.95514461e+02],
    [0.00000000e+00, 1.07338748e+04, 3.65205692e+02],
    [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
    distCoeffs = np.array([[ 7.31913177e+00, -3.64743644e+03, -1.37997410e-03,  2.24620344e-02,
    -7.65969550e+00]])
    def show(self,arg):
        return arg

    def show_webcam(self,mirror=False):
        scale=40

        while True:
            ret, frame = height.cap.read()
            if mirror: 
                frame = cv2.flip(frame, 1)

            #get the webcam size
            height, width, channels = frame.shape

            #prepare the crop
            centerX,centerY=int(height/2),int(width/2)
            radiusX,radiusY= int(scale*height/100),int(scale*width/100)

            minX,maxX=centerX-radiusX,centerX+radiusX
            minY,maxY=centerY-radiusY,centerY+radiusY

            cropped = frame[minX:maxX, minY:maxY]
            resized_cropped = cv2.resize(cropped, (width, height)) 

            gray = cv2.cvtColor(resized_cropped, cv2.COLOR_BGR2GRAY)

            # Detect the ArUco tag in the frame
            corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, height.aruco_dict, parameters=height.parameters)
            # Draw the ArUco tag corners on the frame
            cv2.aruco.drawDetectedMarkers(resized_cropped, corners)

            # Display the frame
            cv2.imshow("Webcam", resized_cropped)
            # Exit the loop  if the 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if ids is not None:
                # Estimate the pose of each marker
                rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, height.markerLength, height.cameraMatrix, height.distCoeffs)

                for i in range(len(ids)):
                    # Convert the rotation vector to a rotation matrix
                    rmat, _ = cv2.Rodrigues(rvecs[i])

                    # Calculate the distance between the marker and the camera
                    distance = np.linalg.norm(tvecs[i])
                    print("Marker ID:", ids[i], "Distance:", distance)
                    #self.show(distance)
                    return distance

            
        
    #show_webcam()
    cap.release()
    cv2.destroyAllWindows()