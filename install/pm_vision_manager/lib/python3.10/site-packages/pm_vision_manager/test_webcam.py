import cv2
print('Testing UGREEN Camera...')

# Try both video devices
for i in [0, 1]:
    print(f'Testing /dev/video{i}...')
    cap = cv2.VideoCapture(i, cv2.CAP_V4L2)
    if cap.isOpened():
        print(f'  ✓ /dev/video{i} opened successfully')
        
        # Set some reasonable properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        # Try to read a frame
        ret, frame = cap.read()
        if ret and frame is not None:
            print(f'  ✓ SUCCESS: Frame captured! Shape: {frame.shape}')
            print(f'  ✓ Camera is WORKING!')
        else:
            print(f'  ✗ Camera opened but no frame captured')
        
        cap.release()
    else:
        print(f'  ✗ Cannot open /dev/video{i}')