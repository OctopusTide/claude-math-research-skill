"""Shared helpers for the research-campaign scripts.

Stdlib only; needs Python >= 3.11 (tomllib).

All campaign state lives in Markdown "card" files. A card is a level-2 heading whose first word is the card ID,
followed by "- key: value" lines. Indented lines continue the previous value. Anything inside ``` fences is
ignored, so templates can carry examples.
"""
from __future__ import annotations

import datetime
import json
import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_BUDGET = {
    "max_concurrent_agents": 4,
    "total_memory_gb": 8,
    "per_agent_memory_gb": 4,
    "max_active_per_or_node": 2,
}
DEFAULT_CONFIG = {
    "python": "",           # interpreter for the scripts; empty = python/python3 on PATH
    "projects_root": "",    # where research projects live; empty = ask the user
    "lean_bin": "",         # folder with lean/lake; empty = use PATH
    "mathlib_cache": "",    # local Mathlib cache; empty = `lake exe cache get`
    "typesetting": "",      # optional HTML math renderer for papers when no TeX engine exists
}


def _load_toml(files, base: dict) -> tuple[dict, list[str]]:
    out, src = dict(base), ["built-in defaults"]
    for f in files:
        if f.exists():
            with open(f, "rb") as fh:
                out.update(tomllib.load(fh))
            src.append(str(f))
    return out, src


def config() -> dict:
    """Machine settings: config.toml (shipped, generic) overridden by config.local.toml (this machine's)."""
    return _load_toml((SKILL_DIR / "config.toml", SKILL_DIR / "config.local.toml"), DEFAULT_CONFIG)[0]

HEAD = re.compile(r"^## +(\S+)[ \t]*(.*)$")
FIELD = re.compile(r"^- +([A-Za-z_][\w-]*):[ \t]?(.*)$")


def utf8_stdout() -> None:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:
            pass


def now() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def today() -> str:
    return datetime.date.today().isoformat()


# ---------------------------------------------------------------- cards

def _blocks(lines):
    """Yield (start, end, id, title) for every card heading outside code fences."""
    fence = False
    heads = []
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if not fence:
            m = HEAD.match(line)
            if m:
                heads.append((i, m.group(1), m.group(2).strip()))
    for k, (i, cid, title) in enumerate(heads):
        end = heads[k + 1][0] if k + 1 < len(heads) else len(lines)
        yield i, end, cid, title


def read_cards(path: Path) -> list[dict]:
    path = Path(path)
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    cards = []
    for start, end, cid, title in _blocks(lines):
        card = {"_id": cid, "_title": title, "_file": str(path)}
        last = None
        fence = False
        for line in lines[start + 1:end]:
            if line.lstrip().startswith("```"):
                fence = not fence
                continue
            if fence:
                continue
            f = FIELD.match(line)
            if f:
                last = f.group(1).lower()
                card[last] = f.group(2).strip()
            elif last and line.startswith("  ") and line.strip():
                card[last] = (card[last] + "\n" + line.strip()).strip()
            elif not line.strip():
                last = None
        cards.append(card)
    return cards


def card_map(path: Path) -> dict:
    return {c["_id"]: c for c in read_cards(path)}


def _render_field(key: str, value) -> list[str]:
    parts = str(value).splitlines() or [""]
    out = [f"- {key}: {parts[0]}".rstrip()]
    out += ["  " + p for p in parts[1:]]
    return out


def set_fields(path: Path, card_id: str, updates: dict) -> None:
    """Edit fields of one card in place, leaving the rest of the file untouched."""
    path = Path(path)
    lines = path.read_text(encoding="utf-8").splitlines()
    for start, end, cid, _ in _blocks(lines):
        if cid != card_id:
            continue
        block = lines[start:end]
        for key, value in updates.items():
            idx = None
            for j, line in enumerate(block):
                f = FIELD.match(line)
                if f and f.group(1).lower() == key.lower():
                    idx = j
                    break
            new = _render_field(key, value)
            if idx is not None:
                stop = idx + 1
                while stop < len(block) and block[stop].startswith("  ") and block[stop].strip():
                    stop += 1
                block[idx:stop] = new
            else:
                last_field = 0
                for j, line in enumerate(block):
                    if FIELD.match(line) or (line.startswith("  ") and j > 0 and line.strip()):
                        last_field = j
                block[last_field + 1:last_field + 1] = new
        lines[start:end] = block
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return
    raise KeyError(f"card {card_id} not found in {path}")


