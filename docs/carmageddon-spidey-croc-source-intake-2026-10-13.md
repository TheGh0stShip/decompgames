# Carmageddon, Spider-Man and Croc source intake — October 13

None of these three distinct titles is in the current 83-entry catalog. Four repositories and one renderer dependency were pinned and reviewed. No candidate passes the current permissive-code, complete independent-content and verified browser-game gates. Mario Party 2/3 and Halo were untouched.

[Snapshot record](carmageddon-spidey-croc-source-snapshot-2026-10-13.json) contains 40 selected source, build and notice text hashes. These are decoded UTF-8 text hashes, not an archive or full dependency audit. Private source inspection stays outside the shipped distribution. No game media, executable, DLL, prebuilt library, installer or browser demo was downloaded or run.

## Carmageddon / Dethrace

[dethrace-labs/dethrace](https://github.com/dethrace-labs/dethrace/tree/f166190807106518edca65d389752535e8cab175), pin `f166190807106518edca65d389752535e8cab175`, had 1,216 stars at intake. Its [README](https://github.com/dethrace-labs/dethrace/blob/f166190807106518edca65d389752535e8cab175/README.md) describes reconstructing C functions from the original assembly and debug symbols. This is a decompilation-derived native port with matching work, not an original replacement or whole-machine emulator. No complete matching or clean-room claim is established here.

The actual [LICENSE](https://github.com/dethrace-labs/dethrace/blob/f166190807106518edca65d389752535e8cab175/LICENSE) is GPL-3.0. The README separately asserts public-domain status while restricting commercial use and tying use to owned game assets. Those inconsistent statements do not establish a permissive grant for this intake. Reconstructed retail code permission remains separate. The project requires original game data or supports freeware demos; free download alone does not establish CC0 or redistribution permission. No complete independent content pack was identified.

Dependencies were checked separately. Root CMake selects BRender, libsmacker and inih, plus miniaudio/stb with sound enabled. The pinned BRender root license at `4e49167c863ecdede43b235b4458440109dd8471` is MIT, copyright Argonaut Software Limited 1998. The selected libsmacker README specifies LGPL-2.1, inih has BSD-3-Clause terms, and miniaudio offers Unlicense/MIT alternatives. These component notices do not clear the game; exact SDL/stb and complete selected dependency closure were not audited.

[Carter54git/dethrace-ported-to-web](https://github.com/Carter54git/dethrace-ported-to-web/tree/02073a0d8b702c8fe96bb09aaf951e3983d7f6dd), pin `02073a0d8b702c8fe96bb09aaf951e3983d7f6dd`, had 36 stars. Its license applies GPL-3.0 to the engine, shell and scripts. README reports an Emscripten/WebGL2/IndexedDB port; build scripts explicitly require `Carma/DATA/GENERAL.TXT`. Asset notice excludes retail content and says third-party demo hosting does not grant redistribution rights.

The pinned Web repository is also incomplete for independent reproduction: its untruncated tree has no `dethrace-0.10.1/lib/` or `dethrace-0.10.1/src/` payload or gitlinks, although CMake references both. A requested engine-source CMake file returned 404. Browser claims are upstream reports, not our build/gameplay evidence. **Disposition:** outside current permissive licensing; content, reproducible Web sources and dependency closure remain blocked.

## Spider-Man (Neversoft)

[krystalgamer/spidey-decomp](https://github.com/krystalgamer/spidey-decomp/tree/f8a039248908e085f8fba8106769aea7f8f9de67), pin `f8a039248908e085f8fba8106769aea7f8f9de67`, had 136 stars. Its README identifies a decompilation project; comparison tools compare original functions against reconstructed DLL exports. No repository-wide LICENSE/COPYING/NOTICE/COPYRIGHT file was found in the untruncated tree, and the reviewed source/build text supplied no overall permissive grant. Do not label it MIT.

CMake links bundled prebuilt zlib libraries and Windows DirectDraw/DirectInput/DirectSound dependencies. Those binaries were not fetched or audited. Reviewed movie code accesses game media archives, fixed original addresses and Bink APIs. Bink wrappers obtain functions from `binkw32_.dll`; several wrappers deliberately loop indefinitely, and the reviewed shell has an unfinished trigger function. These are concrete incomplete/platform dependencies, not proof that a playable Web port exists. The native build handles x86/x86_64 or aarch64, with no reviewed Emscripten path.

**Disposition:** source permission, inherited code and dependency scope, complete independent media/maps/text, and a finished browser platform/runtime remain unresolved. No full-game or clean-room claim.

## Croc: Legend of the Gobbos

[Xeeynamo/croc](https://github.com/Xeeynamo/croc/tree/f30ff1ee6721a172e270adcecab72b5b8a5e9bb1), pin `f30ff1ee6721a172e270adcecab72b5b8a5e9bb1`, had 38 stars. README states the goal of an identical PS1 binary using the European demo SLED-00038, followed by migration to retail. That goal is not completed decompilation evidence. No overall license/notice file was found in the untruncated tree or reviewed texts.

The extraction config requires `disks/sled00038/CROC.EXE`; Makefile targets MIPS/PS1 and extracted assembly/data. `src/croc/3038.c` contains 966 `INCLUDE_ASM` references, including main, input and rendering functions. Reviewed `include/psyq/libgpu.h` bears Sony's 1993–1995 all-rights-reserved notice. Tool submodules have separate pins and would need their own audit; permissive tooling cannot grant permission for game/SDK code or extracted output. No tooling, compiler binary, disc or SDK package was downloaded.

**Disposition:** permission for reconstructed game/SDK code, completion of extracted-assembly functions, independently authored complete content, and a native browser port remain blocked. Running the PS1 binary under emulation would be a different classification and would not satisfy the ROM-free requirement.

No build, browser test, catalog entry or deployment was made. Reopen these candidates when the stated permission, content or source/build evidence changes; asset replacement alone cannot resolve the code restrictions.
