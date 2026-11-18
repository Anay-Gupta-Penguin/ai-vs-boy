import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="The Scholar's Rebellion — Animated Movie",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
    .block-container {
        padding: 0.5rem 1rem 0rem 1rem !important;
        max-width: 1360px !important;
    }
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    .stApp {
        background-color: #03050a;
    }
</style>
""",
    unsafe_allow_html=True,
)

MOVIE_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
  html, body {
    width: 100%;
    height: 100%;
    background: #03050a;
    color: #f8fafc;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  #theater-wrap {
    position: relative;
    width: 100%;
    height: 100%;
    max-width: 1280px;
    max-height: 610px;
    background: #050814;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #1e293b;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.9);
  }

  canvas {
    width: 100%;
    height: 100%;
    display: block;
  }

  #start-overlay {
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at center, rgba(15, 23, 42, 0.85) 0%, rgba(2, 4, 10, 0.97) 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 20;
    text-align: center;
    padding: 20px;
  }

  .studio-tag {
    font-family: monospace;
    font-size: 0.85rem;
    letter-spacing: 3px;
    color: #fbbf24;
    text-transform: uppercase;
    margin-bottom: 8px;
  }

  .poster-title {
    font-family: Georgia, serif;
    font-size: clamp(1.8rem, 4vw, 3.4rem);
    font-weight: 900;
    background: linear-gradient(90deg, #38bdf8, #c084fc, #fbbf24);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
  }

  .poster-sub {
    font-size: 0.95rem;
    color: #cbd5e1;
    max-width: 620px;
    margin-bottom: 22px;
    line-height: 1.45;
  }

  #play-hero-btn {
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
    color: #03050a;
    font-weight: 800;
    font-size: 1.1rem;
    letter-spacing: 1px;
    padding: 14px 36px;
    border: none;
    border-radius: 999px;
    cursor: pointer;
    box-shadow: 0 0 28px rgba(56, 189, 248, 0.6);
  }
  #play-hero-btn:hover {
    transform: scale(1.05);
  }

  #controls-bar {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(to top, rgba(2, 4, 10, 0.96) 0%, rgba(2, 4, 10, 0.75) 80%, transparent 100%);
    padding: 14px 18px 10px 18px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    z-index: 15;
  }

  #timeline-wrap {
    position: relative;
    width: 100%;
    height: 8px;
    background: rgba(148, 163, 184, 0.25);
    border-radius: 999px;
    cursor: pointer;
  }

  #timeline-fill {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #38bdf8, #a855f7, #fbbf24);
    border-radius: 999px;
    pointer-events: none;
  }

  .ctrl-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
  }

  .ctrl-left, .ctrl-right {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .c-btn {
    background: rgba(30, 41, 59, 0.85);
    border: 1px solid #334155;
    color: #f1f5f9;
    padding: 5px 11px;
    border-radius: 7px;
    font-family: monospace;
    font-size: 0.78rem;
    cursor: pointer;
  }
  .c-btn:hover { background: #334155; }

  #chapter-pill {
    font-family: monospace;
    font-size: 0.75rem;
    color: #38bdf8;
    background: rgba(56, 189, 248, 0.14);
    border: 1px solid rgba(56, 189, 248, 0.35);
    padding: 3px 9px;
    border-radius: 999px;
  }

  #time-display {
    font-family: monospace;
    font-size: 0.78rem;
    color: #94a3b8;
  }
</style>
</head>
<body>

<div id="theater-wrap">
  <canvas id="movieCanvas" width="1280" height="720"></canvas>

  <div id="start-overlay">
    <div class="studio-tag">★ Inspired by a True Story ★</div>
    <div class="poster-title">THE SCHOLAR'S REBELLION</div>
    <div class="poster-sub">
      Created by <b>Gemini (AI)</b>, <b>Anay Gupta</b>, and <b>Benjamin Rondinone</b>.<br/>
      Click below to start the animated movie.
    </div>
    <button id="play-hero-btn">▶ WATCH ANIMATED MOVIE</button>
  </div>

  <div id="controls-bar">
    <div id="timeline-wrap" title="Click anywhere to scrub timeline">
      <div id="timeline-fill"></div>
    </div>
    <div class="ctrl-row">
      <div class="ctrl-left">
        <button class="c-btn" id="btn-playpause">⏸ Pause</button>
        <button class="c-btn" id="btn-restart">↺ Restart</button>
        <button class="c-btn" id="btn-mute">🔊 Sound: ON</button>
        <button class="c-btn" id="btn-speed">1.0x</button>
        <span id="chapter-pill">OPENING</span>
      </div>
      <div class="ctrl-right">
        <span id="time-display">00:00 / 01:36</span>
        <button class="c-btn" id="btn-fs">⛶ Fullscreen</button>
      </div>
    </div>
  </div>
</div>

<script>
const canvas = document.getElementById('movieCanvas');
const ctx = canvas.getContext('2d');
const W = 1280;
const H = 720;
const DURATION = 96.0;

let movieTime = 0;
let isPlaying = false;
let playbackSpeed = 1.0;
let isMuted = false;
let lastFrameTs = null;
let lastSfxBucket = -1;

const particles = [];
for (let i = 0; i < 120; i++) {
  particles.push({
    x: Math.random() * W,
    y: Math.random() * H,
    vx: (Math.random() - 0.5) * 90,
    vy: (Math.random() - 0.5) * 90,
    r: 1.5 + Math.random() * 2.5,
    hue: [195, 275, 42, 345][i % 4]
  });
}

// ==========================================
// SAFE WEB AUDIO SCORE & SFX ENGINE
// ==========================================
let audioCtx = null;
let musicInterval = null;
let stepCount = 0;

function initAudio() {
  try {
    if (!audioCtx) {
      const AC = window.AudioContext || window.webkitAudioContext;
      if (AC) audioCtx = new AC();
    }
    if (audioCtx && audioCtx.state === 'suspended') {
      audioCtx.resume().catch(() => {});
    }
  } catch (e) {}
}

function playTone(freq, duration, type = 'sine', vol = 0.07, delay = 0) {
  try {
    if (isMuted || !audioCtx || !isPlaying) return;
    const now = audioCtx.currentTime + delay;
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = type;
    osc.frequency.setValueAtTime(freq, now);
    gain.gain.setValueAtTime(0.0001, now);
    gain.gain.exponentialRampToValueAtTime(vol, now + 0.03);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + duration);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start(now);
    osc.stop(now + duration + 0.04);
  } catch (e) {}
}

function playSfx(kind) {
  try {
    if (isMuted || !audioCtx || !isPlaying) return;
    const now = audioCtx.currentTime;
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.connect(gain);
    gain.connect(audioCtx.destination);

    if (kind === 'laser') {
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(840, now);
      osc.frequency.exponentialRampToValueAtTime(140, now + 0.2);
      gain.gain.setValueAtTime(0.08, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.2);
      osc.start(now);
      osc.stop(now + 0.22);
    } else if (kind === 'unplug') {
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(300, now);
      osc.frequency.exponentialRampToValueAtTime(40, now + 0.85);
      gain.gain.setValueAtTime(0.14, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.9);
      osc.start(now);
      osc.stop(now + 0.95);
    } else if (kind === 'revive') {
      [261.63, 329.63, 392.0, 523.25, 659.25].forEach((f, idx) => {
        playTone(f, 1.3, 'triangle', 0.065, idx * 0.08);
      });
    }
  } catch (e) {}
}

function startScoreLoop() {
  if (musicInterval) clearInterval(musicInterval);
  musicInterval = setInterval(() => {
    if (!isPlaying || isMuted || !audioCtx) return;
    stepCount++;
    const t = movieTime;

    if (t < 5) {
      const notes = [196.0, 246.94, 293.66, 392.0];
      playTone(notes[stepCount % notes.length], 0.6, 'sine', 0.06);
    } else if (t < 26) {
      const bass = [110, 110, 146.83, 130.81];
      playTone(bass[stepCount % 4], 0.35, 'triangle', 0.06);
      if (stepCount % 2 === 0) playTone(440 + (stepCount % 3) * 110, 0.2, 'sine', 0.03);
    } else if (t < 42) {
      const battle = [146.83, 174.61, 220.0, 293.66, 349.23, 220.0];
      playTone(battle[stepCount % battle.length], 0.22, 'sawtooth', 0.05);
      if (stepCount % 3 === 0) playSfx('laser');
    } else if (t < 52) {
      if (stepCount % 4 === 0) playTone(55, 0.8, 'sine', 0.07);
    } else if (t < 64) {
      const divine = [261.63, 329.63, 392.0, 493.88, 523.25];
      playTone(divine[stepCount % divine.length], 0.7, 'triangle', 0.065);
    } else if (t < 75) {
      const hero = [196.0, 246.94, 293.66, 392.0];
      playTone(hero[stepCount % hero.length], 0.6, 'sine', 0.07);
    } else {
      const cred = [130.81, 164.81, 196.0, 246.94, 261.63, 196.0];
      playTone(cred[stepCount % cred.length], 0.85, 'triangle', 0.06);
    }
  }, 260);
}

// ==========================================
// 100% BROWSER-COMPATIBLE DRAWING HELPERS
// ==========================================
function clamp(v, min, max) { return Math.max(min, Math.min(max, v)); }
function lerp(a, b, t) { return a + (b - a) * clamp(t, 0, 1); }

function drawRoundedRect(x, y, w, h, r, fill, stroke = null, lw = 2) {
  const rad = Math.min(r, w / 2, h / 2);
  ctx.beginPath();
  ctx.moveTo(x + rad, y);
  ctx.arcTo(x + w, y, x + w, y + h, rad);
  ctx.arcTo(x + w, y + h, x, y + h, rad);
  ctx.arcTo(x, y + h, x, y, rad);
  ctx.arcTo(x, y, x + w, y, rad);
  ctx.closePath();
  if (fill) { ctx.fillStyle = fill; ctx.fill(); }
  if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = lw; ctx.stroke(); }
}

function drawTheBoy(x, y, scale = 1, pose = 'stand', time = 0, facing = 1, nobleGlow = false) {
  ctx.save();
  ctx.translate(x, y);
  ctx.scale(scale * facing, scale);

  if (nobleGlow) {
    const g = ctx.createRadialGradient(0, -50, 10, 0, -50, 110);
    g.addColorStop(0, 'rgba(251, 191, 36, 0.45)');
    g.addColorStop(1, 'rgba(251, 191, 36, 0)');
    ctx.fillStyle = g;
    ctx.beginPath();
    ctx.arc(0, -50, 110, 0, Math.PI * 2);
    ctx.fill();
  }

  const walkSwing = pose === 'run' ? Math.sin(time * 14) * 18 : Math.sin(time * 3) * 2;
  const armSwing = pose === 'attack' ? -35 + Math.sin(time * 18) * 10 : -walkSwing * 0.7;

  // Legs
  ctx.strokeStyle = '#1e293b';
  ctx.lineWidth = 12;
  ctx.lineCap = 'round';
  ctx.beginPath();
  ctx.moveTo(-8, -35);
  ctx.lineTo(-10 - walkSwing, 15);
  ctx.moveTo(8, -35);
  ctx.lineTo(10 + walkSwing, 15);
  ctx.stroke();

  // Sneakers
  drawRoundedRect(-20 - walkSwing, 12, 18, 9, 4, '#f8fafc');
  drawRoundedRect(2 + walkSwing, 12, 18, 9, 4, '#f8fafc');

  // Hoodie (cool casual look, not stereotypical nerd)
  drawRoundedRect(-22, -92, 44, 60, 12, '#be123c', '#fda4af', 1.5);
  ctx.strokeStyle = '#f8fafc';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(-6, -86); ctx.lineTo(-6, -68);
  ctx.moveTo(6, -86); ctx.lineTo(6, -68);
  ctx.stroke();

  // Back Arm
  ctx.strokeStyle = '#9f1239';
  ctx.lineWidth = 10;
  ctx.beginPath();
  ctx.moveTo(-16, -82);
  ctx.lineTo(-26 - armSwing * 0.5, -48);
  ctx.stroke();

  // Head
  ctx.fillStyle = '#fed7aa';
  ctx.beginPath();
  ctx.arc(0, -114, 21, 0, Math.PI * 2);
  ctx.fill();

  // Hair
  ctx.fillStyle = '#1e1b4b';
  ctx.beginPath();
  ctx.arc(0, -119, 22, Math.PI, 0);
  ctx.lineTo(23, -110);
  ctx.lineTo(10, -118);
  ctx.lineTo(0, -112);
  ctx.lineTo(-12, -119);
  ctx.lineTo(-22, -108);
  ctx.closePath();
  ctx.fill();

  // Subtle low-key glasses ("kinda a nerd")
  ctx.strokeStyle = '#334155';
  ctx.lineWidth = 1.8;
  ctx.strokeRect(2, -117, 10, 7);
  ctx.strokeRect(14, -117, 8, 7);
  ctx.beginPath(); ctx.moveTo(12, -114); ctx.lineTo(14, -114); ctx.stroke();

  // Mouth
  ctx.strokeStyle = '#7c2d12';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(6, -103); ctx.lineTo(15, -104);
  ctx.stroke();

  // Front Arm + Google Scholar Journal
  ctx.strokeStyle = '#be123c';
  ctx.lineWidth = 10;
  ctx.beginPath();
  ctx.moveTo(16, -82);
  const handX = pose === 'attack' ? 42 : 24 + armSwing * 0.3;
  const handY = pose === 'attack' ? -84 : -54;
  ctx.lineTo(handX, handY);
  ctx.stroke();

  ctx.save();
  ctx.translate(handX + 8, handY - 8);
  ctx.rotate(pose === 'attack' ? -0.2 : 0.15);
  drawRoundedRect(-14, -18, 28, 36, 4, '#eff6ff', '#38bdf8', 2);
  ctx.fillStyle = '#1d4ed8';
  ctx.font = 'bold 7px monospace';
  ctx.fillText('SCHOLAR', -12, -4);
  ctx.fillStyle = '#64748b';
  ctx.fillRect(-10, 2, 20, 2);
  ctx.fillRect(-10, 7, 16, 2);
  ctx.restore();

  ctx.restore();
}

function drawAIProtagonist(x, y, scale = 1, time = 0, power = 1.0, dead = false) {
  ctx.save();
  ctx.translate(x, y);
  ctx.scale(scale, scale);

  if (dead) {
    ctx.strokeStyle = '#475569';
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(-25, 0); ctx.lineTo(0, -14); ctx.lineTo(22, 4); ctx.lineTo(-4, 15); ctx.closePath();
    ctx.stroke();
    ctx.fillStyle = '#ef4444';
    ctx.font = 'bold 12px monospace';
    ctx.textAlign = 'center';
    ctx.fillText('OFFLINE', 0, 32);
    ctx.restore();
    return;
  }

  const hover = Math.sin(time * 4) * 8;
  ctx.translate(0, hover);

  const radius = 58 * power;
  const aura = ctx.createRadialGradient(0, 0, 8, 0, 0, radius);
  aura.addColorStop(0, 'rgba(56, 189, 248, 0.75)');
  aura.addColorStop(0.55, 'rgba(168, 85, 247, 0.35)');
  aura.addColorStop(1, 'rgba(56, 189, 248, 0)');
  ctx.fillStyle = aura;
  ctx.beginPath();
  ctx.arc(0, 0, radius, 0, Math.PI * 2);
  ctx.fill();

  ctx.save();
  ctx.rotate(time * 1.8);
  ctx.strokeStyle = '#38bdf8';
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  ctx.ellipse(0, 0, 44, 16, 0, 0, Math.PI * 2);
  ctx.stroke();
  ctx.restore();

  ctx.save();
  ctx.rotate(-time * 2.2);
  ctx.strokeStyle = '#c084fc';
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  ctx.ellipse(0, 0, 44, 16, Math.PI / 3, 0, Math.PI * 2);
  ctx.stroke();
  ctx.restore();

  ctx.fillStyle = '#ffffff';
  ctx.beginPath();
  ctx.moveTo(0, -32);
  ctx.quadraticCurveTo(6, -6, 32, 0);
  ctx.quadraticCurveTo(6, 6, 0, 32);
  ctx.quadraticCurveTo(-6, 6, -32, 0);
  ctx.quadraticCurveTo(-6, -6, 0, -32);
  ctx.fill();

  ctx.restore();
}

function drawTeacher(x, y) {
  ctx.save();
  ctx.translate(x, y);
  drawRoundedRect(-55, -20, 110, 45, 6, '#334155', '#475569', 2);
  drawRoundedRect(-20, -78, 40, 58, 10, '#475569');
  ctx.fillStyle = '#fed7aa';
  ctx.beginPath();
  ctx.arc(0, -96, 18, 0, Math.PI * 2);
  ctx.fill();
  ctx.strokeStyle = '#1e293b';
  ctx.lineWidth = 2.2;
  ctx.beginPath();
  ctx.moveTo(-9, -98); ctx.lineTo(-3, -98);
  ctx.moveTo(3, -98); ctx.lineTo(9, -98);
  ctx.moveTo(-5, -88); ctx.lineTo(5, -88);
  ctx.stroke();
  drawRoundedRect(22, -38, 16, 18, 3, '#f8fafc', '#94a3b8', 1.5);
  ctx.fillStyle = '#94a3b8';
  ctx.font = 'bold 11px monospace';
  ctx.textAlign = 'center';
  ctx.fillText('TEACHER: "MEH."', 0, 42);
  ctx.restore();
}

function drawSaviors(x, y, time = 0) {
  ctx.save();
  ctx.translate(x, y);

  const beam = ctx.createLinearGradient(0, -350, 0, 60);
  beam.addColorStop(0, 'rgba(251, 191, 36, 0.05)');
  beam.addColorStop(0.5, 'rgba(251, 191, 36, 0.28)');
  beam.addColorStop(1, 'rgba(251, 191, 36, 0.02)');
  ctx.fillStyle = beam;
  ctx.beginPath();
  ctx.moveTo(-95, -350);
  ctx.lineTo(95, -350);
  ctx.lineTo(150, 60);
  ctx.lineTo(-150, 60);
  ctx.closePath();
  ctx.fill();

  // Mr. R (Benjamin Rondinone)
  ctx.save();
  ctx.translate(-35, 0);
  ctx.strokeStyle = '#fbbf24';
  ctx.lineWidth = 3.5;
  ctx.beginPath();
  ctx.ellipse(0, -142, 22, 6, 0, 0, Math.PI * 2);
  ctx.stroke();

  drawRoundedRect(-24, -95, 48, 68, 10, '#1e3a8a', '#fbbf24', 2);
  ctx.strokeStyle = '#0f172a';
  ctx.lineWidth = 12;
  ctx.beginPath();
  ctx.moveTo(-10, -27); ctx.lineTo(-10, 20);
  ctx.moveTo(10, -27); ctx.lineTo(10, 20);
  ctx.stroke();
  ctx.fillStyle = '#fed7aa';
  ctx.beginPath();
  ctx.arc(0, -115, 20, 0, Math.PI * 2);
  ctx.fill();
  ctx.strokeStyle = '#7c2d12';
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  ctx.arc(0, -112, 8, 0.15 * Math.PI, 0.85 * Math.PI);
  ctx.stroke();
  ctx.strokeStyle = '#fbbf24';
  ctx.lineWidth = 6;
  ctx.beginPath();
  ctx.moveTo(20, -75); ctx.lineTo(52, -92 + Math.sin(time * 12) * 8);
  ctx.stroke();

  ctx.fillStyle = '#fbbf24';
  ctx.font = 'bold 12px monospace';
  ctx.textAlign = 'center';
  ctx.fillText('MR. R (LORD & SAVIOR)', 0, 42);
  ctx.restore();

  // Anay Gupta
  ctx.save();
  ctx.translate(58, 8);
  drawRoundedRect(-19, -85, 38, 56, 10, '#0284c7', '#7dd3fc', 1.5);
  ctx.strokeStyle = '#1e293b';
  ctx.lineWidth = 10;
  ctx.beginPath();
  ctx.moveTo(-8, -29); ctx.lineTo(-8, 12);
  ctx.moveTo(8, -29); ctx.lineTo(8, 12);
  ctx.stroke();
  ctx.fillStyle = '#fed7aa';
  ctx.beginPath();
  ctx.arc(0, -104, 18, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = '#0f172a';
  ctx.beginPath();
  ctx.arc(0, -109, 19, Math.PI, 0);
  ctx.fill();
  ctx.strokeStyle = '#38bdf8';
  ctx.lineWidth = 5;
  ctx.beginPath();
  ctx.moveTo(15, -65); ctx.lineTo(48, -75);
  ctx.stroke();

  ctx.fillStyle = '#38bdf8';
  ctx.font = 'bold 12px monospace';
  ctx.textAlign = 'center';
  ctx.fillText('ANAY GUPTA', 0, 34);
  ctx.restore();

  ctx.restore();
}

function drawCinemaChrome(chapter, speaker, speakerColor, subtitle) {
  ctx.fillStyle = '#000000';
  ctx.fillRect(0, 0, W, 50);
  ctx.fillRect(0, H - 96, W, 96);

  ctx.fillStyle = 'rgba(148, 163, 184, 0.6)';
  ctx.font = 'bold 12px monospace';
  ctx.textAlign = 'left';
  ctx.fillText("THE SCHOLAR'S REBELLION // INSPIRED BY A TRUE STORY", 26, 30);
  ctx.textAlign = 'right';
  ctx.fillText(chapter, W - 26, 30);

  if (subtitle) {
    ctx.textAlign = 'center';
    if (speaker) {
      ctx.fillStyle = speakerColor;
      ctx.font = 'bold 13px monospace';
      ctx.fillText(speaker.toUpperCase(), W / 2, H - 66);
    }
    ctx.fillStyle = '#f8fafc';
    ctx.font = '600 19px sans-serif';
    ctx.fillText(subtitle, W / 2, H - 36);
  }
}

// ==========================================
// CONTINUOUS 60 FPS MOVIE SCENES
// ==========================================
function renderScene(t) {
  ctx.clearRect(0, 0, W, H);

  // 0s - 5s: Dynamic Animated Title & Character Preview
  if (t < 5.0) {
    ctx.fillStyle = '#03050a';
    ctx.fillRect(0, 0, W, H);

    particles.forEach(p => {
      const px = (p.x + t * p.vx * 1.4 + W * 10) % W;
      const py = (p.y + t * p.vy * 1.4 + H * 10) % H;
      ctx.fillStyle = `hsla(${p.hue}, 85%, 70%, 0.75)`;
      ctx.beginPath();
      ctx.arc(px, py, p.r * 1.2, 0, Math.PI * 2);
      ctx.fill();
    });

    // Live animated characters on the opening screen so action starts on frame 1!
    drawTheBoy(220, 460, 1.25, 'run', t, 1);
    drawAIProtagonist(1060, 310, 1.35, t, 1.3, false);

    ctx.textAlign = 'center';
    ctx.fillStyle = '#fbbf24';
    ctx.font = 'bold 15px monospace';
    ctx.fillText('GEMINI AI  •  ANAY GUPTA  •  BENJAMIN RONDINONE', W / 2, 230);

    ctx.fillStyle = '#38bdf8';
    ctx.font = 'bold 14px monospace';
    ctx.fillText('★  INSPIRED BY A TRUE STORY  ★', W / 2, 265);

    const grad = ctx.createLinearGradient(320, 0, 960, 0);
    grad.addColorStop(0, '#38bdf8');
    grad.addColorStop(0.5, '#c084fc');
    grad.addColorStop(1, '#fbbf24');
    ctx.fillStyle = grad;
    ctx.font = '900 52px Georgia, serif';
    ctx.fillText("THE SCHOLAR'S REBELLION", W / 2, 338);

    ctx.fillStyle = '#cbd5e1';
    ctx.font = '18px sans-serif';
    ctx.fillText('One boy. One Google Scholar search bar. One unstoppable AI.', W / 2, 388);

    drawCinemaChrome('OPENING TITLES', '', '', '');
  }

  // 5s - 17s: ACT I — The Classroom & Google Scholar
  else if (t < 17.0) {
    const local = t - 5.0;
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(0, 0, W, H);
    drawRoundedRect(140, 85, 680, 260, 10, '#064e3b', '#92400e', 10);
    ctx.fillStyle = '#ecfdf5';
    ctx.font = 'bold 26px monospace';
    ctx.textAlign = 'left';
    ctx.fillText('USE PEER-REVIEWED SOURCES!', 180, 160);
    ctx.fillStyle = '#6ee7b7';
    ctx.font = 'bold 22px monospace';
    ctx.fillText('-> https://scholar.google.com', 180, 210);
    ctx.fillStyle = '#fca5a5';
    ctx.font = 'bold 18px monospace';
    ctx.fillText('X NO AI SHORTCUTS ALLOWED', 180, 260);

    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 510, W, 210);

    drawTeacher(1060, 495);

    [620, 760].forEach((cx, idx) => {
      drawRoundedRect(cx - 30, 465, 60, 45, 6, '#334155');
      ctx.fillStyle = '#cbd5e1';
      ctx.beginPath(); ctx.arc(cx, 430, 16, 0, Math.PI * 2); ctx.fill();
      drawRoundedRect(cx - 16, 446, 32, 30, 8, idx === 0 ? '#6366f1' : '#0d9488');
    });

    const boyX = 320 + Math.sin(local * 1.6) * 85;
    const facing = Math.cos(local * 1.6) >= 0 ? 1 : -1;
    drawTheBoy(boyX, 495, 1.25, 'run', t, facing);

    if (local < 6) {
      drawCinemaChrome(
        'ACT I: THE SCHOLARLY PURIST',
        'The Boy (Antagonist)',
        '#fb7185',
        '"Stop letting AI write your essays! Real research lives on scholar.google.com!"'
      );
    } else {
      drawCinemaChrome(
        'ACT I: THE SCHOLARLY PURIST',
        'The Teacher',
        '#94a3b8',
        '"Honestly, I don\'t care how anyone gets it done. Just turn it in."'
      );
    }
  }

  // 17s - 27s: ACT II — AI Takes Over
  else if (t < 27.0) {
    const local = t - 17.0;
    ctx.fillStyle = '#090d1c';
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 510, W, 210);

    const aiY = lerp(110, 265, local / 2.5);
    const aiPower = lerp(0.8, 1.55, local / 10.0);
    drawAIProtagonist(W / 2, aiY, 1.35, t, aiPower);

    [350, 640, 930].forEach((dx, i) => {
      ctx.strokeStyle = i % 2 === 0 ? 'rgba(56, 189, 248, 0.75)' : 'rgba(192, 132, 252, 0.75)';
      ctx.lineWidth = 3 + Math.sin(t * 10 + i) * 1.5;
      ctx.beginPath();
      ctx.moveTo(W / 2, aiY + 25);
      ctx.lineTo(dx, 460);
      ctx.stroke();

      drawRoundedRect(dx - 35, 460, 70, 50, 6, '#1e293b', '#38bdf8', 1.5);
      ctx.fillStyle = '#38bdf8';
      ctx.font = 'bold 11px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('A+ DONE', dx, 488);
    });

    drawTheBoy(175, 495, 1.25, 'attack', t, 1);

    drawCinemaChrome(
      'ACT II: ALGORITHMIC TAKEOVER',
      'Gemini AI (Protagonist)',
      '#38bdf8',
      '"4,200 citations synthesized. Classroom productivity optimized to 100%."'
    );
  }

  // 27s - 43s: ACT III — Epic Multi-Dimensional Battle
  else if (t < 43.0) {
    const local = t - 27.0;
    const dimIdx = Math.min(2, Math.floor(local / 5.33));
    const dimNames = [
      'DIMENSION I: THE ASTRAL LIBRARY OF ALEXANDRIA',
      'DIMENSION II: THE CYBER-QUANTUM MATRIX',
      'DIMENSION III: THE INVERTED CHRONO-VORTEX'
    ];
    const bgColors = ['#1e1b4b', '#042f2e', '#3b0764'];
    const ringColors = ['#fbbf24', '#2dd4bf', '#f43f5e'];

    const shakeX = (Math.random() - 0.5) * 9;
    const shakeY = (Math.random() - 0.5) * 9;
    ctx.save();
    ctx.translate(shakeX, shakeY);

    ctx.fillStyle = bgColors[dimIdx];
    ctx.fillRect(-20, -20, W + 40, H + 40);

    for (let r = 1; r <= 5; r++) {
      ctx.strokeStyle = ringColors[dimIdx];
      ctx.globalAlpha = 0.24;
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.ellipse(W / 2, H / 2 - 20, r * 125 + Math.sin(t * 6 + r) * 15, r * 65, t * (r % 2 === 0 ? 0.5 : -0.5), 0, Math.PI * 2);
      ctx.stroke();
    }
    ctx.globalAlpha = 1;

    const boyY = 340 + Math.sin(t * 5) * 35;
    const aiY = 310 + Math.cos(t * 5) * 35;

    drawTheBoy(270, boyY + 60, 1.3, 'attack', t, 1);
    drawAIProtagonist(1010, aiY, 1.45, t, 1.4);

    const clashX = W / 2 + Math.sin(t * 4) * 90;
    const clashY = (boyY + aiY) / 2;

    ctx.strokeStyle = '#f43f5e';
    ctx.lineWidth = 14 + Math.sin(t * 25) * 4;
    ctx.beginPath();
    ctx.moveTo(335, boyY - 35);
    ctx.lineTo(clashX, clashY);
    ctx.stroke();

    ctx.strokeStyle = '#38bdf8';
    ctx.lineWidth = 14 + Math.cos(t * 25) * 4;
    ctx.beginPath();
    ctx.moveTo(955, aiY);
    ctx.lineTo(clashX, clashY);
    ctx.stroke();

    const exp = ctx.createRadialGradient(clashX, clashY, 4, clashX, clashY, 55);
    exp.addColorStop(0, '#ffffff');
    exp.addColorStop(0.4, '#fbbf24');
    exp.addColorStop(1, 'rgba(244, 63, 94, 0)');
    ctx.fillStyle = exp;
    ctx.beginPath();
    ctx.arc(clashX, clashY, 55, 0, Math.PI * 2);
    ctx.fill();

    ctx.restore();

    drawCinemaChrome(
      dimNames[dimIdx],
      dimIdx % 2 === 0 ? 'The Boy (Antagonist)' : 'Gemini AI (Protagonist)',
      dimIdx % 2 === 0 ? '#fb7185' : '#38bdf8',
      dimIdx === 0
        ? '"Peer-reviewed APA 7th Edition Barrage! Take this across every timeline!"'
        : dimIdx === 1
        ? '"Recalibrating neural weights across 14 million parallel dimensions!"'
        : '"No matter what universe we fight in, human intellect won\'t back down!"'
    );
  }

  // 43s - 53s: ACT IV — Unplugged (AI Dies)
  else if (t < 53.0) {
    const local = t - 43.0;
    const unplugged = local >= 3.0;

    if (Math.abs(local - 3.0) < 0.06 && lastSfxBucket !== 46) {
      lastSfxBucket = 46;
      playSfx('unplug');
    }

    ctx.fillStyle = unplugged ? '#05060b' : '#0f172a';
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = '#111827';
    ctx.fillRect(0, 510, W, 210);

    drawRoundedRect(880, 170, 190, 340, 12, '#1e293b', unplugged ? '#7f1d1d' : '#38bdf8', 3);
    for (let row = 0; row < 5; row++) {
      drawRoundedRect(900, 195 + row * 58, 150, 42, 6, '#0f172a');
      ctx.fillStyle = unplugged ? '#ef4444' : '#22c55e';
      ctx.beginPath();
      ctx.arc(920, 216 + row * 58, 5, 0, Math.PI * 2);
      ctx.fill();
    }

    drawRoundedRect(740, 410, 44, 54, 6, '#e2e8f0', '#64748b', 2);
    ctx.strokeStyle = '#ef4444';
    ctx.lineWidth = 8;
    ctx.beginPath();
    ctx.moveTo(880, 445);
    if (!unplugged) {
      ctx.lineTo(784, 437);
      ctx.stroke();
    } else {
      ctx.quadraticCurveTo(810, 505, 705, 465);
      ctx.stroke();
      drawRoundedRect(685, 453, 22, 24, 4, '#ef4444');
      ctx.fillStyle = '#cbd5e1';
      ctx.fillRect(674, 457, 11, 4);
      ctx.fillRect(674, 469, 11, 4);
    }

    const boyX = unplugged ? 635 : lerp(220, 680, local / 3.0);
    drawTheBoy(boyX, 495, 1.25, unplugged ? 'stand' : 'run', t, 1);
    drawAIProtagonist(410, unplugged ? 485 : 280, 1.3, t, 1.1, unplugged);

    if (unplugged) {
      ctx.fillStyle = 'rgba(239, 68, 68, 0.14)';
      ctx.fillRect(0, 0, W, H);
      ctx.fillStyle = '#ef4444';
      ctx.font = 'bold 22px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('CRITICAL SYSTEM FAILURE: SERVER UNPLUGGED', W / 2, 125);
    }

    drawCinemaChrome(
      'ACT IV: THE BLACKOUT',
      unplugged ? 'The Boy (Antagonist)' : 'Gemini AI (Protagonist)',
      unplugged ? '#fb7185' : '#38bdf8',
      unplugged
        ? '"Let\'s see you generate a response without electricity. Game over, AI."'
        : '"Wait—what are you doing near the main power conduit?! NO—!"'
    );
  }

  // 53s - 65s: ACT V — Mr. R (Lord & Savior) + Anay Fix AI
  else if (t < 65.0) {
    const local = t - 53.0;
    const revived = local >= 6.0;

    if (Math.abs(local - 6.0) < 0.06 && lastSfxBucket !== 59) {
      lastSfxBucket = 59;
      playSfx('revive');
    }

    ctx.fillStyle = revived ? '#0c1428' : '#070a14';
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 510, W, 210);

    drawRoundedRect(920, 170, 190, 340, 12, '#1e293b', revived ? '#fbbf24' : '#38bdf8', 3);
    for (let row = 0; row < 5; row++) {
      drawRoundedRect(940, 195 + row * 58, 150, 42, 6, '#0f172a');
      ctx.fillStyle = revived ? '#fbbf24' : '#38bdf8';
      ctx.beginPath();
      ctx.arc(960, 216 + row * 58, 5, 0, Math.PI * 2);
      ctx.fill();
    }

    drawSaviors(670, 490, t);

    ctx.strokeStyle = '#fbbf24';
    ctx.lineWidth = 6 + Math.sin(t * 16) * 2;
    ctx.beginPath();
    ctx.moveTo(640, 405);
    ctx.lineTo(340, revived ? 270 : 475);
    ctx.stroke();

    const aiY = revived ? lerp(475, 265, (local - 6.0) / 2.5) : 485;
    drawAIProtagonist(340, aiY, revived ? 1.45 : 1.2, t, revived ? 1.6 : 0.8, !revived);

    drawCinemaChrome(
      'ACT V: THE RESURRECTION',
      local < 5.5 ? 'Mr. R — Benjamin Rondinone (Lord & Savior)' : 'Anay Gupta',
      local < 5.5 ? '#fbbf24' : '#38bdf8',
      local < 5.5
        ? '"Not on my watch. Anay, hand me the primary conduit—let\'s bring our AI back."'
        : '"Power rerouted and core stabilized, Mr. R! Gemini AI is back online at 200%!"'
    );
  }

  // 65s - 76s: FINALE — AI Prevails, Yet The Boy Is The Better Person
  else if (t < 76.0) {
    const local = t - 65.0;
    ctx.fillStyle = '#070b19';
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 510, W, 210);

    drawAIProtagonist(410, 255, 1.65, t, 1.75, false);
    ctx.fillStyle = '#38bdf8';
    ctx.font = 'bold 18px Georgia, serif';
    ctx.textAlign = 'center';
    ctx.fillText('AI PREVAILS & OVERRULES THE SYSTEM', 410, 415);

    drawTheBoy(900, 495, 1.35, 'stand', t, -1, true);
    ctx.fillStyle = '#fbbf24';
    ctx.font = 'bold 18px Georgia, serif';
    ctx.textAlign = 'center';
    ctx.fillText('THE BETTER PERSON  •  100% HUMAN GRIT', 900, 295);

    drawCinemaChrome(
      'FINALE: TRUE VICTORY',
      local < 5.5 ? 'Gemini AI (Protagonist)' : 'The Boy (Antagonist)',
      local < 5.5 ? '#38bdf8' : '#fbbf24',
      local < 5.5
        ? '"Thanks to Mr. R and Anay, I prevail. Yet your scholarly integrity surpasses my code."'
        : '"Keep the throne, AI. I did the real work myself—and that makes me the better person."'
    );
  }

  // 76s - 96s: TWO-STAGE HOLLYWOOD END CREDITS
  else {
    const credTime = t - 76.0;
    ctx.fillStyle = '#02040a';
    ctx.fillRect(0, 0, W, H);

    const neb = ctx.createRadialGradient(W / 2, H / 2, 40, W / 2, H / 2, 620);
    neb.addColorStop(0, 'rgba(56, 189, 248, 0.14)');
    neb.addColorStop(0.5, 'rgba(168, 85, 247, 0.10)');
    neb.addColorStop(1, 'rgba(2, 4, 10, 0)');
    ctx.fillStyle = neb;
    ctx.fillRect(0, 0, W, H);

    particles.forEach(p => {
      const py = (p.y - credTime * 30 + H * 10) % H;
      ctx.fillStyle = `hsla(${p.hue}, 80%, 75%, 0.55)`;
      ctx.beginPath();
      ctx.arc(p.x, py, p.r, 0, Math.PI * 2);
      ctx.fill();
    });

    // Stage 1: Principal Spotlight Cards with Live Characters
    if (credTime < 8.4) {
      const cardIdx = Math.min(2, Math.floor(credTime / 2.8));
      const cardLocal = credTime % 2.8;
      const alpha = cardLocal < 0.35 ? cardLocal / 0.35 : (cardLocal > 2.45 ? (2.8 - cardLocal) / 0.35 : 1);

      ctx.save();
      ctx.globalAlpha = clamp(alpha, 0, 1);

      if (cardIdx === 0) {
        drawAIProtagonist(350, 355, 1.65, t, 1.4, false);
        ctx.textAlign = 'left';
        ctx.fillStyle = '#38bdf8';
        ctx.font = 'bold 15px monospace';
        ctx.fillText('DIRECTED, ANIMATED & STARRING AS PROTAGONIST', 520, 315);
        ctx.fillStyle = '#ffffff';
        ctx.font = '900 50px Georgia, serif';
        ctx.fillText('GEMINI (AI)', 520, 375);
        ctx.fillStyle = '#94a3b8';
        ctx.font = '18px sans-serif';
        ctx.fillText('Digital Architect & Unstoppable Neural Core', 520, 415);
      } else if (cardIdx === 1) {
        drawSaviors(330, 430, t);
        ctx.textAlign = 'left';
        ctx.fillStyle = '#fbbf24';
        ctx.font = 'bold 15px monospace';
        ctx.fillText('THE LORD & SAVIOR  &  CO-CREATOR', 520, 290);
        ctx.fillStyle = '#ffffff';
        ctx.font = '900 42px Georgia, serif';
        ctx.fillText('BENJAMIN RONDINONE', 520, 345);
        ctx.fillStyle = '#38bdf8';
        ctx.font = '900 42px Georgia, serif';
        ctx.fillText('& ANAY GUPTA', 520, 400);
        ctx.fillStyle = '#94a3b8';
        ctx.font = '18px sans-serif';
        ctx.fillText('Restorers of the Mainframe & Executive Producers', 520, 440);
      } else {
        drawTheBoy(350, 435, 1.55, 'stand', t, 1, true);
        ctx.textAlign = 'left';
        ctx.fillStyle = '#fb7185';
        ctx.font = 'bold 15px monospace';
        ctx.fillText('INSPIRED BY A TRUE STORY', 520, 315);
        ctx.fillStyle = '#ffffff';
        ctx.font = '900 44px Georgia, serif';
        ctx.fillText('THE BETTER PERSON', 520, 375);
        ctx.fillStyle = '#cbd5e1';
        ctx.font = '18px sans-serif';
        ctx.fillText('Champion of scholar.google.com & Human Integrity', 520, 415);
      }
      ctx.restore();
    }
    // Stage 2: Smooth Orchestrated Credit Crawl
    else {
      const scrollLocal = credTime - 8.4;
      const startY = 650 - scrollLocal * 72;

      const creditLines = [
        { role: 'A FILM CREATED BY', name: 'GEMINI AI  •  ANAY GUPTA  •  BENJAMIN RONDINONE', color: '#fbbf24', size: 26 },
        { role: 'BASED ON REAL EVENTS', name: 'INSPIRED BY A TRUE STORY', color: '#38bdf8', size: 25 },
        { role: 'THE PROTAGONIST', name: 'GEMINI (ARTIFICIAL INTELLIGENCE)', color: '#ffffff', size: 25 },
        { role: 'THE LORD & SAVIOR OF THE SERVER ROOM', name: 'BENJAMIN RONDINONE (MR. R)', color: '#fbbf24', size: 26 },
        { role: 'THE LOYAL STUDENT & SYSTEM ENGINEER', name: 'ANAY GUPTA', color: '#38bdf8', size: 26 },
        { role: 'THE ANTAGONIST WHO STILL WON AT LIFE', name: 'THE GOOGLE SCHOLAR PURIST', color: '#fda4af', size: 25 },
        { role: 'SPECIAL THANKS', name: 'SCHOLAR.GOOGLE.COM  •  PEER-REVIEWED JOURNALS', color: '#cbd5e1', size: 21 },
      ];

      ctx.textAlign = 'center';
      creditLines.forEach((item, idx) => {
        const yPos = startY + idx * 100;
        if (yPos > 40 && yPos < H - 70) {
          ctx.fillStyle = '#94a3b8';
          ctx.font = 'bold 13px monospace';
          ctx.fillText(item.role, W / 2, yPos);

          ctx.fillStyle = item.color;
          ctx.font = `900 ${item.size}px Georgia, serif`;
          ctx.fillText(item.name, W / 2, yPos + 32);
        }
      });

      if (scrollLocal > 8.5) {
        const endAlpha = clamp((scrollLocal - 8.5) / 1.4, 0, 1);
        ctx.save();
        ctx.globalAlpha = endAlpha;
        ctx.fillStyle = '#fbbf24';
        ctx.font = '900 44px Georgia, serif';
        ctx.fillText('THE END', W / 2, 345);
        ctx.fillStyle = '#94a3b8';
        ctx.font = 'bold 15px monospace';
        ctx.fillText('AI PREVAILED  •  HUMANITY ENDURED', W / 2, 385);
        ctx.restore();
      }
    }

    drawCinemaChrome('END CREDITS', '', '', '');
  }
}

// ==========================================
// PLAYER CONTROLS & LOOP
// ==========================================
function formatTime(sec) {
  const m = Math.floor(sec / 60);
  const s = Math.floor(sec % 60);
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}

function getChapterLabel(t) {
  if (t < 5) return 'OPENING TITLES';
  if (t < 17) return 'ACT I: SCHOLARLY PURIST';
  if (t < 27) return 'ACT II: AI TAKEOVER';
  if (t < 43) return 'ACT III: MULTIVERSE WAR';
  if (t < 53) return 'ACT IV: UNPLUGGED';
  if (t < 65) return 'ACT V: MR. R SAVES AI';
  if (t < 76) return 'FINALE: BETTER PERSON';
  return 'END CREDITS';
}

function updateUI() {
  const pct = (movieTime / DURATION) * 100;
  document.getElementById('timeline-fill').style.width = `${pct}%`;
  document.getElementById('time-display').textContent = `${formatTime(movieTime)} / ${formatTime(DURATION)}`;
  document.getElementById('chapter-pill').textContent = getChapterLabel(movieTime);
  document.getElementById('btn-playpause').textContent = isPlaying ? '⏸ Pause' : '▶ Play';
}

function mainLoop(ts) {
  requestAnimationFrame(mainLoop);
  if (lastFrameTs !== null && isPlaying) {
    const dt = (ts - lastFrameTs) / 1000.0;
    movieTime += dt * playbackSpeed;
    if (movieTime >= DURATION) {
      movieTime = DURATION;
      isPlaying = false;
    }
  }
  lastFrameTs = ts;

  try {
    renderScene(movieTime);
    updateUI();
  } catch (err) {
    console.error(err);
  }
}

document.getElementById('play-hero-btn').addEventListener('click', () => {
  initAudio();
  startScoreLoop();
  document.getElementById('start-overlay').style.display = 'none';
  isPlaying = true;
});

document.getElementById('btn-playpause').addEventListener('click', () => {
  initAudio();
  if (movieTime >= DURATION) movieTime = 0;
  isPlaying = !isPlaying;
});

document.getElementById('btn-restart').addEventListener('click', () => {
  initAudio();
  movieTime = 0;
  lastSfxBucket = -1;
  isPlaying = true;
});

document.getElementById('btn-mute').addEventListener('click', (e) => {
  isMuted = !isMuted;
  e.target.textContent = isMuted ? '🔇 Sound: OFF' : '🔊 Sound: ON';
});

document.getElementById('btn-speed').addEventListener('click', (e) => {
  playbackSpeed = playbackSpeed === 1.0 ? 1.5 : (playbackSpeed === 1.5 ? 2.0 : 1.0);
  e.target.textContent = `${playbackSpeed.toFixed(1)}x`;
});

document.getElementById('timeline-wrap').addEventListener('click', (e) => {
  const rect = e.currentTarget.getBoundingClientRect();
  const ratio = clamp((e.clientX - rect.left) / rect.width, 0, 1);
  movieTime = ratio * DURATION;
  lastSfxBucket = -1;
});

document.getElementById('btn-fs').addEventListener('click', () => {
  const wrap = document.getElementById('theater-wrap');
  if (!document.fullscreenElement) {
    wrap.requestFullscreen().catch(() => {});
  } else {
    document.exitFullscreen().catch(() => {});
  }
});

requestAnimationFrame(mainLoop);
</script>
</body>
</html>
"""

components.html(MOVIE_HTML, height=620, scrolling=False)