def append_card(path: Path, card_id: str, title: str, fields: dict, body: str = "") -> None:
    path = Path(path)
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    out = [f"## {card_id} {title}".rstrip()]
    for k, v in fields.items():
        out += _render_field(k, v)
    if body:
        out += ["", body.rstrip()]
    sep = "" if text.endswith("\n\n") or not text else ("\n" if text.endswith("\n") else "\n\n")
    path.write_text(text + sep + "\n".join(out) + "\n\n", encoding="utf-8")


def card_text(path: Path, card_id: str) -> str:
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    for start, end, cid, _ in _blocks(lines):
        if cid == card_id:
            return "\n".join(lines[start:end]).strip()
    return ""


# ---------------------------------------------------------------- campaign

class Campaign:
    def __init__(self, d):
        self.dir = Path(d).resolve()
        if not (self.dir / "CAMPAIGN.md").exists():
            sys.exit(f"Not a campaign folder (no CAMPAIGN.md): {self.dir}")

    def p(self, name: str) -> Path:
        return self.dir / name

    @property
    def meta(self) -> dict:
        return card_map(self.p("CAMPAIGN.md")).get("META", {})

    @property
    def target(self) -> dict:
        return card_map(self.p("CAMPAIGN.md")).get("TARGET", {})

    def routes(self) -> dict:
        return card_map(self.p("routes.md"))

    def nodes(self) -> dict:
        return card_map(self.p("tree.md"))

    def barriers(self) -> dict:
        return card_map(self.p("barriers.md"))

    def results(self) -> dict:
        return card_map(self.p("results.md"))

    def ledger(self) -> dict:
        return card_map(self.p("ledger.md"))

    def running(self) -> list[dict]:
        return [c for c in self.ledger().values() if c.get("status", "").lower() == "running"]

    def budget(self) -> tuple[dict, list[str]]:
        """budget.toml (shipped) < budget.local.toml (the user's machine) < the campaign's own budget.toml."""
        return _load_toml((SKILL_DIR / "budget.toml", SKILL_DIR / "budget.local.toml", self.p("budget.toml")),
                          DEFAULT_BUDGET)

    def next_id(self, path: Path, prefix: str, width: int = 3) -> str:
        n = 0
        for cid in card_map(path):
            m = re.fullmatch(re.escape(prefix) + r"(\d+)", cid)
            if m:
                n = max(n, int(m.group(1)))
        return f"{prefix}{n + 1:0{width}d}"


def num(x):
    try:
        return float(str(x).split()[0])
    except Exception:
        return None


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")


def ids_in(text: str) -> set[str]:
    return set(re.findall(r"\b[A-Z][A-Z0-9]*-?[A-Za-z0-9]*-?\d+\b", str(text)))


VOLATILE = {"status", "agent", "outcome", "blocked_by", "check_status", "check_by", "check_ref", "frozen",
            "history", "user_approved", "target_status"}


def state_hash(c: "Campaign", route: str = "", result: str = "") -> str:
    """Fingerprint of everything a prompt was built from (target, route/result card, barrier list).
    make_prompt.py stamps it into the prompt; check_launch.py rejects the prompt if the state moved since."""
    import hashlib

    def stable(card: dict) -> list:
        return sorted((k, v) for k, v in card.items() if not k.startswith("_") and k not in VOLATILE)

    parts = [stable(c.target), sorted(c.barriers())]
    if route:
        parts.append(stable(c.routes().get(route, {})))
    if result:
        parts.append(stable(c.results().get(result, {})))
    return hashlib.sha1(json.dumps(parts, ensure_ascii=False).encode("utf-8")).hexdigest()[:12]


# ---------------------------------------------------------------- tree propagation

ROUTE_SOLVED = {"done", "solved"}
ROUTE_BLOCKED = {"killed", "blocked"}


def route_state(r: dict) -> str:
    st = r.get("status", "").lower()
    if st in ROUTE_SOLVED and r.get("outcome", "positive").lower() != "negative":
        return "solved"
    if st in ROUTE_BLOCKED or (st in ROUTE_SOLVED and r.get("outcome", "").lower() == "negative"):
        return "blocked"
    return "open"


