def print_report(classified_results):
    total = len(classified_results)
    correct = sum(1 for r in classified_results if r["classification"] == "CORRECT")
    hallucinations = total - correct

    print("\n" + "="*50)
    print("HALLUCINATION REGRESSION TEST REPORT")
    print("="*50)
    print(f"Total tests:     {total}")
    print(f"Correct:         {correct} ({round(correct/total*100)}%)")
    print(f"Hallucinations:  {hallucinations} ({round(hallucinations/total*100)}%)")
    print("="*50)

    categories = {}
    for r in classified_results:
        c = r["classification"]
        categories[c] = categories.get(c, 0) + 1

    print("\nBreakdown by type:")
    for category, count in categories.items():
        print(f"  {category}: {count}")

    print("\nDetailed Results:")
    print("-"*50)
    for r in classified_results:
        print(f"\n[{r['id']}] {r['prompt']}")
        print(f"  Expected:       {r['expected']}")
        print(f"  Actual:         {r['actual'][:100]}...")
        print(f"  Classification: {r['classification']}")
        print(f"  Explanation:    {r['explanation']}")


def print_consistency_report(all_runs):
    """
    all_runs: list of 3 classified result lists
    """
    print("\n" + "="*50)
    print("CONSISTENCY REPORT")
    print("="*50)

    # Get all question ids from first run
    ids = [r["id"] for r in all_runs[0]]

    consistent = 0
    inconsistent = 0
    inconsistent_questions = []

    for qid in ids:
        # Get classification for this question across all runs
        classifications = []
        for run in all_runs:
            for r in run:
                if r["id"] == qid:
                    classifications.append(r["classification"])

        # Check if all runs agreed
        if len(set(classifications)) == 1:
            consistent += 1
        else:
            inconsistent += 1
            inconsistent_questions.append({
                "id": qid,
                "classifications": classifications
            })

    total = len(ids)
    print(f"Total questions:   {total}")
    print(f"Consistent:        {consistent} ({round(consistent/total*100)}%)")
    print(f"Inconsistent:      {inconsistent} ({round(inconsistent/total*100)}%)")

    if inconsistent_questions:
        print("\nInconsistent Questions:")
        print("-"*50)
        for q in inconsistent_questions:
            print(f"\n  [{q['id']}] Classifications across 3 runs:")
            for i, c in enumerate(q['classifications']):
                print(f"    Run {i+1}: {c}")