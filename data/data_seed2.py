"""Script to generate analytics data"""

from datetime import date, timedelta
import random


def generate_sales_history() -> list[dict]:
    """Generate the synthetic Sales History Data"""

    random.seed(42)

    sales_history = []

    seasons = [
        ("2025-01-01", 30, "winter"),
        ("2025-07-01", 30, "summer")
    ]

    for start_date_str, days, season in seasons:

        start_date = date.fromisoformat(start_date_str)

        for day_offset in range(days):

            current_date = start_date + timedelta(days=day_offset)

            weekend = current_date.weekday() >= 4

            daily_sales = {

                "Pepperoni Pizza":
                    random.randint(25, 35) if weekend
                    else random.randint(18, 25),

                "Margherita Pizza":
                    random.randint(22, 30) if season == "summer" and weekend
                    else random.randint(16, 24) if season == "summer"
                    else random.randint(10, 15),

                "Vegetarian Pizza":
                    random.randint(20, 28) if season == "summer" and weekend
                    else random.randint(14, 22) if season == "summer"
                    else random.randint(8, 12),

                "Alfredo Pasta":
                    random.randint(18, 25) if season == "winter" and weekend
                    else random.randint(12, 18) if season == "winter"
                    else random.randint(7, 12),

                "Spaghetti Bolognese":
                    random.randint(20, 28) if season == "winter" and weekend
                    else random.randint(14, 20) if season == "winter"
                    else random.randint(8, 12),

                "Pesto Penne":
                    random.randint(14, 20) if season == "summer" and weekend
                    else random.randint(10, 15) if season == "summer"
                    else random.randint(5, 8),
            }

            for menu_item, quantity_sold in daily_sales.items():

                sales_history.append(
                    {
                        "sale_date": current_date.isoformat(),
                        "menu_item": menu_item,
                        "quantity_sold": quantity_sold
                    }
                )

    return sales_history


SALES_HISTORY_DATA = generate_sales_history()

# --------------------------------------------------------


def generate_menu_specials() -> list:
    """Generate synthetic historical menu specials."""

    return [
        {
            "special_name": "Mozzarella Madness",
            "start_date": "2025-01-05",
            "end_date": "2025-01-11",
            "ingredients_used": "Mozzarella,Basil",
            "reason": "Waste Reduction",
            "active": 0
        },
        {
            "special_name": "Comfort Pasta Week",
            "start_date": "2025-01-10",
            "end_date": "2025-01-16",
            "ingredients_used": "Penne,Alfredo Sauce,Parmesan",
            "reason": "Seasonal Promotion",
            "active": 0
        },
        {
            "special_name": "Bolognese Bonanza",
            "start_date": "2025-01-15",
            "end_date": "2025-01-21",
            "ingredients_used": "Ground Beef,Spaghetti",
            "reason": "Seasonal Promotion",
            "active": 0
        },
        {
            "special_name": "Fresh Herb Feast",
            "start_date": "2025-01-20",
            "end_date": "2025-01-26",
            "ingredients_used": "Basil,Tomato Sauce",
            "reason": "Waste Reduction",
            "active": 0
        },
        {
            "special_name": "Pizza Lovers Week",
            "start_date": "2025-01-25",
            "end_date": "2025-01-31",
            "ingredients_used": "Mozzarella,Pepperoni",
            "reason": "Inventory Surplus",
            "active": 0
        },
        {
            "special_name": "Garden Fresh Pizza",
            "start_date": "2025-07-03",
            "end_date": "2025-07-09",
            "ingredients_used": "Bell Peppers,Mushrooms,Onions",
            "reason": "Seasonal Promotion",
            "active": 0
        },
        {
            "special_name": "Summer Pesto Special",
            "start_date": "2025-07-08",
            "end_date": "2025-07-14",
            "ingredients_used": "Pesto Sauce,Parmesan",
            "reason": "Seasonal Promotion",
            "active": 0
        },
        {
            "special_name": "Veggie Celebration",
            "start_date": "2025-07-13",
            "end_date": "2025-07-19",
            "ingredients_used": "Bell Peppers,Mushrooms,Basil",
            "reason": "Waste Reduction",
            "active": 0
        },
        {
            "special_name": "Mediterranean Pizza Week",
            "start_date": "2025-07-18",
            "end_date": "2025-07-24",
            "ingredients_used": "Tomato Sauce,Basil,Mozzarella",
            "reason": "Inventory Surplus",
            "active": 0
        },
        {
            "special_name": "Pesto Garden Feast",
            "start_date": "2025-07-23",
            "end_date": "2025-07-30",
            "ingredients_used": "Pesto Sauce,Bell Peppers",
            "reason": "Waste Reduction",
            "active": 0
        }
    ]


