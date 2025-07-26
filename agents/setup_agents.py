"""
Utility helpers to build AutoGen agents and run a game
"""

from typing import Dict
import streamlit as st
from autogen import ConversableAgent, register_function
from agents.functions import available_moves, execute_move
from config.settings import DEFAULT_MODEL


def _termination_checker(_msg) -> bool:
    """
    Tell GameMaster when to yield:
    True when a move was applied.
    """
    made = st.session_state.made_move
    st.session_state.made_move = False
    return made


def initialize_agents() -> Dict[str, ConversableAgent]:
    """
    Creates Whit, Black, and GameMaster agents
    and register tools
    """
    api_key = st.session_state.openai_api_key
    model_cfg = {"config_list": [{"model": DEFAULT_MODEL,
                                  "api_key": api_key}]}

    agent_white = ConversableAgent(
        name="Agent_White",
        system_message=(
            "You are a professional chess player (white pieces). "
            "Call available_moves() first; then execute_move(move)."
        ),
        llm_config=model_cfg,
    )

    agent_black = ConversableAgent(
        name="Agent_Black",
        system_message=(
            "You are a professional chess player (black pieces). "
            "Call available_moves() first; then execute_move(move)."
        ),
        llm_config=model_cfg,
    )

    game_master = ConversableAgent(
        name="GameMaster",
        llm_config=False,
        is_termination_msg=_termination_checker,
        default_auto_reply="Waiting for a move…",
        human_input_mode="NEVER",
    )

    for agent in (agent_white, agent_black):
        register_function(
            available_moves,
            caller=agent,
            executor=game_master,
            name="available_moves",
            description="Returns a list of all legal UCI moves."
        )
        register_function(
            execute_move,
            caller=agent,
            executor=game_master,
            name="execute_move",
            description="Executes a UCI move."
        )

    agent_white.register_nested_chats(
        trigger=agent_black,
        chat_queue=[{"sender": game_master, "recipient": agent_white}]
    )
    agent_black.register_nested_chats(
        trigger=agent_white,
        chat_queue=[{"sender": game_master, "recipient": agent_black}]
    )

    return {"white": agent_white, "black": agent_black, "gm": game_master}


def play_game(agents: Dict[str, ConversableAgent]):
    """
    Kick off the conversation loop. Black sends first message to White
    so White makes the opening move.
    """
    return agents["black"].initiate_chat(
        recipient=agents["white"],
        message="Your move.",
        max_turns=st.session_state.max_turns,
        summary_method="reflection_with_llm",
    )
