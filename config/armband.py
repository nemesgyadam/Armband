settings = {
    "data_path": "data",
    "signal_length": 2,
    "save_location": "data",
    "classes": ["Rest", "Left", "Right", "Fist"],
    "normalize_range": [-10000, 10000],
    "input_length": 1000,  # AKA resampleTO
    "patient_threshold": 50, # kb 2 sec
    # Contorl
    #"thresholds": {"gas": 0.5, "left": -0.3,"right":0.7},
    "thresholds": {"gas": 0.9, "left": -0.9,"right":0.9},
    "move_thresholds": {"gas": 60, "left": 80,"right":80},
    "steps": 100 # Steps to wait in ros-step target
}
