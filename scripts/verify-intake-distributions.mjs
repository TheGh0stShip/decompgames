// Audited distributions only; this checks bytes, not licensing or gameplay.
import {readFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import path from 'node:path';

const root = path.resolve('public');
const manifests = ['tennis-sdl', 'craft', 'openduelyst', 'roboden-replacement', '2048', 'open-cadet', 'zzt-demo', 'cinder-abuse', 'kiln-super-zzt', 'beacon-yard', 'paper-rooms', 'beacon-relay'];
const failures = [];
let checked = 0;
for (const id of manifests) {
  const manifest = JSON.parse(await readFile(`public/manifests/${id}.json`, 'utf8'));
  const files = manifest.files.map(file => ({...file, path: manifest.base + file.path}));
  files.push({path: manifest.sourceArchive, sha256: manifest.sourceArchiveSha256 ?? manifest.sourceArchiveSHA256, bytes: manifest.sourceArchiveBytes});
  for (const file of files) {
    const target = path.resolve(root, '.' + file.path);
    if (!file.path.startsWith('/') || !target.startsWith(root + path.sep) || !/^[a-f0-9]{64}$/.test(file.sha256 ?? '')) {
      failures.push(`${id}: invalid path or SHA-256 for ${file.path}`);
      continue;
    }
    try {
      const bytes = await readFile(target);
      const hash = createHash('sha256').update(bytes).digest('hex');
      if (hash !== file.sha256 || (file.bytes !== undefined && bytes.length !== file.bytes)) {
        failures.push(`${id}: distribution mismatch at ${file.path} (${bytes.length} bytes, SHA-256 ${hash})`);
      }
      checked++;
    } catch (error) {
      failures.push(`${id}: cannot read ${file.path}: ${error.message}`);
    }
  }
}
if (failures.length) {
  console.error(failures.join('\n'));
  process.exitCode = 1;
} else {
  console.log(`Verified ${checked} distribution files and source archives across ${manifests.length} audited entries.`);
}
