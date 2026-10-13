# Tennis browser build

Pinned author source catsocks/tennis-sdl 0338d21bc13994ffa440ce70375e1369ef2a64e8, CC0 except explicit third-party notices. Procedural shapes/digits and generated tones require no ROM/data/assets. This is an original Pong-style implementation, not a retail decompilation. Source MIT exceptions retain notices; bundled SDL2 is zlib, Emscripten MIT/NCSA. Silent edition modifications are in silent-edition.patch and the source archive.

Rebuild source archive src/*.c using emcc -O2 -std=c99 -sUSE_SDL=2 -sWASM=1 -sEXPORTED_FUNCTIONS='["_main","_browser_value"]' -o game.js. Use supplied host index.html. Audio device stays paused, tone generation/queue disabled, M does not unmute. Read-only browser_value diagnostic export reports paddles/ball/score/pause/mute/time. No cheats enabled.

2026-10-09 muted headless Edge test PASS: both keyboard paddles, moving ball, real scored point, pause game-time freeze, resume, restart clears score, M remains mute, page errors empty. Touch/controller and complete match playthrough unverified. No persistence implemented; round restarts on reload. Players closed after test. No external publishing.
