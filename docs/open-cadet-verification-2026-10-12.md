# Open Cadet verification checkpoint


2026-10-12 Open Cadet input/settings checkpoint: live muted normal F2 changes table to Awaiting Deployment; Space/Z/slash inputs submitted, but capture does not prove launch/scoring or full flipper response. Engine generates /libsdl/SpaceCadetPinball/imgui_pb.ini with empty high-score slots(-999). Separate Stop/Start test restores this settings file byteforbyte (open-cadet-settings-persistence-2026-10-12.json), errors empty, browser stopped/closed. Initial harness Unicode button selector was misdecoded and timedout; stable #start-game selector corrected, rerunpassed. This verifies settings persistence only, NOT a played high-score or ball-in-progress save. Sound off/--mute-audio preserved; no audible verification.

Existing entry; not counted as a new game. No deployment or catalog verification promotion.


2026-10-12 live launch/flipper visual checks: sustained Space2500ms then release visibly moves ball from right launchlane into upper table, with mission instruction changing from Awaiting Deployment. Held Z+slash raises bothflippers; release restores lowered pose in paired captures. These are actual normalkeyboard/production runtime checks, errors empty, Sound off/--mute-audio, Stop pressed/browserclosed. Screenshot hashes retained in open-cadet-gameplay-input-2026-10-12.json; captures private. Numeric score fields are not readable in reviewed captures, so no visible score or played high-score persistence proof. Next inspect score rendering/data and obtain completed-game/high-score evidence; do not substitute injected high-scorefile for played proof.
