# VOICE website

This is the canonical editable website folder requested by the user. Save all website changes here, including source, media, assets and the rebuilt `dist/` output.

## Commands

- Build: `npm run build`
- Preview: `npm run dev` at http://127.0.0.1:4173/
- Do not stop an existing user-requested preview server unless asked.

## Editing

- Hero: `src/hero-simple.template.html`.
- Mumbai illusion: `src/mumbai-alley.template.html` and `src/build_alley.py`.
- Full website base markup: `src/original-index.html`.
- Build integration: `src/assemble.py`.
- Media: `src/media/`.
- Preserve the current hero video and sound toggle, original moon loader, and Cormorant SC / ABeeZee / Borel typography unless the user requests changes.
- Rebuild after source edits and check the affected behavior.

The child directory `VOICE-website/` is an older duplicate. Do not edit, package, or delete it without a user request.

The sibling `../VOICE-website.zip` is a snapshot. Refresh it after website changes from this project's known source, output, manifest, documentation and launcher files, excluding the nested duplicate and caches. Publishing uses the existing checkout at `../../work/sleep-well-replica/`; synchronize this project's current source and build into that checkout before publication. Preserve its Git metadata and `.openai/hosting.json` identity.
