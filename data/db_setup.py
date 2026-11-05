"""Script to Populate SQLite database"""
import sqlite3
from pathlib import Path

# Import seeded data
# Very important to use parmaterized queries.

from data.data_seed import (INVENTORY_DATA, RECIPES_DATA,
                            VENDOR_PRICES_DATA, MENU_ITEMS_DATA)

from data.data_seed2 import (
    SALES_HISTORY_DATA, MENU_SPECIALS_DATA, SPECIAL_PERFORMANCE_DATA, MANAGER_DECISIONS_DATA, WORKFLOW_RUNS_DATA)


BASE_DIR = Path(__file__).resolve().parent

DB_NAME = "restaurant.db"
DB_PATH = BASE_DIR / DB_NAME


def get_connection():
    """Create and return a SQLite connection."""
    return sqlite3.connect(DB_PATH)


CREATE_TABLES = {

    "inventory": """
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingredient_name TEXT UNIQUE NOT NULL,
            quantity REAL NOT NULL,
            unit TEXT NOT NULL,
            reorder_threshold REAL NOT NULL,
            days_to_expiry INTEGER NOT NULL
        );
    """,

    "recipes": """
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            menu_item TEXT NOT NULL,
            ingredient_name TEXT NOT NULL,
            quantity_required REAL NOT NULL
        );
    """,

    "vendor_prices": """
        CREATE TABLE IF NOT EXISTS vendor_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor_name TEXT NOT NULL,
            ingredient_name TEXT NOT NULL,
            price_per_kg REAL NOT NULL,
            delivery_days INTEGER NOT NULL
        );
    """,

    "menu_items": """
        CREATE TABLE IF NOT EXISTS menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            menu_item TEXT NOT NULL,
            active INTEGER NOT NULL,
            special INTEGER NOT NULL
        );
    """,
    # Analytics Tables
    "sales_history": """
        CREATE TABLE IF NOT EXISTS sales_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_date TEXT NOT NULL,
            menu_item TEXT NOT NULL,
            quantity_sold INTEGER NOT NULL
        );
    """,
    "menu_specials": """
        CREATE TABLE IF NOT EXISTS menu_specials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            special_name TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            ingredients_used TEXT NOT NULL,
            reason TEXT NOT NULL,
            active INTEGER NOT NULL DEFAULT 0
        );
    """,
    "special_performance": """
        CREATE TABLE IF NOT EXISTS special_performance (
            special_id INTEGER NOT NULL,
            special_name TEXT NOT NULL,
            units_sold INTEGER NOT NULL,
            estimated_profit REAL NOT NULL,
            estimated_waste_reduction REAL NOT NULL
        );
    """,

    "manager_decisions": """
        CREATE TABLE IF NOT EXISTS manager_decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workflow_id TEXT NOT NULL,
            decision TEXT NOT NULL,
            reason TEXT NOT NULL,
            decision_timestamp TEXT NOT NULL
        );
    """,

    "workflow_runs": """
        CREATE TABLE IF NOT EXISTS workflow_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workflow_id TEXT NOT NULL,
            workflow_type TEXT NOT NULL,
            run_timestamp TEXT NOT NULL,
            final_status TEXT NOT NULL,
            execution_time_seconds REAL NOT NULL,
            agents_invoked TEXT NOT NULL,
            total_tokens INTEGER NOT NULL,
            estimated_cost REAL NOT NULL
        );
    """
}

TABLES = ["inventory", "recipes", "vendor_prices",
          "menu_items", "sales_history", "menu_specials", "special_performance", "workflow_runs", "manager_decisions"]

# Analytics Indexes

CREATE_INDEXES = {
    "idx_sales_history_date": """
        CREATE INDEX IF NOT EXISTS idx_sales_history_date
        ON sales_history(sale_date);
    """,

    "idx_sales_history_menu_item": """
        CREATE INDEX IF NOT EXISTS idx_sales_history_menu_item
        ON sales_history(menu_item);
    """,
    "idx_menu_specials_name": """
        CREATE INDEX IF NOT EXISTS idx_menu_specials_name
        ON menu_specials(special_name);
    """,

    "idx_menu_specials_reason": """
        CREATE INDEX IF NOT EXISTS idx_menu_specials_reason
        ON menu_specials(reason);
    """,

    "idx_special_performance_special_id": """
        CREATE INDEX IF NOT EXISTS idx_special_performance_special_id
        ON special_performance(special_id);
    """,

    "idx_manager_decisions_decision": """
        CREATE INDEX IF NOT EXISTS idx_manager_decisions_decision
        ON manager_decisions(decision);
    """,

    "idx_manager_decisions_workflow": """
        CREATE INDEX IF NOT EXISTS idx_manager_decisions_workflow
        ON manager_decisions(workflow_id);
    """,

    "idx_workflow_runs_workflow_id": """
        CREATE INDEX IF NOT EXISTS idx_workflow_runs_workflow_id
        ON workflow_runs(workflow_id);
    """,

    "idx_workflow_runs_status": """
        CREATE INDEX IF NOT EXISTS idx_workflow_runs_status
        ON workflow_runs(final_status);
    """,
}


