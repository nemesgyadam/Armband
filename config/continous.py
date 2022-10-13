settings = {
    "data_path": "train_data",
    "signal_length": 1,
    "save_location": "data",
    "targets": ['Distance', 'Degree'],
    "normalize_range": [-10000, 10000],
    "input_length": 500,  # AKA resampleTO
    "sampler": "overlap",  #"random" | "overlap"
    "overlap": 400,
    "batch_size": 200
}
