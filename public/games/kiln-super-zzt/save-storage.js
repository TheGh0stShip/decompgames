/* Copyright 2026 DecompGames contributors. SPDX-License-Identifier: MIT. */
(function () {
  const key = 'decompgames-kiln-super-zzt-saves-v2';
  const status = document.querySelector('#storage');
  let last = null;
  const validName = name => /^[A-Z0-9_-]{1,8}\.SAV$/.test(name);
  const setStatus = text => { status.textContent = text; };
  Module.preRun = [() => {
    try {
      const raw = localStorage.getItem(key);
      if (!raw) return setStatus('No local checkpoint yet.');
      const data = JSON.parse(raw);
      if (!data || typeof data !== 'object' || Array.isArray(data)) throw Error('Invalid stored checkpoint collection');
      const entries = Object.entries(data);
      for (const [name, bytes] of entries) {
        if (!validName(name) || !parseKilnSave(bytes)) throw Error('Stored checkpoint is incompatible');
      }
      let restored = 0;
      for (const [name, bytes] of entries) {
        Module.FS.writeFile('/' + name, new Uint8Array(bytes)); restored++;
      }
      setStatus('Restored ' + restored + ' checkpoint file(s). Use R at the start menu.');
    } catch (e) { setStatus('Local restore failed: ' + e.message); }
  }];
  Module.onRuntimeInitialized = () => {
    window.ready = true;
    setInterval(() => {
      try {
        const saves = {};
        for (const name of Module.FS.readdir('/')) {
          if (!validName(name)) continue;
          const bytes = Array.from(Module.FS.readFile('/' + name));
          if (parseKilnSave(bytes)) saves[name] = bytes;
        }
        if (Object.keys(saves).length === 0) return;
        const encoded = JSON.stringify(saves);
        if (encoded === last) return;
        localStorage.setItem(key, encoded);
        last = encoded;
        setStatus('Checkpoint saved locally.');
      } catch (e) { setStatus('Local save failed: ' + e.message); }
    }, 500);
  };
})();
