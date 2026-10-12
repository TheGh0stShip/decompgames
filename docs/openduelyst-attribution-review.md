# OpenDuelyst staged release review

Existing JavaScript game adapted for local two-player Sandbox. Upstream pin: 2843f2400854136598631288c2e8dfb8f5173de7 (open-duelyst/duelyst). First-party project content is CC0; dependencies retain their MIT, ISC, BSD, Apache and 0BSD terms. Do not describe the entire distribution as CC0, a decompilation, WASM, or certified clean-room work.

The isolated staged player passed movement, save/reload, reset, turn switching and concession under /games/openduelyst/. A separate normal starter-deck general combat test reached a draw. Decisive combat victory and exhaustive card/resource coverage remain unverified. Audio is disabled; no audible verification. Online accounts and multiplayer services are unsupported in this adaptation.

292 pinned media files have per-file hashes and provenance. No font or audio files are shipped. Original embedded engine images were replaced with authored SVG placeholders. Restrictive Spine, legacy Firebase 2 and unverified Chroma code are excluded from the tested runtime. Firebase 4 Apache code remains, without connecting to services during these tests. Retained Cocos PNG, TIFF, zlib, Marionette bundled component and inherited FXAA shader notices must accompany release.

97 runtime package roots have retained license evidence. The additional 25 source-archive support roots have full notice evidence. Three build tools use publisher-declared MIT/ISC licensing (object-keys 0.4.0, glslify-deps 1.3.2, @choojs/findup 0.2.1); retain package metadata, author attribution and standard terms. Their original standalone notice files were not recovered; exact object-keys credited-origin revision is unverified, and available origin notices are preserved. These evidence limitations are not proof of nonpermissive licensing.

The source archive rebuilt byte-identically in an isolated extraction on Node 24.19.0. Runtime media is separate from the source archive. This review package is private; no deployment or catalogue integration is claimed. Before publication reconcile GitHub main, commit/push release files, and deploy only the matching revision.
