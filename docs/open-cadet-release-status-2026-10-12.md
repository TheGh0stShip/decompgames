# Open Cadet private repair release status

Existing entry; no new game count. Production remains unchanged.

The private repair replaces indistinguishable score digits and the embedded message font with independently authored data, and writes confirmed high scores before browser filesystem synchronization. The menu font retains its own MIT licence. Original icon, splash and instrument-bank files are excluded. Historical ImGui and renderer provenance is recorded separately. No clean-room certification.

Passed: launch/flipper visual response, readable played scores and messages, settings reload on the build without diagnostic hooks, and isolated source rebuild with byte-identical JS/WASM/data. The final build without diagnostic hooks also passed naturally earned score confirmation, save reload and loaded high-score UI review (191,750).

Remaining gates:
- Completed: final build earned 191,750, confirmed normally, restored exact save bytes and displayed Player 1 / 191,750 in the reopened High Scores UI.
- Complete linked-runtime dependency inventory and refresh all source/notices.
- Integrate exact artifacts, run local release checks, reconcile main, commit/push before deployment, then verify production.

All browser tests muted and closed; audible audio remains unverified. Details: [verification log](open-cadet-verification-2026-10-12.md).
