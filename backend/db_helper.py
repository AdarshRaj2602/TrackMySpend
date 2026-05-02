import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logging

logger = setup_logging('db_helper')

@contextmanager
def get_db_cursor(commit = False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager"
    )

    if connection.is_connected():
        print("connected to db mySQL server")
    else:
        print("Failed to connect to db mySQL server")

    cursor = connection.cursor(dictionary= True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()

def fetch_expense_for_date(expense_date):
    logger.info(f"fetch_expense_for_date called the {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses

def delete_expense_for_date(expense_date):
    logger.info(f"delete_expense_for_date called the {expense_date}")
    with get_db_cursor(commit = True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))

def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}")
    with get_db_cursor(commit = True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )

def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start date: {start_date} end date: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            """SELECT category, SUM(amount) as total
                        FROM expenses
                        WHERE expense_date BETWEEN %s AND %s
                        GROUP BY category;""",
            (start_date, end_date)
        )
        data = cursor.fetchall()
        return data

def fetch_expense_monthly_summary():
    logger.info(f"fetch_expense_monthly_summary")
    with get_db_cursor() as cursor:
        cursor.execute(
            """SELECT DISTINCT 
                        MONTHNAME(expense_date) AS month_name,
                        SUM(amount) AS total
                        FROM expenses
                        GROUP BY month_name
                        ORDER BY MONTH(month_name);""",
        )
        data = cursor.fetchall()
        return data

if __name__ == "__main__":
    expenses = fetch_expense_for_date("2024/08/01")
    for expense in expenses:
        print(expense)
    insert_expense("2024/08/25", 40, "Food", "Eat tasty samosa chat")
    delete_expense_for_date("2024/08/25")
    summary = fetch_expense_summary("2024/08/01", "2024/08/05")
    for report in summary:
        print(report)
