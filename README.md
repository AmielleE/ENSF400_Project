# On My Agenda
LLM-Powered Semester Deadline Tracker

ENSF 400 Project

## Team Members (Team 3)

| Name                     |
|--------------------------|
| Joshua Obinna-Eze        |
| Amielle El Makhzoumi     |
| Erioluwa Olubadejo       |
| Miriam Zeresenai         |
| Manjot Sekhon            |

## Overview

On My Agenda helps students organize deadlines across multiple courses by converting course outlines into a single, structured Excel spreadsheet.

Users upload course outlines, and the system uses a Large Language Model (LLM) to extract deadlines and generate a date-sorted, formatted spreadsheet for easy tracking.

## Features

- Upload up to 6 course outlines (PDF/text)

- Automatically extract deadlines using an LLM

- Review and edit extracted data

- Generate a sorted, color-coded Excel file

- Secure processing (no permanent file storage)

## Architecture
- app.py: Main controller

- ui.py: Upload interface

- file_parser.py: Extracts text from files

- llm_deadline_extraction.py: LLM processing

- dataframe_ui.py: Editable table UI

- excel_export.py: Excel generation

## Requirements

    pip install -r requirements.txt