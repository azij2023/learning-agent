# src/runnables.py
from langchain_core.runnables import RunnableLambda
from src.nodes.define_checkpoint import define_checkpoint
from src.nodes.gather_context import gather_context
from src.nodes.validate_context import validate_context
from src.nodes.context_processor import context_processor
from src.nodes.topic_explainer import topic_explainer   # NEW
from src.nodes.question_generator import question_generator
from src.nodes.verifier import verifier
from src.nodes.logic import conditional_logic

# Wrap each node
define = RunnableLambda(define_checkpoint)
gather = RunnableLambda(gather_context)
validate = RunnableLambda(validate_context)
process = RunnableLambda(context_processor)
explain = RunnableLambda(topic_explainer)              # NEW
generate = RunnableLambda(question_generator)
verify = RunnableLambda(lambda state: verifier(state, [
    "Probability is the measure of likelihood of events.",
    "Events can be independent or mutually exclusive in probability theory."
]))
logic = RunnableLambda(conditional_logic)

# Sequence the pipeline
agent_pipeline = (
    define
    .pipe(gather)
    .pipe(validate)
    .pipe(process)
    .pipe(explain)     # teach first
    .pipe(generate)    # then test
    .pipe(verify) 
    .pipe(logic) 
)