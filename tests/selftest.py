"""End-to-end self-test of the campaign scripts on a throwaway campaign in a temp folder.

Run after changing any script:   python tests/selftest.py     (exit code 1 if a gate misbehaves)
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

S = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(S))
from rclib import append_card, set_fields  # noqa: E402

PY = sys.executable
ROOT = Path(tempfile.mkdtemp(prefix="rc_selftest_"))
PROJ = ROOT / "proj"
PROJ.mkdir(parents=True)
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")
FAILS = []


def run(*args, ok=None, has=None):
    """ok: expected success (True/False/None=don't care); has: substring the output must contain."""
    r = subprocess.run([PY, "-I", str(S / args[0]), *map(str, args[1:])], capture_output=True, text=True,
                       encoding="utf-8", env=ENV)
    out = (r.stdout + r.stderr).strip()
    bad = (ok is not None and (r.returncode == 0) != ok) or (has is not None and has not in out)
    label = f"{args[0]} {' '.join(str(x) for x in args[2:6])}"
    print(("FAIL " if bad else "ok   ") + label + (f"\n{out}\n" if bad else ""))
    if bad:
        FAILS.append(label)
    return out


def prompt(label):
    return C / "prompts_out" / f"{label}.md"


# phase 0: an older campaign to inherit from, then the new one
run("init_campaign.py", "--project", PROJ, "--name", "old", "--goal", "old goal", "--date", "2026-09-01", ok=True)
OLD = PROJ / "campaigns" / "2026-09-01-old"
(OLD / "lit_pool" / "L0.md").write_text("## P-L0-001 Old paper\n- claim: x\n- source: http://a.org/x\n"
                                        "- status: verified\n- relevance: target\n", encoding="utf-8")
append_card(OLD / "barriers.md", "B01", "old barrier", {"statement": "s", "scope": "spectral", "evidence": "e"})
run("init_campaign.py", "--project", PROJ, "--name", "tdemo", "--goal", "把常数 c 推到 1.20 以下", "--date", "2026-10-09",
    ok=True, has="inheritable: 2026-09-01-old")
C = PROJ / "campaigns" / "2026-10-09-tdemo"
run("init_campaign.py", "--dir", C, "--inherit-from", OLD, ok=True, has="1 barriers")

# phase 1: pool shards; a verifier overrides the sweeper's status
(C / "lit_pool" / "L0.md").write_text(
    "## P-L0-001 Paper A\n- claim: c<=1.214\n- source: https://example.edu/~a/c.pdf\n- status: rough\n"
    "- relevance: target\n\n## P-L0-002 Tool B\n- claim: bounds\n- source: arxiv.org/abs/0000.00001\n"
    "- status: rough\n- relevance: tool\n", encoding="utf-8")
(C / "lit_pool" / "V2.md").write_text(
    "## P-L0-001\n- status: verified\n- verified_by: V2\n- obstructions: cannot pass 1.21 (p.14)\n", encoding="utf-8")
run("merge_pool.py", C, ok=True, has="still rough (unverified): 1")

# phase 2: two quantifiers; tool hunt refused before cross-check
for q, mem in (("Q1", 4), ("Q2", 8)):
    run("make_prompt.py", C, "--kind", "quant", "--label", q, "--mem", mem, ok=True)
    run("check_launch.py", C, "--kind", "quant", "--label", q, "--mem", mem, "--prompt", prompt(q), ok=True)
run("make_prompt.py", C, "--kind", "tool", "--label", "TH1", "--mem", 0, "--node", "N2", ok=True)
run("check_launch.py", C, "--kind", "tool", "--label", "TH1", "--mem", 0, "--prompt", prompt("TH1"), ok=False,
    has="tool hunt needs 'cross-checked'")
run("finish_run.py", C, "L001", "--outcome", "x", "--tokens", "300000", "--knowable", "no", ok=True)
run("finish_run.py", C, "L002", "--outcome", "x", "--tokens", "280000", ok=True)
set_fields(C / "CAMPAIGN.md", "TARGET", {"target_status": "cross-checked", "statement": "delta",
                                          "target_value": "0.031", "unit": "delta", "better": "higher"})

# phase 3: tree; tool hunt now allowed
tree = C / "tree.md"
tree.write_text(tree.read_text(encoding="utf-8").replace(
    "## N0 {{root: the user's goal}}\n- type: AND\n- parent: -\n- statement:\n- needed:",
    "## N0 root\n- type: AND\n- parent: -\n- needed: 0.031\n\n## N1 side A\n- type: OR\n- parent: N0\n\n"
    "## N2 side B\n- type: OR\n- parent: N0\n- inputs: P-L0-002"), encoding="utf-8")
run("make_prompt.py", C, "--kind", "tool", "--label", "TH1", "--mem", 0, "--node", "N2", ok=True)
run("check_launch.py", C, "--kind", "tool", "--label", "TH1", "--mem", 0, "--prompt", prompt("TH1"), ok=True)
run("finish_run.py", C, "L003", "--outcome", "tools", ok=True)

# phase 6/7: routes
R = C / "routes.md"
base = {"needed": "x<=1.20", "needed_value": "1.20", "better": "lower", "verdict": "pending", "memory_gb": "2",
        "status": "draft"}
append_card(R, "R01", "trace", dict(base, method_class="moment-method", node="N2", mechanism="m", inputs="P-L0-002"))
append_card(R, "R02", "expansion", dict(base, method_class="Moment method", node="N2", mechanism="m"))
append_card(R, "R03", "pairs", dict(base, method_class="exponent-pairs", node="N1", mechanism="m",
                                    needed_value="0.287", ceiling="0.35", ceiling_value="0.35",
                                    derivation="one line", verdict="GO", memory_gb="0"))
run("make_prompt.py", C, "--kind", "scout", "--label", "S-R01", "--route", "R01", ok=True)
run("check_launch.py", C, "--kind", "scout", "--label", "S-R01", "--route", "R01", "--prompt", prompt("S-R01"),
    ok=False, has="needs 'confirmed'")
set_fields(C / "CAMPAIGN.md", "TARGET", {"target_status": "confirmed"})
run("check_launch.py", C, "--kind", "scout", "--label", "S-R01", "--route", "R01", "--prompt", prompt("S-R01"),
    ok=True)
run("make_prompt.py", C, "--kind", "scout", "--label", "S-R02", "--route", "R02", ok=True)
run("check_launch.py", C, "--kind", "scout", "--label", "S-R02", "--route", "R02", "--prompt", prompt("S-R02"),
    ok=False, has="dedup: R01 (scouting)")
run("make_prompt.py", C, "--kind", "attack", "--label", "A-R03", "--route", "R03", ok=True)
run("check_launch.py", C, "--kind", "attack", "--label", "A-R03", "--route", "R03", "--prompt", prompt("A-R03"),
    ok=False, has="does not meet needed")
set_fields(R, "R03", {"ceiling_value": "0.28", "ceiling": "0.28"})
run("check_launch.py", C, "--kind", "attack", "--label", "A-R03", "--route", "R03", "--prompt", prompt("A-R03"),
    ok=False, has="stale")
run("make_prompt.py", C, "--kind", "attack", "--label", "A-R03", "--route", "R03", ok=True)
run("check_launch.py", C, "--kind", "attack", "--label", "A-R03", "--route", "R03", "--prompt", prompt("A-R03"),
    ok=True)
run("check_launch.py", C, "--kind", "other", "--label", "big", "--mem", 9, "--prompt", prompt("Q1"), ok=False,
    has="per-agent cap")

# scout kills R01; relaunching the same class needs differs_from + bypasses, and a fresh prompt
run("finish_run.py", C, "L004", "--outcome", "KILL", "--route-status", "killed", "--blocked-by", "B02", ok=True)
append_card(C / "barriers.md", "B02", "square-root barrier", {"statement": "s", "scope": "moment-method", "evidence": "e"})
run("check_launch.py", C, "--kind", "scout", "--label", "S-R02", "--route", "R02", "--prompt", prompt("S-R02"),
    ok=False, has="bypasses")
set_fields(R, "R02", {"differs_from": "R01: uses a thin subfamily, not the full family", "bypasses": "B02"})
run("make_prompt.py", C, "--kind", "scout", "--label", "S-R02", "--route", "R02", ok=True)
run("check_launch.py", C, "--kind", "scout", "--label", "S-R02", "--route", "R02", "--prompt", prompt("S-R02"),
    ok=True)

# phase 9: one check per result version
run("result.py", C, "add", "--title", "T", "--route", "R03", "--statement", "s", "--check-plan", "referee",
    ok=True, has="RES-01")
run("result.py", C, "add", "--title", "Cor", "--statement", "c", "--check-plan", "main", "--depends", "RES-01",
    ok=True)
run("make_prompt.py", C, "--kind", "referee", "--label", "REF-01", "--result", "RES-01", "--mem", 2, ok=True)
run("check_launch.py", C, "--kind", "referee", "--label", "REF-01", "--result", "RES-01", "--mem", 2,
    "--prompt", prompt("REF-01"), ok=True)
run("check_launch.py", C, "--kind", "referee", "--label", "REF-01b", "--result", "RES-01", "--mem", 2,
    "--prompt", prompt("REF-01"), ok=False, has="already has its one check")
run("result.py", C, "check", "RES-01", "--by", "main", "--status", "passed", ok=False, has="REFUSED")
run("finish_run.py", C, "L007", "--outcome", "VALID", "--result-check", "passed", ok=True)
run("result.py", C, "bump", "RES-01", "--why", "fix", ok=True, has="Dependents to re-examine: RES-02")
run("result.py", C, "check", "RES-01", "--by", "main", "--status", "passed", ok=True)
run("result.py", C, "freeze", ok=True, has="froze RES-01 v2")

# phase 10: propagation to the root + barrier convergence
set_fields(R, "R02", {"status": "killed", "blocked_by": "B02"})
append_card(R, "R04", "k", {"method_class": "spectral", "node": "N2", "mechanism": "m", "needed": "n",
                            "memory_gb": "0", "status": "killed", "blocked_by": "B02"})
append_card(R, "R05", "t", {"method_class": "expansion", "node": "N1", "mechanism": "m", "needed": "n",
                            "memory_gb": "0", "status": "blocked", "blocked_by": "B02"})
run("tree_status.py", C, ok=True, has="STOP RULE: root N0 is blocked")
run("tree_status.py", C, ok=True, has="blocked 3 independent method classes")
run("status.py", C, ok=True, has="agents 2/")

shutil.rmtree(ROOT, ignore_errors=True)
print(f"\nSELFTEST: {len(FAILS)} failures" + (f": {FAILS}" if FAILS else ""))
sys.exit(1 if FAILS else 0)
