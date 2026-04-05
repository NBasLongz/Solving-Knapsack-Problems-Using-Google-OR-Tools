from ortools.algorithms.python import knapsack_solver
import time


def solve_knapsack(values, weights, capacity, time_limit=180):
    solver = knapsack_solver.KnapsackSolver(
        knapsack_solver.SolverType.KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER,
        "Knapsack"
    )

    solver.init(values, [weights], [capacity])
    solver.set_time_limit(time_limit)  

    start = time.time()
    computed_value = solver.solve()
    end = time.time()

    packed_items = []
    total_weight = 0

    for i in range(len(values)):
        if solver.best_solution_contains(i):
            packed_items.append(i)
            total_weight += weights[i]

    return {
        "total_value": computed_value,
        "total_weight": total_weight,
        "packed_items": len(packed_items),
        "is_optimal": solver.is_solution_optimal(),
        "solve_time": end - start,
        "status": "OPTIMAL" if solver.is_solution_optimal() else "TIME_LIMIT"
    }