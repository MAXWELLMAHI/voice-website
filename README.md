# VOICE website

This folder contains the complete current website, its assets, and editable source code. The hero uses IMG_7508.MP4 with its audio, the centered VOICE heading and Built in the Noise. tagline, the original moon loader, and a sound toggle.

This is the canonical working folder for all future website edits. Use this outer `VOICE-website` folder; the nested folder with the same name is an older copy. `../VOICE-website.zip` is a downloadable snapshot, while this folder holds the current working files. Workspace guidance is saved in `AGENTS.md` so future chats can follow the same location.

## Open the website locally

Run `npm run dev`, then open http://127.0.0.1:4173/ in your browser. Keep the terminal open while using the preview; Ctrl+C stops it. No npm installation step is needed. Node.js/npm and Python 3 must be available.

You can also double-click `start-preview.cmd` to start the same Python preview without npm.

You can also run this command from this folder:

```sh
python -m http.server 4173 --bind 127.0.0.1 --directory dist
```

## Where the code lives

| Path | Contents |
| --- | --- |
| `dist/index.html` | Complete website, including the original lower sections |
| `dist/voice-hero.html` | Standalone hero with its video, poster and fonts embedded |
| `dist/assets/` | Stylesheets, animation JavaScript, images, audio and decorative clips |
| `dist/assets/site-typography.css` | Current site-wide font definitions and role mappings |
| `dist/assets/fonts/` | Cormorant SC, ABeeZee and Borel fonts and their OFL licenses |
| `dist/models/` | 3D models used by the lower sections |
| `src/hero-simple.template.html` | Editable hero markup, CSS and Three.js / GSAP code |
| `src/original-index.html` | Base markup for the complete website |
| `src/intro-story.css` | Responsive introduction: serif welcome and handwritten aside |
| `src/assemble.py` | Builds the current hero and integrates it into the complete website |
| `src/prepare_fonts.py` | Downloads the font files and updates site-wide typography rules |
| `src/font-faces.css` | Font-face definitions used when embedding fonts into the hero |
| `src/media/` | Web-ready copy of the latest supplied video, with audio, and its poster |
| `.openai/hosting.json` | Existing Sites project identity and static hosting configuration |

## Make changes

Edit `src/hero-simple.template.html` for hero content, styles and animations. Edit `src/original-index.html` for the lower sections. Run `npm run build` after source changes, or double-click `rebuild.cmd`. The equivalent Python command is:

```sh
python src/assemble.py
```

Reload the local preview to see changes. Rebuilding uses the bundled assets and needs no package installation. To change typography roles, edit `src/prepare_fonts.py` and run it before rebuilding; that font refresh contacts Google Fonts.

Cormorant SC is used for headings and display statements, ABeeZee for body text and interfaces, and Borel for handwritten notes. The video retains its full 55.1-second timeline and audio; only its existing black borders were cropped for the web version. The original large recording remains in Downloads.

## Dependencies and source notes

The hero loads pinned Three.js r128 and GSAP / ScrollTrigger 3.12.5 from jsDelivr. The integrated site serves its fonts locally. The original site's separate note-panel film is an external HLS dependency. Internet access is needed for those external dependencies.

The original lower-section runtime is included as its published JavaScript bundle, with its existing credits. The original author's unbundled development project is not available. Local Git history, credentials, temporary experiments, and the portable Blender installation are excluded from this folder.

## Mumbai alley illusion

The Mumbai section uses the supplied landscape artwork, `Teal-Hazed Urban Canyon at Night.png`. Its original 1672×941 pixels are copied byte-for-byte into `src/media/teal-urban-canyon.png` and `dist/assets/mumbai/teal-urban-canyon.png`. The earlier portrait artwork is retained in the source folder.

`src/mumbai-alley.template.html` maps six smoothly joined depth bands onto a continuous perspective surface. Inverse projection preserves the exact artwork at entry, with no repeated images or cutout seams. The foreground passes the camera faster than the distant teal lane during a 680-viewport-height scroll journey. “Sleep well,” “Respect your body,” and “Don't pull up” occupy three separate depths, fade in and out, and can be occluded by closer buildings. The scene also supports restrained pointer parallax, touch and keyboard scrolling. `src/build_alley.py` integrates it into the full page on `npm run build`.

Reduced-motion settings show the still landscape with all three phrases and a shorter section. A still-image fallback remains available if WebGL or the scene library cannot load. The standalone `/mumbai-alley.html` preview offers the same scroll journey. Browser captures and the visual storyboard are saved under `review/`.
