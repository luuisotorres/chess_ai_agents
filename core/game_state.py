"""
Initializes and manages game-level variables inside st.session_state.
"""

import streamlit as st
import chess
from config.settings import SVG_SIZE


def init_game_state() -> None:
    """
    Initializes the game state in Streamlit's session state.
    """
    defaults = {
        "board": chess.Board(),
        "move_history": [],
        "made_move": False,
        "max_turns": SVG_SIZE
    }
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)


def reset_game_state() -> None:
    """
    Resets the game state in Streamlit's session state.
    """
    st.session_state.board.reset()
    st.session_state.move_history.clear()
    st.session_state.made_move = False
