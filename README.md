# Pandas Project

This repository is a local, notebook-based Pandas practice project. You will work through a small ecommerce scenario, complete the TODOs in the notebooks and in `src/student_tasks.py`, run the tests locally, and then commit and push your work to GitHub.

The project generates its own synthetic data locally, so you do not need to download any datasets.

## What You Will Practice

- creating DataFrames from scratch
- loading CSV files with `read_csv`
- inspecting and selecting data
- filtering rows with one or more conditions
- creating, renaming, dropping, and transforming columns
- working with missing values
- saving data with `to_csv`
- merging and concatenating datasets
- aggregating with `groupby`, `agg`, `value_counts`, and `pivot_table`
- grouping with datetime logic

## Scenario

You are working with a small ecommerce dataset that includes:

- customers
- products
- orders
- order_items

The datasets are related, small enough to explore locally, and include realistic issues such as:

- missing values
- duplicate rows
- date columns
- categorical columns
- numeric columns
- keys needed for joins

## Project Structure

```text
README.md
requirements.txt
.gitignore
data/
  raw/
  processed/
notebooks/
  00_setup_and_overview.ipynb
  01_dataframes_and_loading.ipynb
  02_access_filter_modify.ipynb
  03_merge_nulls_aggregation.ipynb
src/
  __init__.py
  data_generation.py
  exercise_utils.py
  student_tasks.py
tests/
  test_01_dataframes_and_loading.py
  test_02_access_filter_modify.py
  test_03_merge_nulls_aggregation.py
scripts/
  generate_data.py
```

## Setup

Clone the repository and move into the project folder:

```bash
git clone <your-repo-url>
cd pandas_tets
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Generate the synthetic data:

```bash
python scripts/generate_data.py
```

## How To Work Through The Project

Open the full project folder in Visual Studio and work through the notebooks in this order:

1. `notebooks/00_setup_and_overview.ipynb`
2. `notebooks/01_dataframes_and_loading.ipynb`
3. `notebooks/02_access_filter_modify.ipynb`
4. `notebooks/03_merge_nulls_aggregation.ipynb`

Use this workflow as you go:

1. Read the learning goals at the top of the notebook.
2. Run the example cells.
3. Find the related TODO in `src/student_tasks.py`.
4. Implement one function at a time.
5. Re-run the notebook cell that uses that function.
6. Run `pytest` to check your progress.
7. Repeat until all notebooks are complete and the tests pass.

## Running Tests

Run the full test suite with:

```bash
pytest
```

You can also run a single test file:

```bash
pytest tests/test_01_dataframes_and_loading.py
```

Or one specific test:

```bash
pytest tests/test_02_access_filter_modify.py::test_filter_high_value_orders_matches_expected_rows
```

At the beginning of the project, some tests may fail because the exercise functions in `src/student_tasks.py` are still incomplete. That is expected. As you implement the TODOs, more tests should pass.

## Submitting Your Work

When you finish:

1. Make sure all notebooks run top-to-bottom.
2. Make sure `pytest` passes.
3. Commit your changes.
4. Push your branch or `main` back to GitHub.

Example:

```bash
git add .
git commit -m "Complete pandas project exercises"
git push
```

## Done Checklist

You are done when:

- all notebook TODOs are completed
- all required functions in `src/student_tasks.py` are implemented
- the notebooks run from top to bottom
- `pytest` passes
- your work is committed and pushed to GitHub

## Troubleshooting

If files are missing in `data/raw/`, run:

```bash
python scripts/generate_data.py
```

If a notebook still shows an old version of a function after you edited `src/student_tasks.py`, save the file, restart the kernel, and run the notebook again from the top.

If imports fail from a notebook, make sure you opened the project root folder in Visual Studio, not only the `notebooks/` folder.
