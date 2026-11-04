# Sleep Well Creatives recreation

A standalone static recreation of https://sleep-well-creatives.com/ as retrieved on November 4, 2026.

## Run locally

From this directory, run:

```sh
python -m http.server 4173 --directory dist
```

Open http://localhost:4173 and select **Enter Site**. Serve over HTTP; opening index.html directly with a file URL will prevent ES modules and model loading.

## Included

- Complete page markup, responsive styles and custom fonts.
- Original animation runtime with Three.js, GSAP and smooth scrolling.
- All twelve GLB models, environment texture, Draco decoders and scene textures.
- Ambient music, six spoken insights, decorative videos, interactive light control, animated clock and scroll scenes.
- Original designer and project credits.
- All 75 downloadable runtime assets are served locally.

The original development-only localhost script was removed. Asset paths and canonical metadata point at this copy. A cursor initialization issue encountered when resizing across breakpoints was repaired.

## External dependency

The note panel's separate HLS film remains linked to the original Bunny CDN stream. That stream returned HTTP 403 during inspection, so its playback cannot be guaranteed. It is separate from the local 3D scenes, music, spoken insights and decorative clips.

`asset-manifest.json` records each local asset and its reference URL. The available JavaScript is the published bundled runtime; the original author's unbundled development project is not included.

## Deploy elsewhere

Upload the contents of `dist/` to any static host. Files under `.openai/` describe this copy's private Sites deployment and are not needed on other hosts.
