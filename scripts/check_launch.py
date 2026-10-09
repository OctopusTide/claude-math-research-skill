"""Gate every subagent launch. PASS registers the run in ledger.md; REJECT explains why (exit code 1).

check_launch.py <campaign dir> --kind <kind> --label <label> --mem <GB> --prompt <file>
                [--route Rxx] [--result RES-xx] [--dry-run]

kinds: lit  read  quant  tool  scout  attack  referee  audit  paper  lean  other

Checks:
  every kind  budget (max concurrent agents, total memory, per-agent memory) read fresh from budget.toml
  quant       nothing extra (literature must be merged first: checked loosely via lit_pool.md)
  tool        target is cross-checked or confirmed
  scout       target confirmed; route card complete; dedup; per-node limit
  attack      target confirmed; verdict GO (or CONJ + user_approved: yes); ceiling meets need; dedup;
              per-node limit; prompt generated for this route and current target
  referee     the result version has no check yet (one check per result version)
  prompts     contain the markers make_prompt.py writes (TARGET / MEMORY CAP / KNOWN BARRIERS / RETURN WHEN)
"""
import argparse
import re
import sys
from pathlib import Path

import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # works under python -I too
from rclib import Campaign, append_card, ids_in, norm, now, num, set_fields, state_hash, utf8_stdout

ACTIVE = {"scouting", "attacking"}
DEAD = {"killed", "blocked"}
MARKERS = {
    "lit": ["MEMORY CAP:", "RETURN WHEN:"],
    "read": ["MEMORY CAP:", "RETURN WHEN:"],
    "quant": ["MEMORY CAP:", "RETURN WHEN:"],
    "tool": ["TARGET:", "MEMORY CAP:", "KNOWN BARRIERS:", "RETURN WHEN:"],
    "scout": ["TARGET:", "MEMORY CAP:", "KNOWN BARRIERS:", "RETURN WHEN:"],
    "attack": ["TARGET:", "MEMORY CAP:", "KNOWN BARRIERS:", "RETURN WHEN:"],
    "referee": ["RESULT UNDER CHECK:", "MEMORY CAP:", "RETURN WHEN:"],
    "audit": ["TARGET:", "MEMORY CAP:", "RETURN WHEN:"],
    "paper": ["MEMORY CAP:", "RETURN WHEN:"],
    "lean": ["MEMORY CAP:", "RETURN WHEN:"],
    "other": ["MEMORY CAP:"],
}
ROUTE_REQUIRED = ["method_class", "node", "mechanism", "needed", "memory_gb"]


