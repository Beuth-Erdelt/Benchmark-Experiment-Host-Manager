#!/usr/bin/env python3
import argparse
import os
import re
import sys
from typing import List, Tuple, Optional
import yaml  # PyYAML

# -------- Parsing of --set selectors --------

SELECTOR_RE = re.compile(
    r'^(?P<kind>deployment|statefulset)\[(?P<workload>[^\]]+)\]\.container\[(?P<container>[^\]]+)\]\.(?P<param>[A-Za-z0-9_]+)$',
    re.IGNORECASE
)

def parse_set_arg(s: str) -> Tuple[dict, str]:
    """
    Parses a single --set argument of the form:
      <selector>=<value>
    where selector is:
      deployment[NAME].container[CONTAINER].PARAM
      statefulset[NAME].container[CONTAINER].PARAM
    Returns: (selector_dict, value_str)
    """
    if "=" not in s:
        raise ValueError(f"--set expects selector=value (got: {s})")
    selector, value = s.split("=", 1)
    m = SELECTOR_RE.match(selector.strip())
    if not m:
        raise ValueError(
            "Invalid selector. Expected e.g. "
            "deployment[sut].container[dbms].max_worker_processes"
        )
    d = m.groupdict()
    d["kind"] = d["kind"].lower()
    return d, value.strip()

# -------- YAML helpers --------

def find_workloads(doc: dict, kind: str, name: str) -> bool:
    """
    Returns True if this YAML document is the desired kind+name.
    """
    k = doc.get("kind", "")
    if kind == "deployment" and k != "Deployment":
        return False
    if kind == "statefulset" and k != "StatefulSet":
        return False
    md = doc.get("metadata", {}) or {}
    return md.get("name") == name

def ensure_arg_pairs(args_list: Optional[List[str]], updates: List[Tuple[str, str]]) -> List[str]:
    """
    Given a container.args list (e.g. ["-c","max_connections=3000","-c","max_worker_processes=64"]),
    update or add the provided (key,value) pairs, returning the new list.
    """
    args = list(args_list or [])
    # Index existing "-c key=value" pairs
    pos_by_key = {}  # key -> index of the value token (not the "-c")
    i = 0
    while i < len(args) - 1:
        if args[i] == "-c":
            val = args[i+1]
            if isinstance(val, str) and "=" in val:
                k = val.split("=", 1)[0]
                pos_by_key[k] = i + 1
            i += 2
        else:
            i += 1

    # Apply updates
    for k, v in updates:
        if k in pos_by_key:
            args[pos_by_key[k]] = f"{k}={v}"
        else:
            args.extend(["-c", f"{k}={v}"])
    return args

def patch_container(doc: dict, container_name: str, param: str, value: str) -> bool:
    """
    Patches a single container's args in Deployment/StatefulSet doc.
    Returns True if changes were made.
    """
    spec = doc.get("spec", {}) or {}
    tpl = spec.get("template", {}) or {}
    pspec = tpl.get("spec", {}) or {}
    containers = pspec.get("containers", []) or []
    changed = False

    for c in containers:
        if c.get("name") != container_name:
            continue
        old_args = c.get("args", [])
        new_args = ensure_arg_pairs(old_args, [(param, value)])
        if new_args != old_args:
            c["args"] = new_args
            changed = True
    return changed

# -------- Main processing --------

def process(file_path: str, operations: List[Tuple[dict, str]]) -> bool:
    """
    Apply all operations across documents in the file.
    operations: list of (selector_dict, value_str).
    Returns True if any change occurred.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        docs = list(yaml.safe_load_all(f))

    any_changed = False
    print(type(docs))

    for sel, val in operations:
        kind = sel["kind"]          # deployment | statefulset
        workload = sel["workload"]  # resource name
        container = sel["container"]
        param = sel["param"]

        found_doc = False
        found_container = False
        changed_this = False

        for doc in docs:
            if not isinstance(doc, dict):
                continue
            if not find_workloads(doc, kind, workload):
                continue
            found_doc = True
            # patch container
            before = yaml.safe_dump(doc, sort_keys=False)
            if patch_container(doc, container, param, val):
                changed_this = True
                any_changed = True
            # track whether the container existed
            spec = doc.get("spec", {}) or {}
            tpl = spec.get("template", {}) or {}
            pspec = tpl.get("spec", {}) or {}
            containers = pspec.get("containers", []) or []
            if any(c.get("name") == container for c in containers):
                found_container = True

        if not found_doc:
            print(f"[WARN] {kind}[{workload}] not found in file.", file=sys.stderr)
        elif not found_container:
            print(f"[WARN] container[{container}] not found in {kind}[{workload}].", file=sys.stderr)
        elif changed_this:
            print(f"[OK]   Updated {kind}[{workload}].container[{container}].{param} = {val}")
        else:
            print(f"[SKIP] {kind}[{workload}].container[{container}].{param} already set to desired value.")

    if any_changed:
        backup = file_path + ".bak"
        if not os.path.exists(backup):
            with open(backup, "w", encoding="utf-8") as b:
                yaml.safe_dump_all(docs, b, sort_keys=False)
        with open(file_path, "w", encoding="utf-8") as out:
            yaml.safe_dump_all(docs, out, sort_keys=False)

    return any_changed

def main():
    ap = argparse.ArgumentParser(description="Patch -c key=value args in K8s Deployment/StatefulSet containers.")
    ap.add_argument("--file", required=True, help="Path to YAML manifest (multi-doc supported).")
    ap.add_argument("--set", dest="sets", action="append", default=[],
                    help=("Selector assignment, e.g. "
                          "deployment[sut].container[dbms].max_worker_processes=128"))
    args = ap.parse_args()
    print(args)

    if not args.sets:
        print("No --set provided.", file=sys.stderr)
        return 2

    operations = []
    for s in args.sets:
        sel, value = parse_set_arg(s)
        operations.append((sel, value))
    print(operations)

    changed = process(args.file, operations)
    return 0 if changed else 0  # 0 either way; warnings printed for misses

if __name__ == "__main__":
    sys.exit(main())