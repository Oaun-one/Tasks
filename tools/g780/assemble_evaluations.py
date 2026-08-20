import json, os, shutil, glob

PKG = r"E:/WORK/TU/tasks/g780/gen-g780-realestate-fairhousing-collateral-audit"
JOBS = r"E:/WORK/TU/jobs"
E = os.path.join(PKG, "evaluations")

if os.path.isdir(E):
    shutil.rmtree(E)


def read_json(p):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return None


def summarise(ctrf_path):
    """Build verifier_summary.json from the CTRF report."""
    d = read_json(ctrf_path)
    if not d:
        return None
    tests = d.get("results", {}).get("tests", [])
    items = []
    for t in tests:
        name = t.get("name", "")
        if "[" in name and "]" in name:
            name = name[name.index("[") + 1:name.rindex("]")]
        passed = t.get("status") == "passed"
        items.append({
            "name": name,
            "passed": passed,
            "weight": round(1.0 / max(len(tests), 1), 6),
            "motivation": t.get("message") or ("deterministic assertion satisfied" if passed
                                               else "deterministic assertion failed"),
        })
    npass = sum(1 for i in items if i["passed"])
    return {
        "total": len(items),
        "passed": npass,
        "failed": len(items) - npass,
        "all_passed": npass == len(items),
        "grading": "binary - tests/test.sh writes reward 1 only if every verifier passes",
        "items": items,
    }


def final_answer(traj_path):
    t = read_json(traj_path)
    if not t:
        return None
    steps = t if isinstance(t, list) else t.get("messages", t.get("steps", []))
    for s in reversed(steps):
        if isinstance(s, dict) and s.get("source") == "agent":
            msg = (s.get("message") or "").strip()
            if msg:
                return msg
    return None


def copy_run(src, dst, model=None):
    os.makedirs(os.path.join(dst, "agent"), exist_ok=True)
    os.makedirs(os.path.join(dst, "verifier"), exist_ok=True)

    for rel in ["agent/trajectory.json", "agent/opencode.txt", "agent/oracle.txt",
                "verifier/ctrf.json", "verifier/reward.txt", "verifier/test-stdout.txt",
                "config.json", "result.json"]:
        s = os.path.join(src, rel)
        if os.path.isfile(s):
            shutil.copy2(s, os.path.join(dst, rel))

    rtxt = os.path.join(dst, "verifier", "reward.txt")
    reward = None
    if os.path.isfile(rtxt):
        reward = float(open(rtxt).read().strip())
        json.dump({"reward": reward}, open(os.path.join(dst, "verifier", "reward.json"), "w"), indent=2)

    summ = summarise(os.path.join(dst, "verifier", "ctrf.json"))
    if summ:
        json.dump(summ, open(os.path.join(dst, "verifier", "verifier_summary.json"), "w"), indent=2)

    rj = os.path.join(dst, "result.json")
    if os.path.isfile(rj):
        d = read_json(rj) or {}
        if model:
            d["model"] = model
        if reward is not None:
            d["reward"] = reward
            d["overall_pass"] = bool(reward == 1.0)
        fa = final_answer(os.path.join(dst, "agent", "trajectory.json"))
        if fa:
            d["final_answer"] = fa
        d["judge_provenance"] = {
            "judged_verifiers": 0,
            "judge_model": None,
            "note": "All verifiers in tests/manifest.json are deterministic; no LLM judge is invoked.",
        }
        json.dump(d, open(rj, "w", encoding="utf-8"), indent=2)
    return reward


def one(job):
    dirs = sorted(glob.glob(os.path.join(JOBS, job, "gen-g780*/")))
    return dirs


# oracle
copy_run(one("oracle-v9")[0], os.path.join(E, "oracle"), model="oracle")

# five GLM rollouts
rewards = []
for i, d in enumerate(one("glm-5x-v9-NONC-B1-1001608"), 1):
    rewards.append(copy_run(d, os.path.join(E, "glm-5.2", "r%d" % i), model="GLM-5.2"))

# stability repeats
for i, d in enumerate(one("oracle-stability-v9"), 1):
    copy_run(d, os.path.join(E, "stability", "repeat-%02d" % i), model="oracle")

# strip opencode internal state
for root, dirs, files in os.walk(E, topdown=False):
    for dname in list(dirs):
        if dname in ("xdg-data", "snapshot", "opencode", "setup"):
            shutil.rmtree(os.path.join(root, dname), ignore_errors=True)

print("rewards:", rewards)
print("binary k/5:", sum(1 for r in rewards if r == 1.0), "/ 5")
for p in sorted(glob.glob(os.path.join(E, "*", "*", ""))) + [os.path.join(E, "oracle", "")]:
    pass
print("\nevaluations tree:")
for root, dirs, files in os.walk(E):
    lvl = root.replace(E, "").count(os.sep)
    if lvl <= 2:
        print("  " * lvl + os.path.basename(root) + "/", sorted(files) if lvl == 2 else "")
