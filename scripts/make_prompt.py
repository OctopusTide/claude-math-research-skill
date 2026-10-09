"""Generate a subagent prompt file from a template plus the campaign's current state.

make_prompt.py <campaign dir> --kind <kind> --label <label> --mem <GB>
               [--route Rxx] [--result RES-xx] [--node Nx] [--extra "text"] [--extra-file F]

Writes prompts_out/<label>.md and prints its path. Launch the agent with a SHORT prompt that points at the
file ("Read your full instructions in <path> and follow them."), so the long text never enters the
coordinator's context. Then gate it: check_launch.py ... --prompt <path>.
"""
import argparse
import re
from pathlib import Path

import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # works under python -I too
from rclib import SKILL_DIR, Campaign, card_map, card_text, config, ids_in, num, state_hash, utf8_stdout

KINDS = ["lit_sweep", "lit_verify", "lit_read", "quant", "tool", "scout", "attack", "referee",
         "audit_logic", "audit_numerics", "audit_lit", "paper", "lean"]
GATE_KIND = {"lit_sweep": "lit", "lit_verify": "lit", "lit_read": "read", "audit_logic": "audit",
             "audit_numerics": "audit", "audit_lit": "audit"}


def memory_line(gb: float) -> str:
    if gb <= 0:
        return ("MEMORY CAP: 0 GB of heavy compute. Light scripts only (< 1 GB, no JVM batches, no parallel "
                "processes).")
    xmx = max(1, int(gb) - 1)
    return (f"MEMORY CAP: {gb:g} GB for everything you start. At most ONE JVM at a time with -Xmx{xmx}g (or one "
            f"Python process of comparable size); no parallel batch runners.")


def target_block(c: Campaign) -> str:
    t = c.target
    if not t.get("target_value") and not t.get("statement"):
        return ("TARGET: not yet quantified. Goal in the user's words: " + c.meta.get("goal_verbatim", "")
                + "\n(Do not invent a target number; report what you find in your own units.)")
    return (f"TARGET: {t.get('statement', '')}\n"
            f"  value {t.get('target_value', '')} {t.get('unit', '')} (better = {t.get('better', '')}); "
            f"current record {t.get('record_value', '')}; status {t.get('target_status', '')}\n"
            f"  chain: {t.get('chain', '')}\n"
            f"  ladder: {t.get('ladder', '')}\n"
            f"  sensitivity: {t.get('sensitivity', '')}")


def barriers_block(c: Campaign) -> str:
    bars = c.barriers()
    if not bars:
        return "KNOWN BARRIERS: none registered yet."
    out = ["KNOWN BARRIERS: do not re-derive these; if your route runs into one, stop and report it."]
    for bid, b in bars.items():
        out.append(f"- {bid} {b['_title']}: {b.get('statement', '')} [scope: {b.get('scope', '')}; "
                   f"evidence: {b.get('evidence', '')}]")
    return "\n".join(out)


def pool_notes(c: Campaign, ids: set) -> str:
    pool = card_map(c.p("lit_pool.md"))
    got = [card_text(c.p("lit_pool.md"), i) for i in sorted(ids) if i in pool]
    if not got:
        return "(no specific pool entries attached; consult lit_pool.md's index)"
    return "\n\n".join(got)


def main():
    utf8_stdout()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir")
    ap.add_argument("--kind", required=True, choices=KINDS)
    ap.add_argument("--label", required=True)
    ap.add_argument("--mem", type=float)
    ap.add_argument("--route")
    ap.add_argument("--result")
    ap.add_argument("--node")
    ap.add_argument("--extra", default="")
    ap.add_argument("--extra-file")
    a = ap.parse_args()
    c = Campaign(a.dir)
    route = c.routes().get(a.route or "", {})
    if a.mem is None:
        a.mem = num(route.get("memory_gb")) if route else 0.0
        a.mem = a.mem or 0.0
    node = a.node or route.get("node", "")
    extra = a.extra
    if a.extra_file:
        extra += "\n" + Path(a.extra_file).read_text(encoding="utf-8")

    pool_ids = ids_in(route.get("inputs", "")) if route else set()
    result_card = ""
    if a.result:
        result_card = card_text(c.p("results.md"), a.result)
        pool_ids |= ids_in(c.results().get(a.result, {}).get("depends_on", ""))
    if node and node in c.nodes():
        pool_ids |= ids_in(c.nodes()[node].get("inputs", ""))

    run_file = c.p("runs") / f"{a.label}.md"
    shard = c.p("lit_pool") / f"{a.label}.md"
    subs = {
        "LABEL": a.label,
        "CAMPAIGN_DIR": str(c.dir),
        "GOAL": c.meta.get("goal_verbatim", ""),
        "TARGET_BLOCK": target_block(c),
        "UNIT": c.target.get("unit", "") or "(not fixed yet)",
        "MEMORY_CAP": memory_line(a.mem),
        "BARRIERS_BLOCK": barriers_block(c),
        "ROUTE_ID": a.route or "",
        "ROUTE_CARD": card_text(c.p("routes.md"), a.route) if a.route else "",
        "NODE_ID": node,
        "NODE_CARD": card_text(c.p("tree.md"), node) if node else "",
        "TREE_FILE": str(c.p("tree.md")),
        "POOL_NOTES": pool_notes(c, pool_ids),
        "RESULT_ID": a.result or "",
        "RESULT_CARD": result_card,
        "RUN_FILE": str(run_file),
        "SHARD_FILE": str(shard),
        "SHARD_PREFIX": "P-" + re.sub(r"[^A-Za-z0-9]", "", a.label) + "-",
        "PACKAGE_DIR": str(c.p("package")),
        "EXTRA": extra.strip() or "(none)",
    }
    cfg = config()
    subs["LEAN_TOOLCHAIN"] = (
        (f"Lean toolchain: {cfg['lean_bin']} (lean, lake; may not be on PATH). " if cfg["lean_bin"]
         else "Lean toolchain: lean and lake from PATH (elan). ")
        + (f"A local Mathlib cache is in {cfg['mathlib_cache']}: unpack it instead of downloading." if cfg["mathlib_cache"]
           else "Get Mathlib's prebuilt cache with `lake exe cache get`."))
    subs["TYPESETTING"] = (f"render a readable HTML version with the typesetting tool at {cfg['typesetting']}"
                           if cfg["typesetting"] else "render a readable HTML version (e.g. Markdown with MathJax/KaTeX)")
    common = (SKILL_DIR / "prompts" / "_common.md").read_text(encoding="utf-8")
    body = (SKILL_DIR / "prompts" / f"{a.kind}.md").read_text(encoding="utf-8")
    text = body.replace("{{COMMON_RULES}}", common)
    for k, v in subs.items():
        text = text.replace("{{" + k + "}}", v)
    left = sorted(set(re.findall(r"\{\{([A-Z_]+)\}\}", text)))
    if left:
        print("warning: unfilled placeholders:", ", ".join(left))
    text = text.rstrip() + f"\n\n<!-- STATE-HASH: {state_hash(c, a.route or '', a.result or '')} -->\n"
    out = c.p("prompts_out") / f"{a.label}.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(text, encoding="utf-8")
    gate = GATE_KIND.get(a.kind, a.kind)
    print(out)
    print(f"next: check_launch.py \"{c.dir}\" --kind {gate} --label {a.label} --mem {a.mem:g} --prompt \"{out}\""
          + (f" --route {a.route}" if a.route else "") + (f" --result {a.result}" if a.result else ""))
    print(f"agent prompt: Read your full instructions in {out} and follow them exactly.")


if __name__ == "__main__":
    main()
