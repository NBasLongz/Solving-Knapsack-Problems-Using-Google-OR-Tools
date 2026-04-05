# 🚀 How to Run the Project

## 1. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 2. Prepare dataset

Download KPLIB dataset:

https://github.com/likr/kplib

Place it into project folder:

```
project/
├── kplib/
├── main.py
```

---

## 3. Run all test cases

```bash
pip install ortools pandas matplotlib reportlab

python src/main.py

```

* Runs ~91 test cases (7 per group × 13 groups)
* Time limit per test: **60 seconds**
* Results will be saved in:

```
results/
```

---

## 4. Generate summary statistics

```bash
python stats.py
```

Output:

* Summary table printed to console
* File saved at:

```
results/summary_stats.csv
```

---

## 5. Output explanation

Each result file contains:

* Instance name
* Total Value (objective)
* Total Weight
* Packed Items
* Is Optimal (True/False)
* Solve Time (seconds)
* Solver Status

---

## 6. Experiment setup

* Solver: OR-Tools CP-SAT
* Time limit per instance: 60 seconds
* Test selection:

  * 13 groups
  * 7 test cases per group
  * Sizes: 50, 100, 200, 500, 1000 items

---

## 7. Evaluation

We analyze:

* Optimal solution rate (%)
* Average solving time
* Average value and weight

Groups are classified as:

* **Easy** → high optimal %, low time
* **Hard** → low optimal %, high time

---

## 8. Notes

* Some large instances may not reach optimal due to time limit
* Solver returns:

  * OPTIMAL → proven optimal
  * FEASIBLE → best found within time

---
