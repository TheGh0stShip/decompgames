# Open Cadet repair — deployed checkpoint

Existing entry; no new game count. Released from main commit `84aa204` in Pages deployment `a36123d7`.

The repair replaces score digits, embedded message font and expressive resource text with independently authored replacements. It writes confirmed high scores before filesystem synchronization. Functional resource IDs/format tokens/configuration remain compatible. Menu font and engine/dependency code retain separate notices; no whole-distribution CC0 or clean-room claim. Original font blob, icon, splash and instrument sample bank are excluded from the corresponding source package.

Verified on the final authored-text binary: normal launch/flipper response, readable messages and scores, naturally earned 112,750 confirmed and displayed after reload, and isolated byte-identical JS/WASM/data rebuild. Live shared-player startup/settings Stop/Start pass; all production runtime and source archive hashes match the committed manifest. Halo CE, Mario Party 2, Craft, Tennis SDL, OpenDuelyst and Roboden page spot checks return 200.

Limits: all objectives/full playthrough and audible audio remain unverified; no MIDI music provided. The October12 live test covered startup/settings only. October13 live normal play earned144000 and its accepted high-score entry/settings survived a full browser restart; the reopened table visibly confirms it. [Live score test](open-cadet-earned-score-production-test.json). Older checkpoints in the verification log are historical, not current release gates.

Current runtime revision: `0bc12d3ca97a-authored-c51f8473a6`. Production source archive SHA256: `33d4502ff6f3d8023b0248b9fff68c2a1f709a12cee9584625618be658f04a42`.

All tests muted and closed. [Detailed verification](open-cadet-verification-2026-10-12.md), [production hashes](open-cadet-production-release.json).
