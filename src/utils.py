import csv
import os

def read_kp_file(filepath):
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    n = int(lines[0])
    capacity = int(lines[1])

    values = []
    weights = []

    for i in range(n):
        v, w = map(int, lines[2 + i].split())
        values.append(v)
        weights.append(w)

    return values, weights, capacity, n


def save_results(file_path, result):
    os.makedirs("results", exist_ok=True)

    parts = os.path.normpath(file_path).split(os.sep)
    group_name = parts[-4]
    instance_name = os.path.basename(file_path)

    # File kết quả tổng hợp
    all_file = "results/all_results.csv"
    write_header = not os.path.exists(all_file)

    with open(all_file, 'a', newline='') as f:
        writer = csv.writer(f)

        if write_header:
            writer.writerow([
                "Group",
                "Instance",
                "Items",
                "Capacity",
                "Total Value",
                "Total Weight",
                "Packed Items",
                "Is Optimal",
                "Solve Time (s)",
                "Status"
            ])

        writer.writerow([
            group_name,
            instance_name,
            result["n"],
            result["capacity"],
            result["total_value"],
            result["total_weight"],
            result["packed_items"],
            result["is_optimal"],
            f"{result['solve_time']:.4f}",
            result["status"]
        ])

    # File kết quả theo nhóm
    group_file = f"results/{group_name}.csv"
    write_header = not os.path.exists(group_file)

    with open(group_file, 'a', newline='') as f:
        writer = csv.writer(f)

        if write_header:
            writer.writerow([
                "Instance",
                "Items",
                "Capacity",
                "Total Value",
                "Total Weight",
                "Packed Items",
                "Is Optimal",
                "Solve Time (s)",
                "Status"
            ])

        writer.writerow([
            instance_name,
            result["n"],
            result["capacity"],
            result["total_value"],
            result["total_weight"],
            result["packed_items"],
            result["is_optimal"],
            f"{result['solve_time']:.4f}",
            result["status"]
        ])