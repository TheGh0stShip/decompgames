export type PlayMode = 'instant' | 'files' | 'embed';
export type Shelf = 'cleanroom' | 'classic';
export type ProjectKind = 'Decompilation' | 'Recompilation' | 'Engine recreation' | 'Source port' | 'Original implementation' | 'Emulation';
export interface Verification { status: 'unverified' | 'smoke-tested' | 'gameplay-tested'; date: string | null; browsers: string[]; scope: string; playthrough: boolean; }
export interface GameEntry {
  id: string; title: string; aliases: string[]; year: number; genre: string; kind: ProjectKind;
  mode: PlayMode; engine: string; description: string; overview: string; source: string; website?: string;
  engineLicense: string; assetLicense: string; assetRequirements: string; controls: string[];
  saveInstructions: string; limitations: string[]; inputs: string[]; downloadMB: number | null;
  complete: boolean; image?: string; color: string; runtime?: string; dataKey?: string;
  shelf: Shelf; platform: string;
  // Clean-room builds are hosted in their own repositories and framed from embedUrl.
  embedUrl?: string; launch?: 'embed' | 'tab'; requires?: 'webgpu'; touch?: boolean;
  verification: Verification;
}
export interface RuntimeManifest { id: string; packageRevision: string; sourceRevision: string | null; repository: string; toolchain: string; recipe: string; sourceArchive: string; sourceArchiveSha256?: string; sourceArchiveBytes?: number; requirements: string[]; files: { path: string; sha256: string; bytes: number }[]; }
