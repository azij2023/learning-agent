# src/state.py
class AgentState:
    def __init__(self):
        self.checkpoints = []
        self.checkpoint_index = 0
        self.context_raw = ""
        self.context_processed = None
        self.explanation = ""
        self.questions = []
        self.messages = []

        # NEW: learner answers + verification score
        self.learner_answers = []   # list of answers from learner
        self.verification_score = None
        self.feynman_required = False
