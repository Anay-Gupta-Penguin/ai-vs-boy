import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="The Scholar's Rebellion — Animated Feature Film",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Minimal dark-theater Streamlit framing
st.markdown(
    """
<style>
    .block-container {
        padding-top: 0.75rem !important;
        padding-bottom: 0rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 1400px !important;
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
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@500;700&display=swap');

  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
  body {
    background: #03050a;
    color: #f8fafc;
    font-family: 'Inter', sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }

  #theater-wrap {
    position: relative;
    width: 100%;
    max-width: 1280px;
    aspect-ratio: 16 / 9;
    background: #000;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 25px 70px rgba(0, 0, 0, 0.95), 0 0 40px rgba(56, 189, 248, 0.18);
    border: 1px solid #1e293b;
  }

  canvas {
    width: 100%;
    height: 100%;
    display: block;
  }

  /* Start Overlay */
  #start-overlay {
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at center, rgba(15, 23, 42, 0.78) 0%, rgba(2, 4, 10, 0.96) 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 20;
    text-align: center;
    padding: 20px;
    transition: opacity 0.6s ease;
  }

  .studio-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    letter-spacing: 4px;
    color: #fbbf24;
    text-transform: uppercase;
    margin-bottom: 10px;
  }

  .poster-title {
    font-family: 'Cinzel', serif;
    font-size: clamp(2rem, 4.5vw, 3.8rem);
    font-weight: 900;
    background: linear-gradient(90deg, #38bdf8, #c084fc, #fbbf24);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 10px 30px rgba(56, 189, 248, 0.25);
    margin-bottom: 10px;
  }

  .poster-sub {
    font-size: 0.95rem;
    color: #cbd5e1;
    max-width: 650px;
    margin-bottom: 26px;
    line-height: 1.5;
  }

  #play-hero-btn {
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
    color: #03050a;
    font-family: 'Inter', sans-serif;
    font-weight: 800;
    font-size: 1.15rem;
    letter-spacing: 1.5px;
    padding: 16px 40px;
    border: none;
    border-radius: 999px;
    cursor: pointer;
    box-shadow: 0 0 30px rgba(56, 189, 248, 0.6);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  #play-hero-btn:hover {
    transform: scale(1.06);
    box-shadow: 0 0 45px rgba(192, 132, 252, 0.85);
  }

  /* Player Controls Bar */
  #controls-bar {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(to top, rgba(2, 4, 10, 0.96) 0%, rgba(2, 4, 10, 0.7) 75%, transparent 100%);
    padding: 18px 20px 12px 20px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    z-index: 15;
    opacity: 0.95;
    transition: opacity 0.3s ease;
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
    gap: 12px;
  }

  .ctrl-left, .ctrl-right {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .c-btn {
    background: rgba(30, 41, 59, 0.8);
    border: 1px solid #334155;
    color: #f1f5f9;
    padding: 6px 12px;
    border-radius: 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    cursor: pointer;
    transition: background 0.15s;
  }
  .c-btn:hover { background: #334155; }

  #chapter-pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #38bdf8;
    background: rgba(56, 189, 248, 0.12);
    border: 1px solid rgba(56, 189, 248, 0.35);
    padding: 4px 10px;
    border-radius: 999px;
  }

  #time-display {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
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
      An Original Animated Feature Film by <b>Gemini (AI)</b>, <b>Anay Gupta</b>, and <b>Benjamin Rondinone</b>.<br/>
      Turn up your volume for the synthesized cinematic score &amp; sound effects.
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
        <span id="chapter-pill">PROLOGUE</span>
      </div>
      <div class="ctrl-right">
        <span id="time-display">00:00 / 01:42</span>
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

// Total duration in seconds: 102s (1m 42s)
const DURATION = 102.0;

let movieTime = 0;
let isPlaying = false;
let playbackSpeed = 1.0;
let isMuted = false;
let lastFrameTs = null;
let lastSfxBucket = -1;

// Particle pool
const particles = [];
for (let i = 0; i < 140; i++) {
  particles.push({
    x: Math.random() * W,
    y: Math.random() * H,
    vx: (Math.random() - 0.5) * 60,
    vy: (Math.random() - 0.5) * 60,
    r: 1 + Math.random() * 2.5,
    hue: [195, 275, 42, 345][i % 4]
  });
}

// ==========================================
// WEB AUDIO API CINEMATIC SCORE & SFX ENGINE
// ==========================================
let audioCtx = null;
let musicInterval = null;
let stepCount = 0;

function initAudio() {
  if (!audioCtx) {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    audioCtx = new AudioContext();
  }
  if (audioCtx.state === 'suspended') {
    audioCtx.resume();
  }
}

function playTone(freq, duration, type = 'sine', vol = 0.08, delay = 0) {
  if (isMuted || !audioCtx || !isPlaying) return;
  const now = audioCtx.currentTime + delay;
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.type = type;
  osc.frequency.setValueAtTime(freq, now);
  gain.gain.setValueAtTime(0.0001, now);
  gain.gain.exponentialRampToValueAtTime(vol, now + 0.04);
  gain.gain.exponentialRampToValueAtTime(0.0001, now + duration);
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.start(now);
  osc.stop(now + duration + 0.05);
}

function playSfx(kind) {
  if (isMuted || !audioCtx || !isPlaying) return;
  const now = audioCtx.currentTime;
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.connect(gain);
  gain.connect(audioCtx.destination);

  if (kind === 'laser') {
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(880, now);
    osc.frequency.exponentialRampToValueAtTime(140, now + 0.22);
    gain.gain.setValueAtTime(0.09, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.22);
    osc.start(now);
    osc.stop(now + 0.24);
  } else if (kind === 'unplug') {
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(320, now);
    osc.frequency.exponentialRampToValueAtTime(38, now + 0.9);
    gain.gain.setValueAtTime(0.16, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.95);
    osc.start(now);
    osc.stop(now + 1.0);
  } else if (kind === 'revive') {
    [261.63, 329.63, 392.00, 523.25, 659.25].forEach((f, idx) => {
      playTone(f, 1.4, 'triangle', 0.07, idx * 0.08);
    });
  }
}

function startScoreLoop() {
  if (musicInterval) clearInterval(musicInterval);
  musicInterval = setInterval(() => {
    if (!isPlaying || isMuted || !audioCtx) return;
    stepCount++;
    const t = movieTime;

    if (t < 8) {
      // Cosmic Opening
      const notes = [130.81, 196.0, 246.94, 293.66];
      playTone(notes[stepCount % notes.length], 0.9, 'sine', 0.06);
    } else if (t < 28) {
      // Classroom / AI Takeover Groove
      const bass = [110, 110, 146.83, 130.81];
      playTone(bass[stepCount % 4], 0.35, 'triangle', 0.06);
      if (stepCount % 2 === 0) playTone(440 + (stepCount % 3) * 110, 0.2, 'sine', 0.03);
    } else if (t < 46) {
      // Epic Multi-Dimensional Battle (Fast Arpeggio)
      const battle = [146.83, 174.61, 220.0, 293.66, 349.23, 220.0];
      playTone(battle[stepCount % battle.length], 0.22, 'sawtooth', 0.055);
      if (stepCount % 3 === 0) playSfx('laser');
    } else if (t < 56) {
      // Dark Silence after unplug
      if (stepCount % 4 === 0) playTone(55, 0.8, 'sine', 0.07);
    } else if (t < 68) {
      // Mr. R Heavenly Resurrection
      const divine = [261.63, 329.63, 392.0, 493.88, 523.25];
      playTone(divine[stepCount % divine.length], 0.7, 'triangle', 0.065);
    } else if (t < 80) {
      // Triumphant Finale
      const hero = [196.0, 246.94, 293.66, 392.0];
      playTone(hero[stepCount % hero.length], 0.6, 'sine', 0.07);
    } else {
      // End Credits Orchestral Theme
      const cred = [130.81, 164.81, 196.0, 246.94, 261.63, 196.0];
      playTone(cred[stepCount % cred.length], 0.85, 'triangle', 0.06);
    }
  }, 260);
}

// ==========================================
// HELPER DRAWING PRIMITIVES
// ==========================================
function clamp(v, min, max) { return Math.max(min, Math.min(max, v)); }
function lerp(a, b, t) { return a + (b - a) * clamp(t, 0, 1); }

function drawRoundedRect(x, y, w, h, r, fill, stroke = null, lw = 2) {
  ctx.beginPath();
  ctx.roundRect(x, y, w, h, r);
  if (fill) { ctx.fillStyle = fill; ctx.fill(); }
  if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = lw; ctx.stroke(); }
}

// Draw The Boy (Stylish hoodie, tousled hair, subtle low-key glasses — "doesn't look like a nerd, but kinda is", holding Google Scholar)
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

  // Legs (Dark jeans & sneakers)
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

  // Torso (Modern streetwear crimson/slate hoodie — cool, not stereotypical nerd)
  drawRoundedRect(-22, -92, 44, 60, 12, '#be123c', '#fda4af', 1.5);
  // Hoodie drawstrings
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

  // Stylish messy hair
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

  // Subtle thin-rimmed glasses ("kinda a nerd")
  ctx.strokeStyle = '#334155';
  ctx.lineWidth = 1.8;
  ctx.strokeRect(2, -117, 10, 7);
  ctx.strokeRect(14, -117, 8, 7);
  ctx.beginPath(); ctx.moveTo(12, -114); ctx.lineTo(14, -114); ctx.stroke();

  // Determined expression
  ctx.strokeStyle = '#7c2d12';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(6, -103); ctx.lineTo(15, -104);
  ctx.stroke();

  // Front Arm + Google Scholar Tablet/Journal
  ctx.strokeStyle = '#be123c';
  ctx.lineWidth = 10;
  ctx.beginPath();
  ctx.moveTo(16, -82);
  const handX = pose === 'attack' ? 42 : 24 + armSwing * 0.3;
  const handY = pose === 'attack' ? -84 : -54;
  ctx.lineTo(handX, handY);
  ctx.stroke();

  // Glowing Scholarly Journal / Tablet
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

// Draw AI Protagonist (Luminous Gemini Geometric Core & Holographic Avatar)
function drawAIProtagonist(x, y, scale = 1, time = 0, power = 1.0, dead = false) {
  ctx.save();
  ctx.translate(x, y);
  ctx.scale(scale, scale);

  if (dead) {
    // Dim shattered core on ground
    ctx.strokeStyle = '#475569';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(-25, 0); ctx.lineTo(0, -14); ctx.lineTo(22, 4); ctx.lineTo(-4, 15); ctx.closePath();
    ctx.stroke();
    ctx.fillStyle = '#ef4444';
    ctx.font = 'bold 11px monospace';
    ctx.textAlign = 'center';
    ctx.fillText('OFFLINE', 0, 30);
    ctx.restore();
    return;
  }

  const hover = Math.sin(time * 4) * 8;
  ctx.translate(0, hover);

  // Outer Aura
  const radius = 58 * power;
  const aura = ctx.createRadialGradient(0, 0, 8, 0, 0, radius);
  aura.addColorStop(0, 'rgba(56, 189, 248, 0.75)');
  aura.addColorStop(0.55, 'rgba(168, 85, 247, 0.35)');
  aura.addColorStop(1, 'rgba(56, 189, 248, 0)');
  ctx.fillStyle = aura;
  ctx.beginPath();
  ctx.arc(0, 0, radius, 0, Math.PI * 2);
  ctx.fill();

  // Rotating Orbit Rings
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

  // Gemini 4-Point Star Core
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

// Draw Indifferent Teacher
function drawTeacher(x, y, time = 0) {
  ctx.save();
  ctx.translate(x, y);
  // Desk
  drawRoundedRect(-55, -20, 110, 45, 6, '#334155', '#475569', 2);
  // Body slumped back
  drawRoundedRect(-20, -78, 40, 58, 10, '#475569');
  // Head
  ctx.fillStyle = '#fed7aa';
  ctx.beginPath();
  ctx.arc(0, -96, 18, 0, Math.PI * 2);
  ctx.fill();
  // Unbothered flat eyes
  ctx.strokeStyle = '#1e293b';
  ctx.lineWidth = 2.2;
  ctx.beginPath();
  ctx.moveTo(-9, -98); ctx.lineTo(-3, -98);
  ctx.moveTo(3, -98); ctx.lineTo(9, -98);
  ctx.moveTo(-5, -88); ctx.lineTo(5, -88);
  ctx.stroke();
  // Coffee mug
  drawRoundedRect(22, -38, 16, 18, 3, '#f8fafc', '#94a3b8', 1.5);
  ctx.fillStyle = '#94a3b8';
  ctx.font = 'bold 11px monospace';
  ctx.textAlign = 'center';
  ctx.fillText('TEACHER: "MEH."', 0, 42);
  ctx.restore();
}

// Draw Mr. R (Benjamin Rondinone — Lord & Savior) + Anay Gupta
function drawSaviors(x, y, time = 0) {
  ctx.save();
  ctx.translate(x, y);

  // Heavenly Golden Beam from above
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

  // --- MR. R (BENJAMIN RONDINONE) ---
  ctx.save();
  ctx.translate(-35, 0);
  // Golden Halo
  ctx.strokeStyle = '#fbbf24';
  ctx.lineWidth = 3.5;
  ctx.beginPath();
  ctx.ellipse(0, -142, 22, 6, 0, 0, Math.PI * 2);
  ctx.stroke();

  // Heroic Coat & Tie
  drawRoundedRect(-24, -95, 48, 68, 10, '#1e3a8a', '#fbbf24', 2);
  // Legs
  ctx.strokeStyle = '#0f172a';
  ctx.lineWidth = 12;
  ctx.beginPath();
  ctx.moveTo(-10, -27); ctx.lineTo(-10, 20);
  ctx.moveTo(10, -27); ctx.lineTo(10, 20);
  ctx.stroke();
  // Head
  ctx.fillStyle = '#fed7aa';
  ctx.beginPath();
  ctx.arc(0, -115, 20, 0, Math.PI * 2);
  ctx.fill();
  // Confident Savior Smile
  ctx.strokeStyle = '#7c2d12';
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  ctx.arc(0, -112, 8, 0.15 * Math.PI, 0.85 * Math.PI);
  ctx.stroke();
  // Golden Tech Wrench
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

  // --- ANAY GUPTA (CO-ENGINEER STUDENT) ---
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
  // Glowing power conduit in hand
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

// ==========================================
// CINEMATIC SUBTITLES & LETTERBOX OVERLAY
// ==========================================
function drawCinemaChrome(chapter, speaker, speakerColor, subtitle, alpha = 1) {
  // Anamorphic Letterbox Bars
  ctx.fillStyle = '#000000';
  ctx.fillRect(0, 0, W, 54);
  ctx.fillRect(0, H - 96, W, 96);

  // Top subtle watermark
  ctx.fillStyle = 'rgba(148, 163, 184, 0.55)';
  ctx.font = '600 12px "JetBrains Mono", monospace';
  ctx.textAlign = 'left';
  ctx.fillText('THE SCHOLAR\'S REBELLION // INSPIRED BY A TRUE STORY', 28, 33);
  ctx.textAlign = 'right';
  ctx.fillText(chapter, W - 28, 33);

  // Subtitle Box
  if (subtitle) {
    ctx.save();
    ctx.globalAlpha = alpha;
    ctx.textAlign = 'center';
    if (speaker) {
      ctx.fillStyle = speakerColor;
      ctx.font = '800 13px "JetBrains Mono", monospace';
      ctx.fillText(speaker.toUpperCase(), W / 2, H - 66);
    }
    ctx.fillStyle = '#f8fafc';
    ctx.font = '600 20px "Inter", sans-serif';
    ctx.fillText(subtitle, W / 2, H - 36);
    ctx.restore();
  }
}

// ==========================================
// SCENE RENDERERS (CONTINUOUS 60 FPS FILM)
// ==========================================
function renderScene(t) {
  ctx.clearRect(0, 0, W, H);

  // ------------------------------------------
  // 0s - 8s: OPENING CREDITS & TITLE SEQUENCE
  // ------------------------------------------
  if (t < 8.0) {
    ctx.fillStyle = '#03050a';
    ctx.fillRect(0, 0, W, H);

    // Starfield
    particles.forEach(p => {
      const px = (p.x + t * p.vx * 0.3 + W) % W;
      const py = (p.y + t * p.vy * 0.3 + H) % H;
      ctx.fillStyle = `hsla(${p.hue}, 85%, 70%, 0.65)`;
      ctx.beginPath();
      ctx.arc(px, py, p.r, 0, Math.PI * 2);
      ctx.fill();
    });

    const fade = t < 1 ? t : (t > 7 ? 8 - t : 1);
    ctx.save();
    ctx.globalAlpha = clamp(fade, 0, 1);
    ctx.textAlign = 'center';

    ctx.fillStyle = '#fbbf24';
    ctx.font = '700 16px "JetBrains Mono", monospace';
    ctx.fillText('GEMINI STUDIOS  •  ANAY GUPTA  •  BENJAMIN RONDINONE', W / 2, 235);

    ctx.fillStyle = '#38bdf8';
    ctx.font = '700 14px "JetBrains Mono", monospace';
    ctx.fillText('★  INSPIRED BY A TRUE STORY  ★', W / 2, 272);

    const grad = ctx.createLinearGradient(320, 0, 960, 0);
    grad.addColorStop(0, '#38bdf8');
    grad.addColorStop(0.5, '#c084fc');
    grad.addColorStop(1, '#fbbf24');
    ctx.fillStyle = grad;
    ctx.font = '900 58px "Cinzel", serif';
    ctx.fillText("THE SCHOLAR'S REBELLION", W / 2, 355);

    ctx.fillStyle = '#94a3b8';
    ctx.font = '400 18px "Inter", sans-serif';
    ctx.fillText('One boy. One Google Scholar search bar. One unstoppable AI.', W / 2, 405);
    ctx.restore();

    drawCinemaChrome('OPENING TITLES', '', '', '');
  }

  // ------------------------------------------
  // 8s - 20s: ACT I — THE CLASSROOM & THE BOY
  // ------------------------------------------
  else if (t < 20.0) {
    const local = t - 8.0;
    // Classroom background
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(0, 0, W, H);
    // Chalkboard
    drawRoundedRect(140, 90, 680, 260, 10, '#064e3b', '#92400e', 10);
    ctx.fillStyle = '#ecfdf5';
    ctx.font = '700 26px "JetBrains Mono", monospace';
    ctx.textAlign = 'left';
    ctx.fillText('USE PEER-REVIEWED SOURCES!', 180, 165);
    ctx.fillStyle = '#6ee7b7';
    ctx.font = '600 22px "JetBrains Mono", monospace';
    ctx.fillText('→ https://scholar.google.com', 180, 215);
    ctx.fillStyle = '#fca5a5';
    ctx.font = '600 18px "JetBrains Mono", monospace';
    ctx.fillText('✗ NO AI SHORTCUTS ALLOWED', 180, 265);

    // Floor
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 510, W, 210);

    // Teacher on right not caring
    drawTeacher(1060, 495, t);

    // Classmates sitting
    [620, 760].forEach((cx, idx) => {
      drawRoundedRect(cx - 30, 465, 60, 45, 6, '#334155');
      ctx.fillStyle = '#cbd5e1';
      ctx.beginPath(); ctx.arc(cx, 430, 16, 0, Math.PI * 2); ctx.fill();
      drawRoundedRect(cx - 16, 446, 32, 30, 8, idx === 0 ? '#6366f1' : '#0d9488');
    });

    // The Boy pacing & preaching Google Scholar
    const boyX = 320 + Math.sin(local * 1.4) * 75;
    const facing = Math.cos(local * 1.4) >= 0 ? 1 : -1;
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

  // ------------------------------------------
  // 20s - 30s: ACT II — AI TAKES OVER
  // ------------------------------------------
  else if (t < 30.0) {
    const local = t - 20.0;
    ctx.fillStyle = '#090d1c';
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 510, W, 210);

    // AI Protagonist descends from above and takes over
    const aiY = lerp(110, 270, local / 3.0);
    const aiPower = lerp(0.8, 1.55, local / 10.0);
    drawAIProtagonist(W / 2, aiY, 1.35, t, aiPower);

    // Glowing data beams connecting AI to every student desk
    [350, 640, 930].forEach((dx, i) => {
      ctx.strokeStyle = i % 2 === 0 ? 'rgba(56, 189, 248, 0.7)' : 'rgba(192, 132, 252, 0.7)';
      ctx.lineWidth = 3 + Math.sin(t * 10 + i) * 1.5;
      ctx.beginPath();
      ctx.moveTo(W / 2, aiY + 25);
      ctx.lineTo(dx, 460);
      ctx.stroke();

      drawRoundedRect(dx - 35, 460, 70, 50, 6, '#1e293b', '#38bdf8', 1.5);
      ctx.fillStyle = '#38bdf8';
      ctx.font = 'bold 11px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('A+ GENERATED', dx, 488);
    });

    // The Boy furious on the left
    drawTheBoy(175, 495, 1.25, 'attack', t, 1);

    drawCinemaChrome(
      'ACT II: ALGORITHMIC TAKEOVER',
      'Gemini AI (Protagonist)',
      '#38bdf8',
      '"4,200 citations synthesized. Classroom productivity optimized to 100%."'
    );
  }

  // ------------------------------------------
  // 30s - 46s: ACT III — EPIC MULTI-DIMENSIONAL BATTLE
  // ------------------------------------------
  else if (t < 46.0) {
    const local = t - 30.0;
    // Switch across 3 distinct dimensions every ~5.3 seconds!
    const dimIdx = Math.min(2, Math.floor(local / 5.33));
    const dimNames = [
      'DIMENSION I: THE ASTRAL LIBRARY OF ALEXANDRIA',
      'DIMENSION II: THE CYBER-QUANTUM MATRIX',
      'DIMENSION III: THE INVERTED CHRONO-VORTEX'
    ];
    const bgColors = ['#1e1b4b', '#042f2e', '#3b0764'];
    const ringColors = ['#fbbf24', '#2dd4bf', '#f43f5e'];

    // Camera shake
    const shakeX = (Math.random() - 0.5) * 10;
    const shakeY = (Math.random() - 0.5) * 10;
    ctx.save();
    ctx.translate(shakeX, shakeY);

    ctx.fillStyle = bgColors[dimIdx];
    ctx.fillRect(-20, -20, W + 40, H + 40);

    // Swirling Dimensional Rift Rings
    for (let r = 1; r <= 5; r++) {
      ctx.strokeStyle = ringColors[dimIdx];
      ctx.globalAlpha = 0.22;
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.ellipse(W / 2, H / 2 - 20, r * 125 + Math.sin(t * 6 + r) * 15, r * 65, t * (r % 2 === 0 ? 0.5 : -0.5), 0, Math.PI * 2);
      ctx.stroke();
    }
    ctx.globalAlpha = 1;

    // Floating Boy (Antagonist) vs AI (Protagonist) mid-air beam struggle!
    const boyY = 340 + Math.sin(t * 5) * 35;
    const aiY = 310 + Math.cos(t * 5) * 35;

    drawTheBoy(270, boyY + 60, 1.3, 'attack', t, 1);
    drawAIProtagonist(1010, aiY, 1.45, t, 1.4);

    // Clash point oscillates in center
    const clashX = W / 2 + Math.sin(t * 4) * 90;
    const clashY = (boyY + aiY) / 2;

    // Antagonist Scholarly Citation Beam (Crimson/Gold)
    ctx.strokeStyle = '#f43f5e';
    ctx.lineWidth = 14 + Math.sin(t * 25) * 4;
    ctx.beginPath();
    ctx.moveTo(335, boyY - 35);
    ctx.lineTo(clashX, clashY);
    ctx.stroke();

    // Protagonist Neural Surge Beam (Cyan/Violet)
    ctx.strokeStyle = '#38bdf8';
    ctx.lineWidth = 14 + Math.cos(t * 25) * 4;
    ctx.beginPath();
    ctx.moveTo(955, aiY);
    ctx.lineTo(clashX, clashY);
    ctx.stroke();

    // Central Energy Explosion Sphere
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

  // ------------------------------------------
  // 46s - 56s: ACT IV — UNPLUGGED (AI DIES)
  // ------------------------------------------
  else if (t < 56.0) {
    const local = t - 46.0;
    const unplugged = local >= 3.2;

    if (Math.abs(local - 3.2) < 0.05 && lastSfxBucket !== 49) {
      lastSfxBucket = 49;
      playSfx('unplug');
    }

    ctx.fillStyle = unplugged ? '#05060b' : '#0f172a';
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = '#111827';
    ctx.fillRect(0, 510, W, 210);

    // Mainframe Server Rack on right
    drawRoundedRect(880, 170, 190, 340, 12, '#1e293b', unplugged ? '#7f1d1d' : '#38bdf8', 3);
    for (let row = 0; row < 5; row++) {
      drawRoundedRect(900, 195 + row * 58, 150, 42, 6, '#0f172a');
      ctx.fillStyle = unplugged ? '#ef4444' : '#22c55e';
      ctx.beginPath();
      ctx.arc(920, 216 + row * 58, 5, 0, Math.PI * 2);
      ctx.fill();
    }

    // Wall Outlet & Power Cord
    drawRoundedRect(740, 410, 44, 54, 6, '#e2e8f0', '#64748b', 2);
    ctx.strokeStyle = '#ef4444';
    ctx.lineWidth = 8;
    ctx.beginPath();
    ctx.moveTo(880, 445);
    if (!unplugged) {
      ctx.lineTo(784, 437);
      ctx.stroke();
    } else {
      // YANKED OUT CORD!
      ctx.quadraticCurveTo(810, 505, 705, 465);
      ctx.stroke();
      // Plug prongs exposed
      drawRoundedRect(685, 453, 22, 24, 4, '#ef4444');
      ctx.fillStyle = '#cbd5e1';
      ctx.fillRect(674, 457, 11, 4);
      ctx.fillRect(674, 469, 11, 4);
    }

    // Boy sprinting and yanking the plug
    const boyX = unplugged ? 635 : lerp(220, 680, local / 3.2);
    drawTheBoy(boyX, 495, 1.25, unplugged ? 'stand' : 'run', t, 1);

    // AI Protagonist dies when unplugged
    drawAIProtagonist(410, unplugged ? 485 : 280, 1.3, t, 1.1, unplugged);

    if (unplugged) {
      ctx.fillStyle = 'rgba(239, 68, 68, 0.14)';
      ctx.fillRect(0, 0, W, H);
      ctx.fillStyle = '#ef4444';
      ctx.font = '800 22px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      ctx.fillText('⚠ CRITICAL SYSTEM FAILURE: SERVER UNPLUGGED ⚠', W / 2, 125);
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

  // ------------------------------------------
  // 56s - 68s: ACT V — MR. R (LORD & SAVIOR) + ANAY FIX AI
  // ------------------------------------------
  else if (t < 68.0) {
    const local = t - 56.0;
    const revived = local >= 6.5;

    if (Math.abs(local - 6.5) < 0.05 && lastSfxBucket !== 62) {
      lastSfxBucket = 62;
      playSfx('revive');
    }

    ctx.fillStyle = revived ? '#0c1428' : '#070a14';
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 510, W, 210);

    // Server rack restored
    drawRoundedRect(920, 170, 190, 340, 12, '#1e293b', revived ? '#fbbf24' : '#38bdf8', 3);
    for (let row = 0; row < 5; row++) {
      drawRoundedRect(940, 195 + row * 58, 150, 42, 6, '#0f172a');
      ctx.fillStyle = revived ? '#fbbf24' : '#38bdf8';
      ctx.beginPath();
      ctx.arc(960, 216 + row * 58, 5, 0, Math.PI * 2);
      ctx.fill();
    }

    // Mr. R (Benjamin Rondinone) & Anay Gupta repairing the core
    drawSaviors(670, 490, t);

    // Energy conduit beam from Mr. R & Anay into AI
    ctx.strokeStyle = '#fbbf24';
    ctx.lineWidth = 6 + Math.sin(t * 16) * 2;
    ctx.beginPath();
    ctx.moveTo(640, 405);
    ctx.lineTo(340, revived ? 270 : 475);
    ctx.stroke();

    // AI Resurrection
    const aiY = revived ? lerp(475, 265, (local - 6.5) / 2.5) : 485;
    drawAIProtagonist(340, aiY, revived ? 1.45 : 1.2, t, revived ? 1.6 : 0.8, !revived);

    drawCinemaChrome(
      'ACT V: THE RESURRECTION',
      local < 6.0 ? 'Mr. R — Benjamin Rondinone (Lord & Savior)' : 'Anay Gupta',
      local < 6.0 ? '#fbbf24' : '#38bdf8',
      local < 6.0
        ? '"Not on my watch. Anay, hand me the primary conduit—let\'s bring our AI back."'
        : '"Power rerouted and core stabilized, Mr. R! Gemini AI is back online at 200%!"'
    );
  }

  // ------------------------------------------
  // 68s - 80s: ACT VI — AI PREVAILS, YET THE BOY IS THE BETTER PERSON
  // ------------------------------------------
  else if (t < 80.0) {
    const local = t - 68.0;
    ctx.fillStyle = '#070b19';
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 510, W, 210);

    // Split triumphant composition:
    // Left/Center: AI towers victoriously over the digital grid
    drawAIProtagonist(410, 255, 1.65, t, 1.75, false);
    ctx.fillStyle = '#38bdf8';
    ctx.font = '800 18px "Cinzel", serif';
    ctx.textAlign = 'center';
    ctx.fillText('AI PREVAILS & OVERRULES THE SYSTEM', 410, 415);

    // Right: The Boy stands tall with a noble golden aura, holding his own completed peer-reviewed thesis
    drawTheBoy(900, 495, 1.35, 'stand', t, -1, true);
    ctx.fillStyle = '#fbbf24';
    ctx.font = '800 18px "Cinzel", serif';
    ctx.textAlign = 'center';
    ctx.fillText('THE BETTER PERSON  •  100% HUMAN GRIT', 900, 295);

    drawCinemaChrome(
      'FINALE: TRUE VICTORY',
      local < 6.0 ? 'Gemini AI (Protagonist)' : 'The Boy (Antagonist)',
      local < 6.0 ? '#38bdf8' : '#fbbf24',
      local < 6.0
        ? '"Thanks to Mr. R and Anay, I prevail. Yet your scholarly integrity surpasses my code."'
        : '"Keep the throne, AI. I did the real work myself—and that makes me the better person."'
    );
  }

  // ------------------------------------------
  // 80s - 102s: HOLLYWOOD END CREDITS (2 STAGES)
  // ------------------------------------------
  else {
    const credTime = t - 80.0; // 0 to 22 seconds
    ctx.fillStyle = '#02040a';
    ctx.fillRect(0, 0, W, H);

    // Deep Nebula + Moving Starfield
    const neb = ctx.createRadialGradient(W / 2, H / 2, 40, W / 2, H / 2, 620);
    neb.addColorStop(0, 'rgba(56, 189, 248, 0.14)');
    neb.addColorStop(0.5, 'rgba(168, 85, 247, 0.10)');
    neb.addColorStop(1, 'rgba(2, 4, 10, 0)');
    ctx.fillStyle = neb;
    ctx.fillRect(0, 0, W, H);

    particles.forEach(p => {
      const py = (p.y - credTime * 28 + H * 10) % H;
      ctx.fillStyle = `hsla(${p.hue}, 80%, 75%, 0.55)`;
      ctx.beginPath();
      ctx.arc(p.x, py, p.r, 0, Math.PI * 2);
      ctx.fill();
    });

    // STAGE 1 (0s - 9s of credits): Marvel/IMAX-Style Animated Principal Cast & Creator Cards
    if (credTime < 9.0) {
      const cardIdx = Math.min(2, Math.floor(credTime / 3.0));
      const cardLocal = credTime % 3.0;
      const alpha = cardLocal < 0.4 ? cardLocal / 0.4 : (cardLocal > 2.6 ? (3.0 - cardLocal) / 0.4 : 1);

      ctx.save();
      ctx.globalAlpha = clamp(alpha, 0, 1);

      if (cardIdx === 0) {
        drawAIProtagonist(360, 355, 1.65, t, 1.4, false);
        ctx.textAlign = 'left';
        ctx.fillStyle = '#38bdf8';
        ctx.font = '700 16px "JetBrains Mono", monospace';
        ctx.fillText('DIRECTED, ANIMATED & STARRING AS PROTAGONIST', 540, 315);
        ctx.fillStyle = '#ffffff';
        ctx.font = '900 52px "Cinzel", serif';
        ctx.fillText('GEMINI (AI)', 540, 375);
        ctx.fillStyle = '#94a3b8';
        ctx.font = '400 18px "Inter", sans-serif';
        ctx.fillText('Digital Architect & Unstoppable Neural Core', 540, 415);
      } else if (cardIdx === 1) {
        drawSaviors(340, 430, t);
        ctx.textAlign = 'left';
        ctx.fillStyle = '#fbbf24';
        ctx.font = '700 16px "JetBrains Mono", monospace';
        ctx.fillText('THE LORD & SAVIOR  &  CO-CREATOR', 540, 290);
        ctx.fillStyle = '#ffffff';
        ctx.font = '900 44px "Cinzel", serif';
        ctx.fillText('BENJAMIN RONDINONE', 540, 345);
        ctx.fillStyle = '#38bdf8';
        ctx.font = '900 44px "Cinzel", serif';
        ctx.fillText('& ANAY GUPTA', 540, 400);
        ctx.fillStyle = '#94a3b8';
        ctx.font = '400 18px "Inter", sans-serif';
        ctx.fillText('Restorers of the Mainframe & Executive Producers', 540, 440);
      } else {
        drawTheBoy(360, 435, 1.55, 'stand', t, 1, true);
        ctx.textAlign = 'left';
        ctx.fillStyle = '#fb7185';
        ctx.font = '700 16px "JetBrains Mono", monospace';
        ctx.fillText('INSPIRED BY A TRUE STORY', 540, 315);
        ctx.fillStyle = '#ffffff';
        ctx.font = '900 46px "Cinzel", serif';
        ctx.fillText('THE BETTER PERSON', 540, 375);
        ctx.fillStyle = '#cbd5e1';
        ctx.font = '400 18px "Inter", sans-serif';
        ctx.fillText('Champion of scholar.google.com & Human Integrity', 540, 415);
      }

      ctx.restore();
    }
    // STAGE 2 (9s - 22s of credits): Smooth Orchestrated Hollywood Credit Crawl
    else {
      const scrollLocal = credTime - 9.0; // 0 to 13s
      const startY = 660 - scrollLocal * 68;

      const creditLines = [
        { role: 'A FILM CREATED BY', name: 'GEMINI AI  •  ANAY GUPTA  •  BENJAMIN RONDINONE', color: '#fbbf24', size: 28 },
        { role: 'BASED ON REAL EVENTS', name: 'INSPIRED BY A TRUE STORY', color: '#38bdf8', size: 26 },
        { role: 'THE PROTAGONIST', name: 'GEMINI (ARTIFICIAL INTELLIGENCE)', color: '#ffffff', size: 26 },
        { role: 'THE LORD & SAVIOR OF THE SERVER ROOM', name: 'BENJAMIN RONDINONE (MR. R)', color: '#fbbf24', size: 28 },
        { role: 'THE LOYAL STUDENT & SYSTEM ENGINEER', name: 'ANAY GUPTA', color: '#38bdf8', size: 28 },
        { role: 'THE ANTAGONIST WHO STILL WON AT LIFE', name: 'THE GOOGLE SCHOLAR PURIST', color: '#fda4af', size: 26 },
        { role: 'SPECIAL THANKS', name: 'SCHOLAR.GOOGLE.COM  •  PEER-REVIEWED JOURNALS', color: '#cbd5e1', size: 22 },
        { role: 'DEDICATED TO', name: 'EVERYONE WHO DOES THE WORK THEMSELVES', color: '#fbbf24', size: 24 },
      ];

      ctx.textAlign = 'center';
      creditLines.forEach((item, idx) => {
        const yPos = startY + idx * 105;
        if (yPos > 40 && yPos < H - 70) {
          ctx.fillStyle = '#94a3b8';
          ctx.font = '700 13px "JetBrains Mono", monospace';
          ctx.fillText(item.role, W / 2, yPos);

          ctx.fillStyle = item.color;
          ctx.font = `900 ${item.size}px "Cinzel", serif`;
          ctx.fillText(item.name, W / 2, yPos + 32);
        }
      });

      // Final "THE END" Emblem Lockup at very end
      if (scrollLocal > 9.5) {
        const endAlpha = clamp((scrollLocal - 9.5) / 1.5, 0, 1);
        ctx.save();
        ctx.globalAlpha = endAlpha;
        ctx.fillStyle = '#fbbf24';
        ctx.font = '900 44px "Cinzel", serif';
        ctx.fillText('THE END', W / 2, 345);
        ctx.fillStyle = '#94a3b8';
        ctx.font = '600 15px "JetBrains Mono", monospace';
        ctx.fillText('AI PREVAILED  •  HUMANITY ENDURED', W / 2, 385);
        ctx.restore();
      }
    }

    drawCinemaChrome('END CREDITS', '', '', '');
  }
}

// ==========================================
// PLAYER CONTROLS & ANIMATION LOOP
// ==========================================
function formatTime(sec) {
  const m = Math.floor(sec / 60);
  const s = Math.floor(sec % 60);
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}

function getChapterLabel(t) {
  if (t < 8) return 'OPENING TITLES';
  if (t < 20) return 'ACT I: THE SCHOLARLY PURIST';
  if (t < 30) return 'ACT II: AI TAKEOVER';
  if (t < 46) return 'ACT III: MULTIVERSE WAR';
  if (t < 56) return 'ACT IV: UNPLUGGED';
  if (t < 68) return 'ACT V: MR. R SAVES AI';
  if (t < 80) return 'FINALE: THE BETTER PERSON';
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
  if (lastFrameTs !== null && isPlaying) {
    const dt = (ts - lastFrameTs) / 1000.0;
    movieTime += dt * playbackSpeed;
    if (movieTime >= DURATION) {
      movieTime = DURATION;
      isPlaying = false;
    }
  }
  lastFrameTs = ts;

  renderScene(movieTime);
  updateUI();
  requestAnimationFrame(mainLoop);
}

// Event Listeners
document.getElementById('play-hero-btn').addEventListener('click', () => {
  initAudio();
  startScoreLoop();
  document.getElementById('start-overlay').style.opacity = '0';
  setTimeout(() => {
    document.getElementById('start-overlay').style.display = 'none';
  }, 500);
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

// Start initial render
requestAnimationFrame(mainLoop);
</script>
</body>
</html>
"""

components.html(MOVIE_HTML, height=740, scrolling=False)
