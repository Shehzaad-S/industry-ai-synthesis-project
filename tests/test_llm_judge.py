from libs.llm import create_agent
""
import asyncio
from libs.token_tracker import TokenTracker
from libs.agents import IntentRouterAgent
import logging
from pydantic import BaseModel, Field


from libs.logging_config import get_logger
from libs.orchestrators import (
    AnalyticsOrchestrator
)

from tests.utils import (
    reset_test_environment,
)

from libs.state import (
    AnalyticsState
)
from libs.models import (
    AnalyticsFinding
)


logging.disable(logging.CRITICAL)

LLM_JUDGE_CASES = [
    {
        "question":
            "Which specials reduced waste most effectively?",

        "route":
            "operations_analytics",
    },

    {
        "question":
            "Which ingredients appeared most frequently in successful specials?",

        "route":
            "operations_analytics",
    },

    {
        "question":
            "How often are manager approvals rejected?",

        "route":
            "workflow_analytics",
    },

    {
        "question":
            "Why are workflows rejected?",

        "route":
            "workflow_analytics",
    },
]

# What will our LLM base judgments on??


class JudgeEvaluation(BaseModel):
    """
    Independent evaluation of response
    quality.
    """

    relevance: int = Field(
        ge=1,
        le=5,
    )

    correctness: int = Field(
        ge=1,
        le=5,
    )

    explainability: int = Field(
        ge=1,
        le=5,
    )

    reasoning: str

    relevance: int

    correctness: int

    explainability: int


# Our Judge
class LLMJudgeAgent:
    """
    Evaluates analytics response quality
    using an independent LLM judge.
    """

    SYSTEM_PROMPT = """
        You are an impartial evaluator.

        Evaluate the quality of an analytics
        response.

        Scoring Guide:

        5 = Excellent
        4 = Good
        3 = Acceptable
        2 = Weak
        1 = Poor

        Evaluate:

        1. Relevance
           - Did the response answer
             the question?

        2. Correctness
           - Are conclusions supported
             by findings and evidence?

        3. Explainability
           - Is the reasoning clearly
             communicated?

        Return a structured evaluation.
    """

    def __init__(
        self,
        token_tracker: TokenTracker,
    ) -> None:

        self.agent_name = (
            "LLMJudgeAgent"
        )

        self.judge_agent = create_agent(
            system_prompt=self.SYSTEM_PROMPT,
            result_type=JudgeEvaluation,
            agent_name=self.agent_name,
        )

        self.token_tracker = (
            token_tracker
        )

        self.logger = get_logger(
            self.agent_name
        )

    async def execute(
        self,
        question: str,
        summary: str,
        findings: list[AnalyticsFinding],
    ) -> JudgeEvaluation:

        findings_text = "\n".join(
            [
                f"- {finding.finding}"
                for finding in findings
            ]
        )

        prompt = f"""
            Question:

            {question}

            Analytics Summary:

            {summary}

            Findings:

            {findings_text}
            """
        # if logging active in future
        self.logger.info(
            "Evaluating analytics response."
        )

        self.logger.info(
            f"Question: {question}"
        )

        result = await (
            self.judge_agent.run(
                prompt
            )
        )

        self.token_tracker.update_from_run_usage(
            result.usage
        )
        self.logger.info(
            self.token_tracker.summary()
        )

        return result.output

# Tests for LLM heavy workflow (analytics workflow)


async def evaluate_llm_judge():
    """
    Evaluate analytics response quality
    using an independent LLM judge.
    """

    print(
        "\n====================================="
    )

    print(
        "LLM JUDGE EVALUATION"
    )

    print(
        "====================================="
    )

    reset_test_environment()

    token_tracker = TokenTracker()

    analytics_orchestrator = (
        AnalyticsOrchestrator(
            token_tracker
        )
    )

    judge = LLMJudgeAgent(
        token_tracker
    )

    total_cases = len(
        LLM_JUDGE_CASES
    )

    total_relevance = 0

    total_correctness = 0

    total_explainability = 0

    for index, case in enumerate(
        LLM_JUDGE_CASES,
        start=1,
    ):

        analytics_state = AnalyticsState(
            session_id=(
                f"judge-{index}"
            ),
            original_question=(
                case["question"]
            ),
            current_question=(
                case["question"]
            ),
            analytics_route=(
                case["route"]
            ),
        )

        analytics_state = await (
            analytics_orchestrator.run(
                analytics_state
            )
        )

        response = (
            analytics_state
            .analytics_response
        )

        assert (
            response is not None
        ), (
            "Analytics response missing."
        )

        evaluation = await (
            judge.execute(
                question=(
                    case["question"]
                ),
                summary=(
                    response.summary
                ),
                findings=(
                    response.findings
                ),
            )
        )

        total_relevance += (
            evaluation.relevance
        )

        total_correctness += (
            evaluation.correctness
        )

        total_explainability += (
            evaluation.explainability
        )

        print(
            f"\nCASE {index}"
        )

        print(
            f"Question:\n"
            f"{case['question']}"
        )

        print(
            f"\nRelevance: "
            f"{evaluation.relevance}/5"
        )

        print(
            f"Correctness: "
            f"{evaluation.correctness}/5"
        )

        print(
            f"Explainability: "
            f"{evaluation.explainability}/5"
        )

        print(
            f"\nReasoning:\n"
            f"{evaluation.reasoning}"
        )

        print(
            "\n-------------------------------------"
        )

    avg_relevance = (
        total_relevance
        / total_cases
    )

    avg_correctness = (
        total_correctness
        / total_cases
    )

    avg_explainability = (
        total_explainability
        / total_cases
    )

    print(
        "\n====================================="
    )

    print(
        "LLM JUDGE SUMMARY"
    )

    print(
        "====================================="
    )

    print(
        f"Cases Evaluated: "
        f"{total_cases}"
    )

    print(
        f"\nAverage Relevance: "
        f"{avg_relevance:.2f}/5"
    )

    print(
        f"Average Correctness: "
        f"{avg_correctness:.2f}/5"
    )

    print(
        f"Average Explainability: "
        f"{avg_explainability:.2f}/5"
    )

    assert (
        avg_relevance >= 4.0
    ), (
        "Average relevance below threshold."
    )

    assert (
        avg_correctness >= 4.0
    ), (
        "Average correctness below threshold."
    )

    assert (
        avg_explainability >= 4.0
    ), (
        "Average explainability below threshold."
    )

    print(
        "\nPASS"
    )


if __name__ == "__main__":
    asyncio.run(
        evaluate_llm_judge()
    )