MENU_SPECIALS_DATA = generate_menu_specials()

# ------------------------------------------------------------


def generate_special_performance() -> list:
    """Generate synthetic menu special performance data."""

    return [
        {
            "special_id": 1,
            "special_name": "Mozzarella Madness",
            "units_sold": 85,
            "estimated_profit": 420.0,
            "estimated_waste_reduction": 22.0
        },
        {
            "special_id": 2,
            "special_name": "Comfort Pasta Week",
            "units_sold": 74,
            "estimated_profit": 510.0,
            "estimated_waste_reduction": 8.0
        },
        {
            "special_id": 3,
            "special_name": "Bolognese Bonanza",
            "units_sold": 68,
            "estimated_profit": 465.0,
            "estimated_waste_reduction": 6.0
        },
        {
            "special_id": 4,
            "special_name": "Fresh Herb Feast",
            "units_sold": 58,
            "estimated_profit": 295.0,
            "estimated_waste_reduction": 18.0
        },
        {
            "special_id": 5,
            "special_name": "Pizza Lovers Week",
            "units_sold": 97,
            "estimated_profit": 615.0,
            "estimated_waste_reduction": 15.0
        },
        {
            "special_id": 6,
            "special_name": "Garden Fresh Pizza",
            "units_sold": 79,
            "estimated_profit": 485.0,
            "estimated_waste_reduction": 10.0
        },
        {
            "special_id": 7,
            "special_name": "Summer Pesto Special",
            "units_sold": 72,
            "estimated_profit": 445.0,
            "estimated_waste_reduction": 11.0
        },
        {
            "special_id": 8,
            "special_name": "Veggie Celebration",
            "units_sold": 88,
            "estimated_profit": 520.0,
            "estimated_waste_reduction": 24.0
        },
        {
            "special_id": 9,
            "special_name": "Mediterranean Pizza Week",
            "units_sold": 81,
            "estimated_profit": 540.0,
            "estimated_waste_reduction": 17.0
        },
        {
            "special_id": 10,
            "special_name": "Pesto Garden Feast",
            "units_sold": 63,
            "estimated_profit": 390.0,
            "estimated_waste_reduction": 16.0
        }
    ]


SPECIAL_PERFORMANCE_DATA = generate_special_performance()

# --------------------------------------------------
# Manager Decisions Data


def generate_manager_decisions() -> list:
    """Generate synthetic manager approval decisions."""

    return [
        {
            "workflow_id": "WF-001",
            "decision": "approved",
            "reason": "Inventory replenishment justified.",
            "decision_timestamp": "2025-01-05"
        },
        {
            "workflow_id": "WF-002",
            "decision": "approved",
            "reason": "Waste reduction opportunity identified.",
            "decision_timestamp": "2025-01-08"
        },
        {
            "workflow_id": "WF-003",
            "decision": "rejected",
            "reason": "Expected demand too low.",
            "decision_timestamp": "2025-01-12"
        },
        {
            "workflow_id": "WF-004",
            "decision": "approved",
            "reason": "Seasonal promotion aligns with demand.",
            "decision_timestamp": "2025-01-15"
        },
        {
            "workflow_id": "WF-005",
            "decision": "approved",
            "reason": "Low inventory risk requires action.",
            "decision_timestamp": "2025-01-20"
        },
        {
            "workflow_id": "WF-011",
            "decision": "rejected",
            "reason": "Inventory surplus assessment unclear.",
            "decision_timestamp": "2025-01-25"
        },
        {
            "workflow_id": "WF-012",
            "decision": "approved",
            "reason": "Food waste reduction strategy accepted.",
            "decision_timestamp": "2025-07-03"
        },
        {
            "workflow_id": "WF-013",
            "decision": "approved",
            "reason": "Special promotion expected to perform well.",
            "decision_timestamp": "2025-07-08"
        },
        {
            "workflow_id": "WF-014",
            "decision": "approved",
            "reason": "Inventory recommendation supported by critic review.",
            "decision_timestamp": "2025-07-12"
        },
        {
            "workflow_id": "WF-015",
            "decision": "rejected",
            "reason": "Potential overstocking concern.",
            "decision_timestamp": "2025-07-18"
        }
    ]


