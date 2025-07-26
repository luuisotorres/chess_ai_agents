"""
Streamlit front-end for the Chess-AutoGen demo.

Runs with:  streamlit run app.py
"""

from __future__ import annotations
import streamlit as st
import chess.svg
from config.settings import DEFAULT_MAX_TURNS, SVG_SIZE
from core.game_state import init_game_state, reset_game_state
from agents.setup_agents import initialize_agents, play_game

init_game_state()

st.sidebar.title("🔑  OpenAI & Game Settings")

api_key = st.sidebar.text_input("OpenAI API key", type="password")
if api_key:
    st.session_state.openai_api_key = api_key
else:
    st.sidebar.warning("⚠️ Please enter your OpenAI API key to start playing!")

max_turns = st.sidebar.number_input(
    "Max half-moves (turns)", value=DEFAULT_MAX_TURNS,
    min_value=1, max_value=1000
)
st.session_state.max_turns = max_turns

st.sidebar.info(
    "⚠️ A full chess game may exceed 200 half-moves and burn credits. "
    "For demos stick to ~10."
)

st.title("♟️  AutoGen Agents Play Chess")

# Add instructions for the user
st.info(
    "🎮 **How to use:**\n"
    "1. Enter your OpenAI API key in the sidebar\n"
    "2. Click '▶️ Start Game' to begin\n"
    "3. **Watch the live game progress in your terminal/console** - "
    "agents will discuss moves in real-time\n"
    "4. After the game ends, review each move in the history below"
)

svg_board = chess.svg.board(st.session_state.board, size=SVG_SIZE)
st.image(svg_board)

col1, col2 = st.columns(2)
with col1:
    if st.button("▶️  Start Game", disabled=not api_key):
        spinner_msg = ("🤖 Agents are playing... "
                       "Check your terminal for live updates!")
        with st.spinner(spinner_msg):
            reset_game_state()
            agents = initialize_agents()
            chat_result = play_game(agents)
        st.success("🎉 Game finished! Review the moves below:")
        st.markdown(chat_result.summary)

        st.subheader("📋 Move History")
        st.info("Each move shows the board state after that move was played.")
        for idx, svg in enumerate(st.session_state.move_history):
            actor = "White" if idx % 2 == 0 else "Black"
            st.caption(f"Move {idx+1} by **{actor}**")
            st.image(svg)

with col2:
    if st.button("🔄  Reset Board"):
        reset_game_state()
        st.info("✅ Board reset! Press **Start Game** to play a new match.")
