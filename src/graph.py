from collections.abc import Callable
from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph

from src.nodes.context_processor import context_processor
from src.nodes.define_checkpoint import define_checkpoint
from src.nodes.feynman import feynman_node
from src.nodes.gather_context import gather_context
from src.nodes.logic import conditional_logic
from src.nodes.question_generator import question_generator
from src.nodes.topic_explainer import topic_explainer
from src.nodes.validate_context import validate_context
from src.nodes.verifier import verifier
from src.state import AgentState


class LearningGraphState(TypedDict):
    agent_state: AgentState
    action: Literal["generate", "score"]


def _adapt_node(
    node: Callable[[AgentState], AgentState],
) -> Callable[[LearningGraphState], dict[str, AgentState]]:
    def run(graph_state: LearningGraphState) -> dict[str, AgentState]:
        return {"agent_state": node(graph_state["agent_state"])}

    return run


def _route_action(graph_state: LearningGraphState) -> Literal["generate", "score"]:
    action = graph_state["action"]
    return action


def _route_after_scoring(graph_state: LearningGraphState) -> str:
    return (
        "remediate"
        if graph_state["agent_state"].feynman_required
        else "complete"
    )


def build_graph():
    graph = StateGraph(LearningGraphState)
    graph.add_node("define_checkpoint", _adapt_node(define_checkpoint))
    graph.add_node("gather_context", _adapt_node(gather_context))
    graph.add_node("validate_context", _adapt_node(validate_context))
    graph.add_node("process_context", _adapt_node(context_processor))
    graph.add_node("explain_topic", _adapt_node(topic_explainer))
    graph.add_node("generate_questions", _adapt_node(question_generator))
    graph.add_node("verify_answers", _adapt_node(verifier))
    graph.add_node("decide_progression", _adapt_node(conditional_logic))
    graph.add_node("feynman_explanation", _adapt_node(feynman_node))

    graph.add_conditional_edges(
        START,
        _route_action,
        {"generate": "define_checkpoint", "score": "verify_answers"},
    )
    graph.add_edge("define_checkpoint", "gather_context")
    graph.add_edge("gather_context", "validate_context")
    graph.add_edge("validate_context", "process_context")
    graph.add_edge("process_context", "explain_topic")
    graph.add_edge("explain_topic", "generate_questions")
    graph.add_edge("generate_questions", END)
    graph.add_edge("verify_answers", "decide_progression")
    graph.add_conditional_edges(
        "decide_progression",
        _route_after_scoring,
        {"remediate": "feynman_explanation", "complete": END},
    )
    graph.add_edge("feynman_explanation", END)

    return graph.compile()


learning_graph = build_graph()