MANAGER_DECISIONS_DATA = generate_manager_decisions()

# --------------------------------------
# Workflow Runs


def generate_workflow_runs() -> list:
    """Generate synthetic workflow execution history."""

    return [
        {
            "workflow_id": "WF-001",
            "workflow_type": "inventory",
            "run_timestamp": "2025-01-05",
            "final_status": "completed",
            "execution_time_seconds": 9.4,
            "agents_invoked":
                "Sales Intake,Inventory Operations,Critic",
            "total_tokens": 4200,
            "estimated_cost": 0.08
        },
        {
            "workflow_id": "WF-002",
            "workflow_type": "inventory",
            "run_timestamp": "2025-01-08",
            "final_status": "completed",
            "execution_time_seconds": 11.2,
            "agents_invoked":
                "Sales Intake,Inventory Operations,Reorder,Critic",
            "total_tokens": 5100,
            "estimated_cost": 0.10
        },
        {
            "workflow_id": "WF-003",
            "workflow_type": "inventory",
            "run_timestamp": "2025-01-12",
            "final_status": "rejected",
            "execution_time_seconds": 15.8,
            "agents_invoked":
                "Sales Intake,Inventory Operations,Menu Strategy,Critic",
            "total_tokens": 7800,
            "estimated_cost": 0.15
        },
        {
            "workflow_id": "WF-004",
            "workflow_type": "inventory",
            "run_timestamp": "2025-01-15",
            "final_status": "completed",
            "execution_time_seconds": 12.4,
            "agents_invoked":
                "Sales Intake,Inventory Operations,Menu Strategy,Critic",
            "total_tokens": 6200,
            "estimated_cost": 0.12
        },
        {
            "workflow_id": "WF-005",
            "workflow_type": "inventory",
            "run_timestamp": "2025-01-20",
            "final_status": "completed",
            "execution_time_seconds": 8.8,
            "agents_invoked":
                "Sales Intake,Inventory Operations,Critic",
            "total_tokens": 3900,
            "estimated_cost": 0.07
        },

        # Analytics Workflows

        {
            "workflow_id": "WF-006",
            "workflow_type": "analytics",
            "run_timestamp": "2025-01-25",
            "final_status": "completed",
            "execution_time_seconds": 14.1,
            "agents_invoked":
                "Intake Router,Analytics Agent",
            "total_tokens": 7200,
            "estimated_cost": 0.14
        },
        {
            "workflow_id": "WF-007",
            "workflow_type": "analytics",
            "run_timestamp": "2025-07-03",
            "final_status": "completed",
            "execution_time_seconds": 16.8,
            "agents_invoked":
                "Intake Router,Analytics Agent",
            "total_tokens": 8900,
            "estimated_cost": 0.17
        },
        {
            "workflow_id": "WF-008",
            "workflow_type": "analytics",
            "run_timestamp": "2025-07-08",
            "final_status": "completed",
            "execution_time_seconds": 12.7,
            "agents_invoked":
                "Intake Router,Analytics Agent",
            "total_tokens": 6400,
            "estimated_cost": 0.12
        },
        {
            "workflow_id": "WF-009",
            "workflow_type": "analytics",
            "run_timestamp": "2025-07-12",
            "final_status": "completed",
            "execution_time_seconds": 18.3,
            "agents_invoked":
                "Intake Router,Analytics Agent",
            "total_tokens": 10400,
            "estimated_cost": 0.20
        },
        {
            "workflow_id": "WF-010",
            "workflow_type": "analytics",
            "run_timestamp": "2025-07-18",
            "final_status": "rejected",
            "execution_time_seconds": 21.5,
            "agents_invoked":
                "Intake Router,Analytics Agent",
            "total_tokens": 11800,
            "estimated_cost": 0.23
        }
    ]


WORKFLOW_RUNS_DATA = generate_workflow_runs()
