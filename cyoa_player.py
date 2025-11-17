#!/usr/bin/env python3
import sys
import yaml


def load_story(path):
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise SystemExit("Story file must be a YAML mapping")
    return data


def get_node(story, node_id):
    nodes = story.get("nodes") or {}
    return nodes.get(node_id)


def play(story):
    current = story.get("start")
    if not current:
        raise SystemExit("Story must define a top-level `start` node id")
    while True:
        node = get_node(story, current)
        if node is None:
            print(f"ERROR: node '{current}' is missing")
            return

        # Print text
        print()
        print(node.get("text", ""))
        print()

        # End node
        if node.get("end"):
            print("--- THE END ---")
            return

        choices = node.get("choices") or []
        if not choices:
            print("No choices available. The story ends here.")
            return

        for i, c in enumerate(choices, start=1):
            print(f"{i}. {c.get('text', '<choice>')}")

        # Input loop
        while True:
            try:
                ans = input("Choose: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
            if not ans:
                continue
            if ans.isdigit():
                idx = int(ans) - 1
                if 0 <= idx < len(choices):
                    target = choices[idx].get("target")
                    if not target:
                        print("Choice has no target; exiting.")
                        return
                    current = target
                    break
            print("Please enter a number for your choice.")


def main(argv):
    if len(argv) < 2:
        print("Usage: cyoa_player.py <story.yaml>")
        return
    path = argv[1]
    story = load_story(path)
    play(story)


if __name__ == "__main__":
    main(sys.argv)
