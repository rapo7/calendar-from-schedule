**Project Overview (at a glance):**

This project processes CSV files containing class schedules to generate optimized "Epiphan check session" events for each day. It provides a GUI for users to upload a CSV, processes the data to minimize the number of check sessions needed, and allows downloading a calendar-ready CSV of these sessions.

---

## STAR Method for Action Points

- **Situation:**  
  Need to schedule "Epiphan check sessions" to cover all classes in a day, minimizing the number of checks while ensuring each class is checked within a 15-minute window after it starts.

- **Task:**  
  Build a tool that reads class schedules from CSV, groups classes by day, and computes the minimal set of check sessions per day. Provide a user-friendly interface for file upload and download.

- **Action:**  
  - Remove duplicate classes by title and start time.
  - Group classes by date.
  - For each day, use a greedy algorithm to select check times so every class is checked within 15 minutes of its start.
  - Output the check sessions as a calendar CSV.
  - Provide a GUI for file upload and download.

- **Result:**  
  Users get a calendar CSV with the minimal number of 15-minute "Epiphan check" sessions needed to cover all classes, ready for import into calendar software.

---

## File-by-File Breakdown

### main.py
**Purpose:**  
Provides a simple Tkinter GUI for users to upload a CSV file, process it, and download the resulting calendar CSV.

**Key Actions:**
- Lets users select a CSV file via a file dialog.
- Calls `process_csv` from utils.py to process the file.
- Enables downloading the processed calendar CSV.

---

### utils.py
**Purpose:**  
Contains the core logic for processing the class schedule CSV and generating the check sessions.

**Key Actions:**
- **Deduplication:** Removes duplicate classes by title and start time.
- **Grouping:** Groups class start times by date.
- **Session Minimization:**  
  - For each day, finds the minimal set of check sessions (using a greedy algorithm) so every class is checked within 15 minutes of its start.
  - Builds a list of check sessions and their coverage.
- **Calendar Output:**  
  - Constructs a DataFrame with calendar event details for each check session.
  - Returns this DataFrame for export.

---

### class_checker.py
**Purpose:**  
A script version (possibly for testing or batch processing) that reads a CSV, processes it, and outputs statistics and the calendar CSV.

**Key Actions:**
- Reads and deduplicates the CSV.
- Groups by date and computes check sessions (using similar logic as utils.py).
- Prints statistics about class distribution.
- Outputs the calendar CSV.

---

## Summary Table

| File                | Purpose/Role                                                                 |
|---------------------|------------------------------------------------------------------------------|
| main.py           | GUI for uploading, processing, and downloading CSV files.                    |
| utils.py          | Core logic for deduplication, grouping, session minimization, and output.    |
| class_checker.py  | Script for batch/statistical processing and calendar CSV generation.          |

---

**In summary:**  
The project efficiently schedules and exports "Epiphan check sessions" for class schedules, minimizing checks while ensuring all classes are covered, with both GUI and script interfaces.
