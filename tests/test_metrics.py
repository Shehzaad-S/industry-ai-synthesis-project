"""Metrics Analysis (Token Usage and Time complexity) """

import asyncio
from libs.token_tracker import TokenTracker
from libs.agents import SalesIntakeAgent
import logging
import io
from contextlib import redirect_stdout

from libs.logging_config import get_logger
from libs.orchestrators import (
    AnalyticsOrchestrator,
    InventoryOrchestrator,
)

from tests.utils import (
    reset_test_environment,
    auto_approve,
)

from libs.state import (
    AnalyticsState,
    WorkflowState,
)

logging.disable(logging.CRITICAL)


async def evaluate_metrics() -> None:
    """
    Collect representative token usage and
    cost metrics for each workflow.
    """

    print(
        "\n====================================="
    )

    print(
        "PERFORMANCE ANALYSIS"
    )

    print(
        "====================================="
    )

    reset_test_environment()

    #
    # Inventory Workflow
    #

    inventory_tracker = TokenTracker()

    sales_agent = SalesIntakeAgent(
        inventory_tracker
    )

    inventory_orchestrator = (
        InventoryOrchestrator(
            inventory_tracker,
            approval_function=auto_approve,
        )
    )

    buffer = io.StringIO()
    # Supress summaries for test purposes
    with redirect_stdout(buffer):

        sales_report = await (
            sales_agent.execute(
                """
                Today we sold:

                - 4 Margherita Pizzas
                - 3 Alfredo Pastas
                - 6 Spaghetti Bolognese
                """
            )
        )

        inventory_response = await (
            inventory_orchestrator.run(
                WorkflowState(
                    sales_report=sales_report
                )
            )
        )

    #
    # Operations Analytics
    #

    operations_tracker = TokenTracker()

    analytics_orchestrator = (
        AnalyticsOrchestrator(
            operations_tracker
        )
    )

    operations_state = AnalyticsState(
        session_id="operations-eval",
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

    await analytics_orchestrator.run(
        operations_state
    )

    #
    # Workflow Analytics
    #

    workflow_tracker = TokenTracker()

    analytics_orchestrator = (
        AnalyticsOrchestrator(
            workflow_tracker
        )
    )

    workflow_state = AnalyticsState(
        session_id="workflow-eval",
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

    await analytics_orchestrator.run(
        workflow_state
    )

    #
    # Results
    #

    print(
        "\nInventory Workflow"
    )

    print(
        f"Total Tokens: "
        f"{inventory_tracker.usage.total_tokens}"
    )

    print(
        f"Estimated Cost: "
        f"${inventory_tracker.usage.estimated_cost:.5f}"
    )

    print(
        "\nOperations Analytics"
    )

    print(
        f"Total Tokens: "
        f"{operations_tracker.usage.total_tokens}"
    )

    print(
        f"Estimated Cost: "
        f"${operations_tracker.usage.estimated_cost:.5f}"
    )

    print(
        "\nWorkflow Analytics"
    )

    print(
        f"Total Tokens: "
        f"{workflow_tracker.usage.total_tokens}"
    )

    print(
        f"Estimated Cost: "
        f"${workflow_tracker.usage.estimated_cost:.5f}"
    )

if __name__ == "__main__":

    asyncio.run(
        evaluate_metrics()
    )
