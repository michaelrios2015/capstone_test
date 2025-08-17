## 📂 Project Structure

```
project-root/
│
├── biz_day/ # Entry points for each "business day" workflow
│ ├── day1.py
│ ├── day2.py
│ └── ...
│
├── data_parsing/ # Core functions for data processing
│ ├── cpr4th.py # Main parsing/processing functions
│ │
│ ├── davids_scripts/ # Scripts with calculation logic
│ │ ├── calc_x.py
│ │ └── ...
│ │
│ ├── loaders/ # Database loading scripts
│ │ ├── db_loader.py
│ │ └── ...
│ │
│ ├── downloaders/ # File download automation (Selenium, etc.)
│ │ ├── selenium_downloader.py
│ │ └── ...
│ │
│ └── parsers/ # Extract/clean raw data from downloaded files
│ ├── pool_parser.py
│ └── ...
│
└── README.md # Project documentation
```

---

## 🚀 Usage

1. **Run a business day workflow**

   Each script in `biz_day/` represents a full end-to-end workflow for a specific reporting/business day.
   Example:

   ```
   python biz_day/sixth.py
   ```

This will:

- Download the necessary Ginnie Mae files
- Parse and extract the required data
- Perform calculations (e.g., CPR, SMM, prepayment metrics)
- Load results into the database

---

## 🔧 Components

### 1. **Business Day Scripts (`biz_day/`)**

- Contain **top-level functions** that can be run directly.
- Serve as orchestration points — they call into parsing, downloading, and loading modules.

### 2. **Data Parsing (`data_parsing/`)**

- **`cpr4th.py`** — main entry for parsing functions.
- Subfolders:

  - **`davids/`** — numerical/statistical calculations on parsed data.
  - **`db_loader/`** — database integration (e.g., insert/update logic).
  - **`ginnie_extract/`** — automated file download via Selenium and other methods.
  - **`local_parser/`** — logic for cleaning and structuring raw datasets.

---

## 🛠 Dependencies

- **Python 3.x**
- **Selenium** (for automated downloads)
- **Pandas / NumPy** (data wrangling & calculations)
- **Psycopg2** (for loading into a SQL database)

---

## 📌 Notes

- The **biz_day scripts** are designed to be standalone.
- Supporting functions live in **data_parsing** and its submodules.
- Code is modular, so new data sources or calculations can be added by extending the relevant subfolder.

---

```



```
