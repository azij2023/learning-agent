# src/nodes/define_checkpoint.py
from src.state import AgentState

def define_checkpoint(state: AgentState) -> AgentState:
    idx = state.checkpoint_index
    cp = state.checkpoints[idx]
    state.messages.append(f"DefineCheckpoint: idx={idx}, topic={cp.topic}")
    return state
