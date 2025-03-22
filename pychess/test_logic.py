import pytest


def test_chess_notation_to_indices():
    from logic.chess_logic import ChessLogic
    p = ChessLogic()

    assert p.chess_notation_to_indices("a5") == (3, 0)
    assert p.chess_notation_to_indices("a8") == (0, 0)
    assert p.chess_notation_to_indices("h1") == (7, 7)
    assert p.chess_notation_to_indices("b2") == (6, 1)
    assert p.chess_notation_to_indices("b1") == (7, 1)


def test_repr_and_str():
    from logic.chess_logic import ChessLogic
    p = ChessLogic()

    assert "K" in p.board.__str__()
    assert "k" in p.board.__str__()

    assert "Q" in p.board.__repr__()
    assert "q" in p.board.__repr__()


def test_index_to_move():
    from logic.chess_logic import ChessLogic
    p = ChessLogic()

    assert p.index_to_move(3, 0) == "a5"
    assert p.index_to_move(0, 0) == "a8"
    assert p.index_to_move(7, 7) == "h1"
    assert p.index_to_move(6, 1) == "b2"
    assert p.index_to_move(7, 1) == "b1"


def test_dir_increment_decrement():
    from logic.chess_logic import ChessLogic
    p = ChessLogic()

    assert p.dir_increment_decrement(1, 0) == -1
    assert p.dir_increment_decrement(0, 1) == 1
    assert p.dir_increment_decrement(2, 5) == 1


def test_is_pawn_moving_forward():
    from logic.chess_logic import ChessLogic
    p = ChessLogic()

    x, y = p.chess_notation_to_indices("b2") # White pawn
    # Move the pawn forward 1
    assert p.is_pawn_moving_forward(x, y, x - 1)

    x, y = p.chess_notation_to_indices("h2") # White pawn
    # Move the pawn forward 1
    assert p.is_pawn_moving_forward(x, y, x - 1)

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


def test_queen_movement_valid():
    from logic.chess_logic import ChessLogic
    p = ChessLogic()

    # Not the queen
    assert not p.queen_movement_valid("a6a4")

    # Move the pawn
    p.update_board("d2d3", False, False, False, False)

    p.update_board("d7d6", False, False, False, False)

    print(p.board)

    # assert p.queen_movement_valid("d1d2")  # TODO: THIS SHOULD WORK
    # assert p.queen_movement_valid("d7d6")  # TODO: THIS SHOULD WORK


def test_pawn_promotion_white():
    from logic.chess_logic import ChessLogic
    p = ChessLogic()

    # Remove the other pieces
    p.board[0] = [""] * 8
    p.board[1] = [""] * 8

    p.update_board("d2d4", False, False, False, False)
    p.update_board("d4d5", False, False, False, False)
    p.update_board("d5d6", False, False, False, False)
    p.update_board("d6d7", False, False, False, False)

    x, y = p.chess_notation_to_indices("d7")
    nx, ny = p.chess_notation_to_indices("d8")

    print(p.board)

    assert p.pawn_promotion(x, y, nx, ny)

def test_pawn_promotion_black():
    from logic.chess_logic import ChessLogic
    p = ChessLogic()

    # Remove the other pieces
    p.board[7] = [""] * 8
    p.board[6] = [""] * 8

    p.update_board("d7d5", False, False, False, False)
    p.update_board("d5d4", False, False, False, False)
    p.update_board("d4d3", False, False, False, False)
    p.update_board("d3d2", False, False, False, False)

    x, y = p.chess_notation_to_indices("d2")
    nx, ny = p.chess_notation_to_indices("d1")

    p.display_board()

    assert p.pawn_promotion(x, y, nx, ny)


def test_player_in_check():
    from logic.chess_logic import ChessLogic
    p = ChessLogic()

    # Remove line of pawns to put into check
    p.board[6] = [""] * 8
    p.board[1] = [""] * 8

    assert not p.player_in_check("e1")

    # Place a queen
    a, b = p.chess_notation_to_indices("e5")
    p.board[a][b] = "q"

    p.display_board()

    assert p.player_in_check("e1")  # TODO: THIS SHOULD WORK

