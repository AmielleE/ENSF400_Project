import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from the .env file
load_dotenv()


def extract_deadlines(file_df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes a DataFrame with columns:
        - filename
        - text

    Returns a DataFrame with columns:
        - classname
        - assignment_name
        - due_date

    due_date should be in MM/DD/YYYY format.
    """

    # Create Gemini client using API key from environment variables
    client = genai.Client()

    # Store all extracted deadline rows from all files
    all_deadlines = []

    # Tell Gemini the exact JSON structure we want back
    response_schema = {
        "type": "ARRAY",
        "items": {
            "type": "OBJECT",
            "properties": {
                "classname": {"type": "STRING"},
                "assignment_name": {"type": "STRING"},
                "due_date": {"type": "STRING"}
            },
            "required": ["classname", "assignment_name", "due_date"]
        }
    }

    # Loop through each parsed file in the input DataFrame
    for _, row in file_df.iterrows():
        filename = row["filename"]
        text = row["text"]

        # Prompt Gemini to extract deadlines from the course outline text
        prompt = f"""
You are extracting course deadlines from a course outline.

From the text below, extract all important deadlines and return only structured data.

Rules:
- Return every assignment, lab, quiz, midterm, final, project, or other graded deadline if a due date is provided.
- Use the course name as "classname".
- Use the exact assignment/test/lab name as "assignment_name" or make reasonable inferences if not provided.
- Convert every due date into MM/DD/YYYY format.
- If the year is missing but can be reasonably inferred from the document, infer it.
- Do not include explanations.
- Run a final check to ensure all due dates are in the correct format and that all required fields are present.
- No empty fields. If any information is missing, make reasonable inferences or leave it out if inference isn't possible.
- Do not return an empty array, if not deadlines are found go through the text again. Under no circumstances should you return an empty array.

File name: {filename}

Course outline text:
{text}
"""

        try:
            # Send the prompt to Gemini and request structured JSON output
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=response_schema
                ),
            )

            # Use parsed output if Gemini returns valid structured data
            extracted_rows = response.parsed if response.parsed is not None else []

            # Add each extracted deadline to the final results list
            for item in extracted_rows:
                all_deadlines.append({
                    "classname": item.get("classname", "").strip(),
                    "assignment_name": item.get("assignment_name", "").strip(),
                    "due_date": item.get("due_date", "").strip()
                })

        except Exception as e:
            print(f"Error extracting deadlines from {filename}: {e}")

    # Convert the collected deadline rows into a DataFrame
    return pd.DataFrame(
        all_deadlines,
        columns=["classname", "assignment_name", "due_date"]
    )