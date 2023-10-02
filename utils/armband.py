import mindrove
from mindrove.data_filter import DataFilter, FilterTypes, AggOperations
from mindrove.board_shim import (
    BoardShim,
    MindRoveInputParams,
    BoardIds,
    MindRoveError
)


def init():
    ####      INIT BOARD        #######
    BoardShim.enable_dev_board_logger()
    params = MindRoveInputParams()
    board_id = BoardIds.MINDROVE_WIFI_BOARD.value    
    board = BoardShim(board_id, params)
    board.prepare_session()

    try:
        board.stop_stream()
        board.release_session()
    except:
        ...


    sample_rate = board.get_sampling_rate(board_id)
    n_channels = 8

    print("Device ready (sampling rate: {}hz)".format(sample_rate))
    return board
