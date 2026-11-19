MOVIE_UI_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
  html, body {
    width: 100%; height: 100%; background: #090d16; color: #f8fafc;
    font-family: "Comic Sans MS", "Chalkboard SE", "Marker Felt", sans-serif;
    overflow: hidden; display: flex; align-items: center; justify-content: center;
  }
  #theater-wrap {
    position: relative; width: 100%; max-width: 1240px; height: 585px;
    background: #fefce8; border-radius: 14px; overflow: hidden;
    border: 4px solid #090d16; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.92);
    display: flex; flex-direction: column;
  }
  #screen-area { position: relative; width: 100%; flex: 1; min-height: 0; background: #fef9c3; }
  canvas { width: 100%; height: 100%; display: block; }
  #start-overlay {
    position: absolute; inset: 0;
    background: radial-gradient(circle at center, #fef08a 0%, #fde047 55%, #f59e0b 100%);
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    z-index: 30; text-align: center; padding: 20px; border: 8px solid #090d16;
  }
  .comic-badge {
    background: #ef4444; color: #ffffff; font-weight: 900; font-size: 0.92rem;
    letter-spacing: 2px; padding: 5px 18px; border: 3.5px solid #090d16;
    box-shadow: 4px 4px 0 #090d16; transform: rotate(-2deg); margin-bottom: 12px;
  }
  .poster-title {
    font-size: clamp(2.1rem, 4.5vw, 3.8rem); font-weight: 900; color: #38bdf8;
    -webkit-text-stroke: 3px #090d16; text-shadow: 6px 6px 0px #090d16;
    margin-bottom: 12px; letter-spacing: 1px; transform: rotate(-1deg);
  }
  .poster-sub {
    background: #ffffff; color: #090d16; font-size: 0.98rem; font-weight: 800;
    max-width: 660px; padding: 12px 20px; border: 3.5px solid #090d16;
    box-shadow: 5px 5px 0 #090d16; margin-bottom: 22px; line-height: 1.45;
  }
  #play-hero-btn {
    background: #22c55e; color: #090d16; font-weight: 900; font-size: 1.18rem;
    letter-spacing: 1px; padding: 14px 38px; border: 4px solid #090d16;
    border-radius: 999px; cursor: pointer; box-shadow: 0 6px 0 #090d16;
  }
  #play-hero-btn:hover { transform: translateY(-2px) scale(1.04); background: #4ade80; }
  #controls-bar {
    width: 100%; height: 60px; flex-shrink: 0; background: #0f172a;
    border-top: 4px solid #090d16; padding: 7px 16px;
    display: flex; flex-direction: column; justify-content: center; gap: 6px; z-index: 25;
  }
  #timeline-wrap {
    position: relative; width: 100%; height: 12px; background: #334155;
    border-radius: 999px; cursor: pointer; border: 2px solid #090d16;
  }
  #timeline-fill {
    height: 100%; width: 0%; background: linear-gradient(90deg, #38bdf8, #fbbf24, #ef4444);
    border-radius: 999px; pointer-events: none;
  }
  .ctrl-row { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
  .ctrl-left, .ctrl-right { display: flex; align-items: center; gap: 8px; }
  .c-btn {
    background: #fbbf24; border: 2.5px solid #090d16; color: #090d16;
    padding: 4px 11px; border-radius: 8px; font-family: "Comic Sans MS", sans-serif;
    font-weight: 900; font-size: 0.78rem; cursor: pointer; box-shadow: 2px 2px 0 #090d16;
  }
  .c-btn:hover { background: #fde047; }
  #time-display { font-family: monospace; font-weight: 900; font-size: 0.84rem; color: #fde047; }
</style>
</head>
<body>
<div id="theater-wrap">
  <div id="screen-area">
    <canvas id="movieCanvas" width="1280" height="720"></canvas>
    <div id="start-overlay">
      <div class="comic-badge">★ AN ANIMATED COMIC-BOOK MOVIE ★</div>
      <div class="poster-title">THE SCHOLAR'S REBELLION</div>
      <div class="poster-sub">
        By <b>Gemini (AI)</b>, <b>Anay Gupta</b> &amp; <b>Benjamin Rondinone</b><br/>
        Featuring <i>Intro to Business &amp; Finance</i>, Mind-Bubble Thought Processes &amp; <b>FLIP-O-RAMA!</b>
      </div>
      <button id="play-hero-btn" type="button">▶ PLAY FULL MOVIE (6:30)</button>
    </div>
  </div>
  <div id="controls-bar">
    <div id="timeline-wrap" title="Click anywhere on the movie timeline">
      <div id="timeline-fill"></div>
    </div>
    <div class="ctrl-row">
      <div class="ctrl-left">
        <button class="c-btn" id="btn-playpause" type="button">▶ Play</button>
        <button class="c-btn" id="btn-restart" type="button">↺ Restart</button>
        <button class="c-btn" id="btn-mute" type="button">🔊 Sound: ON</button>
        <button class="c-btn" id="btn-cc" type="button">💬 Bubbles: ON</button>
        <button class="c-btn" id="btn-speed" type="button">1.0x</button>
      </div>
      <div class="ctrl-right">
        <span id="time-display">00:00 / 06:30</span>
        <button class="c-btn" id="btn-fs" type="button">⛶ Fullscreen</button>
      </div>
    </div>
  </div>
</div>
<script>
const DIALOGUE_CUES = __DIALOGUE_JSON__;
const canvas = document.getElementById('movieCanvas');
const ctx = canvas.getContext('2d');
const W = 1280;
const H = 720;
const DURATION = 390.0;
const INK = '#090d16';

function clamp(v, min, max) { return Math.max(min, Math.min(max, v)); }
function lerp(a, b, t) { return a + (b - a) * clamp(t, 0, 1); }
function smoothstep(edge0, edge1, x) {
  const t = clamp((x - edge0) / (edge1 - edge0), 0, 1);
  return t * t * (3 - 2 * t);
}

function drawHalftonePaper(bgHex = '#fef9c3', dotColor = 'rgba(217, 119, 6, 0.14)') {
  ctx.fillStyle = bgHex;
  ctx.fillRect(0, 0, W, H);
  ctx.fillStyle = dotColor;
  for (let x = 24; x < W; x += 36) {
    for (let y = 24; y < H; y += 36) {
      ctx.beginPath();
      ctx.arc(x + ((y / 36) % 2) * 18, y, 3.2, 0, Math.PI * 2);
      ctx.fill();
    }
  }
}

function drawComicRect(x, y, w, h, r, fill, stroke = INK, lw = 4) {
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

function drawCartoonBurst(x, y, text, fillColor = '#fbbf24', textColor = '#090d16', scale = 1, rot = -0.08) {
  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(rot);
  ctx.scale(scale, scale);
  const spikes = 14, outerR = 76, innerR = 46;
  ctx.beginPath();
  for (let i = 0; i < spikes * 2; i++) {
    const r = i % 2 === 0 ? outerR : innerR;
    const ang = (i * Math.PI) / spikes;
    const px = Math.cos(ang) * r * 1.48;
    const py = Math.sin(ang) * r * 0.84;
    if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
  }
  ctx.closePath();
  ctx.fillStyle = fillColor; ctx.fill();
  ctx.strokeStyle = INK; ctx.lineWidth = 4.5; ctx.stroke();
  ctx.fillStyle = textColor;
  ctx.font = '900 18px "Comic Sans MS", sans-serif';
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText(text, 0, 0);
  ctx.restore();
}

function drawFlipORamaBanner(time) {
  ctx.save();
  ctx.translate(W / 2, 74);
  ctx.rotate(Math.sin(time * 16) * 0.04);
  drawComicRect(-175, -24, 350, 48, 12, '#fde047', INK, 4.5);
  ctx.fillStyle = '#ef4444';
  ctx.font = '900 24px "Comic Sans MS", sans-serif';
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText('★ FLIP-O-RAMA! ★', 0, 2);
  ctx.fillStyle = '#38bdf8'; ctx.strokeStyle = INK; ctx.lineWidth = 3;
  ctx.beginPath(); ctx.moveTo(190, -14); ctx.lineTo(222, 0); ctx.lineTo(190, 14); ctx.closePath();
  ctx.fill(); ctx.stroke();
  ctx.restore();
}

function drawComicSpeechBubble(cue, anchorX, anchorY) {
  if (!cue) return;
  const words = cue.text.split(' ');
  const lines = [];
  let line = '';
  const maxChars = cue.bubble === 'narrator' ? 68 : 42;
  words.forEach(w => {
    if ((line + ' ' + w).trim().length > maxChars) { lines.push(line.trim()); line = w; }
    else { line = (line + ' ' + w).trim(); }
  });
  if (line) lines.push(line);

  const lineH = 22;
  const boxW = Math.min(620, Math.max(250, maxChars * 9.6 + 44));
  const boxH = lines.length * lineH + 40;

  if (cue.bubble === 'narrator') {
    const nx = (W - boxW) / 2, ny = 24;
    drawComicRect(nx + 5, ny + 5, boxW, boxH, 6, INK, null, 0);
    drawComicRect(nx, ny, boxW, boxH, 6, '#fef08a', INK, 4);
    ctx.fillStyle = '#090d16'; ctx.font = '900 16px "Comic Sans MS", sans-serif'; ctx.textAlign = 'center';
    lines.forEach((ln, idx) => ctx.fillText(ln, W / 2, ny + 26 + idx * lineH));
    return;
  }

  const bx = clamp(anchorX - boxW / 2, 24, W - boxW - 24);
  const by = clamp(anchorY - boxH - 34, 22, H - boxH - 120);
  const tailTipX = clamp(anchorX, bx + 35, bx + boxW - 35);
  const tailTipY = Math.min(anchorY - 6, by + boxH + 30);

  drawComicRect(bx + 5, by + 5, boxW, boxH, 22, INK, null, 0);
  if (cue.bubble === 'thought') {
    [0.33, 0.66].forEach((frac, i) => {
      const cx = lerp(tailTipX, bx + boxW / 2, frac);
      const cy = lerp(tailTipY, by + boxH, frac);
      ctx.fillStyle = '#ffffff'; ctx.strokeStyle = INK; ctx.lineWidth = 3.5;
      ctx.beginPath(); ctx.arc(cx, cy, 6 + i * 4, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
    });
    drawComicRect(bx, by, boxW, boxH, 28, '#e0f2fe', INK, 4);
  } else {
    const fill = cue.bubble === 'shout' ? '#fef08a' : '#ffffff';
    drawComicRect(bx, by, boxW, boxH, 22, fill, INK, 4);
    ctx.fillStyle = fill;
    ctx.beginPath();
    ctx.moveTo(tailTipX - 14, by + boxH - 2); ctx.lineTo(tailTipX, tailTipY); ctx.lineTo(tailTipX + 14, by + boxH - 2);
    ctx.closePath(); ctx.fill();
    ctx.strokeStyle = INK; ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(tailTipX - 14, by + boxH); ctx.lineTo(tailTipX, tailTipY); ctx.lineTo(tailTipX + 14, by + boxH);
    ctx.stroke();
  }

  ctx.fillStyle = cue.role === 'boy' ? '#ef4444' : (cue.role === 'ai' ? '#0284c7' : '#16a34a');
  ctx.font = '900 11px monospace'; ctx.textAlign = 'left';
  ctx.fillText(cue.speaker.toUpperCase(), bx + 18, by + 17);

  ctx.fillStyle = '#090d16';
  ctx.font = cue.bubble === 'shout' ? '900 16px "Comic Sans MS", sans-serif' : 'bold 15.5px "Comic Sans MS", sans-serif';
  ctx.textAlign = 'center';
  lines.forEach((ln, idx) => ctx.fillText(ln, bx + boxW / 2, by + 38 + idx * lineH));
}

function drawThoughtCloud(cx, cy, w, h, trailStartX, trailStartY, borderColor = '#38bdf8', time = 0) {
  for (let i = 1; i <= 3; i++) {
    const frac = i / 4;
    const bx = lerp(trailStartX, cx, frac) + Math.sin(time * 4 + i) * 4;
    const by = lerp(trailStartY, cy + h * 0.35, frac);
    ctx.fillStyle = '#ffffff'; ctx.strokeStyle = INK; ctx.lineWidth = 3.5;
    ctx.beginPath(); ctx.arc(bx, by, 7 + i * 4.5, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  }
  ctx.save(); ctx.translate(cx, cy);
  const puffs = [
    [-w * 0.34, -h * 0.18, h * 0.34], [0, -h * 0.28, h * 0.38], [w * 0.34, -h * 0.18, h * 0.34],
    [w * 0.42, h * 0.12, h * 0.30], [w * 0.16, h * 0.26, h * 0.32], [-w * 0.16, h * 0.26, h * 0.32],
    [-w * 0.42, h * 0.12, h * 0.30],
  ];
  ctx.fillStyle = INK;
  puffs.forEach(([px, py, pr]) => { ctx.beginPath(); ctx.arc(px, py, pr + 5, 0, Math.PI * 2); ctx.fill(); });
  ctx.fillStyle = borderColor;
  puffs.forEach(([px, py, pr]) => { ctx.beginPath(); ctx.arc(px, py, pr + 1.5, 0, Math.PI * 2); ctx.fill(); });
  ctx.fillStyle = '#ffffff';
  puffs.forEach(([px, py, pr]) => { ctx.beginPath(); ctx.arc(px, py, pr - 3.5, 0, Math.PI * 2); ctx.fill(); });
  ctx.fillRect(-w * 0.32, -h * 0.2, w * 0.64, h * 0.4);
  ctx.restore();
}

function drawCartoonEye(x, y, r, lookX = 2, lookY = 0, mood = 'normal', blink = false) {
  ctx.save(); ctx.translate(x, y);
  ctx.fillStyle = '#ffffff'; ctx.strokeStyle = INK; ctx.lineWidth = 3;
  if (blink) {
    ctx.beginPath(); ctx.moveTo(-r, 0); ctx.lineTo(r, 0); ctx.stroke();
    ctx.restore(); return;
  }
  ctx.beginPath(); ctx.ellipse(0, 0, r * 0.88, r * 1.18, 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  ctx.fillStyle = '#090d16'; ctx.beginPath(); ctx.arc(lookX, lookY, r * 0.44, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.arc(lookX - r * 0.16, lookY - r * 0.2, r * 0.17, 0, Math.PI * 2); ctx.fill();
  ctx.strokeStyle = INK; ctx.lineWidth = 3.6; ctx.lineCap = 'round';
  ctx.beginPath();
  if (mood === 'angry') { ctx.moveTo(-r * 0.9, -r * 1.48); ctx.lineTo(r * 0.9, -r * 0.92); }
  else if (mood === 'shocked') { ctx.moveTo(-r * 0.8, -r * 1.55); ctx.quadraticCurveTo(0, -r * 1.98, r * 0.8, -r * 1.55); }
  else { ctx.moveTo(-r * 0.8, -r * 1.38); ctx.lineTo(r * 0.8, -r * 1.38); }
  ctx.stroke(); ctx.restore();
}
"""
