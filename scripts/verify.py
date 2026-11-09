"""Recompute every headline number in README.md from the CSV itself.

  python scripts/verify.py data/graded_predictions.csv
"""
import csv, sys, statistics as st

IDX = {"H": 0, "D": 1, "A": 2}


def main(path):
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    n = len(rows)

    # invariant: probabilities sum to 1
    bad = [r["prediction_id"] for r in rows
           if abs(float(r["mkt_p_home"]) + float(r["mkt_p_draw"]) + float(r["mkt_p_away"]) - 1) > 0.0002]

    # invariant: outcome matches final_score
    def outcome_of(score):
        h, a = score.split("-")
        h, a = int(h), int(a)
        return "H" if h > a else ("D" if h == a else "A")

    mismatch = [r["prediction_id"] for r in rows if outcome_of(r["final_score"]) != r["outcome"]]

    # market baseline brier
    briers = []
    for r in rows:
        p = [float(r["mkt_p_home"]), float(r["mkt_p_draw"]), float(r["mkt_p_away"])]
        y = IDX[r["outcome"]]
        briers.append(sum((pi - (1.0 if i == y else 0.0)) ** 2 for i, pi in enumerate(p)))

    # direction exact match (two-way leans count as misses)
    m = {"home": "H", "away": "A", "draw": "D"}
    hits = sum(1 for r in rows if m.get(r["direction"]) == r["outcome"])

    dist = {k: sum(1 for r in rows if r["outcome"] == k) for k in "HDA"}

    print(f"rows                       {n}")
    print(f"distinct models            {len({r['model_ref'] for r in rows})}")
    print(f"kickoff range              {min(r['kickoff_date'] for r in rows)} -> {max(r['kickoff_date'] for r in rows)}")
    print(f"prob sum violations        {len(bad)}")
    print(f"outcome mismatches         {len(mismatch)}")
    print(f"outcome distribution       H={dist['H']} D={dist['D']} A={dist['A']}"
          f"  (draw {dist['D']/n*100:.1f}%)")
    print(f"market baseline brier      {st.mean(briers):.4f}")
    print(f"direction exact hit        {hits}/{n} = {hits/n*100:.1f}%")
    print(f"two-way leans              {sum(1 for r in rows if '/' in r['direction'])}")

    ok = not bad and not mismatch
    print("\nINVARIANTS", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "data/graded_predictions.csv"))
