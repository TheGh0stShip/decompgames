/* Copyright 2026 DecompGames contributors. SPDX-License-Identifier: MIT.
 * Structural admission for this authored four-board pack, not a signature,
 * general Super ZZT validator, or hostile-code sandbox. */
(function (root) {
  function parseKilnSave(bytes) {
    if (!Array.isArray(bytes) || bytes.length < 1026 || bytes.length > 1048576 ||
        !bytes.every(n => Number.isInteger(n) && n >= 0 && n <= 255)) return null;
    const u = new Uint8Array(bytes), v = new DataView(u.buffer);
    const i16 = p => v.getInt16(p, true), u16 = p => v.getUint16(p, true);
    function name(p, limit) {
      if (u[p] > limit) return null;
      let out = '';
      for (let n = 1; n <= u[p]; n++) {
        if (u[p + n] < 32 || u[p + n] > 126) return null;
        out += String.fromCharCode(u[p + n]);
      }
      return out;
    }
    if (i16(0) !== -2 || i16(2) !== 3 || name(27, 20) !== 'KILN' || u[388] !== 1) return null;
    const current = i16(17);
    if (current < 0 || current > 3) return null;
    for (let p = 48; p <= 363; p += 21) if (name(p, 20) === null) return null;
    for (let p = 8; p <= 14; p++) if (u[p] > 1) return null;
    let pos = 1024;
    const boards = [];
    for (let bid = 0; bid <= 3; bid++) {
      if (pos + 2 > u.length) return null;
      const len = u16(pos); pos += 2;
      const end = pos + len;
      if (len < 119 || end > u.length) return null;
      const label = name(pos, 60);
      if (label !== ['Kiln title', 'Relay Hall', 'Current Gallery', 'Kiln complete'][bid]) return null;
      pos += 61;
      let cells = 0;
      while (cells < 7680) {
        if (pos + 3 > end) return null;
        const count = u[pos], element = u[pos + 1];
        if (count === 0 || element > 80 || cells + count > 7680) return null;
        cells += count; pos += 3;
      }
      if (pos + 30 > end || u[pos + 5] > 1) return null;
      for (let n = 1; n <= 4; n++) if (u[pos + n] > 3) return null;
      if (u[pos + 6] < 1 || u[pos + 6] > 96 || u[pos + 7] < 1 || u[pos + 7] > 80) return null;
      pos += 28;
      const statCount = i16(pos); pos += 2;
      if (statCount < 0 || statCount > 128) return null;
      const stats = [];
      for (let sid = 0; sid <= statCount; sid++) {
        if (pos + 25 > end) return null;
        const x = u[pos], y = u[pos + 1];
        if (x > 96 || y > 80 || ((x === 0) !== (y === 0)) || (sid === 0 && x === 0)) return null;
        for (const p of [11, 13]) if (i16(pos + p) < -1 || i16(pos + p) > statCount) return null;
        if (u[pos + 15] > 80 || v.getUint32(pos + 17, true) !== 0) return null;
        const codeLen = i16(pos + 23), codePos = i16(pos + 21);
        if (codeLen < 0 && (-codeLen < 1 || -codeLen >= sid)) return null;
        if (codeLen >= 0 && (codePos < -1 || codePos > codeLen)) return null;
        pos += 25;
        if (codeLen > 0) { if (pos + codeLen > end) return null; pos += codeLen; }
        stats.push({x, y, codeLen});
      }
      if (pos !== end) return null;
      boards.push({name: label, player: stats[0], statCount: stats.length});
    }
    if (pos !== u.length) return null;
    return {version: -2, currentBoard: current, ammo: i16(4), gems: i16(6),
      health: i16(15), score: i16(25), stones: i16(389), flags: Array.from({length:16}, (_,n)=>name(48+n*21,20)).filter(Boolean), keys: Array.from(u.slice(8,15)), boards};
  }
  root.parseKilnSave = parseKilnSave;
  if (typeof module !== 'undefined') module.exports = {parseKilnSave};
})(typeof globalThis !== 'undefined' ? globalThis : this);
