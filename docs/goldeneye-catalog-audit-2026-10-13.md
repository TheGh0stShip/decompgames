# GoldenEye catalog source audit

Reviewed source HEAD `d1c889929714eb09f853b390df67c3d17de800a0` in andrewnakas/goldeneye-cleanroom. Read-only source review; no ROM downloaded, no browser player opened and no new gameplay test.

Pinned evidence:

- [README](https://github.com/andrewnakas/goldeneye-cleanroom/blob/d1c889929714eb09f853b390df67c3d17de800a0/README.md) explicitly retains code, level/model geometry, setups, text, attract demos and music note sequences. Selected media is generated using extracted colour/alpha/spectral information; this does not establish independent authorship of every asset.
- [STATUS](https://github.com/andrewnakas/goldeneye-cleanroom/blob/d1c889929714eb09f853b390df67c3d17de800a0/STATUS.md) additionally identifies copied geometry, model conversion outputs and boot microcode. Its byte-run scan is limited evidence about compared bytes, not a clean-room isolation or licence audit.
- [Site assembly](https://github.com/andrewnakas/goldeneye-cleanroom/blob/d1c889929714eb09f853b390df67c3d17de800a0/ports/emu/make_site.py) copies a ROM into `game.z64` and configures N64Wasm to load it. The source is decompilation-derived, while runtime execution is emulation. No native WebAssembly game port established by this pipeline.

Corrected this site's overview, licence/requirements wording and limitations; moved the entry to the classic shelf. Preserved the external entry, controls and historical gameplay record, which this turn did not reproduce. A player that supplies a built ROM is different from the current audited ROM-free distribution requirement. Full inherited game-code, emulator dependency and content clearance remain unresolved. No clean-room certification or new completed intake count.

The upstream site and Claude-owned build were not changed. Mario Party 2/3 remain untouched. This metadata correction is shared for review; a whole-site deployment was not performed for it.
