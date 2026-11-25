# LangGraph support-agent workflow will be implemented here.

from langgraph.graph import StateGraph, START, END

from app.agents.support_agent.state import SupportAgentState

from app.agents.support_agent.nodes import (
    validate_question,
    generate_answer,
    evaluate_answer,
    prepare_retry,
    escalate_to_human
)


# Create Support Agent Graph
def create_support_agent(rag_service):

    # Initialize StateGraph
    workflow = StateGraph(SupportAgentState)

    # Register Nodes
    workflow.add_node(
        "validate_question",
        validate_question
    )

    workflow.add_node(
        "generate_answer",
        lambda state: generate_answer(state, rag_service)
    )

    workflow.add_node(
        "evaluate_answer",
        evaluate_answer
    )

    workflow.add_node(
        "prepare_retry",
        prepare_retry
    )

    workflow.add_node(
        "escalate_to_human",
        escalate_to_human
    )

    # Define Starting Point
    workflow.add_edge(
        START,
        "validate_question"
    )

    # Validate Question Routing
    def route_after_validation(state: SupportAgentState):

        if state.get("answer_status") == "invalid":
            return "end"

        return "generate_answer"

    workflow.add_conditional_edges(
        "validate_question",
        route_after_validation,
        {
            "generate_answer": "generate_answer",
            "end": END
        }
    )

    # Generate Answer -> Evaluate Answer
    workflow.add_edge(
        "generate_answer",
        "evaluate_answer"
    )

    # Evaluate Answer Routing
    def route_after_evaluation(state: SupportAgentState):

        if state.get("answer_status") == "satisfactory":
            return "end"

        if state.get("retry_count", 0) < state.get("max_retries", 2):
            return "retry"

        return "escalate"

    workflow.add_conditional_edges(
        "evaluate_answer",
        route_after_evaluation,
        {
            "end": END,
            "retry": "prepare_retry",
            "escalate": "escalate_to_human"
        }
    )

    # Retry -> Generate Answer Again
    workflow.add_edge(
        "prepare_retry",
        "generate_answer"
    )

    # Escalation -> End
    workflow.add_edge(
        "escalate_to_human",
        END
    )

    # Compile Graph
    support_agent = workflow.compile()

    return support_agent
