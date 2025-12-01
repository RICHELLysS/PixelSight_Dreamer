
export type AssetType = 'background' | 'tileset' | 'player' | 'npc' | 'enemy';
export type ArtStyle = '8bit' | '16bit' | 'gameboy' | 'isometric';

export interface ArtResult {
    id: string;
    url: string;
    prompt: string;
    type: AssetType;
}

export interface MusicResult {
    id: string;
    url: string;
    title: string;
    duration: number;
}