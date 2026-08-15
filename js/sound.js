/* Synthesized Web Audio Sound System for MOE Prep (Zero external audio assets) */

class SoundEffects {
  constructor() {
    this.ctx = null;
    this.muted = localStorage.getItem("moe_prep_sound_muted") === "true";
  }

  initCtx() {
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) {
        this.ctx = new AudioCtx();
      }
    }
    if (this.ctx && this.ctx.state === "suspended") {
      this.ctx.resume();
    }
  }

  toggleMute() {
    this.muted = !this.muted;
    localStorage.setItem("moe_prep_sound_muted", this.muted ? "true" : "false");
    return this.muted;
  }

  isMuted() {
    return this.muted;
  }

  playTone(freq, duration = 0.15, type = "sine", gainVal = 0.15, delay = 0) {
    if (this.muted) return;
    this.initCtx();
    if (!this.ctx) return;

    setTimeout(() => {
      try {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, this.ctx.currentTime);

        gain.gain.setValueAtTime(gainVal, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, this.ctx.currentTime + duration);

        osc.connect(gain);
        gain.connect(this.ctx.destination);

        osc.start();
        osc.stop(this.ctx.currentTime + duration);
      } catch (e) {
        // audio context handling fallback
      }
    }, delay * 1000);
  }

  playClick() {
    this.playTone(800, 0.04, "triangle", 0.05);
  }

  playCorrect() {
    // Joyful ascending arpeggio (C5 -> E5 -> G5 -> C6)
    this.playTone(523.25, 0.12, "sine", 0.15, 0);
    this.playTone(659.25, 0.12, "sine", 0.15, 0.06);
    this.playTone(783.99, 0.14, "sine", 0.15, 0.12);
    this.playTone(1046.50, 0.25, "sine", 0.2, 0.18);
  }

  playIncorrect() {
    // Gentle low cue (Eb3 -> Bb2)
    this.playTone(155.56, 0.18, "triangle", 0.15, 0);
    this.playTone(116.54, 0.25, "sine", 0.12, 0.08);
  }

  playStreak(combo = 3) {
    // Multi-tone energetic sparkle
    const baseFreq = Math.min(1200, 440 + combo * 50);
    this.playTone(baseFreq, 0.1, "sine", 0.15, 0);
    this.playTone(baseFreq * 1.25, 0.12, "triangle", 0.15, 0.05);
    this.playTone(baseFreq * 1.5, 0.2, "sine", 0.2, 0.1);
  }

  playLevelUp() {
    // Victorious AL1 Fanfare
    const notes = [
      { f: 523.25, d: 0.1, t: 0 },
      { f: 659.25, d: 0.1, t: 0.08 },
      { f: 783.99, d: 0.1, t: 0.16 },
      { f: 1046.50, d: 0.25, t: 0.24 },
      { f: 880.00, d: 0.15, t: 0.45 },
      { f: 1046.50, d: 0.45, t: 0.58 }
    ];
    notes.forEach(n => this.playTone(n.f, n.d, "triangle", 0.18, n.t));
  }

  playConfetti() {
    this.playTone(987.77, 0.15, "sine", 0.2, 0);
    this.playTone(1318.51, 0.3, "triangle", 0.22, 0.08);
  }
}

export const sound = new SoundEffects();
