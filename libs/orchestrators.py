"""Script for system Orchestrators"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any, Literal

from libs.logging_config import get_logger
from libs.state import WorkflowState, AnalyticsState
from libs.state_machine import (
    EntryPoint,
    StateMachine,
    Step,
    Termination
)

from libs.models import (
    OrchestratorResponse,
    AnalyticsResponse,
)
from libs.llm import create_agent

from libs.state import WorkflowState, AnalyticsState
from libs.token_tracker import TokenTracker

from libs.tools import (
    get_sales_history,
    get_special_performance,
    get_menu_specials,
    get_manager_decisions,
    get_workflow_runs,
)
from libs.manager_input import get_manager_approval

from libs.agents import (
    InventoryOperationsAgent,
    ReorderAgent,
    MenuStrategyAgent,
    CriticAgent,
    WorkflowAnalyticsAgent,
    OperationsAnalyticsAgent,
    IntentRouterAgent,
)

logger = get_logger(__name__)


# <<<<<<<<<<<<<<<Orchestration Agents>>>>>>>>>>>>>> -------


class InventoryOrchestrator:

    MAX_RETRIES = 3

    def __init__(
            self,
            token_tracker: TokenTracker,
            approval_function=get_manager_approval):

        self.logger = get_logger(
            self.__class__.__name__
        )

        self.approval_function = approval_function

        self.token_tracker = token_tracker

        self.inventory_agent = (
            InventoryOperationsAgent(
                self.token_tracker
            )
        )

        self.reorder_agent = (
            ReorderAgent(
                self.token_tracker
            )
        )

        self.menu_agent = (
            MenuStrategyAgent(
                self.token_tracker
            )
        )

        self.critic_agent = (
            CriticAgent(
                self.token_tracker
            )
        )

        self.workflow = (
            self._build_workflow()
        )

    async def _inventory_analysis_step(
        self,
        state: WorkflowState,
    ) -> dict:
        """
        Execute inventory analysis.

        Args:
            state:
                Current workflow state.

        Returns:
            Workflow state updates.
        """

        assessment = (
            await self.inventory_agent.execute(
                state
            )
        )

        return {
            "inventory_assessment": assessment,
        }

    async def _reorder_step(
        self,
        state: WorkflowState,
    ) -> dict:
        """
        Generate reorder recommendations.
        """

        recommendations = (
            await self.reorder_agent.execute(
                state
            )
        )

        return {
            "reorder_recommendations":
                recommendations,
        }

    async def _menu_step(
        self,
        state: WorkflowState,
    ) -> dict:
        """
        Generate menu recommendations.
        """

        recommendation = (
            await self.menu_agent.execute(
                state
            )
        )

        return {
            "menu_recommendations": [
                recommendation
            ],
        }

    async def _critic_step(
        self,
        state: WorkflowState,
    ) -> dict:
        """
        Review workflow recommendations.
        """

        review = (
            await self.critic_agent.execute(
                state
            )
        )

        return {
            "critic_review": review,
        }

    def _manager_approval_step(
        self,
        state: WorkflowState,
    ) -> dict:
        """
        Request manager approval.
        """

        self.logger.info(
            "Awaiting manager approval."
        )

        #
        # Reorder Recommendations
        #

        self.logger.info(
            "\n=== REORDER RECOMMENDATIONS ==="
        )

        print(
            "\n=== REORDER RECOMMENDATIONS ==="
        )

        for recommendation in (
            state.reorder_recommendations
        ):

            recommendation_text = f"""
            Ingredient    : {recommendation.ingredient_name}
            Quantity      : {recommendation.reorder_quantity} kg
            Vendor        : {recommendation.recommended_vendor}
            Total Cost    : ${recommendation.total_cost:.2f}

            Justification:
            {recommendation.justification}
            """

            self.logger.info(
                recommendation_text
            )

            print(
                recommendation_text
            )

        if not state.reorder_recommendations:
            print("No reorder actions required")

        #
        # Menu Recommendations
        #

        self.logger.info(
            "\n=== MENU RECOMMENDATIONS ==="
        )

        print(
            "\n=== MENU RECOMMENDATIONS ==="
        )

        for recommendation in (
            state.menu_recommendations
        ):

            recommendation_text = f"""
            Special Name:
            {recommendation.special_name}

            Ingredients Used:
            {', '.join(recommendation.ingredients_used)}

            Reasoning:
            {recommendation.reasoning}
            """

            self.logger.info(
                recommendation_text
            )

            print(
                recommendation_text
            )
        if not state.menu_recommendations:
            print("No menu strategy actions required")

        #
        # Critic Review
        #

        if state.critic_review:

            critic_text = f"""
            === CRITIC REVIEW ===

            Approved:
            {state.critic_review.approved}

            Confidence Score:
            {state.critic_review.confidence_score:.2f}

            Feedback:
            {state.critic_review.feedback}
            """

            self.logger.info(
                critic_text
            )

            print(
                critic_text
            )

        #
        # Manager Decision
        #

        decision = (
            self.approval_function()
        )

        self.logger.info(
            f"Manager approval result: "
            f"{decision.approved}"
        )

        return {
            "manager_decision": decision,
        }

    async def _execute_updates_step(
        self,
        state: WorkflowState,
    ) -> dict:
        """
        Execute approved workflow actions.
        """

        actions: list[str] = []

        for recommendation in (
            state.reorder_recommendations
        ):

            result = (
                await self.inventory_agent.replenish(
                    ingredient_name=recommendation.ingredient_name,
                    quantity=recommendation.reorder_quantity,
                )
            )

            actions.append(result)

        for recommendation in (
            state.menu_recommendations
        ):

            result = (
                await self.inventory_agent.add_special(
                    recommendation
                )
            )

            actions.append(result)

        return {
            "final_actions": actions
        }

    def _is_inventory_healthy(
        self,
        state: WorkflowState,
    ) -> str:
        """
        Determine whether additional workflow
        processing is required.
        """

        assessment = state.inventory_assessment

        if (
            assessment
            and assessment.inventory_healthy
        ):
            return "FINALIZE"

        return "REORDER_RECOMMENDATION"

    def _is_critic_approved(
        self,
        state: WorkflowState,
    ) -> str:
        """
        Route workflow based on critic review.
        """

        review = state.critic_review

        if review is None:
            return "REJECT"

        if review.approved:
            return "MANAGER_APPROVAL"

        if (
            state.critic_retry_count
            < self.MAX_RETRIES
        ):
            return "CRITIC_RETRY"

        return "REJECT"

    def _is_manager_approved(
        self,
        state: WorkflowState,
    ) -> str:
        """
        Route workflow based on manager decision.
        """

        decision = state.manager_decision

        if decision is None:
            return "REJECT"

        if decision.approved:
            return "EXECUTE_UPDATES"

        if (
            state.manager_retry_count
            < self.MAX_RETRIES
        ):
            return "MANAGER_RETRY"

        return "REJECT"

    def _critic_retry_step(
        self,
        state: WorkflowState,
    ) -> dict:

        return {
            "critic_retry_count":
                state.critic_retry_count + 1
        }

    def _manager_retry_step(
        self,
        state: WorkflowState,
    ) -> dict:

        return {
            "manager_retry_count":
                state.manager_retry_count + 1
        }

    def _reject_workflow_step(
        self,
        state: WorkflowState,
    ) -> dict:
        """
        Record workflow rejection details and
        produce a final rejection summary.
        """

        if (
            state.critic_review is not None
            and not state.critic_review.approved
        ):
            return {
                "workflow_status": "rejected",
                "summary": (
                    "Workflow rejected after "
                    f"{state.critic_retry_count} critic retries. "
                    f"Final critic feedback: "
                    f"{state.critic_review.feedback}"
                ),
            }

        if (
            state.manager_decision is not None
            and not state.manager_decision.approved
        ):
            return {
                "workflow_status": "rejected",
                "summary": (
                    "Workflow rejected after "
                    f"{state.manager_retry_count} manager retries. "
                    f"Final manager feedback: "
                    f"{state.manager_decision.feedback}"
                ),
            }

        return {
            "workflow_status": "rejected",
            "summary": "Workflow rejected.",
        }

    def _finalize_step(
        self,
        state: WorkflowState,
    ) -> dict:
        """
        Produce the final workflow summary.
        """

        return {
            "workflow_status": "completed",
            "summary": (
                f"Workflow completed successfully. "
                f"Executed {len(state.final_actions)} actions. "
                f"Agents Invoked: "
                f"{', '.join(state.metrics.agents_invoked)}."
            ),
        }

    def _build_workflow(
        self,
    ) -> StateMachine[WorkflowState]:
        """
        Build and configure the inventory
        management workflow.
        """

        workflow = StateMachine(
            WorkflowState
        )

        # Entry / Exit

        entry = EntryPoint()

        termination = Termination()

        # Core Steps

        inventory_analysis = Step(
            "INVENTORY_ANALYSIS",
            self._inventory_analysis_step,
        )

        reorder_recommendation = Step(
            "REORDER_RECOMMENDATION",
            self._reorder_step,
        )

        menu_recommendation = Step(
            "MENU_RECOMMENDATION",
            self._menu_step,
        )

        critic_review = Step(
            "CRITIC_REVIEW",
            self._critic_step,
        )

        critic_retry = Step(
            "CRITIC_RETRY",
            self._critic_retry_step,
        )

        manager_approval = Step(
            "MANAGER_APPROVAL",
            self._manager_approval_step,
        )

        manager_retry = Step(
            "MANAGER_RETRY",
            self._manager_retry_step,
        )

        execute_updates = Step(
            "EXECUTE_UPDATES",
            self._execute_updates_step,
        )

        finalize = Step(
            "FINALIZE",
            self._finalize_step,
        )

        reject = Step(
            "REJECT",
            self._reject_workflow_step,
        )

        workflow.add_steps(
            [
                entry,
                inventory_analysis,
                reorder_recommendation,
                menu_recommendation,
                critic_review,
                critic_retry,
                manager_approval,
                manager_retry,
                execute_updates,
                finalize,
                reject,
                termination,
            ]
        )

        #
        # Entry
        #

        workflow.connect(
            entry,
            inventory_analysis,
        )

        #
        # Inventory Analysis
        #

        workflow.connect(
            inventory_analysis,
            [
                finalize,
                reorder_recommendation,
            ],
            self._is_inventory_healthy,
        )

        #
        # Recommendation Pipeline
        #

        workflow.connect(
            reorder_recommendation,
            menu_recommendation,
        )

        workflow.connect(
            menu_recommendation,
            critic_review,
        )

        #
        # Critic Review
        #

        workflow.connect(
            critic_review,
            [
                manager_approval,
                critic_retry,
                reject,
            ],
            self._is_critic_approved,
        )

        workflow.connect(
            critic_retry,
            reorder_recommendation,
        )

        #
        # Manager Approval
        #

        workflow.connect(
            manager_approval,
            [
                execute_updates,
                manager_retry,
                reject,
            ],
            self._is_manager_approved,
        )

        workflow.connect(
            manager_retry,
            reorder_recommendation,
        )

        #
        # Successful Completion
        #

        workflow.connect(
            execute_updates,
            finalize,
        )

        workflow.connect(
            finalize,
            termination,
        )

        #
        # Rejected Workflow
        #

        workflow.connect(
            reject,
            termination,
        )

        return workflow

    async def run(
        self,
        initial_state: WorkflowState,
    ) -> OrchestratorResponse:
        """
        Execute the inventory workflow.

        Args:
            initial_state:
                Starting workflow state.

        Returns:
            Final orchestrator response.
        """

        self.logger.info(
            "Starting inventory workflow."
        )
        # Keep token usage in sync from first LLM interaction (Sales Intake)
        initial_state.metrics.token_usage = (
            self.token_tracker.usage
        )

        run = await self.workflow.run(
            initial_state
        )

        final_state = run.get_final_state()

        if final_state is None:
            raise RuntimeError(
                "Workflow completed without a final state."
            )

        inventory_healthy = (
            final_state.inventory_assessment.inventory_healthy

            if final_state.inventory_assessment

            else False
        )

        self.logger.info(
            f"Workflow completed with status: "
            f"{final_state.workflow_status}"
        )

        return OrchestratorResponse(
            status=final_state.workflow_status,
            inventory_healthy=inventory_healthy,
            summary=final_state.summary or "",
            reorder_recommendations=(
                final_state.reorder_recommendations
            ),
            menu_recommendations=(
                final_state.menu_recommendations
            ),
            critic_review=(
                final_state.critic_review
            ),
            manager_decision=(
                final_state.manager_decision
            ),
            final_actions=(
                final_state.final_actions
            ),
            metrics=(
                final_state.metrics
            ),
        )


class AnalyticsOrchestrator:

    def __init__(
        self,
        token_tracker: TokenTracker,
    ) -> None:

        self.logger = get_logger(
            self.__class__.__name__
        )

        self.token_tracker = (
            token_tracker
        )

        self.operations_agent = (
            OperationsAnalyticsAgent(
                self.token_tracker
            )
        )

        self.workflow_agent = (
            WorkflowAnalyticsAgent(
                self.token_tracker
            )
        )

        self.workflow = (
            self._build_workflow()
        )

    def _route_step(
        self,
        state: AnalyticsState,
    ) -> dict:
        """
        Log and validate the analytics route
        selected by the Intent Router.
        """

        self.logger.info(
            f"Analytics route selected: "
            f"{state.analytics_route}"
        )

        self.logger.info(
            f"Current question: "
            f"{state.current_question}"
        )

        return {}

    # Conditional Logic for Transition
    def _route_to_agent(
        self,
        state: AnalyticsState,
    ) -> str:
        """
        Route analytics workflow execution to
        the appropriate specialist agent.
        """

        if (
            state.analytics_route
            == "operations_analytics"
        ):
            return "OPERATIONS_ANALYTICS"

        return "WORKFLOW_ANALYTICS"

    async def _operations_analytics_step(
        self,
        state: AnalyticsState,
    ) -> dict:
        """
        Execute operations analytics workflow.
        """

        self.logger.info(
            "Executing Operations Analytics Agent."
        )

        response = await (
            self.operations_agent.execute(
                state
            )
        )

        return {
            "analytics_response": response,
        }

    async def _workflow_analytics_step(
        self,
        state: AnalyticsState,
    ) -> dict:
        """
        Execute workflow analytics workflow.
        """

        self.logger.info(
            "Executing Workflow Analytics Agent."
        )

        response = await (
            self.workflow_agent.execute(
                state
            )
        )

        return {
            "analytics_response": response,
        }

    def _finalize_step(
        self,
        state: AnalyticsState,
    ) -> dict:
        """
        Persist findings generated during the
        analytics workflow and finalize the run.
        """

        if state.analytics_response is None:

            self.logger.error(
                "Analytics workflow completed "
                "without an analytics response."
            )

            return {
                "workflow_status": "error",
            }

        persisted_findings = [
            *state.findings,
            *state.analytics_response.findings,
        ]

        self.logger.info(
            f"Persisted "
            f"{len(state.analytics_response.findings)} "
            f"new findings."
        )

        return {
            "workflow_status": "completed",
            "findings": persisted_findings,
        }

    def _build_workflow(
        self,
    ) -> StateMachine[AnalyticsState]:
        """
        Build and configure the analytics
        workflow.
        """

        workflow = StateMachine(
            AnalyticsState
        )

        #
        # Entry / Exit
        #

        entry = EntryPoint()

        termination = Termination()

        #
        # Core Steps
        #

        route = Step(
            "ROUTE",
            self._route_step,
        )

        operations_analytics = Step(
            "OPERATIONS_ANALYTICS",
            self._operations_analytics_step,
        )

        workflow_analytics = Step(
            "WORKFLOW_ANALYTICS",
            self._workflow_analytics_step,
        )

        finalize = Step(
            "FINALIZE",
            self._finalize_step,
        )

        workflow.add_steps(
            [
                entry,
                route,
                operations_analytics,
                workflow_analytics,
                finalize,
                termination,
            ]
        )

        #
        # Entry
        #

        workflow.connect(
            entry,
            route,
        )

        #
        # Route
        #

        workflow.connect(
            route,
            [
                operations_analytics,
                workflow_analytics,
            ],
            self._route_to_agent,
        )

        #
        # Specialist Agents
        #

        workflow.connect(
            operations_analytics,
            finalize,
        )

        workflow.connect(
            workflow_analytics,
            finalize,
        )

        #
        # Completion
        #

        workflow.connect(
            finalize,
            termination,
        )

        return workflow

    async def run(
        self,
        initial_state: AnalyticsState,
    ) -> AnalyticsState:
        """
        Execute the analytics workflow.

        Args:
            initial_state:
                Starting analytics state.

        Returns:
            AnalyticsResponse generated by the
            appropriate analytics agent.
        """

        self.logger.info(
            "Starting analytics workflow."
        )

        initial_state.metrics.token_usage = (
            self.token_tracker.usage
        )

        run = await self.workflow.run(
            initial_state
        )

        final_state = (
            run.get_final_state()
        )

        if final_state is None:

            raise RuntimeError(
                "Workflow completed without a final state."
            )

        if (
            final_state.analytics_response
            is None
        ):

            raise RuntimeError(
                "Workflow completed without an "
                "analytics response."
            )

        self.logger.info(
            f"Analytics workflow completed "
            f"with status: "
            f"{final_state.workflow_status}"
        )

        self.logger.info(
            f"Persisted findings count: "
            f"{len(final_state.findings)}"
        )

        return (
            final_state
        )
