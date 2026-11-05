"""Test workflows"""
import asyncio
from libs.token_tracker import TokenTracker
from libs.agents import (
    SalesIntakeAgent,
)
from libs.orchestrators import (
    InventoryOrchestrator,
    AnalyticsOrchestrator
)

from tests.utils import (
    reset_test_environment,
    auto_approve,
    RejectThenApprove,
)

from libs.state import (
    WorkflowState,
    AnalyticsState
)

import logging

logging.disable(logging.CRITICAL)


async def evaluate_inventory_workflow_completion():
    """
    Evaluate successful completion of the
    Inventory Workflow using automatic
    approval.
    """

    print(
        "\n====================================="
    )

    print(
        "INVENTORY WORKFLOW EVALUATION"
    )

    print(
        "====================================="
    )

    reset_test_environment()

    token_tracker = TokenTracker()

    sales_text = """
    Today we sold:

    - 4 Margherita Pizzas
    - 3 Alfredo Pastas
    - 6 Spaghetti Bolognese
    """

    sales_agent = SalesIntakeAgent(
        token_tracker
    )

    orchestrator = (
        InventoryOrchestrator(
            token_tracker,
            approval_function=auto_approve,
        )
    )

    sales_report = await (
        sales_agent.execute(
            sales_text
        )
    )

    state = WorkflowState(
        sales_report=sales_report
    )

    response = await (
        orchestrator.run(
            state
        )
    )

    print(
        "\nWORKFLOW STATUS:"
    )

    print(
        response.status
    )

    print(
        "\nFINAL ACTIONS:"
    )

    for action in (
        response.final_actions
    ):
        print(
            f"- {action}"
        )

    #
    # Evaluation Assertions
    #

    assert (
        response.status
        == "completed"
    ), (
        "Workflow did not complete."
    )

    assert (
        response.manager_decision
        is not None
    ), (
        "Manager decision missing."
    )

    assert (
        response.manager_decision.approved
        is True
    ), (
        "Expected approval."
    )

    assert (
        len(
            response.final_actions
        ) > 0
    ), (
        "Expected at least one executed action."
    )

    print(
        "\nPASS"
    )

    return response


# Retry Logic for Inventory Workflow

async def evaluate_inventory_workflow_retry():
    """
    Evaluate workflow retry behaviour.

    Validates that manager rejection
    triggers the retry path and that the
    workflow eventually completes after
    approval.
    """

    print(
        "\n====================================="
    )

    print(
        "INVENTORY RETRY EVALUATION"
    )

    print(
        "====================================="
    )

    reset_test_environment()

    token_tracker = TokenTracker()

    sales_text = """
    Today we sold:

    - 4 Margherita Pizzas
    - 3 Alfredo Pastas
    - 6 Spaghetti Bolognese
    """

    sales_agent = SalesIntakeAgent(
        token_tracker
    )

    approval_strategy = (
        RejectThenApprove()
    )

    orchestrator = (
        InventoryOrchestrator(
            token_tracker,
            approval_function=approval_strategy,
        )
    )

    sales_report = await (
        sales_agent.execute(
            sales_text
        )
    )

    state = WorkflowState(
        sales_report=sales_report,
    )

    response = await (
        orchestrator.run(
            state
        )
    )

    print(
        "\nWORKFLOW STATUS:"
    )

    print(
        response.status
    )

    print(
        "\nMANAGER APPROVAL CALLS:"
    )

    print(
        approval_strategy.calls
    )

    print(
        "\nFINAL ACTIONS:"
    )

    for action in response.final_actions:

        print(
            f"- {action}"
        )

    #
    # Evaluation Assertions
    #

    assert (
        approval_strategy.calls == 2
    ), (
        "Expected one rejection "
        "followed by approval."
    )

    assert (
        response.status
        == "completed"
    ), (
        "Workflow failed to complete."
    )

    assert (
        response.manager_decision
        is not None
    ), (
        "Manager decision missing."
    )

    assert (
        response.manager_decision.approved
        is True
    ), (
        "Expected final approval."
    )

    assert (
        len(
            response.final_actions
        ) > 0
    ), (
        "Expected executed actions."
    )

    print(
        "\nPASS"
    )

    return response

# Test Analytics Workflow


async def evaluate_operations_analytics_workflow():
    """
    Evaluate successful execution of the
    Operations Analytics Workflow.
    """

    print(
        "\n====================================="
    )

    print(
        "OPERATIONS ANALYTICS EVALUATION"
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

    response_state = await (
        orchestrator.run(
            state
        )
    )

    response = (
        response_state.analytics_response
    )

    print(
        "\nWORKFLOW STATUS:"
    )

    print(
        response_state.workflow_status
    )

    print(
        "\nFINDINGS GENERATED:"
    )

    print(
        len(response.findings)
    )

    print(
        "\nSUMMARY:"
    )

    print(
        response.summary
    )

    #
    # Evaluation Assertions
    #

    assert (
        response_state.workflow_status
        == "completed"
    ), (
        "Workflow did not complete."
    )

    assert (
        response is not None
    ), (
        "No analytics response generated."
    )

    assert (
        len(response.findings) > 0
    ), (
        "Expected at least one finding."
    )

    assert (
        len(response_state.findings) > 0
    ), (
        "Expected persisted findings."
    )

    assert (
        response.summary
    ), (
        "Expected summary output."
    )

    print(
        "\nPASS"
    )

    return response_state


# Test Analytics Workflow
async def evaluate_workflow_analytics_workflow():
    """
    Evaluate successful execution of the
    Workflow Analytics Workflow.
    """

    print(
        "\n====================================="
    )

    print(
        "WORKFLOW ANALYTICS EVALUATION"
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

    state = AnalyticsState(
        session_id="evaluation-session",
        original_question=(
            "How often are manager "
            "approvals rejected?"
        ),
        current_question=(
            "How often are manager "
            "approvals rejected?"
        ),
        analytics_route=(
            "workflow_analytics"
        ),
    )

    response_state = await (
        orchestrator.run(
            state
        )
    )

    response = (
        response_state.analytics_response
    )

    print(
        "\nWORKFLOW STATUS:"
    )

    print(
        response_state.workflow_status
    )

    print(
        "\nFINDINGS GENERATED:"
    )

    print(
        len(response.findings)
    )

    print(
        "\nSUMMARY:"
    )

    print(
        response.summary
    )

    #
    # Evaluation Assertions
    #

    assert (
        response_state.workflow_status
        == "completed"
    ), (
        "Workflow did not complete."
    )

    assert (
        response is not None
    ), (
        "No analytics response generated."
    )

    assert (
        len(response.findings) > 0
    ), (
        "Expected at least one finding."
    )

    assert (
        len(response_state.findings) > 0
    ), (
        "Expected persisted findings."
    )

    assert (
        response.summary
    ), (
        "Expected summary output."
    )

    print(
        "\nPASS"
    )

    return response_state

if __name__ == "__main__":
    asyncio.run(
        evaluate_workflow_analytics_workflow()
    )
