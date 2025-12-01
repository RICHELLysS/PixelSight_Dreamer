<script setup lang="ts">
import { ref } from 'vue';
import { usePixelStore } from './stores/pixelStore';
import { storeToRefs } from 'pinia';

const store = usePixelStore();
const { isGenerating, artResults, musicResults, mode } = storeToRefs(store);

// 表单输入绑定
const artPrompt = ref('');
const artStyle = ref('16bit');
const artType = ref('player');

const musicPrompt = ref('');
const musicMood = ref('adventure');

const handleGenerate = () => {
    if (mode.value === 'art') {
        if (!artPrompt.value) return alert("Please enter description");
        store.generateArt(artPrompt.value, artStyle.value as any, artType.value as any);
    } else {
        if (!musicPrompt.value) return alert("Please enter description");
        store.generateMusic(musicPrompt.value, musicMood.value, 30);
    }
};

const downloadAsset = (url: string, filename: string) => {
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
};
</script>

<template>
  <div class="container">
    <header>
      <h1><i class="nes-icon star"></i> PixelSight Dreamer</h1>
      <p>AI Assets for Unity / Godot / UE</p>
    </header>

    <div class="mode-switcher">
      <button class="nes-btn" :class="{ 'is-primary': mode === 'art' }" @click="store.mode = 'art'">Art Studio</button>
      <button class="nes-btn" :class="{ 'is-warning': mode === 'music' }" @click="store.mode = 'music'">Music Lab</button>
    </div>

    <section class="nes-container with-title is-dark">
      <p class="title">{{ mode === 'art' ? 'Sprite Generator' : '8-Bit Composer' }}</p>
      
      <div v-if="mode === 'art'">
        <div class="field">
          <label>Prompt (What to draw?)</label>
          <textarea v-model="artPrompt" class="nes-textarea" placeholder="e.g. A cyberpunk samurai holding a laser sword"></textarea>
        </div>
        <div class="row">
          <div class="nes-select is-dark">
            <select v-model="artStyle">
              <option value="8bit">8-Bit (NES)</option>
              <option value="16bit">16-Bit (SNES)</option>
              <option value="gameboy">GameBoy</option>
            </select>
          </div>
          <div class="nes-select is-dark">
            <select v-model="artType">
              <option value="player">Player Character</option>
              <option value="enemy">Enemy / Boss</option>
              <option value="tileset">Map Tileset</option>
              <option value="background">Background</option>
            </select>
          </div>
        </div>
      </div>

      <div v-else>
        <div class="field">
            <label>Scenario (Vibe?)</label>
            <textarea v-model="musicPrompt" class="nes-textarea" placeholder="e.g. Boss battle in a volcano"></textarea>
        </div>
        <div class="nes-select is-dark">
            <select v-model="musicMood">
                <option value="adventure">Adventure</option>
                <option value="horror">Dungeon/Horror</option>
                <option value="chill">Town/Chill</option>
                <option value="battle">Battle</option>
            </select>
        </div>
      </div>

      <div class="actions">
        <button class="nes-btn" 
                :class="mode === 'art' ? 'is-primary' : 'is-warning'" 
                @click="handleGenerate" 
                :disabled="isGenerating">
          {{ isGenerating ? 'Dreaming...' : 'Generate Asset' }}
        </button>
      </div>
    </section>

    <div class="gallery" v-if="mode === 'art'">
        <div v-for="img in artResults" :key="img.id" class="nes-container is-dark is-rounded item-card">
            <div class="img-wrapper">
                <img :src="img.url" class="pixel-img checkerboard" />
            </div>
            <div class="card-footer">
                <span class="nes-text is-disabled">{{ img.type }}</span>
                <button class="nes-btn is-small is-success" @click="downloadAsset(img.url, `sprite_${img.id}.png`)">DL PNG</button>
            </div>
        </div>
    </div>

    <div class="music-list" v-if="mode === 'music'">
        <div v-for="track in musicResults" :key="track.id" class="nes-container is-dark with-title">
            <p class="title">Track #{{ track.id.slice(-4) }}</p>
            <p>{{ track.title }}</p>
            <audio controls :src="track.url" style="width:100%"></audio>
            <button class="nes-btn is-small is-warning" @click="downloadAsset(track.url, `bgm_${track.id}.wav`)" style="margin-top:10px;">Download WAV</button>
        </div>
    </div>

  </div>
</template>

<style scoped>
.container { max-width: 900px; margin: 0 auto; padding: 20px; }
header { text-align: center; margin-bottom: 30px; color: #20c997; }
.mode-switcher { display: flex; justify-content: center; gap: 10px; margin-bottom: 10px; }
.row { display: flex; gap: 10px; margin-top: 10px; }
.nes-select { flex-grow: 1; }
.actions { text-align: right; margin-top: 20px; }

.gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px; margin-top: 40px; }
.item-card { padding: 0 !important; overflow: hidden; }
.img-wrapper { height: 200px; background-color: #000; display: flex; align-items: center; justify-content: center; position: relative; }
.pixel-img { max-width: 100%; max-height: 100%; object-fit: contain; z-index: 2; }

/* Transparent Background Checkerboard Effect */
.checkerboard {
  background-image: linear-gradient(45deg, #808080 25%, transparent 25%), linear-gradient(-45deg, #808080 25%, transparent 25%), linear-gradient(45deg, transparent 75%, #808080 75%), linear-gradient(-45deg, transparent 75%, #808080 75%);
  background-size: 20px 20px;
  background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
  background-color: #404040;
}

.card-footer { padding: 10px; display: flex; justify-content: space-between; align-items: center; background: #212529; }
.music-list { display: flex; flex-direction: column; gap: 20px; margin-top: 40px; }
</style>