def create_tables():
    """Create all database tables safely using context managers."""

    with get_connection() as conn:
        cursor = conn.cursor()

        # Create tables
        for table_name, create_sql in CREATE_TABLES.items():
            cursor.execute(create_sql)
            print(f">>> Created table: {table_name}")

        # Create indexes
        for index_name, create_sql in CREATE_INDEXES.items():
            cursor.execute(create_sql)
            print(f">>> Created index: {index_name}")

    print(">>>> All tables and indexes created successfully.")


def drop_tables():
    """Drop all existing tables safely using context managers."""

    # The 'with' block ensures the connection is closed even if an execution fails
    with get_connection() as conn:
        cursor = conn.cursor()

        for table in TABLES:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
            print(f">>> Dropped table: {table}")

    print(">>>> Database cleaned.")


def reset_database():
    """Reset and recreate all database tables."""

    drop_tables()
    create_tables()

    print(">>>> Database reset complete.")


# Seeding the Tables

def seed_inventory():
    """Populate inventory table."""

    query = """
        INSERT INTO inventory (
            ingredient_name,
            quantity,
            unit,
            reorder_threshold,
            days_to_expiry
        )
        VALUES (?, ?, ?, ?, ?)
    """

    with get_connection() as conn:
        cursor = conn.cursor()

        for item in INVENTORY_DATA:
            cursor.execute(
                query,
                (
                    item["ingredient_name"],
                    item["quantity"],
                    item["unit"],
                    item["reorder_threshold"],
                    item["days_to_expiry"]
                )
            )

    print(f"<<<< Seeded {len(INVENTORY_DATA)} inventory records.")


def seed_recipes():
    """Populate recipes table."""

    query = """
        INSERT INTO recipes (
            menu_item,
            ingredient_name,
            quantity_required
        )
        VALUES (?, ?, ?)
    """

    with get_connection() as conn:
        cursor = conn.cursor()

        for recipe in RECIPES_DATA:
            cursor.execute(
                query,
                (
                    recipe["menu_item"],
                    recipe["ingredient_name"],
                    recipe["quantity_required"]
                )
            )

    print(f"<<<< Seeded {len(RECIPES_DATA)} recipe records.")


def seed_vendor_prices():
    """Populate vendor pricing table."""

    query = """
        INSERT INTO vendor_prices (
            vendor_name,
            ingredient_name,
            price_per_kg,
            delivery_days
        )
        VALUES (?, ?, ?, ?)
    """

    with get_connection() as conn:
        cursor = conn.cursor()

        for record in VENDOR_PRICES_DATA:
            cursor.execute(
                query,
                (
                    record["vendor_name"],
                    record["ingredient_name"],
                    record["price_per_kg"],
                    record["delivery_days"]
                )
            )

    print(f"<<<< Seeded {len(VENDOR_PRICES_DATA)} vendor pricing records.")


def seed_menu_items():
    """Populate menu items table."""

    query = """
        INSERT INTO menu_items (
            menu_item,
            active,
            special
        )
        VALUES (?, ?, ?)
    """

    with get_connection() as conn:
        cursor = conn.cursor()

        for item in MENU_ITEMS_DATA:
            cursor.execute(
                query,
                (
                    item["menu_item"],
                    int(item["active"]),
                    int(item["special"])
                )
            )

    print(f"<<<< Seeded {len(MENU_ITEMS_DATA)} menu items.")

# Added for Analytics agent


def seed_sales_history():
    """Populate sales history table."""

    query = """
        INSERT INTO sales_history (
            sale_date,
            menu_item,
            quantity_sold
        )
        VALUES (?, ?, ?)
    """

    with get_connection() as conn:
        cursor = conn.cursor()

        for record in SALES_HISTORY_DATA:
            cursor.execute(
                query,
                (
                    record["sale_date"],
                    record["menu_item"],
                    record["quantity_sold"]
                )
            )

    print(
        f"<<<< Seeded {len(SALES_HISTORY_DATA)} sales history records."
    )


