This project processes **Ginnie Mae data** using a modular, layered structure.

At the top level, the **`biz_day/`** folder contains the main entry-point scripts. Each script corresponds to a specific business day and can be run independently. These scripts handle the full workflow for that day — downloading, parsing, calculating, and loading the data into the database.

Supporting logic lives in the **`data_parsing/`** folder. Within it:

- **`cpr4th.py`** calculates the speeds for the 4th business day, we have other similar scripts that preform key functions for one of the business days.
- Subfolders organize related functionality:

  - **`davids/`** — custom calculations and analytics performed on the data.
  - **`db_loaders/`** — functions for inserting processed data into the database.
  - **`ginnie_extract/`** — scripts that automate downloading of required files (e.g., via Selenium).
  - **`local_parser/`** — modules for extracting, cleaning, and structuring the raw datasets.

This layered design keeps **high-level workflows** separate from **implementation details**, making the codebase easier to extend and maintain.
