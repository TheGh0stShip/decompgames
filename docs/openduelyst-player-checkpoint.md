# OpenDuelyst private player checkpoint

Private directory: C:/Users/andre/AppData/Local/decomp-builds/openduelyst-intake.
Current playable-host source: private-player.html and private-player-bootstrap.js.
Runtime candidates: browser-migration-probe.js and cocos-no-spine-private.js.
Test runner: node test-integrated-player.cjs (muted Edge, own HTTP host/browser closed in finally).

Integrated UI test: ordinary mouse move, Save, fresh page restore, New game reset all pass with zero page errors/missing files/external requests. Separate runs verify unit summon, targeted spell damage, artifact effects, player swap/movement, post-restore continuation and resignation. Deterministic custom decks were used for card-action tests; integrated player starts normal faction 1/2 starter decks. Full combat match completion is unverified. Audio stays disabled; no audible test.

This is an existing JavaScript game adaptation, not decompilation, WASM or certified clean-room. Root project is CC0 with MIT/Apache/other permissive dependencies retained separately. Candidate excludes old Firebase 2.0.3 and restrictive Spine runtime. The fixed-version Spine exclusion is documented by AST boundaries/hashes; Firebase bridge supports tested local-game path, not legacy account authentication.

Release status: PRIVATE, NOT DEPLOYED. Finish exact served-file license/attribution packaging and reproducible source archive, verify combined end-turn/concede panel and broader combat completion. See docs/openduelyst-release-blockers.md for history and private manifests for evidence. Reconcile GitHub main and commit/push release files before any whole-site deploy. Leave Claude's Halo/Mario Party projects untouched.

Private source-input snapshot now available as openduelyst-private-source-inputs.tar.gz (2,171 entries, 2,843,150 bytes; SHA256 719db9c7205f5fde59404a701fdfe085e464051a4ad38a7511ce5820fff45430). Every archived payload matches its inventory. This is not yet an install/build-reproducible release archive; tool lock and final notices remain required. Integrated End turn/second-player Concede also now pass; see browser-integrated-controls-result.json.

Latest complete private rebuild-input archive: openduelyst-private-rebuild-source.tar.gz, 5,741 entries, 10,578,074 bytes; SHA256 d0db88143a2697f141f3515180602e8be6ccf43a2d9e49409fbff09696aa1464. Includes vendored selected build inputs, instructions and collected notice evidence. Independent build is byte-identical at bundle SHA256 22b56c43c86d83caecb13b625081aa03474d0fc14e6a615194578b2ac88392e6. Final tool/nested attribution and full combat match remain unfinished; archive stays private and runtime media separate. Earlier small source snapshot is superseded for rebuild preparation.

Latest source archive with tool notice evidence: 5,863 entries, 10,605,391 bytes; SHA256 011e6aea38f986d26d4c41bae23dd41f0f666ac10e1e01c09bbb11df03608880. This supersedes the prior archive hash. The general-only normal starter-deck combat test now reaches a draw through ordinary attacks (turn counter 16), with zero errors/missing resources; decisive victory and broad card strategies remain unverified. Attribution coverage/report is in docs/openduelyst-attribution-review.md. The three tool original-notice questions and final packaged support/nested review remain explicitly documented. Runtime remains undeployed. Git fetch on October 12 confirms shared site branch still at d55dc43 with research/docs edits preserved; no wholesale pull/reset was performed.

Current source archive after engine image replacement: 5,866 entries, 10,591,442 bytes; SHA256 e95b6c77ba0afe7d45aa5bfcdf0f7f7b7a6654b2ecb512f2ed08bf5f5c94cb61. Adapted Cocos replaces original embedded GIF/FPS atlas/JPEG with authored SVG placeholders; PNG decoder MIT notice retained. Runtime inventory: 302 files, 36,770,379 bytes. Final attribution review still pending; no catalogue/deployment changes.

Current pruned source archive with all 25 support-root permission texts and inherited FXAA notice: 5,788 entries, 10,573,090 bytes; SHA256 aee6bf25264c9b317405570ab482c5ba200bf8f1af00d4462131c97e2d0e3443. This supersedes previous hashes. Unused example files excluded. Final attribution review remains; runtime unchanged and undeployed.


### 2026-10-12 isolated OpenDuelyst staging verification
302 runtime files staged privately from SHA256-checked input inventory. Host script URLs changed to relative paths for /games/openduelyst/. Isolated static server served only staging files, with no checkout fallback. Real pointer movement, Save/reload restoration, New game reset, End turn/user switching, and normal concession all passed. Zero page errors, missing resources, or external requests. Edge muted; browser and server closed. Existing JavaScript local two-player Sandbox adaptation, not a decompilation or WebAssembly build. No public release/deployment in this checkpoint; full card coverage and decisive combat victory remain unverified. Evidence: private browser-staged-controls-result.json and runtime-staging-candidate/CANDIDATE-MANIFEST.json.


2026-10-12: Consolidated private staging release-review kit with 241 retained notice files, provenance, isolated browser results and source rebuild evidence. Updated docs/openduelyst-attribution-review.md to distinguish publisher license declarations from missing original standalone notices and to record completed draw combat scope. No publication yet.

2026-10-12: Added local experimental OpenDuelyst catalogue entry and public/games/openduelyst runtime with 241 retained notice files. Catalogue validates 80 entries. Source archive materialized under ignored public/sources; object-storage upload and release commit/push/deploy still pending. No production claim.
