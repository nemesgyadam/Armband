import cv2

def format_frame(frame, process_shape, image_rotation):
    frame = cv2.resize(frame,process_shape )
    if image_rotation == 90:
        frame = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)
    if image_rotation == 180:
        frame = cv2.rotate(frame, cv2.cv2.ROTATE_180)
    if image_rotation == 270:
        frame = cv2.rotate(frame, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
    return frame