#  Solving Knapsack Problems Using Google OR-Tools

A comprehensive Python-based pipeline to solve, benchmark, and evaluate the 0-1 Knapsack problem across various difficulty groups using the KPLib dataset and Google OR-Tools.

---

##  Project Structure & File Explanations

```text
project/
├── Analysis/             # The analysis from result
├── kplib/                # (Must be downloaded) The dataset folder containing test cases
├── results/              # Auto-generated folder containing CSV logs and charts
├── main.py               # The Orchestrator
├── solver.py             # The Optimizer
├── utils.py              # The Data Handler
└── stats.py              # The Analytics Engine
```

### What does each file do?
* **`main.py`**: The entry point of the pipeline. It scans the `kplib` directory, groups the files, selects a representative subset of test cases (182 files total across 7 sizes), calls the solver, and logs the progress in real-time.
* **`solver.py`**: Contains the core optimization logic. It wraps the Google OR-Tools library, specifically using the `KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER`, applies the 180-second time limit, and extracts the optimal (or best-found) solution.
* **`utils.py`**: Provides essential helper functions. `read_kp_file()` parses the specific KPLib file format, and `save_results()` handles safely exporting the metrics into structured CSV files (`all_results.csv` and group-specific CSVs).
* **`stats.py`**: The data analytics and reporting script. It reads the generated CSVs using `pandas` to calculate success rates and average times, uses `matplotlib` to draw visual charts, and utilizes `reportlab` to automatically compile everything into a professional PDF report.

---

##  How to Run the Project

### 1. Install Dependencies
Make sure you have Python installed, then run:
```bash
pip install ortools pandas matplotlib reportlab
```

### 2. Prepare the Dataset
Download the **KPLIB dataset** from their official repository:
 [https://github.com/likr/kplib](https://github.com/likr/kplib)

Extract and place the `kplib` folder directly into the root of this project.

### 3. Run the Experiments
To start the solving process, run:
```bash
python main.py
```
* **Scope:** Runs 182 test cases (14 per group × 13 groups: 2 instances for 7 different item sizes).
* **Time limit:** 180 seconds (3 minutes) per test case.
* **Outputs:** Results are saved immediately into the `results/` folder to prevent data loss.

### 4. Generate Summary Statistics & PDF Report
Once `main.py` finishes, run the analytics script:
```bash
python stats.py
```
* **Outputs:** * Summary table printed to the console.
  * Charts generated: `results/optimal_chart.png` and `results/time_chart.png`.
  * **Final Report:** A complete PDF file will be generated automatically.

---

##  Output Explanation

The generated CSV files contain the following columns:
* **Instance**: The name of the test case.
* **Items / Capacity**: Problem dimensions.
* **Total Value / Total Weight**: The objective value and weight of the chosen items.
* **Packed Items**: Number of items selected in the knapsack.
* **Is Optimal**: `True` if the global optimum was proven, `False` otherwise.
* **Solve Time (s)**: CPU time taken by the solver.
* **Status**: `OPTIMAL` or `TIME_LIMIT`.

---

##  Experiment Setup & Evaluation

**Solver Details:**
* Engine: `KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER` (Google OR-Tools)
* Time Limit: 180 seconds per instance.
* Test Selection: 13 dataset groups; Sizes ranging from 50 to 5,000 items.

**Difficulty Classification:**
We analyze the *Optimal Solution Rate (%)* and *Average Solving Time* to classify groups:
* **Easy**: 100% optimal rate, solved in ~0.00s (e.g., Uncorrelated datasets).
* **Medium**: ~50-60% optimal rate (e.g., Almost Strongly Correlated).
* **Hard / Very Hard**: < 40% optimal rate, frequent timeouts (e.g., Spanner, Profit Ceiling datasets).

---

##  Notes
* Hardware limitation: Some extremely large or heavily correlated instances will hit the 180-second time limit. In these cases, the solver gracefully returns the *best feasible solution* found up to that point.