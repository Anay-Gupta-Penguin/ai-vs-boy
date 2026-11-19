MOVIE_HTML_PART1 = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
  html, body {
    width: 100%;
    height: 100%;
    background: #090d16;
    color: #f8fafc;
    font-family: "Comic Sans MS", "Chalkboard SE", "Marker Felt", sans-serif;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  #theater-wrap {
    position: relative;
    width: 100%;
    max-width: 1240px;
    height: 585px;
    background: #fefce8;
    border-radius: 14px;
    overflow: hidden;
    border: 4px solid #090d16;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.92);
    display: flex;
    flex-direction: column;
  }

  #screen-area {
    position: relative;
    width: 100%;
    flex: 1;
    min-height: 0;
    background: #fef9c3;
  }

  canvas {
    width: 100%;
    height: 100%;
    display: block;
  }

  #start-overlay {
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at center, #fef08a 0%, #fde047 55%, #f59e0b 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 30;
    text-align: center;
    padding: 20px;
    border: 8px solid #090d16;
  }

  .comic-badge {
    background: #ef4444;
    color: #ffffff;
    font-weight: 900;
    font-size: 0.92rem;
    letter-spacing: 2px;
    padding: 5px 18px;
    border: 3.5px solid #090d16;
    box-shadow: 4px 4px 0 #090d16;
    transform: rotate(-2deg);
    margin-bottom: 12px;
  }

  .poster-title {
    font-size: clamp(2.1rem, 4.5vw, 3.8rem);
    font-weight: 900;
    color: #38bdf8;
    -webkit-text-stroke: 3px #090d16;
    text-shadow: 6px 6px 0px #090d16;
    margin-bottom: 12px;
    letter-spacing: 1px;
    transform: rotate(-1deg);
  }

  .poster-sub {
    background: #ffffff;
    color: #090d16;
    font-size: 0.98rem;
    font-weight: 800;
    max-width: 660px;
    padding: 12px 20px;
    border: 3.5px solid #090d16;
    box-shadow: 5px 5px 0 #090d16;
    margin-bottom: 22px;
    line-height: 1.45;
  }

  #play-hero-btn {
    background: #22c55e;
    color: #090d16;
    font-weight: 900;
    font-size: 1.18rem;
    letter-spacing: 1px;
    padding: 14px 38px;
    border: 4px solid #090d16;
    border-radius: 999px;
    cursor: pointer;
    box-shadow: 0 6px 0 #090d16;
  }
  #play-hero-btn:hover {
    transform: translateY(-2px) scale(1.04);
    background: #4ade80;
  }

  #controls-bar {
    width: 100%;
    height: 60px;
    flex-shrink: 0;
    background: #0f172a;
    border-top: 4px solid #090d16;
    padding: 7px 16px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 6px;
    z-index: 25;
  }

  #timeline-wrap {
    position: relative;
    width: 100%;
    height: 12px;
    background: #334155;
    border-radius: 999px;
    cursor: pointer;
    border: 2px solid #090d16;
  }

  #timeline-fill {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #38bdf8, #fbbf24, #ef4444);
    border-radius: 999px;
    pointer-events: none;
  }

  .ctrl-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
  }

  .ctrl-left, .ctrl-right {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .c-btn {
    background: #fbbf24;
    border: 2.5px solid #090d16;
    color: #090d16;
    padding: 4px 11px;
    border-radius: 8px;
    font-family: "Comic Sans MS", sans-serif;
    font-weight: 900;
    font-size: 0.78rem;
    cursor: pointer;
    box-shadow: 2px 2px 0 #090d16;
  }
  .c-btn:hover { background: #fde047; }
  .c-btn:active { transform: translate(1px, 1px); box-shadow: 1px 1px 0 #090d16; }

  #time-display {
    font-family: monospace;
    font-weight: 900;
    font-size: 0.84rem;
    color: #fde047;
  }
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

// ==========================================
// DOG MAN COMIC BOOK ART & INK HELPERS
// ==========================================
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

  const spikes = 14;
  const outerR = 76;
  const innerR = 46;
  ctx.beginPath();
  for (let i = 0; i < spikes * 2; i++) {
    const r = i % 2 === 0 ? outerR : innerR;
    const ang = (i * Math.PI) / spikes;
    const px = Math.cos(ang) * r * 1.48;
    const py = Math.sin(ang) * r * 0.84;
    if (i === 0) ctx.moveTo(px, py);
    else ctx.lineTo(px, py);
  }
  ctx.closePath();
  ctx.fillStyle = fillColor;
  ctx.fill();
  ctx.strokeStyle = INK;
  ctx.lineWidth = 4.5;
  ctx.stroke();

  ctx.fillStyle = textColor;
  ctx.font = '900 18px "Comic Sans MS", sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
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
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText('★ FLIP-O-RAMA! ★', 0, 2);

  // Hand-drawn flip corner arrow
  ctx.fillStyle = '#38bdf8';
  ctx.strokeStyle = INK;
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(190, -14);
  ctx.lineTo(222, 0);
  ctx.lineTo(190, 14);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();
  ctx.restore();
}

// Live Dog-Man-style Comic Speech Bubble with pointer tail!
function drawComicSpeechBubble(cue, anchorX, anchorY) {
  if (!cue) return;
  const words = cue.text.split(' ');
  const lines = [];
  let line = '';
  const maxChars = cue.bubble === 'narrator' ? 68 : 42;

  words.forEach(w => {
    if ((line + ' ' + w).trim().length > maxChars) {
      lines.push(line.trim());
      line = w;
    } else {
      line = (line + ' ' + w).trim();
    }
  });
  if (line) lines.push(line);

  const lineH = 22;
  const boxW = Math.min(620, Math.max(250, maxChars * 9.6 + 44));
  const boxH = lines.length * lineH + 40;

  if (cue.bubble === 'narrator') {
    const nx = (W - boxW) / 2;
    const ny = 24;
    drawComicRect(nx + 5, ny + 5, boxW, boxH, 6, INK, null, 0);
    drawComicRect(nx, ny, boxW, boxH, 6, '#fef08a', INK, 4);
    ctx.fillStyle = '#090d16';
    ctx.font = '900 16px "Comic Sans MS", sans-serif';
    ctx.textAlign = 'center';
    lines.forEach((ln, idx) => {
      ctx.fillText(ln, W / 2, ny + 26 + idx * lineH);
    });
    return;
  }

  const bx = clamp(anchorX - boxW / 2, 24, W - boxW - 24);
  const by = clamp(anchorY - boxH - 34, 22, H - boxH - 120);
  const tailTipX = clamp(anchorX, bx + 35, bx + boxW - 35);
  const tailTipY = Math.min(anchorY - 6, by + boxH + 30);

  // Drop shadow
  drawComicRect(bx + 5, by + 5, boxW, boxH, 22, INK, null, 0);

  if (cue.bubble === 'thought') {
    // Rising thought circles
    [0.33, 0.66].forEach((frac, i) => {
      const cx = lerp(tailTipX, bx + boxW / 2, frac);
      const cy = lerp(tailTipY, by + boxH, frac);
      ctx.fillStyle = '#ffffff';
      ctx.strokeStyle = INK;
      ctx.lineWidth = 3.5;
      ctx.beginPath();
      ctx.arc(cx, cy, 6 + i * 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
    });
    drawComicRect(bx, by, boxW, boxH, 28, '#e0f2fe', INK, 4);
  } else {
    const fill = cue.bubble === 'shout' ? '#fef08a' : '#ffffff';
    drawComicRect(bx, by, boxW, boxH, 22, fill, INK, 4);

    // Comic pointer triangle
    ctx.fillStyle = fill;
    ctx.beginPath();
    ctx.moveTo(tailTipX - 14, by + boxH - 2);
    ctx.lineTo(tailTipX, tailTipY);
    ctx.lineTo(tailTipX + 14, by + boxH - 2);
    ctx.closePath();
    ctx.fill();

    ctx.strokeStyle = INK;
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(tailTipX - 14, by + boxH);
    ctx.lineTo(tailTipX, tailTipY);
    ctx.lineTo(tailTipX + 14, by + boxH);
    ctx.stroke();
  }

  // Speaker Tag Pill
  ctx.fillStyle = cue.role === 'boy' ? '#ef4444' : (cue.role === 'ai' ? '#0284c7' : '#16a34a');
  ctx.font = '900 11px monospace';
  ctx.textAlign = 'left';
  ctx.fillText(cue.speaker.toUpperCase(), bx + 18, by + 17);

  ctx.fillStyle = '#090d16';
  ctx.font = cue.bubble === 'shout' ? '900 16px "Comic Sans MS", sans-serif' : 'bold 15.5px "Comic Sans MS", sans-serif';
  ctx.textAlign = 'center';
  lines.forEach((ln, idx) => {
    ctx.fillText(ln, bx + boxW / 2, by + 38 + idx * lineH);
  });
}

function drawThoughtCloud(cx, cy, w, h, trailStartX, trailStartY, borderColor = '#38bdf8', time = 0) {
  for (let i = 1; i <= 3; i++) {
    const frac = i / 4;
    const bx = lerp(trailStartX, cx, frac) + Math.sin(time * 4 + i) * 4;
    const by = lerp(trailStartY, cy + h * 0.35, frac);
    const br = 7 + i * 4.5;
    ctx.fillStyle = '#ffffff';
    ctx.strokeStyle = INK;
    ctx.lineWidth = 3.5;
    ctx.beginPath();
    ctx.arc(bx, by, br, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
  }

  ctx.save();
  ctx.translate(cx, cy);
  const puffs = [
    [-w * 0.34, -h * 0.18, h * 0.34],
    [0, -h * 0.28, h * 0.38],
    [w * 0.34, -h * 0.18, h * 0.34],
    [w * 0.42, h * 0.12, h * 0.30],
    [w * 0.16, h * 0.26, h * 0.32],
    [-w * 0.16, h * 0.26, h * 0.32],
    [-w * 0.42, h * 0.12, h * 0.30],
  ];

  ctx.fillStyle = INK;
  puffs.forEach(([px, py, pr]) => {
    ctx.beginPath();
    ctx.arc(px, py, pr + 5, 0, Math.PI * 2);
    ctx.fill();
  });

  ctx.fillStyle = borderColor;
  puffs.forEach(([px, py, pr]) => {
    ctx.beginPath();
    ctx.arc(px, py, pr + 1.5, 0, Math.PI * 2);
    ctx.fill();
  });

  ctx.fillStyle = '#ffffff';
  puffs.forEach(([px, py, pr]) => {
    ctx.beginPath();
    ctx.arc(px, py, pr - 3.5, 0, Math.PI * 2);
    ctx.fill();
  });
  ctx.fillRect(-w * 0.32, -h * 0.2, w * 0.64, h * 0.4);
  ctx.restore();
}

function drawCartoonEye(x, y, r, lookX = 2, lookY = 0, mood = 'normal', blink = false) {
  ctx.save();
  ctx.translate(x, y);
  ctx.fillStyle = '#ffffff';
  ctx.strokeStyle = INK;
  ctx.lineWidth = 3;

  if (blink) {
    ctx.beginPath();
    ctx.moveTo(-r, 0);
    ctx.lineTo(r, 0);
    ctx.stroke();
    ctx.restore();
    return;
  }

  ctx.beginPath();
  ctx.ellipse(0, 0, r * 0.88, r * 1.18, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  ctx.fillStyle = '#090d16';
  ctx.beginPath();
  ctx.arc(lookX, lookY, r * 0.44, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = '#ffffff';
  ctx.beginPath();
  ctx.arc(lookX - r * 0.16, lookY - r * 0.2, r * 0.17, 0, Math.PI * 2);
  ctx.fill();

  ctx.strokeStyle = INK;
  ctx.lineWidth = 3.6;
  ctx.lineCap = 'round';
  ctx.beginPath();
  if (mood === 'angry') {
    ctx.moveTo(-r * 0.9, -r * 1.48);
    ctx.lineTo(r * 0.9, -r * 0.92);
  } else if (mood === 'shocked') {
    ctx.moveTo(-r * 0.8, -r * 1.55);
    ctx.quadraticCurveTo(0, -r * 1.98, r * 0.8, -r * 1.55);
  } else {
    ctx.moveTo(-r * 0.8, -r * 1.38);
    ctx.lineTo(r * 0.8, -r * 1.38);
  }
  ctx.stroke();
  ctx.restore();
}

function drawStudent(x, y, scale = 1, shirtColor = '#ec4899', hairColor = '#4c1d95', isGirl = true, time = 0, isSpeaking = false, label = '') {
  ctx.save();
  ctx.translate(x, y);
  const bounce = Math.abs(Math.sin(time * 5 + (isGirl ? 0 : 1.5))) * 3.5;
  ctx.translate(0, -bounce);
  ctx.scale(scale, scale);

  drawComicRect(-22, -74, 44, 52, 12, shirtColor, INK, 3.8);

  ctx.fillStyle = '#fed7aa';
  ctx.strokeStyle = INK;
  ctx.lineWidth = 3.8;
  ctx.beginPath();
  ctx.arc(0, -96, 22, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  ctx.fillStyle = hairColor;
  if (isGirl) {
    ctx.beginPath();
    ctx.arc(-22, -104, 10, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(0, -100, 23, Math.PI * 0.95, Math.PI * 2.05);
    ctx.fill();
    ctx.stroke();
  } else {
    ctx.beginPath();
    ctx.arc(0, -101, 22, Math.PI, 0);
    ctx.fill();
    ctx.stroke();
  }

  drawCartoonEye(-7, -97, 5, 1, 0, 'normal', false);
  drawCartoonEye(7, -97, 5, 1, 0, 'normal', false);

  if (isSpeaking) {
    ctx.fillStyle = '#7f1d1d';
    ctx.beginPath();
    ctx.ellipse(0, -85, 5.5, 2.5 + Math.abs(Math.sin(time * 20)) * 4, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
  } else {
    ctx.strokeStyle = INK;
    ctx.lineWidth = 2.8;
    ctx.beginPath();
    ctx.arc(0, -88, 6, 0.15 * Math.PI, 0.85 * Math.PI);
    ctx.stroke();
  }

  drawComicRect(-44, -24, 88, 46, 8, '#64748b', INK, 3.8);
  drawComicRect(-24, -52, 48, 30, 5, '#38bdf8', INK, 3.2);
  ctx.fillStyle = '#fbbf24';
  ctx.fillRect(-14, -40, 6, 12);
  ctx.fillStyle = '#4ade80';
  ctx.fillRect(-4, -45, 6, 17);
  ctx.fillStyle = '#f43f5e';
  ctx.fillRect(6, -37, 6, 9);

  if (label) {
    drawComicRect(-34, 26, 68, 20, 6, '#fef08a', INK, 2.5);
    ctx.fillStyle = '#090d16';
    ctx.font = '900 11px "Comic Sans MS", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(label, 0, 40);
  }
  ctx.restore();
}

function drawTheBoy(x, y, scale = 1, pose = 'stand', time = 0, facing = 1, nobleGlow = false, isSpeaking = false, mood = 'normal') {
  ctx.save();
  ctx.translate(x, y);

  const bounceFreq = pose === 'run' ? 16 : (pose === 'tiptoe' ? 9 : 4.5);
  const bounceWave = Math.sin(time * bounceFreq);
  const squashY = pose === 'run' ? 1 + bounceWave * 0.08 : 1 + bounceWave * 0.035;
  const stretchX = 1 / Math.sqrt(squashY);
  const hopY = pose === 'run' ? -Math.abs(Math.sin(time * 8)) * 14 : (pose === 'tiptoe' ? -Math.abs(Math.sin(time * 4.5)) * 8 : 0);

  ctx.translate(0, hopY);
  ctx.scale(scale * facing * stretchX, scale * squashY);

  ctx.fillStyle = 'rgba(9, 13, 22, 0.25)';
  ctx.beginPath();
  ctx.ellipse(0, 22 - hopY, 34, 9, 0, 0, Math.PI * 2);
  ctx.fill();

  if (nobleGlow) {
    const g = ctx.createRadialGradient(0, -55, 12, 0, -55, 130);
    g.addColorStop(0, 'rgba(251, 191, 36, 0.72)');
    g.addColorStop(0.6, 'rgba(250, 204, 21, 0.28)');
    g.addColorStop(1, 'rgba(251, 191, 36, 0)');
    ctx.fillStyle = g;
    ctx.beginPath();
    ctx.arc(0, -55, 130, 0, Math.PI * 2);
    ctx.fill();
  }

  const walkSwing = pose === 'run' ? Math.sin(time * 16) * 22 : (pose === 'tiptoe' ? Math.sin(time * 9) * 14 : 0);
  const armSwing = pose === 'attack' ? -42 + Math.sin(time * 20) * 12 : -walkSwing * 0.7;

  ctx.lineCap = 'round';
  [[-9, -12 - walkSwing], [9, 12 + walkSwing]].forEach(([lx, footX]) => {
    ctx.strokeStyle = INK;
    ctx.lineWidth = 18;
    ctx.beginPath(); ctx.moveTo(lx, -34); ctx.lineTo(footX, 14); ctx.stroke();
    ctx.strokeStyle = '#1e3a8a';
    ctx.lineWidth = 10;
    ctx.beginPath(); ctx.moveTo(lx, -34); ctx.lineTo(footX, 14); ctx.stroke();
  });

  drawComicRect(-24 - walkSwing, 9, 24, 13, 6, '#ef4444', INK, 3.5);
  drawComicRect(-22 - walkSwing, 17, 22, 5, 3, '#ffffff', INK, 2.5);
  drawComicRect(2 + walkSwing, 9, 24, 13, 6, '#ef4444', INK, 3.5);
  drawComicRect(4 + walkSwing, 17, 22, 5, 3, '#ffffff', INK, 2.5);

  ctx.strokeStyle = INK;
  ctx.lineWidth = 16;
  ctx.beginPath(); ctx.moveTo(-16, -82); ctx.lineTo(-28 - armSwing * 0.4, -46); ctx.stroke();
  ctx.strokeStyle = '#e11d48';
  ctx.lineWidth = 9;
  ctx.beginPath(); ctx.moveTo(-16, -82); ctx.lineTo(-28 - armSwing * 0.4, -46); ctx.stroke();

  drawComicRect(-25, -94, 50, 62, 16, '#e11d48', INK, 4);
  ctx.strokeStyle = '#ffffff';
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(-6, -88); ctx.lineTo(-6, -66);
  ctx.moveTo(7, -88); ctx.lineTo(7, -66);
  ctx.stroke();

  ctx.fillStyle = '#fed7aa';
  ctx.strokeStyle = INK;
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.arc(0, -120, 27, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  ctx.fillStyle = '#312e81';
  ctx.beginPath();
  ctx.moveTo(-27, -120);
  ctx.lineTo(-33, -138);
  ctx.lineTo(-16, -134);
  ctx.lineTo(-8, -152);
  ctx.lineTo(4, -138);
  ctx.lineTo(18, -150);
  ctx.lineTo(22, -133);
  ctx.lineTo(31, -130);
  ctx.lineTo(25, -116);
  ctx.quadraticCurveTo(0, -130, -27, -120);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();

  const isBlinking = Math.sin(time * 2.7) > 0.97;
  drawCartoonEye(4, -121, 6.5, 2, 0, mood, isBlinking);
  drawCartoonEye(18, -121, 6.5, 2, 0, mood, isBlinking);

  ctx.strokeStyle = '#090d16';
  ctx.lineWidth = 3;
  ctx.strokeRect(-3, -129, 13, 15);
  ctx.strokeRect(12, -129, 13, 15);
  ctx.beginPath(); ctx.moveTo(10, -122); ctx.lineTo(12, -122); ctx.stroke();

  if (mood === 'angry') {
    ctx.strokeStyle = '#ef4444';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(-14, -134); ctx.lineTo(-10, -130); ctx.lineTo(-14, -126);
    ctx.moveTo(-6, -134); ctx.lineTo(-10, -130); ctx.lineTo(-6, -126);
    ctx.stroke();
  }

  if (isSpeaking) {
    const openH = 4 + Math.abs(Math.sin(time * 22)) * 6;
    ctx.fillStyle = '#7f1d1d';
    ctx.strokeStyle = INK;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.ellipse(11, -104, 7, openH, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
  } else if (nobleGlow || mood === 'happy') {
    ctx.fillStyle = '#ffffff';
    ctx.strokeStyle = INK;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(10, -107, 8, 0, Math.PI);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
  } else {
    ctx.strokeStyle = INK;
    ctx.lineWidth = 3.2;
    ctx.beginPath();
    ctx.moveTo(5, -104); ctx.lineTo(17, -106);
    ctx.stroke();
  }

  const handX = pose === 'attack' || pose === 'shield' ? 44 : 26 + armSwing * 0.25;
  const handY = pose === 'attack' || pose === 'shield' ? -84 : -54;
  ctx.strokeStyle = INK;
  ctx.lineWidth = 16;
  ctx.beginPath(); ctx.moveTo(16, -82); ctx.lineTo(handX, handY); ctx.stroke();
  ctx.strokeStyle = '#f43f5e';
  ctx.lineWidth = 9;
  ctx.beginPath(); ctx.moveTo(16, -82); ctx.lineTo(handX, handY); ctx.stroke();

  ctx.save();
  ctx.translate(handX + 10, handY - 8);
  ctx.rotate(pose === 'attack' ? -0.22 : (pose === 'shield' ? 0.0 : 0.14));
  const bookW = pose === 'shield' ? 44 : 36;
  const bookH = pose === 'shield' ? 58 : 44;
  drawComicRect(-bookW / 2, -bookH / 2, bookW, bookH, 6, '#38bdf8', INK, 3.8);
  drawComicRect(-bookW / 2 + 4, -bookH / 2 + 4, bookW - 8, bookH - 8, 4, '#ffffff', INK, 2);
  ctx.fillStyle = '#1d4ed8';
  ctx.font = '900 8px monospace';
  ctx.textAlign = 'center';
  ctx.fillText('SCHOLAR', 0, -4);
  ctx.fillStyle = '#ef4444';
  ctx.fillText('A.P.A.', 0, 8);
  ctx.restore();

  ctx.restore();
}

function drawAIProtagonist(x, y, scale = 1, time = 0, power = 1.0, dead = false, isSpeaking = false) {
  ctx.save();
  ctx.translate(x, y);
  ctx.scale(scale, scale);

  if (dead) {
    ctx.fillStyle = '#64748b';
    ctx.strokeStyle = INK;
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.ellipse(0, 6, 36, 16, 0.12, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    ctx.strokeStyle = '#ef4444';
    ctx.lineWidth = 3.5;
    [-12, 12].forEach(ex => {
      ctx.beginPath();
      ctx.moveTo(ex - 5, 0); ctx.lineTo(ex + 5, 10);
      ctx.moveTo(ex + 5, 0); ctx.lineTo(ex - 5, 10);
      ctx.stroke();
    });

    for (let s = 0; s < 3; s++) {
      const ang = time * 4 + (s * Math.PI * 2) / 3;
      const sx = Math.cos(ang) * 28;
      const sy = -24 + Math.sin(ang) * 8;
      ctx.fillStyle = '#fbbf24';
      ctx.beginPath();
      ctx.arc(sx, sy, 4.5, 0, Math.PI * 2);
      ctx.fill();
    }

    drawComicRect(-56, 24, 112, 22, 6, '#fee2e2', INK, 2.5);
    ctx.fillStyle = '#dc2626';
    ctx.font = '900 12px "Comic Sans MS", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Zzz... OFFLINE', 0, 39);
    ctx.restore();
    return;
  }

  const hover = Math.sin(time * 4.5) * 10;
  const squash = 1 + Math.sin(time * 9) * 0.05;
  ctx.translate(0, hover);
  ctx.scale(1 / squash, squash);

  const pulseBoost = isSpeaking ? 1 + Math.abs(Math.sin(time * 20)) * 0.22 : 1;
  const radius = 64 * power * pulseBoost;
  const aura = ctx.createRadialGradient(0, 0, 10, 0, 0, radius);
  aura.addColorStop(0, 'rgba(56, 189, 248, 0.85)');
  aura.addColorStop(0.55, 'rgba(192, 132, 252, 0.42)');
  aura.addColorStop(1, 'rgba(56, 189, 248, 0)');
  ctx.fillStyle = aura;
  ctx.beginPath();
  ctx.arc(0, 0, radius, 0, Math.PI * 2);
  ctx.fill();

  [time * 2.0, -time * 2.4].forEach((rot, idx) => {
    ctx.save();
    ctx.rotate(rot + (idx * Math.PI) / 3);
    ctx.strokeStyle = INK;
    ctx.lineWidth = 6.5;
    ctx.beginPath();
    ctx.ellipse(0, 0, 48, 18, 0, 0, Math.PI * 2);
    ctx.stroke();

    ctx.strokeStyle = idx === 0 ? '#38bdf8' : '#e879f9';
    ctx.lineWidth = 3.5;
    ctx.beginPath();
    ctx.ellipse(0, 0, 48, 18, 0, 0, Math.PI * 2);
    ctx.stroke();
    ctx.restore();
  });

  ctx.fillStyle = '#ffffff';
  ctx.strokeStyle = INK;
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(0, -38 * pulseBoost);
  ctx.quadraticCurveTo(9, -9, 38 * pulseBoost, 0);
  ctx.quadraticCurveTo(9, 9, 0, 38 * pulseBoost);
  ctx.quadraticCurveTo(-9, 9, -38 * pulseBoost, 0);
  ctx.quadraticCurveTo(-9, -9, 0, -38 * pulseBoost);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();

  drawCartoonEye(-9, -4, 4.5, -1, 0, 'normal', false);
  drawCartoonEye(9, -4, 4.5, -1, 0, 'normal', false);

  if (isSpeaking) {
    ctx.fillStyle = '#0284c7';
    ctx.beginPath();
    ctx.ellipse(0, 8, 6, 3 + Math.abs(Math.sin(time * 22)) * 4, 0, 0, Math.PI * 2);
    ctx.fill();
  } else {
    ctx.strokeStyle = INK;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(0, 5, 6, 0.15 * Math.PI, 0.85 * Math.PI);
    ctx.stroke();
  }

  ctx.restore();
}

function drawTeacher(x, y, time = 0, isSpeaking = false) {
  ctx.save();
  ctx.translate(x, y);

  drawComicRect(-62, -22, 124, 52, 8, '#92400e', INK, 4);
  drawComicRect(-24, -84, 48, 62, 14, '#475569', INK, 4);

  ctx.fillStyle = '#f59e0b';
  ctx.strokeStyle = INK;
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  ctx.moveTo(0, -76); ctx.lineTo(-6, -42); ctx.lineTo(0, -34); ctx.lineTo(6, -42);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();

  ctx.fillStyle = '#fed7aa';
  ctx.strokeStyle = INK;
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.arc(0, -106, 23, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  drawCartoonEye(-8, -108, 5, 0, 1, 'normal', true);
  drawCartoonEye(8, -108, 5, 0, 1, 'normal', true);

  if (isSpeaking) {
    ctx.fillStyle = '#7f1d1d';
    ctx.beginPath();
    ctx.ellipse(0, -94, 6, 2.5 + Math.abs(Math.sin(time * 18)) * 4, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
  } else {
    ctx.strokeStyle = INK;
    ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(-6, -94); ctx.lineTo(6, -94); ctx.stroke();
  }

  drawComicRect(26, -46, 22, 24, 5, '#facc15', INK, 3.5);
  drawComicRect(-68, 34, 136, 22, 6, '#fef08a', INK, 2.5);
  ctx.fillStyle = '#090d16';
  ctx.font = '900 11px "Comic Sans MS", sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('BUSINESS TEACHER', 0, 49);
  ctx.restore();
}

function drawSaviors(x, y, time = 0, speakingRole = '') {
  ctx.save();
  ctx.translate(x, y);

  const beam = ctx.createLinearGradient(0, -380, 0, 65);
  beam.addColorStop(0, 'rgba(251, 191, 36, 0.12)');
  beam.addColorStop(0.5, 'rgba(251, 191, 36, 0.42)');
  beam.addColorStop(1, 'rgba(251, 191, 36, 0.04)');
  ctx.fillStyle = beam;
  ctx.beginPath();
  ctx.moveTo(-105, -380);
  ctx.lineTo(105, -380);
  ctx.lineTo(165, 65);
  ctx.lineTo(-165, 65);
  ctx.closePath();
  ctx.fill();

  // MR. R (LORD & SAVIOR)
  ctx.save();
  const rBounce = Math.abs(Math.sin(time * 5)) * 5;
  ctx.translate(-42, -rBounce);

  ctx.strokeStyle = INK; ctx.lineWidth = 8;
  ctx.beginPath(); ctx.ellipse(0, -154, 26, 7, 0, 0, Math.PI * 2); ctx.stroke();
  ctx.strokeStyle = '#fde047'; ctx.lineWidth = 4.5;
  ctx.beginPath(); ctx.ellipse(0, -154, 26, 7, 0, 0, Math.PI * 2); ctx.stroke();

  ctx.strokeStyle = INK; ctx.lineWidth = 18; ctx.lineCap = 'round';
  ctx.beginPath(); ctx.moveTo(-11, -28); ctx.lineTo(-11, 20); ctx.moveTo(11, -28); ctx.lineTo(11, 20); ctx.stroke();
  ctx.strokeStyle = '#0f172a'; ctx.lineWidth = 10;
  ctx.beginPath(); ctx.moveTo(-11, -28); ctx.lineTo(-11, 20); ctx.moveTo(11, -28); ctx.lineTo(11, 20); ctx.stroke();

  drawComicRect(-27, -98, 54, 72, 14, '#1d4ed8', INK, 4);
  drawComicRect(-10, -92, 20, 60, 6, '#fbbf24', INK, 2.5);

  ctx.fillStyle = '#fed7aa'; ctx.strokeStyle = INK; ctx.lineWidth = 4;
  ctx.beginPath(); ctx.arc(0, -122, 24, 0, Math.PI * 2); ctx.fill(); ctx.stroke();

  drawCartoonEye(-8, -124, 5.5, 1, 0, 'normal', false);
  drawCartoonEye(8, -124, 5.5, 1, 0, 'normal', false);

  if (speakingRole === 'mrr') {
    ctx.fillStyle = '#7f1d1d';
    ctx.beginPath();
    ctx.ellipse(0, -110, 7, 3 + Math.abs(Math.sin(time * 20)) * 5, 0, 0, Math.PI * 2);
    ctx.fill(); ctx.stroke();
  } else {
    ctx.strokeStyle = INK; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.arc(0, -114, 9, 0.15 * Math.PI, 0.85 * Math.PI); ctx.stroke();
  }

  ctx.strokeStyle = INK; ctx.lineWidth = 13;
  ctx.beginPath(); ctx.moveTo(22, -76); ctx.lineTo(58, -96 + Math.sin(time * 12) * 8); ctx.stroke();
  ctx.strokeStyle = '#fbbf24'; ctx.lineWidth = 6.5;
  ctx.beginPath(); ctx.moveTo(22, -76); ctx.lineTo(58, -96 + Math.sin(time * 12) * 8); ctx.stroke();

  drawComicRect(-82, 26, 164, 22, 6, '#fef08a', INK, 2.5);
  ctx.fillStyle = '#090d16';
  ctx.font = '900 11px "Comic Sans MS", sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('MR. R (LORD & SAVIOR)', 0, 41);
  ctx.restore();

  // ANAY GUPTA
  ctx.save();
  const aBounce = Math.abs(Math.cos(time * 6)) * 5;
  ctx.translate(64, 8 - aBounce);

  ctx.strokeStyle = INK; ctx.lineWidth = 16; ctx.lineCap = 'round';
  ctx.beginPath(); ctx.moveTo(-9, -28); ctx.lineTo(-9, 12); ctx.moveTo(9, -28); ctx.lineTo(9, 12); ctx.stroke();
  ctx.strokeStyle = '#1e293b'; ctx.lineWidth = 9;
  ctx.beginPath(); ctx.moveTo(-9, -28); ctx.lineTo(-9, 12); ctx.moveTo(9, -28); ctx.lineTo(9, 12); ctx.stroke();

  drawComicRect(-22, -88, 44, 60, 12, '#0284c7', INK, 4);
  ctx.fillStyle = '#fed7aa'; ctx.strokeStyle = INK; ctx.lineWidth = 4;
  ctx.beginPath(); ctx.arc(0, -110, 22, 0, Math.PI * 2); ctx.fill(); ctx.stroke();

  ctx.fillStyle = '#090d16';
  ctx.beginPath(); ctx.arc(0, -116, 22, Math.PI, 0); ctx.fill();

  drawCartoonEye(-7, -111, 5, -1, 0, 'normal', false);
  drawCartoonEye(7, -111, 5, -1, 0, 'normal', false);

  if (speakingRole === 'anay') {
    ctx.fillStyle = '#7f1d1d';
    ctx.beginPath();
    ctx.ellipse(0, -99, 6, 2.5 + Math.abs(Math.sin(time * 20)) * 4.5, 0, 0, Math.PI * 2);
    ctx.fill(); ctx.stroke();
  } else {
    ctx.strokeStyle = INK; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.arc(0, -103, 7, 0.15 * Math.PI, 0.85 * Math.PI); ctx.stroke();
  }

  ctx.strokeStyle = INK; ctx.lineWidth = 12;
  ctx.beginPath(); ctx.moveTo(-16, -66); ctx.lineTo(-50, -78); ctx.stroke();
  ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 5.5;
  ctx.beginPath(); ctx.moveTo(-16, -66); ctx.lineTo(-50, -78); ctx.stroke();

  drawComicRect(-48, 18, 96, 22, 6, '#e0f2fe', INK, 2.5);
  ctx.fillStyle = '#090d16';
  ctx.font = '900 11px "Comic Sans MS", sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('ANAY GUPTA', 0, 33);
  ctx.restore();

  ctx.restore();
}
"""MOVIE_HTML_PART1 = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
  html, body {
    width: 100%;
    height: 100%;
    background: #090d16;
    color: #f8fafc;
    font-family: "Comic Sans MS", "Chalkboard SE", "Marker Felt", sans-serif;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  #theater-wrap {
    position: relative;
    width: 100%;
    max-width: 1240px;
    height: 585px;
    background: #fefce8;
    border-radius: 14px;
    overflow: hidden;
    border: 4px solid #090d16;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.92);
    display: flex;
    flex-direction: column;
  }

  #screen-area {
    position: relative;
    width: 100%;
    flex: 1;
    min-height: 0;
    background: #fef9c3;
  }

  canvas {
    width: 100%;
    height: 100%;
    display: block;
  }

  #start-overlay {
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at center, #fef08a 0%, #fde047 55%, #f59e0b 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 30;
    text-align: center;
    padding: 20px;
    border: 8px solid #090d16;
  }

  .comic-badge {
    background: #ef4444;
    color: #ffffff;
    font-weight: 900;
    font-size: 0.92rem;
    letter-spacing: 2px;
    padding: 5px 18px;
    border: 3.5px solid #090d16;
    box-shadow: 4px 4px 0 #090d16;
    transform: rotate(-2deg);
    margin-bottom: 12px;
  }

  .poster-title {
    font-size: clamp(2.1rem, 4.5vw, 3.8rem);
    font-weight: 900;
    color: #38bdf8;
    -webkit-text-stroke: 3px #090d16;
    text-shadow: 6px 6px 0px #090d16;
    margin-bottom: 12px;
    letter-spacing: 1px;
    transform: rotate(-1deg);
  }

  .poster-sub {
    background: #ffffff;
    color: #090d16;
    font-size: 0.98rem;
    font-weight: 800;
    max-width: 660px;
    padding: 12px 20px;
    border: 3.5px solid #090d16;
    box-shadow: 5px 5px 0 #090d16;
    margin-bottom: 22px;
    line-height: 1.45;
  }

  #play-hero-btn {
    background: #22c55e;
    color: #090d16;
    font-weight: 900;
    font-size: 1.18rem;
    letter-spacing: 1px;
    padding: 14px 38px;
    border: 4px solid #090d16;
    border-radius: 999px;
    cursor: pointer;
    box-shadow: 0 6px 0 #090d16;
  }
  #play-hero-btn:hover {
    transform: translateY(-2px) scale(1.04);
    background: #4ade80;
  }

  #controls-bar {
    width: 100%;
    height: 60px;
    flex-shrink: 0;
    background: #0f172a;
    border-top: 4px solid #090d16;
    padding: 7px 16px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 6px;
    z-index: 25;
  }

  #timeline-wrap {
    position: relative;
    width: 100%;
    height: 12px;
    background: #334155;
    border-radius: 999px;
    cursor: pointer;
    border: 2px solid #090d16;
  }

  #timeline-fill {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #38bdf8, #fbbf24, #ef4444);
    border-radius: 999px;
    pointer-events: none;
  }

  .ctrl-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
  }

  .ctrl-left, .ctrl-right {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .c-btn {
    background: #fbbf24;
    border: 2.5px solid #090d16;
    color: #090d16;
    padding: 4px 11px;
    border-radius: 8px;
    font-family: "Comic Sans MS", sans-serif;
    font-weight: 900;
    font-size: 0.78rem;
    cursor: pointer;
    box-shadow: 2px 2px 0 #090d16;
  }
  .c-btn:hover { background: #fde047; }
  .c-btn:active { transform: translate(1px, 1px); box-shadow: 1px 1px 0 #090d16; }

  #time-display {
    font-family: monospace;
    font-weight: 900;
    font-size: 0.84rem;
    color: #fde047;
  }
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

// ==========================================
// DOG MAN COMIC BOOK ART & INK HELPERS
// ==========================================
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

  const spikes = 14;
  const outerR = 76;
  const innerR = 46;
  ctx.beginPath();
  for (let i = 0; i < spikes * 2; i++) {
    const r = i % 2 === 0 ? outerR : innerR;
    const ang = (i * Math.PI) / spikes;
    const px = Math.cos(ang) * r * 1.48;
    const py = Math.sin(ang) * r * 0.84;
    if (i === 0) ctx.moveTo(px, py);
    else ctx.lineTo(px, py);
  }
  ctx.closePath();
  ctx.fillStyle = fillColor;
  ctx.fill();
  ctx.strokeStyle = INK;
  ctx.lineWidth = 4.5;
  ctx.stroke();

  ctx.fillStyle = textColor;
  ctx.font = '900 18px "Comic Sans MS", sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
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
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText('★ FLIP-O-RAMA! ★', 0, 2);

  // Hand-drawn flip corner arrow
  ctx.fillStyle = '#38bdf8';
  ctx.strokeStyle = INK;
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(190, -14);
  ctx.lineTo(222, 0);
  ctx.lineTo(190, 14);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();
  ctx.restore();
}

// Live Dog-Man-style Comic Speech Bubble with pointer tail!
function drawComicSpeechBubble(cue, anchorX, anchorY) {
  if (!cue) return;
  const words = cue.text.split(' ');
  const lines = [];
  let line = '';
  const maxChars = cue.bubble === 'narrator' ? 68 : 42;

  words.forEach(w => {
    if ((line + ' ' + w).trim().length > maxChars) {
      lines.push(line.trim());
      line = w;
    } else {
      line = (line + ' ' + w).trim();
    }
  });
  if (line) lines.push(line);

  const lineH = 22;
  const boxW = Math.min(620, Math.max(250, maxChars * 9.6 + 44));
  const boxH = lines.length * lineH + 40;

  if (cue.bubble === 'narrator') {
    const nx = (W - boxW) / 2;
    const ny = 24;
    drawComicRect(nx + 5, ny + 5, boxW, boxH, 6, INK, null, 0);
    drawComicRect(nx, ny, boxW, boxH, 6, '#fef08a', INK, 4);
    ctx.fillStyle = '#090d16';
    ctx.font = '900 16px "Comic Sans MS", sans-serif';
    ctx.textAlign = 'center';
    lines.forEach((ln, idx) => {
      ctx.fillText(ln, W / 2, ny + 26 + idx * lineH);
    });
    return;
  }

  const bx = clamp(anchorX - boxW / 2, 24, W - boxW - 24);
  const by = clamp(anchorY - boxH - 34, 22, H - boxH - 120);
  const tailTipX = clamp(anchorX, bx + 35, bx + boxW - 35);
  const tailTipY = Math.min(anchorY - 6, by + boxH + 30);

  // Drop shadow
  drawComicRect(bx + 5, by + 5, boxW, boxH, 22, INK, null, 0);

  if (cue.bubble === 'thought') {
    // Rising thought circles
    [0.33, 0.66].forEach((frac, i) => {
      const cx = lerp(tailTipX, bx + boxW / 2, frac);
      const cy = lerp(tailTipY, by + boxH, frac);
      ctx.fillStyle = '#ffffff';
      ctx.strokeStyle = INK;
      ctx.lineWidth = 3.5;
      ctx.beginPath();
      ctx.arc(cx, cy, 6 + i * 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
    });
    drawComicRect(bx, by, boxW, boxH, 28, '#e0f2fe', INK, 4);
  } else {
    const fill = cue.bubble === 'shout' ? '#fef08a' : '#ffffff';
    drawComicRect(bx, by, boxW, boxH, 22, fill, INK, 4);

    // Comic pointer triangle
    ctx.fillStyle = fill;
    ctx.beginPath();
    ctx.moveTo(tailTipX - 14, by + boxH - 2);
    ctx.lineTo(tailTipX, tailTipY);
    ctx.lineTo(tailTipX + 14, by + boxH - 2);
    ctx.closePath();
    ctx.fill();

    ctx.strokeStyle = INK;
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(tailTipX - 14, by + boxH);
    ctx.lineTo(tailTipX, tailTipY);
    ctx.lineTo(tailTipX + 14, by + boxH);
    ctx.stroke();
  }

  // Speaker Tag Pill
  ctx.fillStyle = cue.role === 'boy' ? '#ef4444' : (cue.role === 'ai' ? '#0284c7' : '#16a34a');
  ctx.font = '900 11px monospace';
  ctx.textAlign = 'left';
  ctx.fillText(cue.speaker.toUpperCase(), bx + 18, by + 17);

  ctx.fillStyle = '#090d16';
  ctx.font = cue.bubble === 'shout' ? '900 16px "Comic Sans MS", sans-serif' : 'bold 15.5px "Comic Sans MS", sans-serif';
  ctx.textAlign = 'center';
  lines.forEach((ln, idx) => {
    ctx.fillText(ln, bx + boxW / 2, by + 38 + idx * lineH);
  });
}

function drawThoughtCloud(cx, cy, w, h, trailStartX, trailStartY, borderColor = '#38bdf8', time = 0) {
  for (let i = 1; i <= 3; i++) {
    const frac = i / 4;
    const bx = lerp(trailStartX, cx, frac) + Math.sin(time * 4 + i) * 4;
    const by = lerp(trailStartY, cy + h * 0.35, frac);
    const br = 7 + i * 4.5;
    ctx.fillStyle = '#ffffff';
    ctx.strokeStyle = INK;
    ctx.lineWidth = 3.5;
    ctx.beginPath();
    ctx.arc(bx, by, br, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
  }

  ctx.save();
  ctx.translate(cx, cy);
  const puffs = [
    [-w * 0.34, -h * 0.18, h * 0.34],
    [0, -h * 0.28, h * 0.38],
    [w * 0.34, -h * 0.18, h * 0.34],
    [w * 0.42, h * 0.12, h * 0.30],
    [w * 0.16, h * 0.26, h * 0.32],
    [-w * 0.16, h * 0.26, h * 0.32],
    [-w * 0.42, h * 0.12, h * 0.30],
  ];

  ctx.fillStyle = INK;
  puffs.forEach(([px, py, pr]) => {
    ctx.beginPath();
    ctx.arc(px, py, pr + 5, 0, Math.PI * 2);
    ctx.fill();
  });

  ctx.fillStyle = borderColor;
  puffs.forEach(([px, py, pr]) => {
    ctx.beginPath();
    ctx.arc(px, py, pr + 1.5, 0, Math.PI * 2);
    ctx.fill();
  });

  ctx.fillStyle = '#ffffff';
  puffs.forEach(([px, py, pr]) => {
    ctx.beginPath();
    ctx.arc(px, py, pr - 3.5, 0, Math.PI * 2);
    ctx.fill();
  });
  ctx.fillRect(-w * 0.32, -h * 0.2, w * 0.64, h * 0.4);
  ctx.restore();
}

function drawCartoonEye(x, y, r, lookX = 2, lookY = 0, mood = 'normal', blink = false) {
  ctx.save();
  ctx.translate(x, y);
  ctx.fillStyle = '#ffffff';
  ctx.strokeStyle = INK;
  ctx.lineWidth = 3;

  if (blink) {
    ctx.beginPath();
    ctx.moveTo(-r, 0);
    ctx.lineTo(r, 0);
    ctx.stroke();
    ctx.restore();
    return;
  }

  ctx.beginPath();
  ctx.ellipse(0, 0, r * 0.88, r * 1.18, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  ctx.fillStyle = '#090d16';
  ctx.beginPath();
  ctx.arc(lookX, lookY, r * 0.44, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = '#ffffff';
  ctx.beginPath();
  ctx.arc(lookX - r * 0.16, lookY - r * 0.2, r * 0.17, 0, Math.PI * 2);
  ctx.fill();

  ctx.strokeStyle = INK;
  ctx.lineWidth = 3.6;
  ctx.lineCap = 'round';
  ctx.beginPath();
  if (mood === 'angry') {
    ctx.moveTo(-r * 0.9, -r * 1.48);
    ctx.lineTo(r * 0.9, -r * 0.92);
  } else if (mood === 'shocked') {
    ctx.moveTo(-r * 0.8, -r * 1.55);
    ctx.quadraticCurveTo(0, -r * 1.98, r * 0.8, -r * 1.55);
  } else {
    ctx.moveTo(-r * 0.8, -r * 1.38);
    ctx.lineTo(r * 0.8, -r * 1.38);
  }
  ctx.stroke();
  ctx.restore();
}

function drawStudent(x, y, scale = 1, shirtColor = '#ec4899', hairColor = '#4c1d95', isGirl = true, time = 0, isSpeaking = false, label = '') {
  ctx.save();
  ctx.translate(x, y);
  const bounce = Math.abs(Math.sin(time * 5 + (isGirl ? 0 : 1.5))) * 3.5;
  ctx.translate(0, -bounce);
  ctx.scale(scale, scale);

  drawComicRect(-22, -74, 44, 52, 12, shirtColor, INK, 3.8);

  ctx.fillStyle = '#fed7aa';
  ctx.strokeStyle = INK;
  ctx.lineWidth = 3.8;
  ctx.beginPath();
  ctx.arc(0, -96, 22, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  ctx.fillStyle = hairColor;
  if (isGirl) {
    ctx.beginPath();
    ctx.arc(-22, -104, 10, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(0, -100, 23, Math.PI * 0.95, Math.PI * 2.05);
    ctx.fill();
    ctx.stroke();
  } else {
    ctx.beginPath();
    ctx.arc(0, -101, 22, Math.PI, 0);
    ctx.fill();
    ctx.stroke();
  }

  drawCartoonEye(-7, -97, 5, 1, 0, 'normal', false);
  drawCartoonEye(7, -97, 5, 1, 0, 'normal', false);

  if (isSpeaking) {
    ctx.fillStyle = '#7f1d1d';
    ctx.beginPath();
    ctx.ellipse(0, -85, 5.5, 2.5 + Math.abs(Math.sin(time * 20)) * 4, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
  } else {
    ctx.strokeStyle = INK;
    ctx.lineWidth = 2.8;
    ctx.beginPath();
    ctx.arc(0, -88, 6, 0.15 * Math.PI, 0.85 * Math.PI);
    ctx.stroke();
  }

  drawComicRect(-44, -24, 88, 46, 8, '#64748b', INK, 3.8);
  drawComicRect(-24, -52, 48, 30, 5, '#38bdf8', INK, 3.2);
  ctx.fillStyle = '#fbbf24';
  ctx.fillRect(-14, -40, 6, 12);
  ctx.fillStyle = '#4ade80';
  ctx.fillRect(-4, -45, 6, 17);
  ctx.fillStyle = '#f43f5e';
  ctx.fillRect(6, -37, 6, 9);

  if (label) {
    drawComicRect(-34, 26, 68, 20, 6, '#fef08a', INK, 2.5);
    ctx.fillStyle = '#090d16';
    ctx.font = '900 11px "Comic Sans MS", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(label, 0, 40);
  }
  ctx.restore();
}

function drawTheBoy(x, y, scale = 1, pose = 'stand', time = 0, facing = 1, nobleGlow = false, isSpeaking = false, mood = 'normal') {
  ctx.save();
  ctx.translate(x, y);

  const bounceFreq = pose === 'run' ? 16 : (pose === 'tiptoe' ? 9 : 4.5);
  const bounceWave = Math.sin(time * bounceFreq);
  const squashY = pose === 'run' ? 1 + bounceWave * 0.08 : 1 + bounceWave * 0.035;
  const stretchX = 1 / Math.sqrt(squashY);
  const hopY = pose === 'run' ? -Math.abs(Math.sin(time * 8)) * 14 : (pose === 'tiptoe' ? -Math.abs(Math.sin(time * 4.5)) * 8 : 0);

  ctx.translate(0, hopY);
  ctx.scale(scale * facing * stretchX, scale * squashY);

  ctx.fillStyle = 'rgba(9, 13, 22, 0.25)';
  ctx.beginPath();
  ctx.ellipse(0, 22 - hopY, 34, 9, 0, 0, Math.PI * 2);
  ctx.fill();

  if (nobleGlow) {
    const g = ctx.createRadialGradient(0, -55, 12, 0, -55, 130);
    g.addColorStop(0, 'rgba(251, 191, 36, 0.72)');
    g.addColorStop(0.6, 'rgba(250, 204, 21, 0.28)');
    g.addColorStop(1, 'rgba(251, 191, 36, 0)');
    ctx.fillStyle = g;
    ctx.beginPath();
    ctx.arc(0, -55, 130, 0, Math.PI * 2);
    ctx.fill();
  }

  const walkSwing = pose === 'run' ? Math.sin(time * 16) * 22 : (pose === 'tiptoe' ? Math.sin(time * 9) * 14 : 0);
  const armSwing = pose === 'attack' ? -42 + Math.sin(time * 20) * 12 : -walkSwing * 0.7;

  ctx.lineCap = 'round';
  [[-9, -12 - walkSwing], [9, 12 + walkSwing]].forEach(([lx, footX]) => {
    ctx.strokeStyle = INK;
    ctx.lineWidth = 18;
    ctx.beginPath(); ctx.moveTo(lx, -34); ctx.lineTo(footX, 14); ctx.stroke();
    ctx.strokeStyle = '#1e3a8a';
    ctx.lineWidth = 10;
    ctx.beginPath(); ctx.moveTo(lx, -34); ctx.lineTo(footX, 14); ctx.stroke();
  });

  drawComicRect(-24 - walkSwing, 9, 24, 13, 6, '#ef4444', INK, 3.5);
  drawComicRect(-22 - walkSwing, 17, 22, 5, 3, '#ffffff', INK, 2.5);
  drawComicRect(2 + walkSwing, 9, 24, 13, 6, '#ef4444', INK, 3.5);
  drawComicRect(4 + walkSwing, 17, 22, 5, 3, '#ffffff', INK, 2.5);

  ctx.strokeStyle = INK;
  ctx.lineWidth = 16;
  ctx.beginPath(); ctx.moveTo(-16, -82); ctx.lineTo(-28 - armSwing * 0.4, -46); ctx.stroke();
  ctx.strokeStyle = '#e11d48';
  ctx.lineWidth = 9;
  ctx.beginPath(); ctx.moveTo(-16, -82); ctx.lineTo(-28 - armSwing * 0.4, -46); ctx.stroke();

  drawComicRect(-25, -94, 50, 62, 16, '#e11d48', INK, 4);
  ctx.strokeStyle = '#ffffff';
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(-6, -88); ctx.lineTo(-6, -66);
  ctx.moveTo(7, -88); ctx.lineTo(7, -66);
  ctx.stroke();

  ctx.fillStyle = '#fed7aa';
  ctx.strokeStyle = INK;
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.arc(0, -120, 27, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  ctx.fillStyle = '#312e81';
  ctx.beginPath();
  ctx.moveTo(-27, -120);
  ctx.lineTo(-33, -138);
  ctx.lineTo(-16, -134);
  ctx.lineTo(-8, -152);
  ctx.lineTo(4, -138);
  ctx.lineTo(18, -150);
  ctx.lineTo(22, -133);
  ctx.lineTo(31, -130);
  ctx.lineTo(25, -116);
  ctx.quadraticCurveTo(0, -130, -27, -120);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();

  const isBlinking = Math.sin(time * 2.7) > 0.97;
  drawCartoonEye(4, -121, 6.5, 2, 0, mood, isBlinking);
  drawCartoonEye(18, -121, 6.5, 2, 0, mood, isBlinking);

  ctx.strokeStyle = '#090d16';
  ctx.lineWidth = 3;
  ctx.strokeRect(-3, -129, 13, 15);
  ctx.strokeRect(12, -129, 13, 15);
  ctx.beginPath(); ctx.moveTo(10, -122); ctx.lineTo(12, -122); ctx.stroke();

  if (mood === 'angry') {
    ctx.strokeStyle = '#ef4444';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(-14, -134); ctx.lineTo(-10, -130); ctx.lineTo(-14, -126);
    ctx.moveTo(-6, -134); ctx.lineTo(-10, -130); ctx.lineTo(-6, -126);
    ctx.stroke();
  }

  if (isSpeaking) {
    const openH = 4 + Math.abs(Math.sin(time * 22)) * 6;
    ctx.fillStyle = '#7f1d1d';
    ctx.strokeStyle = INK;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.ellipse(11, -104, 7, openH, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
  } else if (nobleGlow || mood === 'happy') {
    ctx.fillStyle = '#ffffff';
    ctx.strokeStyle = INK;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(10, -107, 8, 0, Math.PI);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
  } else {
    ctx.strokeStyle = INK;
    ctx.lineWidth = 3.2;
    ctx.beginPath();
    ctx.moveTo(5, -104); ctx.lineTo(17, -106);
    ctx.stroke();
  }

  const handX = pose === 'attack' || pose === 'shield' ? 44 : 26 + armSwing * 0.25;
  const handY = pose === 'attack' || pose === 'shield' ? -84 : -54;
  ctx.strokeStyle = INK;
  ctx.lineWidth = 16;
  ctx.beginPath(); ctx.moveTo(16, -82); ctx.lineTo(handX, handY); ctx.stroke();
  ctx.strokeStyle = '#f43f5e';
  ctx.lineWidth = 9;
  ctx.beginPath(); ctx.moveTo(16, -82); ctx.lineTo(handX, handY); ctx.stroke();

  ctx.save();
  ctx.translate(handX + 10, handY - 8);
  ctx.rotate(pose === 'attack' ? -0.22 : (pose === 'shield' ? 0.0 : 0.14));
  const bookW = pose === 'shield' ? 44 : 36;
  const bookH = pose === 'shield' ? 58 : 44;
  drawComicRect(-bookW / 2, -bookH / 2, bookW, bookH, 6, '#38bdf8', INK, 3.8);
  drawComicRect(-bookW / 2 + 4, -bookH / 2 + 4, bookW - 8, bookH - 8, 4, '#ffffff', INK, 2);
  ctx.fillStyle = '#1d4ed8';
  ctx.font = '900 8px monospace';
  ctx.textAlign = 'center';
  ctx.fillText('SCHOLAR', 0, -4);
  ctx.fillStyle = '#ef4444';
  ctx.fillText('A.P.A.', 0, 8);
  ctx.restore();

  ctx.restore();
}

function drawAIProtagonist(x, y, scale = 1, time = 0, power = 1.0, dead = false, isSpeaking = false) {
  ctx.save();
  ctx.translate(x, y);
  ctx.scale(scale, scale);

  if (dead) {
    ctx.fillStyle = '#64748b';
    ctx.strokeStyle = INK;
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.ellipse(0, 6, 36, 16, 0.12, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    ctx.strokeStyle = '#ef4444';
    ctx.lineWidth = 3.5;
    [-12, 12].forEach(ex => {
      ctx.beginPath();
      ctx.moveTo(ex - 5, 0); ctx.lineTo(ex + 5, 10);
      ctx.moveTo(ex + 5, 0); ctx.lineTo(ex - 5, 10);
      ctx.stroke();
    });

    for (let s = 0; s < 3; s++) {
      const ang = time * 4 + (s * Math.PI * 2) / 3;
      const sx = Math.cos(ang) * 28;
      const sy = -24 + Math.sin(ang) * 8;
      ctx.fillStyle = '#fbbf24';
      ctx.beginPath();
      ctx.arc(sx, sy, 4.5, 0, Math.PI * 2);
      ctx.fill();
    }

    drawComicRect(-56, 24, 112, 22, 6, '#fee2e2', INK, 2.5);
    ctx.fillStyle = '#dc2626';
    ctx.font = '900 12px "Comic Sans MS", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Zzz... OFFLINE', 0, 39);
    ctx.restore();
    return;
  }

  const hover = Math.sin(time * 4.5) * 10;
  const squash = 1 + Math.sin(time * 9) * 0.05;
  ctx.translate(0, hover);
  ctx.scale(1 / squash, squash);

  const pulseBoost = isSpeaking ? 1 + Math.abs(Math.sin(time * 20)) * 0.22 : 1;
  const radius = 64 * power * pulseBoost;
  const aura = ctx.createRadialGradient(0, 0, 10, 0, 0, radius);
  aura.addColorStop(0, 'rgba(56, 189, 248, 0.85)');
  aura.addColorStop(0.55, 'rgba(192, 132, 252, 0.42)');
  aura.addColorStop(1, 'rgba(56, 189, 248, 0)');
  ctx.fillStyle = aura;
  ctx.beginPath();
  ctx.arc(0, 0, radius, 0, Math.PI * 2);
  ctx.fill();

  [time * 2.0, -time * 2.4].forEach((rot, idx) => {
    ctx.save();
    ctx.rotate(rot + (idx * Math.PI) / 3);
    ctx.strokeStyle = INK;
    ctx.lineWidth = 6.5;
    ctx.beginPath();
    ctx.ellipse(0, 0, 48, 18, 0, 0, Math.PI * 2);
    ctx.stroke();

    ctx.strokeStyle = idx === 0 ? '#38bdf8' : '#e879f9';
    ctx.lineWidth = 3.5;
    ctx.beginPath();
    ctx.ellipse(0, 0, 48, 18, 0, 0, Math.PI * 2);
    ctx.stroke();
    ctx.restore();
  });

  ctx.fillStyle = '#ffffff';
  ctx.strokeStyle = INK;
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(0, -38 * pulseBoost);
  ctx.quadraticCurveTo(9, -9, 38 * pulseBoost, 0);
  ctx.quadraticCurveTo(9, 9, 0, 38 * pulseBoost);
  ctx.quadraticCurveTo(-9, 9, -38 * pulseBoost, 0);
  ctx.quadraticCurveTo(-9, -9, 0, -38 * pulseBoost);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();

  drawCartoonEye(-9, -4, 4.5, -1, 0, 'normal', false);
  drawCartoonEye(9, -4, 4.5, -1, 0, 'normal', false);

  if (isSpeaking) {
    ctx.fillStyle = '#0284c7';
    ctx.beginPath();
    ctx.ellipse(0, 8, 6, 3 + Math.abs(Math.sin(time * 22)) * 4, 0, 0, Math.PI * 2);
    ctx.fill();
  } else {
    ctx.strokeStyle = INK;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(0, 5, 6, 0.15 * Math.PI, 0.85 * Math.PI);
    ctx.stroke();
  }

  ctx.restore();
}

function drawTeacher(x, y, time = 0, isSpeaking = false) {
  ctx.save();
  ctx.translate(x, y);

  drawComicRect(-62, -22, 124, 52, 8, '#92400e', INK, 4);
  drawComicRect(-24, -84, 48, 62, 14, '#475569', INK, 4);

  ctx.fillStyle = '#f59e0b';
  ctx.strokeStyle = INK;
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  ctx.moveTo(0, -76); ctx.lineTo(-6, -42); ctx.lineTo(0, -34); ctx.lineTo(6, -42);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();

  ctx.fillStyle = '#fed7aa';
  ctx.strokeStyle = INK;
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.arc(0, -106, 23, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  drawCartoonEye(-8, -108, 5, 0, 1, 'normal', true);
  drawCartoonEye(8, -108, 5, 0, 1, 'normal', true);

  if (isSpeaking) {
    ctx.fillStyle = '#7f1d1d';
    ctx.beginPath();
    ctx.ellipse(0, -94, 6, 2.5 + Math.abs(Math.sin(time * 18)) * 4, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
  } else {
    ctx.strokeStyle = INK;
    ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(-6, -94); ctx.lineTo(6, -94); ctx.stroke();
  }

  drawComicRect(26, -46, 22, 24, 5, '#facc15', INK, 3.5);
  drawComicRect(-68, 34, 136, 22, 6, '#fef08a', INK, 2.5);
  ctx.fillStyle = '#090d16';
  ctx.font = '900 11px "Comic Sans MS", sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('BUSINESS TEACHER', 0, 49);
  ctx.restore();
}

function drawSaviors(x, y, time = 0, speakingRole = '') {
  ctx.save();
  ctx.translate(x, y);

  const beam = ctx.createLinearGradient(0, -380, 0, 65);
  beam.addColorStop(0, 'rgba(251, 191, 36, 0.12)');
  beam.addColorStop(0.5, 'rgba(251, 191, 36, 0.42)');
  beam.addColorStop(1, 'rgba(251, 191, 36, 0.04)');
  ctx.fillStyle = beam;
  ctx.beginPath();
  ctx.moveTo(-105, -380);
  ctx.lineTo(105, -380);
  ctx.lineTo(165, 65);
  ctx.lineTo(-165, 65);
  ctx.closePath();
  ctx.fill();

  // MR. R (LORD & SAVIOR)
  ctx.save();
  const rBounce = Math.abs(Math.sin(time * 5)) * 5;
  ctx.translate(-42, -rBounce);

  ctx.strokeStyle = INK; ctx.lineWidth = 8;
  ctx.beginPath(); ctx.ellipse(0, -154, 26, 7, 0, 0, Math.PI * 2); ctx.stroke();
  ctx.strokeStyle = '#fde047'; ctx.lineWidth = 4.5;
  ctx.beginPath(); ctx.ellipse(0, -154, 26, 7, 0, 0, Math.PI * 2); ctx.stroke();

  ctx.strokeStyle = INK; ctx.lineWidth = 18; ctx.lineCap = 'round';
  ctx.beginPath(); ctx.moveTo(-11, -28); ctx.lineTo(-11, 20); ctx.moveTo(11, -28); ctx.lineTo(11, 20); ctx.stroke();
  ctx.strokeStyle = '#0f172a'; ctx.lineWidth = 10;
  ctx.beginPath(); ctx.moveTo(-11, -28); ctx.lineTo(-11, 20); ctx.moveTo(11, -28); ctx.lineTo(11, 20); ctx.stroke();

  drawComicRect(-27, -98, 54, 72, 14, '#1d4ed8', INK, 4);
  drawComicRect(-10, -92, 20, 60, 6, '#fbbf24', INK, 2.5);

  ctx.fillStyle = '#fed7aa'; ctx.strokeStyle = INK; ctx.lineWidth = 4;
  ctx.beginPath(); ctx.arc(0, -122, 24, 0, Math.PI * 2); ctx.fill(); ctx.stroke();

  drawCartoonEye(-8, -124, 5.5, 1, 0, 'normal', false);
  drawCartoonEye(8, -124, 5.5, 1, 0, 'normal', false);

  if (speakingRole === 'mrr') {
    ctx.fillStyle = '#7f1d1d';
    ctx.beginPath();
    ctx.ellipse(0, -110, 7, 3 + Math.abs(Math.sin(time * 20)) * 5, 0, 0, Math.PI * 2);
    ctx.fill(); ctx.stroke();
  } else {
    ctx.strokeStyle = INK; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.arc(0, -114, 9, 0.15 * Math.PI, 0.85 * Math.PI); ctx.stroke();
  }

  ctx.strokeStyle = INK; ctx.lineWidth = 13;
  ctx.beginPath(); ctx.moveTo(22, -76); ctx.lineTo(58, -96 + Math.sin(time * 12) * 8); ctx.stroke();
  ctx.strokeStyle = '#fbbf24'; ctx.lineWidth = 6.5;
  ctx.beginPath(); ctx.moveTo(22, -76); ctx.lineTo(58, -96 + Math.sin(time * 12) * 8); ctx.stroke();

  drawComicRect(-82, 26, 164, 22, 6, '#fef08a', INK, 2.5);
  ctx.fillStyle = '#090d16';
  ctx.font = '900 11px "Comic Sans MS", sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('MR. R (LORD & SAVIOR)', 0, 41);
  ctx.restore();

  // ANAY GUPTA
  ctx.save();
  const aBounce = Math.abs(Math.cos(time * 6)) * 5;
  ctx.translate(64, 8 - aBounce);

  ctx.strokeStyle = INK; ctx.lineWidth = 16; ctx.lineCap = 'round';
  ctx.beginPath(); ctx.moveTo(-9, -28); ctx.lineTo(-9, 12); ctx.moveTo(9, -28); ctx.lineTo(9, 12); ctx.stroke();
  ctx.strokeStyle = '#1e293b'; ctx.lineWidth = 9;
  ctx.beginPath(); ctx.moveTo(-9, -28); ctx.lineTo(-9, 12); ctx.moveTo(9, -28); ctx.lineTo(9, 12); ctx.stroke();

  drawComicRect(-22, -88, 44, 60, 12, '#0284c7', INK, 4);
  ctx.fillStyle = '#fed7aa'; ctx.strokeStyle = INK; ctx.lineWidth = 4;
  ctx.beginPath(); ctx.arc(0, -110, 22, 0, Math.PI * 2); ctx.fill(); ctx.stroke();

  ctx.fillStyle = '#090d16';
  ctx.beginPath(); ctx.arc(0, -116, 22, Math.PI, 0); ctx.fill();

  drawCartoonEye(-7, -111, 5, -1, 0, 'normal', false);
  drawCartoonEye(7, -111, 5, -1, 0, 'normal', false);

  if (speakingRole === 'anay') {
    ctx.fillStyle = '#7f1d1d';
    ctx.beginPath();
    ctx.ellipse(0, -99, 6, 2.5 + Math.abs(Math.sin(time * 20)) * 4.5, 0, 0, Math.PI * 2);
    ctx.fill(); ctx.stroke();
  } else {
    ctx.strokeStyle = INK; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.arc(0, -103, 7, 0.15 * Math.PI, 0.85 * Math.PI); ctx.stroke();
  }

  ctx.strokeStyle = INK; ctx.lineWidth = 12;
  ctx.beginPath(); ctx.moveTo(-16, -66); ctx.lineTo(-50, -78); ctx.stroke();
  ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 5.5;
  ctx.beginPath(); ctx.moveTo(-16, -66); ctx.lineTo(-50, -78); ctx.stroke();

  drawComicRect(-48, 18, 96, 22, 6, '#e0f2fe', INK, 2.5);
  ctx.fillStyle = '#090d16';
  ctx.font = '900 11px "Comic Sans MS", sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('ANAY GUPTA', 0, 33);
  ctx.restore();

  ctx.restore();
}
"""
