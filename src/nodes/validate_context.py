def validate_context(state):
    cp = state.checkpoints[state.checkpoint_index]

    text = state.context_raw or ""
    objectives = cp.get("objectives", [])

    hits = sum(1 for obj in objectives if obj.lower() in text)
    score = hits / len(objectives) if objectives else 0

    state.relevance_score = score
    state.messages.append(f"ValidateContext: score={score:.2f}")
    return state
