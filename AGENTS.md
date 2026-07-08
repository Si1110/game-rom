# OpenCode Project Guidance

This repository contains a large tracked static asset set under `res/covers/`.

Do not read, attach, summarize, grep, index, or include image assets in model context unless the user explicitly asks to inspect images. Treat these paths as generated/static assets:

- `res/covers/**`
- `res/**/*.png`
- `res/**/*.jpg`
- `res/**/*.jpeg`
- `res/**/*.webp`
- `res/**/*.gif`
- `res/**/*.avif`
- `tmp/**`
- `web_browser_data/**`

Prefer working from source data, HTML, scripts, JSON, Excel files, and templates. When a task touches image references, edit the text/data references without loading the image binaries.

The `res/covers/` directory is intentionally large and tracked by Git. Avoid opening the Review tab for mass image changes; use targeted `git diff --stat`, `git diff --name-only`, or path-limited diffs instead.