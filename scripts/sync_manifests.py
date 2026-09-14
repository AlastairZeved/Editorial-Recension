#!/usr/bin/env python3
"""Keep every client manifest in sync with the package's single source of truth.

Source of truth: ./plugin.json — the Agent Plugins 1.0 portable manifest at the
package root. Identity (name, version, description, author, repository, license)
is read from there and never re-typed in a client adapter.

Generated files (never edit these by hand — run this script instead):

  .claude-plugin/plugin.json                       Claude Code plugin manifest
  .claude-plugin/marketplace.json                  Claude Code marketplace, also consumed by
                                                   VS Code via chat.plugins.marketplaces
  .github/plugin/marketplace.json                  GitHub Copilot CLI marketplace
  .agents/plugins/marketplace.json                 Codex CLI repo marketplace
  .agents/plugins/editorial-recension/plugin.json  Google Antigravity workspace plugin marker
  .agents/plugins/editorial-recension/skills       symlink -> ../../../skills

Modes:

  (no flags)    drift check + structural validation; exit 1 on any problem
  --write       rewrite every generated file from the source of truth
  --check       drift check only
  --validate    structural validation only

The drift check compares generated text byte for byte, so `git diff` stays empty
when the repository is in sync; CI runs this script and fails when it is not.
Standard library only, no network, no writes unless --write is passed.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Content that is not part of the portable manifest, kept in exactly one place.
# ---------------------------------------------------------------------------

# Marketplace listing copy. Rewritten into every marketplace file.
BLURB = (
    "Two-agent editing loop: an editor applies five named schemata, an evaluator "
    "scores blind before reading the editor's trace, and they loop until the text passes."
)

# Codex marketplace entry category (documented as required on every entry).
CODEX_CATEGORY = "Writing"

# Codex marketplace source: object form, as the OpenAI packaging docs specify
# ("Always include policy.installation, policy.authentication, and category").
CODEX_SOURCE_OBJECT = {"source": "local", "path": "./"}
CODEX_POLICY = {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}

# Claude/Copilot marketplace source: path relative to the marketplace root.
MARKETPLACE_SOURCE_PATH = "./"

# Google Antigravity plugin marker schema (antigravity.google/docs/cli/plugins/).
ANTIGRAVITY_SCHEMA = "https://antigravity.google/schemas/v1/plugin.json"

ANTIGRAVITY_DIR = ".agents/plugins/editorial-recension"
ANTIGRAVITY_SKILLS_LINK = "skills"
ANTIGRAVITY_SKILLS_TARGET = "../../../skills"

PLUGIN_SOURCE_KEYS = ("name", "version", "description", "author", "repository", "license")


def read_source(repo_root: str) -> dict:
    with open(os.path.join(repo_root, "plugin.json"), encoding="utf-8") as fh:
        plugin = json.load(fh)
    missing = [k for k in ("name", "version", "description") if not plugin.get(k)]
    if missing:
        raise SystemExit(f"plugin.json is missing required keys: {', '.join(missing)}")
    return plugin


def build_expected(plugin: dict) -> dict:
    """Return {relative path: file text} for every generated manifest."""
    name = plugin["name"]
    version = plugin["version"]
    description = plugin["description"]
    author = plugin.get("author") or {}

    def dump(obj: dict) -> str:
        return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"

    claude_plugin = {
        "name": name,
        "version": version,
        "description": description,
        "author": author,
        "repository": plugin.get("repository"),
        "license": plugin.get("license"),
    }
    claude_plugin = {k: v for k, v in claude_plugin.items() if v is not None}

    claude_marketplace = {
        "name": name,
        "owner": {"name": author.get("name")},
        "metadata": {"description": BLURB, "version": version},
        "plugins": [
            {
                "name": name,
                "source": MARKETPLACE_SOURCE_PATH,
                "description": BLURB,
                "version": version,
            }
        ],
    }

    copilot_marketplace = {
        "name": name,
        "owner": {"name": author.get("name")},
        "metadata": {"description": BLURB, "version": version},
        "plugins": [
            {
                "name": name,
                "description": BLURB,
                "version": version,
                "source": MARKETPLACE_SOURCE_PATH,
            }
        ],
    }

    codex_marketplace = {
        "name": name,
        "interface": {"displayName": plugin.get("extensions", {}).get("com.openai", {}).get("displayName", name)},
        "plugins": [
            {
                "name": name,
                "source": dict(CODEX_SOURCE_OBJECT),
                "policy": dict(CODEX_POLICY),
                "category": CODEX_CATEGORY,
            }
        ],
    }

    antigravity_plugin = {
        "$schema": ANTIGRAVITY_SCHEMA,
        "name": name,
        "description": BLURB,
    }

    return {
        ".claude-plugin/plugin.json": dump(claude_plugin),
        ".claude-plugin/marketplace.json": dump(claude_marketplace),
        ".github/plugin/marketplace.json": dump(copilot_marketplace),
        ".agents/plugins/marketplace.json": dump(codex_marketplace),
        f"{ANTIGRAVITY_DIR}/plugin.json": dump(antigravity_plugin),
    }


def check_drift(repo_root: str, expected: dict) -> list[str]:
    problems = []
    for rel, text in sorted(expected.items()):
        path = os.path.join(repo_root, rel)
        if not os.path.exists(path):
            problems.append(f"{rel}: missing (run: python3 scripts/sync_manifests.py --write)")
            continue
        with open(path, encoding="utf-8") as fh:
            actual = fh.read()
        if actual != text:
            problems.append(f"{rel}: drifted from plugin.json (run: python3 scripts/sync_manifests.py --write)")

    link_path = os.path.join(repo_root, ANTIGRAVITY_DIR, ANTIGRAVITY_SKILLS_LINK)
    if not os.path.islink(link_path):
        problems.append(
            f"{ANTIGRAVITY_DIR}/{ANTIGRAVITY_SKILLS_LINK}: not a symlink to {ANTIGRAVITY_SKILLS_TARGET} "
            "(run: python3 scripts/sync_manifests.py --write; on Windows, enable core.symlinks)"
        )
    else:
        target = os.readlink(link_path)
        if target != ANTIGRAVITY_SKILLS_TARGET:
            problems.append(
                f"{ANTIGRAVITY_DIR}/{ANTIGRAVITY_SKILLS_LINK}: points at {target}, "
                f"expected {ANTIGRAVITY_SKILLS_TARGET}"
            )
    return problems


def write_all(repo_root: str, expected: dict) -> list[str]:
    written = []
    for rel, text in sorted(expected.items()):
        path = os.path.join(repo_root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                if fh.read() == text:
                    continue
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        written.append(rel)

    link_dir = os.path.join(repo_root, ANTIGRAVITY_DIR)
    link_path = os.path.join(link_dir, ANTIGRAVITY_SKILLS_LINK)
    os.makedirs(link_dir, exist_ok=True)
    if os.path.islink(link_path):
        if os.readlink(link_path) != ANTIGRAVITY_SKILLS_TARGET:
            os.remove(link_path)
    if not os.path.islink(link_path):
        if os.path.exists(link_path):
            raise SystemExit(
                f"{link_path} exists and is not a symlink; refusing to overwrite. "
                "On Windows, clone with core.symlinks enabled."
            )
        os.symlink(ANTIGRAVITY_SKILLS_TARGET, link_path)
        written.append(f"{ANTIGRAVITY_DIR}/{ANTIGRAVITY_SKILLS_LINK} (symlink)")
    return written


def load_json(path: str, problems: list[str]) -> dict | None:
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        problems.append(f"{os.path.relpath(path, REPO_ROOT)}: missing")
    except json.JSONDecodeError as exc:
        problems.append(f"{os.path.relpath(path, REPO_ROOT)}: invalid JSON ({exc})")
    return None


def require(obj: dict, keys: tuple[str, ...], label: str, problems: list[str]) -> None:
    for key in keys:
        if not obj.get(key):
            problems.append(f"{label}: missing required field {key!r}")


def validate(repo_root: str, plugin: dict) -> list[str]:
    """Structural checks, one per harness, from the Phase 0 doc table on issue #17."""
    problems: list[str] = []
    name = plugin["name"]
    version = plugin["version"]
    kebab = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

    def path_of(rel: str) -> str:
        return os.path.join(repo_root, rel)

    # --- Claude Code plugin manifest -------------------------------------
    claude_plugin = load_json(path_of(".claude-plugin/plugin.json"), problems)
    if claude_plugin is not None:
        require(claude_plugin, ("name", "version", "description", "author"), ".claude-plugin/plugin.json", problems)
        if claude_plugin.get("name") != name:
            problems.append(f".claude-plugin/plugin.json: name {claude_plugin.get('name')!r} != plugin.json {name!r}")
        if claude_plugin.get("version") != version:
            problems.append(f".claude-plugin/plugin.json: version {claude_plugin.get('version')!r} != plugin.json {version!r}")

    # --- Marketplaces ----------------------------------------------------
    for rel, entry_required in (
        (".claude-plugin/marketplace.json", ("name", "source")),
        (".github/plugin/marketplace.json", ("name", "source")),
    ):
        market = load_json(path_of(rel), problems)
        if market is None:
            continue
        require(market, ("name", "owner", "plugins"), rel, problems)
        if not kebab.match(market.get("name", "")):
            problems.append(f"{rel}: marketplace name {market.get('name')!r} is not kebab-case")
        for entry in market.get("plugins") or []:
            require(entry, entry_required, f"{rel} plugins[]", problems)
            if entry.get("name") != name:
                problems.append(f"{rel}: entry name {entry.get('name')!r} != plugin.json {name!r}")
            if entry.get("version") != version:
                problems.append(f"{rel}: entry version {entry.get('version')!r} != plugin.json {version!r}")
            source = entry.get("source")
            if isinstance(source, str):
                target = os.path.join(repo_root, source)
                if not os.path.isfile(os.path.join(target, "plugin.json")):
                    problems.append(f"{rel}: source {source!r} does not resolve to a plugin (no plugin.json)")
            else:
                problems.append(f"{rel}: source must be a relative path string per the Copilot/Claude schema")

    # --- Codex marketplace ----------------------------------------------
    codex = load_json(path_of(".agents/plugins/marketplace.json"), problems)
    if codex is not None:
        require(codex, ("name", "plugins"), ".agents/plugins/marketplace.json", problems)
        if not codex.get("interface", {}).get("displayName"):
            problems.append(".agents/plugins/marketplace.json: interface.displayName missing")
        for entry in codex.get("plugins") or []:
            label = ".agents/plugins/marketplace.json plugins[]"
            require(entry, ("name", "source", "policy", "category"), label, problems)
            source = entry.get("source") or {}
            if source.get("source") != "local" or not str(source.get("path", "")).startswith("./"):
                problems.append(f"{label}: source must be {{'source': 'local', 'path': './...'}}")
            policy = entry.get("policy") or {}
            if policy.get("installation") not in ("AVAILABLE", "INSTALLED_BY_DEFAULT", "NOT_AVAILABLE"):
                problems.append(f"{label}: policy.installation must be one of AVAILABLE/INSTALLED_BY_DEFAULT/NOT_AVAILABLE")
            if not policy.get("authentication"):
                problems.append(f"{label}: policy.authentication missing")
            target = os.path.join(repo_root, str(source.get("path", "")))
            if not os.path.isfile(os.path.join(target, "plugin.json")):
                problems.append(f"{label}: path {source.get('path')!r} does not resolve to a plugin (no plugin.json)")

    # --- Antigravity workspace plugin ------------------------------------
    anti = load_json(path_of(f"{ANTIGRAVITY_DIR}/plugin.json"), problems)
    if anti is not None:
        allowed = {"$schema", "name", "description"}
        extra = set(anti) - allowed
        if extra:
            problems.append(
                f"{ANTIGRAVITY_DIR}/plugin.json: unsupported keys {sorted(extra)} "
                "(the Antigravity CLI schema sets additionalProperties: false)"
            )
        if anti.get("$schema") != ANTIGRAVITY_SCHEMA:
            problems.append(f"{ANTIGRAVITY_DIR}/plugin.json: $schema must be {ANTIGRAVITY_SCHEMA}")
        if not anti.get("description"):
            problems.append(f"{ANTIGRAVITY_DIR}/plugin.json: description missing")
        if not re.match(r"^[a-zA-Z0-9-_]+$", anti.get("name", "")):
            problems.append(f"{ANTIGRAVITY_DIR}/plugin.json: name must match ^[a-zA-Z0-9-_]+$")
        if anti.get("name") != name:
            problems.append(f"{ANTIGRAVITY_DIR}/plugin.json: name {anti.get('name')!r} != plugin.json {name!r}")

        link = path_of(f"{ANTIGRAVITY_DIR}/{ANTIGRAVITY_SKILLS_LINK}")
        if not os.path.isdir(link):
            problems.append(f"{ANTIGRAVITY_DIR}/{ANTIGRAVITY_SKILLS_LINK}: does not resolve to a directory")
        elif not os.path.isfile(os.path.join(link, name, "SKILL.md")):
            problems.append(f"{ANTIGRAVITY_DIR}/{ANTIGRAVITY_SKILLS_LINK}: missing {name}/SKILL.md")

        # No duplicated plugin content: the wrapper holds a marker and a symlink, nothing else.
        entries = sorted(os.listdir(path_of(ANTIGRAVITY_DIR)))
        if entries != sorted(["plugin.json", ANTIGRAVITY_SKILLS_LINK]):
            problems.append(
                f"{ANTIGRAVITY_DIR}: expected exactly plugin.json + {ANTIGRAVITY_SKILLS_LINK}, found {entries}"
            )

    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync and verify client manifests against plugin.json")
    parser.add_argument("--write", action="store_true", help="rewrite generated files from plugin.json")
    parser.add_argument("--check", action="store_true", help="drift check only")
    parser.add_argument("--validate", action="store_true", help="structural validation only")
    parser.add_argument("--repo-root", default=REPO_ROOT)
    args = parser.parse_args()

    repo_root = os.path.abspath(args.repo_root)
    plugin = read_source(repo_root)
    expected = build_expected(plugin)

    if args.write:
        written = write_all(repo_root, expected)
        if written:
            print("wrote " + ", ".join(written))
        else:
            print("nothing to write; all manifests already in sync")
        return 0

    do_check = args.check or not args.validate
    do_validate = args.validate or not args.check

    problems: list[str] = []
    if do_check:
        problems += check_drift(repo_root, expected)
    if do_validate:
        problems += validate(repo_root, plugin)

    if problems:
        print(f"manifest guard: {len(problems)} problem(s)")
        for problem in problems:
            print(f"  - {problem}")
        return 1

    print(f"manifest guard: OK ({len(expected)} generated file(s) in sync with plugin.json {plugin['version']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())