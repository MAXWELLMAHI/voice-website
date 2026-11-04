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
| `dist/index.html` | Full portfolio: hero, introduction, daily loop, Mumbai, vertical timeline and contact |
| `dist/voice-hero.html` | Standalone hero with its video, poster and fonts embedded |
| `dist/assets/` | Stylesheets, animation JavaScript, images, audio and decorative clips |
| `dist/assets/site-typography.css` | Current site-wide font definitions and role mappings |
| `dist/assets/fonts/` | Cormorant SC, ABeeZee and Borel fonts and their OFL licenses |
| `dist/models/` | 3D models used by the lower sections |
| `src/hero-simple.template.html` | Editable hero markup, CSS and Three.js / GSAP code |
| `src/original-index.html` | Base markup for the complete website |
| `src/intro-story.css` | Responsive introduction: serif welcome and handwritten aside |
| `src/stats-clock.css` | Gold clock asset replacement above the minimum-duration readout |
| `src/daily-loop.data.json` | Seventeen confirmed routine activities and overnight times |
| `src/daily-loop.template.html`, `src/daily-loop.js`, `src/daily-loop.css` | Scroll-driven clock, independent hands and running character |
| `src/project-wave.data.json` | Ten biography milestones, hover copy and three image slots per milestone |
| `src/project-wave.template.html`, `src/project-wave.js`, `src/project-wave.css` | Scroll-driven project score, image piles and scrollable project stories |
| `src/contact.template.html` | Final contact section and contact page |
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

The minimum-duration circle now uses the supplied transparent gold clock and runner in `src/media/clockwork-runner.png`. `src/stats-clock.css` replaces the decorative frame, places the duration below the clock, and preserves the original animated background lines. The build copies the PNG unchanged to `dist/assets/clockwork-runner.png`.

Cormorant SC is used for headings and display statements, ABeeZee for body text and interfaces, and Borel for handwritten notes. The video retains its full 55.1-second timeline and audio; only its existing black borders were cropped for the web version. The original large recording remains in Downloads.

The site logo uses the supplied full-resolution transparent `src/media/navy-cream-arched-emblem.png`, copied unchanged from “Navy and Cream Arched Emblem.png”. The existing logo wrapper, 4.8-second floating motion, 3.6-second glow, hover and press animations retain their original CSS and timing. The same image is used by the footer logo, legacy SVG asset wrapper, browser icon and initial loader. The loader keeps its animated outline using the original `rect-solid` hook.

## Dependencies and source notes

The hero loads pinned Three.js r128 and GSAP / ScrollTrigger 3.12.5 from jsDelivr. The integrated site serves its fonts locally. The original site's separate note-panel film is an external HLS dependency. Internet access is needed for those external dependencies.

The original lower-section runtime is included as its published JavaScript bundle, with its existing credits. The original author's unbundled development project is not available. Local Git history, credentials, temporary experiments, and the portable Blender installation are excluded from this folder.

## Mumbai alley illusion

The Mumbai section uses the supplied landscape artwork, `Teal-Hazed Urban Canyon at Night.png`. Its original 1672×941 pixels are copied byte-for-byte into `src/media/teal-urban-canyon.png` and `dist/assets/mumbai/teal-urban-canyon.png`. The earlier portrait artwork is retained in the source folder.

`src/mumbai-alley.template.html` maps six smoothly joined depth bands onto a continuous perspective surface. Inverse projection preserves the exact artwork at entry, with no repeated images or cutout seams. The foreground passes the camera faster than the distant teal lane during a 680-viewport-height scroll journey. “Mumbai never slows down.”, “Neither does my curiosity.”, and “Look where it took me.” occupy three separate depths, fade in and out, and can be occluded by closer buildings. The scene also supports restrained pointer parallax, touch and keyboard scrolling. `src/build_alley.py` integrates it into the full page on `npm run build`.

Reduced-motion settings show the still landscape with all three phrases and a shorter section. A still-image fallback remains available if WebGL or the scene library cannot load. The standalone `/mumbai-alley.html` preview offers the same scroll journey. Browser captures and the visual storyboard are saved under `review/`.

## Daily loop

`/daily-loop.html` opens the scroll-driven routine directly, without an additional entrance. `src/daily-loop.data.json` contains the user's seventeen activities from 9:00 AM through the following 9:00 AM. Each activity has a semantic scroll segment; the displayed time interpolates across that activity's actual duration. The character and gold dial complete one circuit, and the independent hour and minute hands follow the real elapsed time. Scroll reverses the motion. Reduced-motion users receive the full schedule as a readable list.

## Project score and stories

`/project-wave.html` opens the current musical project score directly. The centered “My work, in motion.” heading and tagline stay inside the sticky desktop viewport as scrolling moves through the image piles. Mobile visitors can swipe the project track. The oversized floating summary panel has been removed; engineering remains a timeline entry. Clicking or pressing Enter on a pile opens its full story in a modal, with a link to `/projects/<id>.html`. Contact immediately follows the score; older sleep-guide chapters remain hidden as compatibility hooks for the original runtime.

Project stories fit within the available viewport and have a visible vertical scrollbar. Their close button stays outside the scrolling content. Wheel, touch and keyboard scrolling are contained inside the story, including when the main site’s Lenis controller is active. Escape closes the modal and restores page scrolling. Each story starts at the top when opened. A subtle five-line waveform loops behind the sticky heading and project cards, pauses outside the section, and stays still for reduced-motion preferences. Its SVG is generated by `build_project_wave.py`.

The supplied photographs and project copy live in `src/media/wave-projects/` and `src/project-wave.data.json`. Every milestone has at least three image slots; stories show all supplied images. Replace copy, paths or ordering in the data file, then rebuild. Project pages use the same data. Earlier generated concept artwork and its prompts remain in the media folder for optional use. The shared contact template includes the supplied phone, email and LinkedIn links on the full site and standalone contact page.

Jaggernaut is the eleventh work entry, with five supplied PNGs copied unchanged into `src/media/wave-projects/`. Its website and campaign hero span the gallery width; all five images retain their natural proportions in the story and `/projects/jaggernaut.html`. Optional `imageCaptions`, `fullWidthImages`, `preserveImageAspect` and `complete` fields control this presentation in the shared project data.

The “THE NOTE” panel now contains Mahesh's supplied Mumbai story, “A little note from behind the noise.” Its paragraph breaks, emphasized lines, signature and closing tagline are retained. `src/personal-note.css` makes the full letter scrollable while keeping the existing reveal and close animation. The original template attribution remains separate below the letter. The supplied `IMG_7529.MOV` is served as `src/media/mahesh-note.mp4`, with the complete 25.43-second video converted from HDR to web-friendly 720p H.264 and its original AAC audio preserved. The note has native playback controls and pauses the video when closed; the previous note video and decorative video overlay are replaced.

The legacy “Find the sleeping Insights” display and its dots are hidden globally. Its DOM hooks remain available for the original animation runtime.

The Note is also accessible over the hero using a labelled, glowing star button. The star responds to hover, focus and clicks; reduced-motion preferences disable the continuous glow. `personal-note.js` resets the letter when opened, keeps keyboard focus in the dialog, and returns focus to the star button when closed.