def seed_menu_specials():
    """Populate menu specials table."""

    query = """
        INSERT INTO menu_specials (
            special_name,
            start_date,
            end_date,
            ingredients_used,
            reason,
            active
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """

    with get_connection() as conn:
        cursor = conn.cursor()

        for special in MENU_SPECIALS_DATA:
            cursor.execute(
                query,
                (
                    special["special_name"],
                    special["start_date"],
                    special["end_date"],
                    special["ingredients_used"],
                    special["reason"],
                    special["active"]
                )
            )

    print(
        f"<<<< Seeded {len(MENU_SPECIALS_DATA)} menu specials."
    )


def seed_special_performance():
    """Populate menu special performance table."""

    query = """
        INSERT INTO special_performance (
            special_id,
            special_name,
            units_sold,
            estimated_profit,
            estimated_waste_reduction
        )
        VALUES (?, ?, ?, ?, ?)
    """

    with get_connection() as conn:
        cursor = conn.cursor()

        for record in SPECIAL_PERFORMANCE_DATA:
            cursor.execute(
                query,
                (
                    record["special_id"],
                    record["special_name"],
                    record["units_sold"],
                    record["estimated_profit"],
                    record["estimated_waste_reduction"]
                )
            )

    print(
        f"<<<< Seeded {len(SPECIAL_PERFORMANCE_DATA)} special performance records."
    )


def seed_manager_decisions():
    """Populate manager decisions table."""

    query = """
        INSERT INTO manager_decisions (
            workflow_id,
            decision,
            reason,
            decision_timestamp
        )
        VALUES (?, ?, ?, ?)
    """

    with get_connection() as conn:
        cursor = conn.cursor()

        for decision in MANAGER_DECISIONS_DATA:
            cursor.execute(
                query,
                (
                    decision["workflow_id"],
                    decision["decision"],
                    decision["reason"],
                    decision["decision_timestamp"]
                )
            )

    print(
        f"<<<< Seeded {len(MANAGER_DECISIONS_DATA)} manager decisions."
    )


def seed_workflow_runs():
    """Populate workflow runs table."""

    query = """
        INSERT INTO workflow_runs (
            workflow_id,
            workflow_type,
            run_timestamp,
            final_status,
            execution_time_seconds,
            agents_invoked,
            total_tokens,
            estimated_cost
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    with get_connection() as conn:
        cursor = conn.cursor()

        for workflow in WORKFLOW_RUNS_DATA:
            cursor.execute(
                query,
                (
                    workflow["workflow_id"],
                    workflow["workflow_type"],
                    workflow["run_timestamp"],
                    workflow["final_status"],
                    workflow["execution_time_seconds"],
                    workflow["agents_invoked"],
                    workflow["total_tokens"],
                    workflow["estimated_cost"]
                )
            )

    print(
        f"<<<< Seeded {len(WORKFLOW_RUNS_DATA)} workflow runs."
    )


def seed_all():
    """Populate all tables with seed data."""

    seed_inventory()
    seed_recipes()
    seed_vendor_prices()
    seed_menu_items()
    seed_sales_history()
    seed_menu_specials()
    seed_special_performance()
    seed_manager_decisions()
    seed_workflow_runs()

    print(">>>>> <<<<<< Database successfully seeded.")


def verify_seeding():
    """Print row counts for all tables."""

    print("\n <<< Verifying Database Seed Counts >>>")

    with get_connection() as conn:
        cursor = conn.cursor()

        for table in TABLES:
            query = f"SELECT COUNT(*) FROM {table}"
            cursor.execute(query)

            count = cursor.fetchone()[0]

            print(f"Table '{table:<15}': {count} rows")

    print("--------------------------------------\n")


def inspect_table(table_name: str, limit: int = 5):
    """Preview sample data from a table."""

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            f"SELECT * FROM {table_name} LIMIT {limit}"
        )

        rows = cursor.fetchall()

    print(f"\n--- {table_name.upper()} ---")
    for row in rows:
        print(row)


if __name__ == "__main__":
    # always reset to avoid duplication (otherwise we can use the UNIQUE keword here)
    reset_database()
    seed_all()
    # verify_seeding()
    # inspect_table("inventory")
    # inspect_table("sales_history", limit=10)
    # inspect_table("menu_specials", limit=10)
    # inspect_table("special_performance", limit=10)
    # inspect_table("workflow_runs", limit=10)
    # inspect_table("manager_decisions", limit=10)
