import pytest


def test_chess_notation_to_indices():
    from logic.chess_logic import ChessLogic
    p = ChessLogic()

    assert p.chess_notation_to_indices("a5") == (3, 0)
    assert p.chess_notation_to_indices("a8") == (0, 0)
    assert p.chess_notation_to_indices("h1") == (7, 7)
    assert p.chess_notation_to_indices("b2") == (6, 1)
    assert p.chess_notation_to_indices("b1") == (7, 1)


def test_dir_increment_decrement():
    from logic.chess_logic import ChessLogic
    p = ChessLogic()

    assert p.dir_increment_decrement(1, 0) == -1
    assert p.dir_increment_decrement(0, 1) == 1
    assert p.dir_increment_decrement(2, 5) == 1


def test_moving_piece():
    pass

def test_not_moving_piece(): # click on piece and click again on same piece (no moving)
    pass

def test_capture_piece():
    # first commit to this
    pass

def test_blocked_move(): # attempting to move onto tile that has same color piece already
    pass

def test_win_cases(): # result field key: empty-in progress, w-white win, b-black win, d-draw
    pass

def test_stalemate(): # draw
    pass

def test_legal_moves(): # for all pieces, reset board between each test
    pass

def test_illegal_moves(): # for all pieces, reset board between each test
    pass

def test_moving_into_checK(): # shouldn't be possible
    pass

def test_initialize_board(): # ensure all pieces present and in the right spot
    pass

def test_check_conditions():
    pass

def test_checkmate_conditions():
    pass

def test_pawn_promotion():
    pass

def test_en_passant():
    pass

def test_queenside_castling():
    pass

def test_kingside_castling():
    pass
