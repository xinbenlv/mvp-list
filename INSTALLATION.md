# Installation

This document explains how to install the MVP List skills from this repository.

The skill packages live at:

```text
skill/mvp-list-curate/
skill/mvp-list-enrich/
skill/mvp-list-propose/
skill/mvp-list-render/
```

## Prerequisites

- This repository is available locally.
- Codex and/or Claude are configured to load local skills.
- Optional: `gbrain` is installed and configured if you want enriched Markdown records to be written directly into gbrain.

## Install For Codex

Create or update symlinks from Codex's skills directory to this repository's skill packages:

```bash
mkdir -p ~/.codex/skills
ln -sfn /Users/zzn/ws/@xinbenlv/mvp-list/skill/mvp-list-curate ~/.codex/skills/mvp-list-curate
ln -sfn /Users/zzn/ws/@xinbenlv/mvp-list/skill/mvp-list-enrich ~/.codex/skills/mvp-list-enrich
ln -sfn /Users/zzn/ws/@xinbenlv/mvp-list/skill/mvp-list-propose ~/.codex/skills/mvp-list-propose
ln -sfn /Users/zzn/ws/@xinbenlv/mvp-list/skill/mvp-list-render ~/.codex/skills/mvp-list-render
```

Verify the skill files exist through the Codex skills path:

```bash
test -f ~/.codex/skills/mvp-list-curate/SKILL.md
test -f ~/.codex/skills/mvp-list-enrich/SKILL.md
test -f ~/.codex/skills/mvp-list-propose/SKILL.md
test -f ~/.codex/skills/mvp-list-render/SKILL.md
```

Restart Codex after installing the symlink so the skill metadata is reloaded.

## Install For Claude

Create or update symlinks from Claude's skills directory to this repository's skill packages:

```bash
mkdir -p ~/.claude/skills
ln -sfn /Users/zzn/ws/@xinbenlv/mvp-list/skill/mvp-list-curate ~/.claude/skills/mvp-list-curate
ln -sfn /Users/zzn/ws/@xinbenlv/mvp-list/skill/mvp-list-enrich ~/.claude/skills/mvp-list-enrich
ln -sfn /Users/zzn/ws/@xinbenlv/mvp-list/skill/mvp-list-propose ~/.claude/skills/mvp-list-propose
ln -sfn /Users/zzn/ws/@xinbenlv/mvp-list/skill/mvp-list-render ~/.claude/skills/mvp-list-render
```

Verify the skill files exist through the Claude skills path:

```bash
test -f ~/.claude/skills/mvp-list-curate/SKILL.md
test -f ~/.claude/skills/mvp-list-enrich/SKILL.md
test -f ~/.claude/skills/mvp-list-propose/SKILL.md
test -f ~/.claude/skills/mvp-list-render/SKILL.md
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
jq empty skill/_shared/references/place.schema.json skill/_shared/references/place-template.json
```

Validate the empty template against the schema if Python `jsonschema` is available:

```bash
python3 -c "import json, jsonschema; schema=json.load(open('skill/_shared/references/place.schema.json')); data=json.load(open('skill/_shared/references/place-template.json')); jsonschema.Draft202012Validator(schema).validate(data); print('template validates')"
```

## Test Invocation

After installing, invoke the skills with prompts such as:

```text
Use mvp-list-curate to extract places from this itinerary.
```

```text
Use mvp-list-enrich to enrich this Google Maps URL into ./demo-md-repo.
```

```text
Use mvp-list-propose on ./demo-md-repo for a Saturday infant-friendly plan, then mvp-list-render the selected plan.
```
