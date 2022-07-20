import brainflow
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations
from brainflow.board_shim import (
    BoardShim,
    BrainFlowInputParams,
    BoardIds,
    BrainFlowError,
)


def init():
    ####      INIT BOARD        #######
    BoardShim.enable_dev_board_logger()
    params = BrainFlowInputParams()
    board = BoardShim(BoardIds.MINDROVE_WIFI_BOARD, params)

    try:
        board.stop_stream()
        board.release_session()
    except:
        ...

    board.prepare_session()
    sample_rate = board.get_sampling_rate(16)
    n_channels = 6

    print("Device ready (sampling rate: {}hz)".format(sample_rate))
    return board
