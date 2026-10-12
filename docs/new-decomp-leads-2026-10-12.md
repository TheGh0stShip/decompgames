# New decompilation/port lead triage

Read-only upstream search; no retail files downloaded, no new catalog entries.

- **Tenkaichi3Decomp** — https://github.com/z3xox/Tenkaichi3Decomp . Upstream licence section explicitly limits MIT to its own port/build code; reconstructed game code belongs to game rights holders. Requires game disc. Blocked for this permissive, ROM-free intake by inherited code rights and full independent content, plus no verified browser build. Port-layer MIT is not whole-game permission.
- **PSP web recomp** — https://github.com/snuri00/psp-web-recomp . Static recompilation/HLE/browser renderer, not source decompilation. Upstream describes disc-data streaming; AT3 dependency remains LGPL-2.1. No independent full game content or permissive whole-distribution audit established. Blocked; do not ship disc/executable data or label it a finished ROM-free decomp.
- **Mikompilation** — https://github.com/Mikompilation/Mikompilation . BSD-2-Clause-labelled Fatal Frame 2 engine project, aiming for a playable PC port. Root label alone does not clear reconstructed code or media. Needs source/dependency scope audit, progress/build evidence, complete independent content and browser adapter verification before eligibility; not presently ready to integrate.

These are precise intake blockers, not a claim that the projects are unlawful. Existing Open Cadet is repaired and deployed; OpenLara remains a private incomplete engine recreation/source-port fixture. Mario Party work remains Claude-owned.


Mikompilation source audit checkpoint: pinned afd5bc1692cd9a11e39416abb66b23a0082ccd69, 1,735 source-tree files. Verified BSD-2-Clause notice copyright2021WilliamAdam-Grenier; this is a declaration, not proof of rights to reconstructed retail code. RootCMake C++17 links spdlog; SDL2/ImGui build paths currentlycommented. main.cpp runs an unbounded do/while phase loop, init_super logs notimplemented and rendering/input/system calls arecommented. Assets README explicitly says PUT YOUR GAME ASSETS HERE. Concrete blockers: incomplete engine systems/rendering/input, no independent completecontent, no verified browserloop/backend, separate reconstructedcode/dependencyprovenance. Downloaded onlylicence/readme/build/source snippets; no gameassets. Not a viable near-term completedgame intake.
