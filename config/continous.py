settings = {
    "data_path": "train_data",
    "signal_length": 1,
    "save_location": "data",
    "targets": ['Distance', 'Degree'],
    "normalize_range": [-10000, 10000],
    "input_length": 1000,  # AKA resampleTO
    "sampler": "overlap",  #"random" | "overlap"
    "overlap": 400,
    "batch_size": 200,
     # Contorl
    "thresholds": {"gas": 0.5, "left": 0.3,"right":0.7},
}