def test_checkmate1():
    from logic.chess_logic import ChessLogic
    p = ChessLogic()

    p.board = [
			['', 'n', '', '', 'k', 'b', '', 'r'],
			['p', '', '', '', '', 'p', 'p', 'p'],
			['', '', '', '', 'q', '', '', ''],
			['', '', '', '', 'p', '', 'B', ''],
			['', '', '', '', 'P', '', '', ''],
			['', '', '', '', '', '', '', ''],
			['P', 'P', 'P', '', '', 'P', 'P', 'P'],
			['', '', 'K', 'R', '', '', '', ''],
    ]

    p.whoseTurn = False # Black's turn

    assert p.player_in_future_check("e8")


def test_checkmate2():
    from logic.chess_logic import ChessLogic
    p = ChessLogic()

    p.board = [
			['', '', '', '', '', '', '', ''],
			['', '', 'k', '', '', '', '', ''],
			['', '', '', '', '', '', '', ''],
			['', '', '', '', '', '', '', ''],
			['', '', '', '', '', '', '', 'Q'],
			['', '', '', '', '', '', '', ''],
			['', '', '', '', '', '', '', ''],
			['', 'R', '', 'R', '', '', 'K', ''],
    ]

    p.whoseTurn = False # Black's turn
    assert not p.player_in_future_check("c7")

    p.whoseTurn = True
    assert not p.player_in_future_check("g1")


def test_checkmate3():
    from logic.chess_logic import ChessLogic
    p = ChessLogic()

    p.board = [
			['', '', '', '', '', 'r', 'k', ''],
			['', '', '', '', '', 'p', '', 'p'],
			['', '', '', '', '', '', '', ''],
			['', '', '', '', '', '', '', ''],
			['', '', '', '', '', '', '', ''],
			['', '', '', '', '', '', '', ''],
			['', 'B', '', '', '', '', '', ''],
			['', '', '', '', '', '', 'R', 'K'],
    ]

    p.whoseTurn = True
    assert p.player_in_check("g8")
    assert p.player_in_future_check("g8")
    assert p.is_game_over() == tuple[True, False, False]


def test_play_move_single():
    from logic.chess_logic import ChessLogic
    p = ChessLogic()

    p.play_move("e2e4")
    assert p.board[4][4] == "P"
    assert p.board[6][4] == ""


def test_play_move_many():
    from logic.chess_logic import ChessLogic
    p = ChessLogic()

    p.play_move("e2e4")
    assert p.board[4][4] == "P"
    assert p.board[6][4] == ""

    p.play_move("d2d3")
    p.display_board()
    assert p.board[6][4] == " "  # This space should now be empty
    assert p.board[5][4] == "P"  # This space should have a pawn


def test_is_game_over():
    from logic.chess_logic import ChessLogic
    p = ChessLogic()

    assert p.is_game_over() == (False, False, False)  # No one should have won

    p.play_move("e2e4")
    assert p.board[4][4] == "P"
    assert p.board[6][4] == ""

    assert p.is_game_over() == (False, False, False)  # No one should have won


def test_castle_chess_notation():
    from logic.chess_logic import ChessLogic
    p = ChessLogic()

    # Check castle with bool
    assert p.chess_notation("e6e5", True, False, True, False, False) == "0-0"
    assert p.chess_notation("e6e5", True, False, False, True, False) == "0-0-0"

    assert p.chess_notation("e6e6", *([False] * 5)) == ""  # Check invalid


def test_update_king_position():
    from logic.chess_logic import ChessLogic
    p = ChessLogic()

    # TODO: update_king_position needs a comment about what it actually does

    p.update_king_position("e1")
    assert p.white_king_pos == "e1"

    p.update_king_position("e2")
    assert p.white_king_pos == "e1"  # Should this fail?

    p.update_king_position("e3")
    assert p.white_king_pos == "e1"  # Should this fail?


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

def test_en_passant():
    pass

def test_queenside_castling():
    pass

def test_kingside_castling():
    pass
