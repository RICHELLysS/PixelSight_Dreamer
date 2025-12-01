import { defineStore } from 'pinia';
import axios from 'axios';
import type { ArtResult, MusicResult, AssetType, ArtStyle } from '../types';

export const usePixelStore = defineStore('pixel', {
    state: () => ({
        mode: 'art' as 'art' | 'music',
        isGenerating: false,
        artResults: [] as ArtResult[],
        musicResults: [] as MusicResult[],
        apiBase: 'http://localhost:5000/api'
    }),
    actions: {
        async generateArt(prompt: string, style: ArtStyle, type: AssetType) {
            this.isGenerating = true;
            try {
                const res = await axios.post(`${this.apiBase}/generate-art`, {
                    prompt, style, type
                });
                
                this.artResults.unshift({
                    id: Date.now().toString(),
                    url: res.data.url,
                    prompt: res.data.prompt_used,
                    type: type
                });
            } catch (error) {
                console.error("Art Gen Failed", error);
                alert("生成失败，请检查后端连接");
            } finally {
                this.isGenerating = false;
            }
        },
        async generateMusic(prompt: string, mood: string, duration: number) {
            this.isGenerating = true;
            try {
                // 拼接 MusicGen 的提示词
                const fullPrompt = `8-bit chiptune, ${mood}, ${prompt}, video game music loops`;
                
                const res = await axios.post(`${this.apiBase}/generate-music`, {
                    prompt: fullPrompt, duration
                });

                this.musicResults.unshift({
                    id: Date.now().toString(),
                    url: res.data.url,
                    title: prompt,
                    duration
                });
            } catch (error) {
                console.error("Music Gen Failed", error);
            } finally {
                this.isGenerating = false;
            }
        }
    }
});
