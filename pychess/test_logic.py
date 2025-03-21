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


def test_is_pawn_moving_forward():
    from logic.chess_logic import ChessLogic
    p = ChessLogic()

    x, y = p.chess_notation_to_indices("b2")
    # Move the pawn forward 1
    assert p.is_pawn_moving_forward(x, y, x + 1)

    x, y = p.chess_notation_to_indices("h2")
    # Move the pawn forward 1
    assert p.is_pawn_moving_forward(x, y, x + 1)

    with pytest.raises(AttributeError):
        # Pawn does not exist
        x, y = p.chess_notation_to_indices("b5")
        assert p.is_pawn_moving_forward(x, y, x + 1)

    with pytest.raises(AttributeError):
        # Pawn does not exist
        x, y = p.chess_notation_to_indices("b4")
        assert p.is_pawn_moving_forward(x, y, x + 1)


def test_opponent_piece_at_tile():
    from logic.chess_logic import ChessLogic
    p = ChessLogic()

    assert p.opponent_piece_at_tile("d7") == True
    assert p.opponent_piece_at_tile("d1") == False
    # Change the turn manually
    p.whoseTurn = False
    assert p.opponent_piece_at_tile("d7") == False
    assert p.opponent_piece_at_tile("d1") == True


def test_is_same_tile():
    from logic.chess_logic import ChessLogic
    p = ChessLogic()

    assert p.is_same_tile("b4b4")
    assert not p.is_same_tile("b4b5")

    assert not p.is_same_tile("a1b1")
    assert not p.is_same_tile("b4a1")

    assert p.is_same_tile("e5e5")


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
