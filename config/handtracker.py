settings = {
    # VIDEO SETTINGS
    # 'window_resolution' : (1280, 720),
    'window_resolution' : (1920, 1080),
    'device_id' : 0, # 0 for webcam, 1 for external camera

    #GESTURES
    "classes": ["Rest", "Left", "Right", "Fist"],

    #DETECTION SETTINGS
    'static_mode' : False,
    'max_hands' : 1,
    'model_complexity' : 1,
    'detection_confidence' : 0.5,
    'tracking_confidence' : 0.5,

    #RECORD SETTINGS
    'record_time' : 20,
    'rest_time' : 3
}