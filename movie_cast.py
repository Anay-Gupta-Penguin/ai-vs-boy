MOVIE_JS_PART1 = r"""
const canvas = document.getElementById('movie-canvas');
const ctx = canvas.getContext('2d');
const W = 1280;
const H = 720;
const DURATION = 390.0;
const INK = '#090d16';

function clamp(v, min, max) {
  return Math.max(min, Math.min(max, v));
}

function lerp(a, b, t) {
  return a + (b - a) * clamp(t, 0, 1);
}

function smoothstep(e0, e1, x) {
  const t = clamp((x - e0) / (e1 - e0), 0, 1);
  return t * t * (3 - 2 * t);
}

function drawHalftonePaper(bgColor, dotColor) {
  ctx.fillStyle = bgColor;
  ctx.fillRect(0, 0, W, H);
  ctx.fillStyle = dotColor;
  for (let y = 16; y < H; y += 28) {
    const offset = ((y / 28) % 2) * 14;
    for (let x = 16 + offset; x < W; x += 28) {
      ctx.beginPath();
      ctx.arc(x, y, 2.3, 0, Math.PI * 2);
      ctx.fill();
    }
  }
}

function drawComicRect(x, y, w, h, r, fill, stroke, lineWidth = 3.5) {
  const rad = Math.min(r, w / 2, h / 2);
  ctx.beginPath();
  ctx.moveTo(x + rad, y);
  ctx.arcTo(x + w, y, x + w, y + h, rad);
  ctx.arcTo(x + w, y + h, x, y + h, rad);
  ctx.arcTo(x, y + h, x, y, rad);
  ctx.arcTo(x, y, x + w, y, rad);
  ctx.closePath();
  if (fill) {
    ctx.fillStyle = fill;
    ctx.fill();
  }
  if (stroke) {
    ctx.strokeStyle = stroke;
    ctx.lineWidth = lineWidth;
    ctx.stroke();
  }
}

function drawCartoonEye(x, y, r, px = 0, py = 0, mood = 'normal', blink = false) {
  ctx.save();
  if (blink) {
    ctx.strokeStyle = INK;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(x - r, y);
    ctx.lineTo(x + r, y);
    ctx.stroke();
    ctx.restore();
    return;
  }
  ctx.fillStyle = '#ffffff';
  ctx.strokeStyle = INK;
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  ctx.arc(x, y, r, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  ctx.fillStyle = INK;
  ctx.beginPath();
  ctx.arc(x + px, y + py, r * 0.48, 0, Math.PI * 2);
  ctx.fill();

  if (mood === 'angry') {
    ctx.strokeStyle = INK;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(x - r, y - r - 2);
    ctx.lineTo(x + r, y - r + 3);
    ctx.stroke();
  }
  ctx.restore();
}

function drawCartoonBurst(x, y, text, bgColor, textColor, scale = 1, angle = 0) {
  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(angle);
  ctx.scale(scale, scale);

  const spikes = 16;
  const outerR = 128;
  const innerR = 88;
  ctx.beginPath();
  for (let i = 0; i < spikes * 2; i++) {
    const rad = i % 2 === 0 ? outerR : innerR;
    const a = (i * Math.PI) / spikes;
    const vx = Math.cos(a) * rad * 1.45;
    const vy = Math.sin(a) * rad * 0.72;
    if (i === 0) ctx.moveTo(vx, vy);
    else ctx.lineTo(vx, vy);
  }
  ctx.closePath();
  ctx.fillStyle = bgColor;
  ctx.fill();
  ctx.strokeStyle = INK;
  ctx.lineWidth = 5;
  ctx.stroke();

  ctx.fillStyle = textColor;
  ctx.font = '900 28px "Comic Sans MS", sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(text, 0, 0);
  ctx.restore();
}

function drawTheBoy(x, y, scale = 1, pose = 'stand', time = 0, facing = 1, hasCrown = false, isSpeaking = false, mood = 'normal') {
  ctx.save();
  ctx.translate(x, y);
  const bob = pose === 'tiptoe' ? Math.abs(Math.sin(time * 7)) * -6 : Math.sin(time * 3) * 1.5;
  ctx.translate(0, bob);
  ctx.scale(scale * facing, scale);

  const step = pose === 'tiptoe' ? Math.sin(time * 7) * 12 : 0;
  ctx.lineCap = 'round';
  [[-9, -8 - step], [9, 8 + step]].forEach(([lx, fx]) => {
    ctx.strokeStyle = INK; ctx.lineWidth = 15;
    ctx.beginPath(); ctx.moveTo(lx, -26); ctx.lineTo(fx, 16); ctx.stroke();
    ctx.strokeStyle = '#1e3a8a'; ctx.lineWidth = 8;
    ctx.beginPath(); ctx.moveTo(lx, -26); ctx.lineTo(fx, 16); ctx.stroke();
  });

  drawComicRect(-22, -82, 44, 58, 12, '#dc2626', INK, 3.8);
  ctx.strokeStyle = '#fef08a'; ctx.lineWidth = 3;
  ctx.beginPath(); ctx.moveTo(-10, -82); ctx.lineTo(-10, -28); ctx.stroke();

  ctx.fillStyle = '#fed7aa'; ctx.strokeStyle = INK; ctx.lineWidth = 3.8;
  ctx.beginPath(); ctx.arc(0, -104, 22, 0, Math.PI * 2); ctx.fill(); ctx.stroke();

  ctx.fillStyle = '#451a03';
  ctx.beginPath();
  ctx.arc(0, -109, 23, Math.PI, Math.PI * 2);
  ctx.fill(); ctx.stroke();

  if (hasCrown) {
    ctx.fillStyle = '#fbbf24'; ctx.strokeStyle = INK; ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(-16, -126); ctx.lineTo(-18, -144); ctx.lineTo(-6, -133);
    ctx.lineTo(0, -148); ctx.lineTo(6, -133); ctx.lineTo(18, -144);
    ctx.lineTo(16, -126); ctx.closePath();
    ctx.fill(); ctx.stroke();
  }

  drawCartoonEye(4, -104, 5, 1.5, 0, mood, false);
  drawCartoonEye(15, -104, 5, 1.5, 0, mood, false);
  drawComicRect(-2, -110, 11, 11, 2, null, INK, 2.2);
  drawComicRect(10, -110, 11, 11, 2, null, INK, 2.2);

  if (isSpeaking) {
    ctx.fillStyle = '#7f1d1d';
    ctx.beginPath(); ctx.ellipse(9, -90, 5.5, 3 + Math.abs(Math.sin(time * 18)) * 3.5, 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  } else if (mood === 'happy') {
    ctx.strokeStyle = INK; ctx.lineWidth = 2.8;
    ctx.beginPath(); ctx.arc(9, -93, 6, 0.1 * Math.PI, 0.9 * Math.PI); ctx.stroke();
  } else {
    ctx.strokeStyle = INK; ctx.lineWidth = 2.8;
    ctx.beginPath(); ctx.moveTo(4, -90); ctx.lineTo(14, -90); ctx.stroke();
  }

  drawComicRect(10, -68, 22, 28, 3, '#38bdf8', INK, 3);
  ctx.restore();

  drawComicRect(x - 46, y + 22, 92, 20, 6, '#e0f2fe', INK, 2.5);
  ctx.fillStyle = INK;
  ctx.font = '900 11px "Comic Sans MS", sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('THE BOY', x, y + 36);
}

function drawAIProtagonist(x, y, scale = 1, time = 0, glowScale = 1.2, isOffline = false, isSpeaking = false) {
  ctx.save();
  const hover = isOffline ? 0 : Math.sin(time * 3.5) * 8;
  ctx.translate(x, y + hover);
  ctx.scale(scale, scale);

  if (!isOffline) {
    const grad = ctx.createRadialGradient(0, 0, 12, 0, 0, 68 * glowScale);
    grad.addColorStop(0, 'rgba(56, 189, 248, 0.55)');
    grad.addColorStop(0.6, 'rgba(168, 85, 247, 0.22)');
    grad.addColorStop(1, 'rgba(56, 189, 248, 0)');
    ctx.fillStyle = grad;
    ctx.beginPath(); ctx.arc(0, 0, 68 * glowScale, 0, Math.PI * 2); ctx.fill();
  }

  ctx.save();
  ctx.rotate(isOffline ? 0.2 : time * 1.1);
  ctx.strokeStyle = isOffline ? '#64748b' : '#fbbf24';
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.ellipse(0, 0, 56, 18, 0, 0, Math.PI * 2);
  ctx.stroke();
  ctx.restore();

  ctx.fillStyle = isOffline ? '#475569' : '#38bdf8';
  ctx.strokeStyle = INK;
  ctx.lineWidth = 4.5;
  ctx.beginPath(); ctx.arc(0, 0, 38, 0, Math.PI * 2); ctx.fill(); ctx.stroke();

  ctx.fillStyle = isOffline ? '#94a3b8' : '#ffffff';
  ctx.beginPath();
  ctx.moveTo(0, -24); ctx.quadraticCurveTo(5, -5, 24, 0);
  ctx.quadraticCurveTo(5, 5, 0, 24); ctx.quadraticCurveTo(-5, 5, -24, 0);
  ctx.quadraticCurveTo(-5, -5, 0, -24); ctx.closePath();
  ctx.fill();

  drawCartoonEye(-11, -4, 6, 0, 0, 'normal', isOffline);
  drawCartoonEye(11, -4, 6, 0, 0, 'normal', isOffline);

  if (isSpeaking && !isOffline) {
    ctx.fillStyle = '#0284c7';
    ctx.beginPath(); ctx.ellipse(0, 12, 7, 3.5 + Math.abs(Math.sin(time * 18)) * 4, 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  } else {
    ctx.strokeStyle = INK; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.arc(0, 10, 8, 0.15 * Math.PI, 0.85 * Math.PI); ctx.stroke();
  }
  ctx.restore();

  drawComicRect(x -
