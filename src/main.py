import os

from utils import read_kp_file, save_results
from solver import solve_knapsack

def main():
    base_dir = os.path.abspath("kplib")

    group_files = {}

    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".kp"):
                filepath = os.path.join(root, file)

                parts = os.path.normpath(filepath).split(os.sep)
                group_name = parts[-4]

                if group_name not in group_files:
                    group_files[group_name] = []

                group_files[group_name].append(filepath)

    print(f"Total groups: {len(group_files)}")


    TARGET_SIZES = [
        "n00050",
        "n00100",
        "n00200",
        "n00500",
        "n01000",
        "n02000",
        "n05000"
    ]

    selected_files = []


    for group, files in group_files.items():
        files = sorted(files)

        count = 0

        for size in TARGET_SIZES:
            matched = [f for f in files if size in f][:2]  
            selected_files.extend(matched)
            count += len(matched)

        print(f"{group}: selected {count} files")

    print(f"\nTotal selected test files: {len(selected_files)}")


    for filepath in selected_files:
        try:
            print(f"\nSolving: {filepath}")

            values, weights, capacity, n = read_kp_file(filepath)
            print(f"  Items: {n}, Capacity: {capacity}")

            result = solve_knapsack(values, weights, capacity, time_limit=180)

            result["n"] = n
            result["capacity"] = capacity

            print(
                f"  Result: {result['total_value']} | Time: {result['solve_time']:.2f}s | {result['status']}"
            )

            save_results(filepath, result)

        except Exception as e:
            print(f"[ERROR] {filepath}: {e}")


if __name__ == "__main__":
    main()