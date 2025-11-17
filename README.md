# Simple Data-Driven CYOA (Choose Your Own Adventure)

This small project provides a minimal, easy-to-edit CYOA engine driven by YAML story files.

Files created:
- `cyoa_player.py`: CLI player that loads a YAML story and runs it interactively.
- `validate_story.py`: Validator to check a story for missing nodes/targets.
- `stories/sample_story.yaml`: Example story demonstrating the format.
- `requirements.txt`: Python dependency list (`PyYAML`).

Story format (YAML):

- Top-level `start`: the id of the starting node.
- Top-level `nodes`: mapping of node id -> node
- Each node contains:
  - `text`: string (can be multiline)
  - optional `choices`: list of choices where each has `text` and `target`
  - optional `end`: boolean (true means story ends at this node)

Example node:

```yaml
start: intro
nodes:
  intro:
    text: "You are at a crossroads."
    choices:
      - text: "Go left"
        target: left_path
      - text: "Go right"
        target: right_path
```

Run the sample story:

```bash
python3 cyoa_player.py stories/sample_story.yaml
```

Validate a story:

```bash
python3 validate_story.py stories/sample_story.yaml
```

To edit the story, modify or add YAML files in the `stories/` directory. Keep the `start` node and `nodes` keys present.
