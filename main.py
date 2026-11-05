import asyncio
import random
import uuid
import io
from contextlib import redirect_stdout

from libs.agents import (
    IntentRouterAgent,
    SalesIntakeAgent,
)
from tests.utils import reset_test_environment

from libs.orchestrators import (
    InventoryOrchestrator,
    AnalyticsOrchestrator,
)
from libs.logging_config import configure_logging

from libs.state import (
    WorkflowState,
    AnalyticsState,
)

from libs.token_tracker import (
    TokenTracker,
)

# Demo Inputs
INVENTORY_DEMOS = [
    """
    Today we sold:

    5 Margherita Pizzas
    3 Alfredo Pastas
    2 Pest Penne
    """,

    """
    Shift Report:

    8 Pepperoni Pizzas
    4 Spaghetti Bolognese
    3 Vegetarian Pizzas
    """
]

OPERATIONS_ANALYTICS_DEMOS = [
    "Which specials reduced waste most effectively?",

    "What menu specials generated the highest profit?",

    "Which ingredients appeared most frequently in successful specials?"
]

WORKFLOW_ANALYTICS_DEMOS = [
    "Why are workflows rejected?",

    "Which workflow consumes the most tokens?",

    "How often are manager approvals rejected?"
]

ALL_DEMOS = (
    INVENTORY_DEMOS
    + OPERATIONS_ANALYTICS_DEMOS
    + WORKFLOW_ANALYTICS_DEMOS
)

# Menu for runner


def display_menu() -> None:

    print(
        """
        =========================================
        Please Choose an Option :)
        =========================================

        1. Random Demo

        2. Inventory Workflow Demo

        3. Operations Analytics Demo

        4. Workflow Analytics Demo

        5. Custom Input

        6. Exit

        =========================================
        """
    )


def get_user_input() -> str | None:
    """
    Retrieve reviewer-selected input.

    Returns:
        User input text or None if the user
        chooses to exit.
    """

    display_menu()

    choice = input(
        "Select an option: "
    ).strip()

    if choice == "1":

        user_input = random.choice(
            ALL_DEMOS
        )

        print(
            "\n=== RANDOM DEMO SELECTED ==="
        )

        print(user_input)

        return user_input

    if choice == "2":

        user_input = random.choice(
            INVENTORY_DEMOS
        )

        print(
            "\n=== INVENTORY DEMO ==="
        )

        print(user_input)

        return user_input

    if choice == "3":

        user_input = random.choice(
            OPERATIONS_ANALYTICS_DEMOS
        )

        print(
            "\n=== OPERATIONS ANALYTICS DEMO ==="
        )

        print(user_input)

        return user_input

    if choice == "4":

        user_input = random.choice(
            WORKFLOW_ANALYTICS_DEMOS
        )

        print(
            "\n=== WORKFLOW ANALYTICS DEMO ==="
        )

        print(user_input)

        return user_input

    if choice == "5":

        return input(
            "\nEnter your request: "
        ).strip()

    if choice == "6":

        return None

    print(
        "\nInvalid selection."
    )

    return get_user_input()


# Create shared classes
token_tracker = TokenTracker()

intent_router = IntentRouterAgent(
    token_tracker
)

sales_intake_agent = SalesIntakeAgent(
    token_tracker
)

inventory_orchestrator = (
    InventoryOrchestrator(
        token_tracker
    )
)

analytics_orchestrator = (
    AnalyticsOrchestrator(
        token_tracker
    )
)

analytics_session_state: (
    AnalyticsState | None
) = None


