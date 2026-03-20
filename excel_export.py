import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo


def export_to_excel(deadline_df: pd.DataFrame, output_path: str = "deadlines.xlsx") -> None:
    """
    Takes a DataFrame with columns:
        - classname
        - assignment_name
        - due_date

    Creates an Excel file that:
        - sorts deadlines by due date ascending
        - adds a Done column
        - color-codes rows by class
        - allows filtering/sorting in Excel
    """

    # Make a copy so the original DataFrame is not modified
    df = deadline_df.copy()

    # Make sure required columns exist
    required_columns = ["classname", "assignment_name", "due_date"]
    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")

    # Convert due_date strings to actual datetime values so sorting works properly
    df["due_date"] = pd.to_datetime(df["due_date"], format="%m/%d/%Y", errors="coerce")

    # Sort by due date ascending
    df = df.sort_values(by="due_date", ascending=True)

    # Add a Done column with default value "Not Done"
    df["done_status"] = "Not Done"

    # Create a workbook and worksheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Deadlines"

    # Define final column order
    columns = ["classname", "assignment_name", "due_date", "done_status"]