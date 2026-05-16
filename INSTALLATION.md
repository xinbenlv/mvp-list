# Installation

This document explains how to install the `mvp-list` skill from this repository.

The skill package lives at:

```text
skill/mvp-list/
```

## Prerequisites

- This repository is available locally.
- Codex and/or Claude are configured to load local skills.
- Optional: `gbrain` is installed and configured if you want `/mvp-list add ...` to write indexed places directly into gbrain.

## Install For Codex

Create or update a symlink from Codex's skills directory to this repository's skill package:

```bash
mkdir -p ~/.codex/skills
ln -sfn /Users/zzn/ws/@xinbenlv/mvp-list/skill/mvp-list ~/.codex/skills/mvp-list
```

Verify the skill file exists through the Codex skills path:

```bash
test -f ~/.codex/skills/mvp-list/SKILL.md
```

Restart Codex after installing the symlink so the skill metadata is reloaded.

## Install For Claude

Create or update a symlink from Claude's skills directory to this repository's skill package:

```bash
mkdir -p ~/.claude/skills
ln -sfn /Users/zzn/ws/@xinbenlv/mvp-list/skill/mvp-list ~/.claude/skills/mvp-list
```

Verify the skill file exists through the Claude skills path:

```bash
test -f ~/.claude/skills/mvp-list/SKILL.md
```

Restart Claude after installing the symlink so the skill metadata is reloaded.

## Configure GBrain

The skill can still produce a Markdown draft without gbrain. To let it write directly into gbrain, configure one of these paths:

1. Install the `gbrain` CLI and make sure it is on `PATH`.
2. Set `GBRAIN_REPO` to the local gbrain repository path.
3. Make sure the gbrain repository documents or exposes a write/import entrypoint for Markdown place records.

Example shell setup:

```bash
export GBRAIN_REPO=/path/to/gbrain
```

If gbrain is missing or no Markdown write entrypoint can be found, the skill should pause and ask the user to install or configure gbrain. It should only output the Markdown draft and must not claim the place was indexed.

## Validate The Skill Files

Validate the JSON files:

```bash
jq empty skill/mvp-list/references/place.schema.json skill/mvp-list/references/place-template.json
```

Validate the empty template against the schema if Python `jsonschema` is available:

```bash
python3 -c "import json, jsonschema; schema=json.load(open('skill/mvp-list/references/place.schema.json')); data=json.load(open('skill/mvp-list/references/place-template.json')); jsonschema.Draft202012Validator(schema).validate(data); print('template validates')"
```

## Test Invocation

After installing, invoke the skill with:

```text
/mvp-list add <url>
```

or:

```text
/mvp-list add <image>
```