async def process_user_input(
    user_input: str,
) -> None:
    """
    Route user input and dispatch the
    appropriate workflow.
    """
    global analytics_session_state

    route = await intent_router.execute(
        user_input
    )

    print(
        "\n========================================="
    )

    print(
        "INTENT ROUTER RESULT"
    )

    print(
        "========================================="
    )

    print(
        f"Route: {route.route}"
    )

    print(
        f"Reasoning: {route.reasoning}"
    )
    if route.requires_retry:

        print(
            "\nRequest could not be processed."
        )

        print(
            f"Reason: {route.reasoning}"
        )

        print(
            "\nPlease provide a valid sales "
            "report or analytics question."
        )

        print(
            "\n========================================="
        )

        print(
            "WORKFLOW COMPLETE"
        )

        print(
            "========================================="
        )

        return

    if route.route == (
        "inventory_workflow"
    ):

        sales_report = await (
            sales_intake_agent.execute(
                user_input
            )
        )

        workflow_state = WorkflowState(
            sales_report=sales_report
        )

        response = await (
            inventory_orchestrator.run(
                workflow_state
            )
        )

        print(
            "\n========================================="
        )

        print(
            "INVENTORY WORKFLOW RESULT"
        )

        print(
            "========================================="
        )

        print(
            f"Status: {response.status}"
        )

        print(
            f"Inventory Healthy: "
            f"{response.inventory_healthy}"
        )

        print(
            f"Summary:\n"
            f"{response.summary}"
        )

        if response.final_actions:

            print(
                "\nEXECUTED ACTIONS"
            )

            for action in response.final_actions:

                print(
                    f"\n- {action}"
                )

        print(
            "\n========================================="
        )

        print(
            "WORKFLOW COMPLETE"
        )

        print(
            "========================================="
        )

        return

    elif route.route in {
        "operations_analytics",
        "workflow_analytics",
    }:

        if analytics_session_state is None:

            analytics_session_state = (
                AnalyticsState(
                    session_id=str(
                        uuid.uuid4()
                    ),
                    original_question=user_input,
                    current_question=user_input,
                    analytics_route=route.route,
                )
            )

        else:

            print(
                "\nReusing analytics session..."
            )

            analytics_session_state.current_question = (
                user_input
            )

            analytics_session_state.analytics_route = (
                route.route
            )
        # Run the orchestrator with relevant state
        analytics_session_state = await (
            analytics_orchestrator.run(
                analytics_session_state
            )
        )

        response = (
            analytics_session_state
            .analytics_response
        )

        print(
            "\n========================================="
        )

        print(
            "ANALYTICS WORKFLOW RESULT"
        )

        print(
            "========================================="
        )

        print(
            f"\nSUMMARY\n"
            f"{response.summary}"
        )

        print(
            "\nFINDINGS"
        )

        for finding in response.findings:

            print(
                f"\n- {finding.finding}"
            )

            print(
                f"  Source: "
                f"{finding.evidence_source}"
            )

            print(
                f"  Confidence: "
                f"{finding.confidence_score:.2f}"
            )

        if response.recommendations:

            print(
                "\nRECOMMENDATIONS"
            )

            for recommendation in (
                response.recommendations
            ):
                print(
                    f"\n- {recommendation}"
                )
        print(
            f"\nSession ID: "
            f"{analytics_session_state.session_id}"
        )

        print(
            f"Total Findings Stored: "
            f"{len(analytics_session_state.findings)}"
        )

        print(
            "\n========================================="
        )

        print(
            "WORKFLOW COMPLETE"
        )

        print(
            "========================================="
        )

        return


async def main() -> None:

    print(
        "\n========================================="
    )

    print(
        "Restaurant Intelligence Platform"
    )

    print(
        "========================================="
    )

    while True:

        user_input = (
            get_user_input()
        )

        if user_input is None:

            print(
                "\nExiting application."
            )

            break

        await process_user_input(
            user_input
        )

if __name__ == "__main__":

    configure_logging()

    buffer = io.StringIO()

    try:
        # suppress print statements for DB reset
        with redirect_stdout(buffer):
            reset_test_environment()

    except Exception as e:

        print(
            f"CRITICAL ERROR: "
            f"Environment reset failed! {e}"
        )

        print(
            "\nCaptured Output before crash:"
        )

        print(
            buffer.getvalue()
        )

        raise

    print(
        ">>>>>Database reset to evaluation state.<<<<<<"
    )

    asyncio.run(
        main()
    )
