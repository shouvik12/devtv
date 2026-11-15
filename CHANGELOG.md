# Changelog

## [Unreleased]

### Added
- **THE DEPTHS channel.** 76 years of the software industry drawn as an ocean: today's AI surface at the top, the first mainframes on the seabed. Companies are glowing jellyfish, acquisitions swallow the company they bought, shutdowns sink as wrecks, and landmark events ping like sonar. A lower-third tracks how software was sold, delivered and built in each era, plus that era's job title. SOUND plays an underwater ambience (swells, a deep rumble, bubbles) that gets more muffled the deeper you go, with a sonar ping at landmark events. The card's DIVE IN button opens it full-screen; ✕ or `Esc` returns to the TV. `?depths` in the address opens it directly.
- The industry worldwide, not just Silicon Valley: LEO I, TCS, SAP, Infosys, Huawei, ARM, Alibaba, Tencent, Spotify, Skype, UPI, Mistral and more, each with where it started.
- Tap any creature to pause on it and read its story. The dive has no remote of its own: the deck's WATCH/STOP plays or pauses it, the speed key sets its pace, and GUIDE jumps between eras. Only ✕ and SOUND sit on the picture. While you dive, the deck keys turn deep-sea teal and return to your skin on exit.
- Three kinds of creature: whales for the giants, manta rays for companies, jellyfish for products and technologies.
- `depths.html` (the dive, Three.js) and `depths/species.json` (its 93 entries). Add or fix history by editing one line of the JSON.

## [2.0.0] - 2026-10-04

### Added
- **GUIDE button** and channel guide. An overlay on the screen lists every channel with what is on it right now. Open it with the new GUIDE key, the `G` key, or by tapping the channel name on the screen. Tap a row, or use `↑` `↓` and `Enter`, to tune. `Esc`, `G` or ✕ close it.
- **Agent Skills channel (12).** New agent skills repositories from the last 14 days with at least 20 stars, ranked by stars, top 10, with the repo's age shown. Merges the `claude-skills` and `agent-skills` topics and removes duplicates. Opening a story shows the repo's README.
- A one-time step so returning visitors get new channels switched on automatically. A channel they turn off stays off.
- TV skins and the Spotlight submission form, which were already on the live page but were not in v1.0.0.

### Changed
- **License: MIT to Apache-2.0** for this release onward, with a `NOTICE` file. The Apache License covers the source code only. The DEV·TV name and logo are not licensed, so forks should use their own name and branding. v1.0.0 and earlier stay available under MIT.
- Spotlight is now channel 13 (it was 12).
- While the guide is open, stories and commercial breaks pause, and opening the guide closes settings, the reader and the submit form.
- README: channel count, channel table, controls and tech notes brought up to date (it still said 10 channels).

### Unchanged
- Channels 1 to 11, their order, their number keys, the reader, fullscreen, power, speed and the commercial breaks.

[2.0.0]: https://github.com/shouvik12/devtv/compare/v1.0.0...v2.0.0

## [1.0.0]

- First tagged release.