def check(c: Campaign, a) -> list[str]:
    bad = []
    b, _ = c.budget()
    t = c.target
    tstat = t.get("target_status", "none").lower()

    # ---------------- budget (always)
    run = c.running()
    used = sum(float(r.get("memory_gb", 0) or 0) for r in run)
    if len(run) + 1 > b["max_concurrent_agents"]:
        bad.append(f"budget: {len(run)} agents already running (max {b['max_concurrent_agents']}) -> queue it")
    if a.mem > b["per_agent_memory_gb"]:
        bad.append(f"budget: {a.mem} GB > per-agent cap {b['per_agent_memory_gb']} GB")
    if used + a.mem > b["total_memory_gb"]:
        bad.append(f"budget: {used:g} GB in use + {a.mem} GB > total {b['total_memory_gb']} GB -> queue it")

    # ---------------- target gating
    if a.kind in ("scout", "attack") and tstat != "confirmed":
        bad.append(f"target: TARGET status is '{tstat}', needs 'confirmed' (user saw target card + tree)")
    if a.kind == "tool" and tstat not in ("cross-checked", "confirmed"):
        bad.append(f"target: TARGET status is '{tstat}', tool hunt needs 'cross-checked'")
    if a.kind == "quant" and not c.p("lit_pool.md").exists():
        bad.append("literature: lit_pool.md missing -> run merge_pool.py after the pool phases first")

    # ---------------- routes
    if a.kind in ("scout", "attack"):
        routes = c.routes()
        r = routes.get(a.route or "")
        if not r:
            return bad + [f"route: card {a.route} not found in routes.md"]
        miss = [k for k in ROUTE_REQUIRED if not r.get(k, "").strip()]
        if miss:
            bad.append(f"route {a.route}: missing fields {', '.join(miss)}")
        verdict = r.get("verdict", "pending").upper() or "PENDING"
        if a.kind == "scout" and verdict not in ("PENDING", "UNCERTAIN", ""):
            bad.append(f"route {a.route}: verdict already {verdict}; scouts only fill pending/uncertain ceilings")
        if a.kind == "attack":
            if verdict == "CONJ":
                if r.get("user_approved", "").lower() not in ("yes", "y", "true"):
                    bad.append(f"route {a.route}: conjecture-strength needs user_approved: yes")
            elif verdict != "GO":
                bad.append(f"route {a.route}: verdict is {verdict}, attack needs GO")
            for k in ("ceiling", "derivation"):
                if not r.get(k, "").strip():
                    bad.append(f"route {a.route}: '{k}' empty — the ceiling gate has not run")
            need, ceil, better = num(r.get("needed_value")), num(r.get("ceiling_value")), r.get("better", "").lower()
            if better in ("higher", "lower"):
                if need is None or ceil is None:
                    bad.append(f"route {a.route}: needed_value/ceiling_value must be numbers when better={better}")
                elif (better == "higher" and ceil < need) or (better == "lower" and ceil > need):
                    bad.append(f"route {a.route}: ceiling {ceil:g} does not meet needed {need:g} (better={better})")
            elif better not in ("n/a", "na"):
                bad.append(f"route {a.route}: set better: higher | lower | n/a")
        # dedup against siblings with the same method class on the same node
        mc, node = norm(r.get("method_class", "")), r.get("node", "").strip()
        differs = r.get("differs_from", "")
        for oid, o in routes.items():
            if oid == a.route or norm(o.get("method_class", "")) != mc or o.get("node", "").strip() != node:
                continue
            ost = o.get("status", "").lower()
            if ost in ACTIVE and (oid not in differs or len(differs) < 20):
                bad.append(f"dedup: {oid} ({ost}) has the same method class '{mc}' on node {node}; "
                           f"merge, or write differs_from naming {oid} and the real difference")
            if ost in DEAD:
                byp = ids_in(r.get("bypasses", ""))
                known = set(c.barriers())
                if oid not in differs or not (byp & known):
                    bad.append(f"dedup: {oid} with method class '{mc}' was {ost}; relaunch needs differs_from "
                               f"naming {oid} and bypasses: <barrier ID it gets around>")
        active_here = [oid for oid, o in routes.items()
                       if oid != a.route and o.get("node", "").strip() == node and o.get("status", "").lower() in ACTIVE]
        if len(active_here) >= b.get("max_active_per_or_node", 2):
            bad.append(f"schedule: node {node} already has {len(active_here)} active routes "
                       f"({', '.join(active_here)}) -> queue it")

    # ---------------- results: one check per version
    if a.kind == "referee":
        res = c.results().get(a.result or "")
        if not res:
            bad.append(f"result: {a.result} not in results.md (register it first)")
        else:
            cs = res.get("check_status", "none").lower() or "none"
            if cs != "none":
                bad.append(f"result {a.result} v{res.get('version', '1')} already has its one check "
                           f"({cs}, by {res.get('check_by', '?')}); bump version only if the result changed")

    # ---------------- prompt
    if not a.prompt:
        bad.append("prompt: pass --prompt <file> (generate it with make_prompt.py)")
    else:
        pf = Path(a.prompt)
        if not pf.exists():
            bad.append(f"prompt: {pf} not found")
        else:
            text = pf.read_text(encoding="utf-8")
            for mk in MARKERS.get(a.kind, []):
                if mk not in text:
                    bad.append(f"prompt: marker '{mk}' missing")
            if a.kind in ("attack", "scout"):
                if a.route and a.route not in text:
                    bad.append(f"prompt: does not mention route {a.route}")
                tv = t.get("target_value", "").strip()
                if tv and tv not in text:
                    bad.append(f"prompt: current target value '{tv}' not in prompt (stale prompt?) -> regenerate")
            if a.kind in ("attack", "scout", "referee", "tool"):
                m = re.search(r"STATE-HASH: (\w+)", text)
                now_hash = state_hash(c, a.route or "", a.result or "")
                if not m:
                    bad.append("prompt: no STATE-HASH stamp -> generate it with make_prompt.py")
                elif m.group(1) != now_hash:
                    bad.append("prompt: stale — target, route/result card or barrier list changed since it was "
                               "generated -> rerun make_prompt.py")
    return bad


def main():
    utf8_stdout()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir")
    ap.add_argument("--kind", required=True, choices=list(MARKERS))
    ap.add_argument("--label", required=True)
    ap.add_argument("--mem", type=float, default=None, help="GB for this agent (default: route card memory_gb)")
    ap.add_argument("--prompt")
    ap.add_argument("--route")
    ap.add_argument("--result")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    c = Campaign(a.dir)
    if a.mem is None:
        r = c.routes().get(a.route or "", {})
        a.mem = num(r.get("memory_gb")) if r else None
        if a.mem is None:
            ap.error("--mem is required (no route card memory_gb to fall back on)")
    bad = check(c, a)
    if bad:
        print(f"REJECT {a.label} ({a.kind}):")
        for x in bad:
            print("  - " + x)
        sys.exit(1)
    if a.dry_run:
        print(f"PASS (dry run) {a.label} ({a.kind})")
        return
    lid = c.next_id(c.p("ledger.md"), "L")
    append_card(c.p("ledger.md"), lid, f"{a.kind} {a.label}", {
        "kind": a.kind, "label": a.label, "route": a.route or "", "result": a.result or "",
        "memory_gb": f"{a.mem:g}", "prompt": a.prompt, "started": now(), "status": "running",
    })
    if a.kind in ("scout", "attack"):
        set_fields(c.p("routes.md"), a.route, {"status": "scouting" if a.kind == "scout" else "attacking",
                                               "agent": f"{a.label} ({lid})"})
    if a.kind == "referee":
        set_fields(c.p("results.md"), a.result, {"check_status": "pending", "check_by": a.label,
                                                 "check_ref": lid})
    print(f"PASS {a.label} ({a.kind}) -> ledger {lid}. Launch the agent now; when it returns run "
          f"finish_run.py {a.dir} {lid} ...")


if __name__ == "__main__":
    main()
