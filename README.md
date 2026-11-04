# Mumbai Chawl Edition

The hero of the Sleep Well recreation now uses the complete IMG_7507.MP4 clip supplied by the user, with its own audio. The original cream moon loading animation is restored. The VOICE heading, logo and tagline have been removed from the hero. Selecting Enter Site starts the clip with sound. A side button mutes and unmutes the video; previous ambient tracks are muted.

The picture's existing black borders were removed. The full 55.53-second timeline and its sound are preserved in a 1280×720, 30 fps H.264 / AAC version. The video remains the visual scene, with gentle curved perspective, mouse parallax, and scroll zoom. No additional city models or story chapter are added.

## Local preview

```sh
python -m http.server 4173 --directory dist
```

Open http://localhost:4173. The integrated page continues into the original lower sections. Their visual animation runtime and designer credits are retained.

## Standalone hero

`dist/voice-hero.html` is a single HTML file with the video and poster embedded. It uses pinned Three.js 0.128.0, GSAP 3.12.5 and ScrollTrigger 3.12.5 from jsDelivr, plus Google Fonts. Open through an HTTP server for best compatibility. Playback with sound begins after the user's Enter Site click, as required by browser autoplay rules. Pixel ratio is capped at 2 and at 1.5 on mobile. Offscreen rendering and video playback pause when the hero leaves view.

The original site's separate note-panel film remains an external HLS dependency; it is unrelated to this hero video. The available legacy site runtime is the published JavaScript bundle, not the original author's development project.
