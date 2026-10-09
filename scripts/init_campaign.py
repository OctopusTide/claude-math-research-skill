"""Phase 0: start a campaign, or resume / inherit into an existing one.

New:      init_campaign.py --project <project dir> --name <slug> --goal "<user's words>"
Resume:   init_campaign.py --dir <campaign dir>
Inherit:  init_campaign.py --dir <campaign dir> --inherit-from <older campaign dir>

Prints the kickoff report that the coordinator relays to the user (in the user's language) before anything is
launched.
"""
import argparse
import shutil
from pathlib import Path

import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # works under python -I too
from rclib import (SKILL_DIR, Campaign, append_card, heavy_processes, memory_gb, read_cards, today,
                   utf8_stdout)
import status as status_mod


def machine_lines(budget: dict) -> list[str]:
    out = []
    free, total = memory_gb()
    if free is not None:
        warn = "  WARNING: below the budget's total memory" if free < budget["total_memory_gb"] else ""
        out.append(f"  machine: {free} GB free of {total} GB{warn}")
    procs = heavy_processes()
    if procs:
        agg: dict = {}
        for name, pid, mb in procs:
            n, m, pids = agg.get(name, (0, 0, []))
            agg[name] = (n + 1, m + mb, pids + [pid])
        desc = "; ".join(f"{k} x{n} (~{m / 1024:.1f} GB, PID {', '.join(map(str, p[:6]))})"
                         for k, (n, m, p) in agg.items())
        out.append(f"  leftover processes: {desc}  <- reported only; never killed without the user")
    else:
        out.append("  leftover processes: no java/python/lean processes")
    return out


def prior_campaigns(project: Path, exclude: Path) -> list[str]:
    root = project / "campaigns"
    out = []
    if not root.exists():
        return out
    for d in sorted(root.iterdir()):
        if not d.is_dir() or d.resolve() == exclude.resolve() or not (d / "CAMPAIGN.md").exists():
            continue
        pool = sum(len(read_cards(f)) for f in (d / "lit_pool").glob("*.md") if f.name != "README.md")
        bars = len(read_cards(d / "barriers.md"))
        out.append(f"  inheritable: {d.name}: {pool} pool entries + {bars} barriers (as of {d.name[:10]})")
    return out


def create(project: Path, name: str, goal: str, date: str) -> Path:
    d = project / "campaigns" / f"{date}-{name}"
    if d.exists():
        print(f"[exists] {d} -- switching to resume mode.\n")
        return d
    shutil.copytree(SKILL_DIR / "templates" / "campaign", d)
    for sub in ("runs", "prompts_out", "lit_pool", "package"):
        (d / sub).mkdir(exist_ok=True)
    camp = d / "CAMPAIGN.md"
    text = camp.read_text(encoding="utf-8")
    for k, v in {"{{NAME}}": name, "{{GOAL}}": goal, "{{DATE}}": date, "{{PROJECT}}": str(project),
                 "{{DIR}}": str(d)}.items():
        text = text.replace(k, v)
    camp.write_text(text, encoding="utf-8")
    c = Campaign(d)
    b, src = c.budget()
    lines = [f"New campaign {name}",
             f"  folder: {d}",
             f"  goal (verbatim): {goal}",
             f"  budget (from {src[-1]}): at most {b['max_concurrent_agents']} agents, "
             f"{b['total_memory_gb']} GB in total, <= {b['per_agent_memory_gb']} GB per agent"]
    lines += machine_lines(b)
    lines += prior_campaigns(project, d) or ["  inheritable: no earlier campaigns in this project"]
    lines.append("Next: launch the L0 rough literature sweep. Ask the user whether to change the goal wording, the "
                 "budget (budget.local.toml), leftover processes or inheritance; otherwise wait for their go.")
    print("\n".join(lines))
    return None


def inherit(dst: Path, src: Path) -> None:
    c = Campaign(dst)
    n_pool = n_bar = 0
    for f in sorted((src / "lit_pool").glob("*.md")):
        if f.name == "README.md":
            continue
        target = dst / "lit_pool" / f"inherited_{src.name}_{f.name}"
        target.write_text(f"<!-- inherited from {src} on {today()}; entries keep their original IDs -->\n"
                          + f.read_text(encoding="utf-8"), encoding="utf-8")
        n_pool += len(read_cards(f))
    have = c.barriers()
    for b in read_cards(src / "barriers.md"):
        if b["_id"] in have:
            continue
        fields = {k: v for k, v in b.items() if not k.startswith("_")}
        fields["inherited_from"] = f"{src.name} ({today()})"
        append_card(dst / "barriers.md", b["_id"], b["_title"], fields)
        n_bar += 1
    print(f"Inherited {src.name}: {n_pool} pool entries (shards copied; run merge_pool.py), {n_bar} barriers. "
          f"L0 only needs to sweep what is newer than {src.name[:10]}.")


def main():
    utf8_stdout()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project")
    ap.add_argument("--name")
    ap.add_argument("--goal")
    ap.add_argument("--date", default=today())
    ap.add_argument("--dir")
    ap.add_argument("--inherit-from")
    a = ap.parse_args()
    if a.dir:
        d = Path(a.dir)
        if a.inherit_from:
            inherit(d, Path(a.inherit_from))
            return
        status_mod.report(Campaign(d))
        return
    if not (a.project and a.name and a.goal):
        ap.error("new campaign needs --project, --name and --goal (or use --dir to resume)")
    existing = create(Path(a.project).resolve(), a.name, a.goal, a.date)
    if existing:
        status_mod.report(Campaign(existing))


if __name__ == "__main__":
    main()
