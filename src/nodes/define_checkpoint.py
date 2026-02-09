def define_checkpoint(state):
    idx = state.checkpoint_index
    cp = state.checkpoints[idx]

    # Ensure required keys exist
    cp.setdefault("topic", "Unknown")
    cp.setdefault("objectives", [])
    cp.setdefault("context", "")

    state.messages.append(
        f"DefineCheckpoint: idx={idx}, topic={cp.get('topic', 'Unknown')}"
    )
    return state
