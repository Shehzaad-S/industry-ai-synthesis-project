"""Test for Context Management"""
import asyncio
from libs.token_tracker import TokenTracker
from libs.agents import IntentRouterAgent
import logging

from libs.orchestrators import (
    AnalyticsOrchestrator
)

from tests.utils import (
    reset_test_environment,
)

from libs.state import (
    AnalyticsState
)


logging.disable(logging.CRITICAL)

# Evalutate our session persistance and context management (so importatant to our design)


async def evaluate_context_management():
    """
    Evaluate analytics session persistence
    and context accumulation across multiple
    investigative questions.
    """

    print(
        "\n====================================="
    )

    print(
        "CONTEXT MANAGEMENT EVALUATION"
    )

    print(
        "====================================="
    )

    reset_test_environment()

    token_tracker = TokenTracker()

    orchestrator = (
        AnalyticsOrchestrator(
            token_tracker
        )
    )

    #
    # Question 1
    #

    state = AnalyticsState(
        session_id="evaluation-session",
        original_question=(
            "Which specials reduced waste "
            "most effectively?"
        ),
        current_question=(
            "Which specials reduced waste "
            "most effectively?"
        ),
        analytics_route=(
            "operations_analytics"
        ),
    )

    state = await (
        orchestrator.run(
            state
        )
    )

    findings_after_q1 = len(
        state.findings
    )

    print(
        "\nQUESTION 1"
    )

    print(
        state.current_question
    )

    print(
        f"Session ID: "
        f"{state.session_id}"
    )

    print(
        f"Findings Stored: "
        f"{findings_after_q1}"
    )

    #
    # Question 2
    #

    state.current_question = (
        "Which of those specials "
        "generated the most profit?"
    )

    state.analytics_route = (
        "operations_analytics"
    )

    state = await (
        orchestrator.run(
            state
        )
    )

    findings_after_q2 = len(
        state.findings
    )

    print(
        "\nQUESTION 2"
    )

    print(
        state.current_question
    )

    print(
        f"Session ID: "
        f"{state.session_id}"
    )

    print(
        f"Findings Stored: "
        f"{findings_after_q2}"
    )

    #
    # Question 3
    #

    state.current_question = (
        "How often are manager "
        "approvals rejected?"
    )

    state.analytics_route = (
        "workflow_analytics"
    )

    state = await (
        orchestrator.run(
            state
        )
    )

    findings_after_q3 = len(
        state.findings
    )

    print(
        "\nQUESTION 3"
    )

    print(
        state.current_question
    )

    print(
        f"Session ID: "
        f"{state.session_id}"
    )

    print(
        f"Findings Stored: "
        f"{findings_after_q3}"
    )

    #
    # Assertions
    #

    assert (
        state.session_id
        == "evaluation-session"
    ), (
        "Session ID changed unexpectedly."
    )

    assert (
        findings_after_q2
        > findings_after_q1
    ), (
        "Findings did not accumulate "
        "after Question 2."
    )

    assert (
        findings_after_q3
        > findings_after_q2
    ), (
        "Findings did not accumulate "
        "after Question 3."
    )

    assert (
        state.original_question
        ==
        "Which specials reduced waste "
        "most effectively?"
    ), (
        "Original investigation was not "
        "preserved."
    )

    assert (
        state.analytics_response
        is not None
    ), (
        "Final analytics response missing."
    )

    print(
        "\n-------------------------------------"
    )

    print(
        "ORIGINAL INVESTIGATION:"
    )

    print(
        state.original_question
    )

    print(
        "\nPASS"
    )

    return state

if __name__ == "__main__":

    asyncio.run(
        evaluate_context_management()
    )
