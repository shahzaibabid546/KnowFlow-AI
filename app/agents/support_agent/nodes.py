
from app.agents.support_agent.state import SupportAgentState


# Node 1: Validate Customer Question
def validate_question(state: SupportAgentState) -> dict:

    question = state.get("question", "")

    if not question or not question.strip():
        return {
            "answer": "Please provide a valid question.",
            "answer_status": "invalid",
            "needs_human": False,
            "escalation_reason": ""
        }

    return {
        "answer_status": "pending",
        "needs_human": False,
        "escalation_reason": ""
    }


# Node 2: Generate Answer Using RAG Service
def generate_answer(
    state: SupportAgentState,
    rag_service
) -> dict:

    question = state["question"]

    result = rag_service.generate_answer(question)

    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "answer_status": "pending"
    }


# Node 3: Evaluate Generated Answer
def evaluate_answer(state: SupportAgentState) -> dict:

    answer = state.get("answer", "")

    if not answer or not answer.strip():
        return {
            "answer_status": "unsatisfactory"
        }

    if "could not find relevant information" in answer.lower():
        return {
            "answer_status": "unsatisfactory"
        }

    if "do not have enough information" in answer.lower():
        return {
            "answer_status": "unsatisfactory"
        }

    return {
        "answer_status": "satisfactory"
    }


# Node 4: Prepare for Another Attempt
def prepare_retry(state: SupportAgentState) -> dict:

    return {
        "retry_count": state.get("retry_count", 0) + 1,
        "answer": "",
        "sources": [],
        "answer_status": "pending"
    }


# Node 5: Escalate to Human Support
def escalate_to_human(state: SupportAgentState) -> dict:

    return {
        "needs_human": True,
        "answer_status": "escalated",
        "escalation_reason": (
            "The AI assistant could not generate "
            "a satisfactory answer after the allowed attempts."
        )
    }