def propagate(c: Campaign) -> dict:
    """Return {node_id: (state, reason)} computed bottom-up from routes."""
    nodes, routes = c.nodes(), c.routes()
    kids = {nid: [] for nid in nodes}
    for nid, n in nodes.items():
        par = n.get("parent", "").strip()
        if par in kids:
            kids[par].append(("node", nid))
    for rid, r in routes.items():
        nd = r.get("node", "").strip()
        if nd in kids:
            kids[nd].append(("route", rid))
    memo: dict = {}

    def state(nid, depth=0):
        if nid in memo:
            return memo[nid]
        if depth > 50:
            return ("open", "cycle?")
        n = nodes[nid]
        override = n.get("status_override", "").lower()
        if override in ("solved", "blocked", "open"):
            memo[nid] = (override, "override")
            return memo[nid]
        ch = []
        for kind, x in kids[nid]:
            ch.append((x, state(x, depth + 1)[0] if kind == "node" else route_state(routes[x])))
        typ = n.get("type", "OR").upper()
        if not ch:
            res = ("open", "no routes yet")
        elif typ == "AND":
            if any(s == "blocked" for _, s in ch):
                res = ("blocked", "AND child blocked: " + ", ".join(x for x, s in ch if s == "blocked"))
            elif all(s == "solved" for _, s in ch):
                res = ("solved", "all AND children solved")
            else:
                res = ("open", "")
        else:
            if any(s == "solved" for _, s in ch):
                res = ("solved", "OR child solved: " + ", ".join(x for x, s in ch if s == "solved"))
            elif all(s == "blocked" for _, s in ch):
                res = ("blocked", "all OR children blocked: " + ", ".join(x for x, _ in ch))
            else:
                res = ("open", "")
        memo[nid] = res
        return res

    return {nid: state(nid) for nid in nodes}, kids


def barrier_convergence(c: Campaign, k: int = 3) -> list[tuple[str, set]]:
    """Barriers that blocked routes from >= k distinct method classes (stop-rule signal)."""
    hits: dict[str, set] = {}
    for r in c.routes().values():
        for b in ids_in(r.get("blocked_by", "")):
            hits.setdefault(b, set()).add(norm(r.get("method_class", "?")))
    return [(b, cls) for b, cls in hits.items() if len(cls) >= k]


# ---------------------------------------------------------------- machine state (Windows, Linux, macOS)

def _ps(cmd: str):
    try:
        out = subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, text=True,
                             timeout=30, encoding="utf-8", errors="replace").stdout.strip()
        return json.loads(out) if out else None
    except Exception:
        return None


def memory_gb():
    """(free_gb, total_gb) or (None, None)."""
    if os.name == "nt":
        j = _ps("Get-CimInstance Win32_OperatingSystem | Select-Object FreePhysicalMemory,TotalVisibleMemorySize"
                " | ConvertTo-Json")
        if j:
            return round(j["FreePhysicalMemory"] / 1048576, 1), round(j["TotalVisibleMemorySize"] / 1048576, 1)
        return None, None
    try:
        info = dict(l.split(":", 1) for l in Path("/proc/meminfo").read_text().splitlines())
        kb = lambda k: int(info[k].split()[0])
        return round(kb("MemAvailable") / 1048576, 1), round(kb("MemTotal") / 1048576, 1)
    except Exception:
        pass
    try:  # macOS
        total = int(subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True,
                                   timeout=10).stdout.strip())
        vm = subprocess.run(["vm_stat"], capture_output=True, text=True, timeout=10).stdout
        page = int(re.search(r"page size of (\d+)", vm).group(1))
        pages = sum(int(re.search(rf"{k}:\s+(\d+)", vm).group(1)) for k in ("Pages free", "Pages inactive"))
        return round(pages * page / 2**30, 1), round(total / 2**30, 1)
    except Exception:
        return None, None


HEAVY = ("java", "javaw", "python", "pythonw", "python3", "lean", "lake")


def heavy_processes():
    """List of (name, pid, mb) for java/python/lean processes, excluding this script."""
    me = {os.getpid(), os.getppid()}
    if os.name == "nt":
        j = _ps("Get-Process java,javaw,python,pythonw,lean,lake -ErrorAction SilentlyContinue | "
                "Select-Object Name,Id,@{n='MB';e={[int]($_.WorkingSet64/1MB)}} | ConvertTo-Json")
        if j is None:
            return []
        if isinstance(j, dict):
            j = [j]
        return [(x["Name"], x["Id"], x["MB"]) for x in j if x["Id"] not in me]
    try:
        out = subprocess.run(["ps", "-axo", "pid=,rss=,comm="], capture_output=True, text=True,
                             timeout=10).stdout
    except Exception:
        return []
    procs = []
    for line in out.splitlines():
        parts = line.split(None, 2)
        if len(parts) < 3:
            continue
        name = Path(parts[2]).name
        if name.startswith(HEAVY) and int(parts[0]) not in me:
            procs.append((name, int(parts[0]), int(parts[1]) // 1024))
    return procs
