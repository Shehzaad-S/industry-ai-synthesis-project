"""TEST UTILITY FUNCTIONS"""


from data.db_setup import (
    reset_database,
    seed_all,
)
from libs.models import ManagerDecision


# We want to reset the DBs before we run each workflow test
def reset_test_environment() -> None:
    """
    Reset the database to a known state before
    workflow evaluation.
    """

    reset_database()
    seed_all()

    print(
        "Test Environment reset and seeded successfully."
    )

# Avoid user input here


def auto_approve() -> ManagerDecision:
    """
    Automatically approve recommendations.
    """

    return ManagerDecision(
        approved=True,
        feedback="Auto-approved for testing.",
    )


class RejectThenApprove:
    """
    Reject the first approval request and
    approve the second to validate workflow
    retry behavior.
    """

    def __init__(self):
        self.calls = 0

    def __call__(
        self,
    ) -> ManagerDecision:

        self.calls += 1

        if self.calls == 1:

            return ManagerDecision(
                approved=False,
                feedback=(
                    "Automatically rejected "
                    "for testing."
                ),
            )

        return ManagerDecision(
            approved=True,
            feedback=(
                "Automatically approved "
                "for testing."
            ),
        )
