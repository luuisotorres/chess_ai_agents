"""
Functions for managing chess moves in a Streamlit application.
"""

from __future__ import annotations
import streamlit as st
import chess
import chess.svg
from config.settings import SVG_SIZE


def available_moves() -> str:
    """
    Returns a comma-separated list of all legal UCI moves.
    """
    board: chess.Board = st.session_state.board
    return ', '.join(str(m) for m in board.legal_moves)


def execute_move(move: str) -> str:
    """
    Push *move* onto the board if legal, update history SVG,
    flip 'made_move' flag so GameMaster yields control.

    Args:
        move (str): The UCI move to execute.
    Returns:
        Human-readable description of what happened (or error message).
    """
    board: chess.Board = st.session_state.board
    try:
        move_obj = chess.Move.from_uci(move)
    except ValueError:
        return f"❌ Invalid UCI string: {move}"

    if move_obj not in board.legal_moves:
        return f"🚫 Illegal move: {move}"

    board.push(move_obj)
    st.session_state.made_move = True

    svg = chess.svg.board(
        board,
        arrows=[
            (
                move_obj.from_square,
                move_obj.to_square,
            )
        ],
        size=SVG_SIZE
    )
    st.session_state.move_history.append(svg)

    piece = board.piece_at(move_obj.to_square)
    desc = (
        f"✅ Moved {piece.symbol()} from "
        f"{chess.square_name(move_obj.from_square)} to "
        f"{chess.square_name(move_obj.to_square)}"
    )
    if board.is_checkmate():
        desc += " - Checkmate! Game over 💀"
    elif board.is_stalemate():
        desc += " - Stalemate! Game over 🤝"
    elif board.is_check():
        desc += " - Check! ⚠️"
    return desc
