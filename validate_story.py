#!/usr/bin/env python3
import sys
import yaml


def load_story(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate(story):
    errors = []
    if not isinstance(story, dict):
        errors.append("Top-level YAML must be a mapping")
        return errors
    start = story.get("start")
    if not start:
        errors.append("Missing top-level 'start' node id")
    nodes = story.get("nodes")
    if not isinstance(nodes, dict):
        errors.append("'nodes' must be a mapping of node_id -> node")
        return errors

    for nid, node in nodes.items():
        if not isinstance(node, dict):
            errors.append(f"Node '{nid}' must be a mapping")
            continue
        # Check choices targets
        for choice in node.get("choices", []) or []:
            tgt = choice.get("target")
            if not tgt:
                errors.append(f"Choice in node '{nid}' missing 'target'")
            elif tgt not in nodes:
                errors.append(f"Choice in node '{nid}' targets unknown node '{tgt}'")

    if start and start not in nodes:
        errors.append(f"Start node '{start}' not found in nodes")

    return errors


def main(argv):
    if len(argv) < 2:
        print("Usage: validate_story.py <story.yaml>")
        return
    path = argv[1]
    story = load_story(path)
    errs = validate(story)
    if not errs:
        print("OK: story looks valid")
        return
    print("Validation errors:")
    for e in errs:
        print(" -", e)
    sys.exit(2)


if __name__ == "__main__":
    main(sys.argv)
