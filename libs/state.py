"""

Workflow state models used by the Inventory
Orchestrator Agent and Analytics Orchestrator Agent.

This module represents the shared session states
that persists throughout a workflow execution.
"""

from typing import Literal

from pydantic import BaseModel, Field

from libs.manager_input import ManagerDecision

from libs.models import (
    SalesReport,
    InventoryAssessment,
    ReorderRecommendation,
    MenuRecommendation,
    CriticReview,
    WorkflowMetrics,
    AnalyticsFinding,
    AnalyticsResponse,
)


class WorkflowState(BaseModel):
    """
    Shared workflow state managed by the
    Inventory Orchestrator Agent.

    This object acts as the working memory
    for the entire workflow execution.
    """

    current_step: Literal[
        "START",
        "SALES_INTAKE",
        "INVENTORY_ANALYSIS",
        "REORDER_RECOMMENDATION",
        "MENU_RECOMMENDATION",
        "CRITIC_REVIEW",
        "CRITIC_RETRY",
        "MANAGER_APPROVAL",
        "MANAGER_RETRY",
        "EXECUTE_UPDATES",
        "FINALIZE",
        "REJECT",
        "COMPLETE",
        "ERROR",
    ] = "START"

    workflow_status: Literal[
        "running",
        "completed",
        "rejected",
        "error",
    ] = "running"

    # Sales Processing

    sales_report: SalesReport | None = None

    # Inventory Analysis

    inventory_assessment: InventoryAssessment | None = None

    # Recommendations

    reorder_recommendations: list[
        ReorderRecommendation
    ] = Field(default_factory=list)

    menu_recommendations: list[
        MenuRecommendation
    ] = Field(default_factory=list)

    # Critic Review

    critic_review: CriticReview | None = None
    critic_retry_count: int = 0

    # Human Approval

    manager_decision: ManagerDecision | None = None
    manager_retry_count: int = 0

    # Final Workflow Output

    final_actions: list[str] = Field(
        default_factory=list
    )

    summary: str | None = None

    # Metrics

    metrics: WorkflowMetrics = Field(
        default_factory=WorkflowMetrics
    )

# ---------------------------------------------------------------------
# Analytics State


class AnalyticsState(BaseModel):
    """
    Shared analytics state managed by the
    Analytics Orchestrator.
    """

    current_step: Literal[
        "START",
        "ROUTE",
        "OPERATIONS_ANALYTICS",
        "WORKFLOW_ANALYTICS",
        "FINALIZE",
        "COMPLETE",
        "ERROR",
    ] = "START"

    workflow_status: Literal[
        "running",
        "completed",
        "error",
    ] = "running"

    session_id: str

    original_question: str

    current_question: str

    findings: list[AnalyticsFinding] = Field(
        default_factory=list
    )

    analytics_response: AnalyticsResponse | None = None

    analytics_route: Literal[
        "operations_analytics",
        "workflow_analytics",
    ]

    metrics: WorkflowMetrics = Field(
        default_factory=WorkflowMetrics
    )
