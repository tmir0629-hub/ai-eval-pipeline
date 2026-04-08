from src.test_cases import TEST_CASES
from src.runner import run_all_tests
from src.classifier import classify_all
from src.reporter import print_report, print_consistency_report

NUM_RUNS = 3

# ── Baseline consistency (no system prompt) ───────────
print("=" * 50)
print("BASELINE CONSISTENCY TEST (no system prompt)")
print("=" * 50)

baseline_runs = []
for i in range(NUM_RUNS):
    print(f"\n--- Baseline Run {i+1} of {NUM_RUNS} ---")
    results = run_all_tests(TEST_CASES, use_system_prompt=False)
    classified = classify_all(results)
    baseline_runs.append(classified)
    correct = sum(1 for r in classified if r["classification"] == "CORRECT")
    print(f"Run {i+1} accuracy: {correct}/50 ({correct*2}%)")

print_consistency_report(baseline_runs)

# ── Experiment consistency (with system prompt) ───────
print("\n\n" + "=" * 50)
print("EXPERIMENT CONSISTENCY TEST (with system prompt)")
print("=" * 50)

experiment_runs = []
for i in range(NUM_RUNS):
    print(f"\n--- Experiment Run {i+1} of {NUM_RUNS} ---")
    results = run_all_tests(TEST_CASES, use_system_prompt=True)
    classified = classify_all(results)
    experiment_runs.append(classified)
    correct = sum(1 for r in classified if r["classification"] == "CORRECT")
    print(f"Run {i+1} accuracy: {correct}/50 ({correct*2}%)")

print_consistency_report(experiment_runs)

# ── Final comparison ──────────────────────────────────
print("\n\n" + "="*50)
print("FINAL COMPARISON")
print("="*50)

baseline_consistent = sum(
    1 for qid in [r["id"] for r in baseline_runs[0]]
    if len(set(
        r["classification"]
        for run in baseline_runs
        for r in run if r["id"] == qid
    )) == 1
)

experiment_consistent = sum(
    1 for qid in [r["id"] for r in experiment_runs[0]]
    if len(set(
        r["classification"]
        for run in experiment_runs
        for r in run if r["id"] == qid
    )) == 1
)

print(f"Baseline consistency:   {baseline_consistent}/50 ({baseline_consistent*2}%)")
print(f"Experiment consistency: {experiment_consistent}/50 ({experiment_consistent*2}%)")
print(f"Difference:             {experiment_consistent - baseline_consistent:+d} questions")