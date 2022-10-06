settings = {
    # VIDEO SETTINGS
    #"stream_url": "http://192.168.0.107:4747/video",
    #"stream_url": "resources/fist.mp4",
    #"stream_url": "resources/all_moves.mp4",
    "stream_url": 0,
    "process_shape": (400, 225),
    "image_rotation": 90, 
    
    # PALM ANGLE SETTINGS
    #"black_upper_limit" : 20,
    "black_upper_limit" : 30,
    "gauss_blur" : 5,
    "dilate_kernel" : 3,
    "dilate_iterations" : 3,
     
    "angle_method" : "box", # "box" or "PCA"
    
    # PALM ANGLE KALMAN SETTINGS
    "angle_dt" : 1.,
    "angle_u" : 2,
    "angle_std_acc" : 100,     
    "angle_std_meas" : 90,     

    # 2D KALMAN SETTINGS
    "dt" : 10.,
    "u_x" : 200,
    "u_y" : 100,
    "std_acc" : 100,     
    "x_std_meas" : 90,    
    "y_std_meas" : 90,

    # FIST SETTINGS
    # old
    # "green_limit_low": (20, 30, 30),
    # "green_limit_high": (70,255,255),
    "green_limit_low": (10, 100, 100),
    "green_limit_high": (100,255,255),
}