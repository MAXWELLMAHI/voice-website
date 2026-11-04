# Timeline image slots

Each milestone has three independent image slots. The images are not filled with stock or generated event photographs.

1. Add image files in this folder, optionally in a subfolder for each milestone.
2. Edit that milestone's `images` array in `src/project-wave.data.json`. Paths are relative to `src/media/`, for example `"timeline/engineering/photo-01.jpg"`.
3. Replace each `null` with the corresponding file path. Keep at least three entries; additional slots are also supported.
4. Run `npm run build`.

The builder copies supplied images unchanged into `dist/assets/timeline/`. Every milestone remains a five-strip wave group, with its three image columns sampled consistently across those strips. Project pages display the same three images independently.

Only the engineering starting year (2023) is specified. Other dates are intentionally not invented. The biography and chronology come from the user's supplied timeline.
