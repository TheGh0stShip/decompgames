# N64 catalog provenance follow-up

Read-only pinned source/document review. No ROM acquisition, no browser/player launch, no new gameplay verification. Existing titles are duplicates, not new intake completions.

| Entry | Source pin | Precise blockers |
|---|---|---|
| Mario Kart 64 | `a9c8262bea9aee4d3b33cdfe17602b72740e8916` | Decompilation-built ROM runs in EmulatorJS. Retains game C, geometry/data, music, RSP microcode and IPL3 boot code; selected regenerated media does not clear these components. |
| Banjo-Kazooie | `5f0b15be10771520d5091f0736d33a79b9d34e25` | Decompilation-built ROM runs in EmulatorJS. Retains geometry/display lists, collision, animation, setups, dialogue/quiz text, music, microcode and boot/assembly code. |
| Donkey Kong 64 | `f77e4aa84c48bfd488d93d1442bea37abe861ac0` | Modified ROM runs in EmulatorJS. STATUS explicitly says matching retail code bytes, boot and overlays are retained; geometry, animation, scripts, cutscenes, text, music and demos remain. Not evidence that this distribution compiles decompiled source. |

Evidence: pinned [MK64 README](https://github.com/andrewnakas/mk64-cleanroom/blob/a9c8262bea9aee4d3b33cdfe17602b72740e8916/README.md), [Banjo README](https://github.com/andrewnakas/bk-cleanroom/blob/5f0b15be10771520d5091f0736d33a79b9d34e25/README.md), [DK64 README](https://github.com/andrewnakas/dk64-cleanroom/blob/f77e4aa84c48bfd488d93d1442bea37abe861ac0/README.md) and [DK64 STATUS](https://github.com/andrewnakas/dk64-cleanroom/blob/f77e4aa84c48bfd488d93d1442bea37abe861ac0/STATUS.md). Upstream MK64/Banjo README identifies EmulatorJS GPL-3.0 and mupen64plus-next GPL-2.0; this is separate from game code/content and does not constitute a complete runtime dependency audit.

Corrected metadata and moved these entries to the classic shelf. Added Emulation classification for DK64 while preserving MK64/Banjo's decompilation source classification and explicitly describing emulator execution. Preserved external links and historical verification records. No formal clean-room certification, no complete permissive content clearance, no new eligible game. Source builds owned by Claude were unchanged; Mario Party 2/3 were untouched. No whole-site deployment for this metadata change.
