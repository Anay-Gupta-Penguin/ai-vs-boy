MOVIE_JS_PART1 = r"""
const canvas = document.getElementById('movie-canvas');
const ctx = canvas.getContext('2d');
const W = 1280, H = 720, DURATION = 390.0, INK = '#090d16';

function clamp(v, min, max) { return Math.max(min, Math.min(max, v)); }
function lerp(a, b, t) { return a + (b - a) * clamp(t, 0, 1); }
function smoothstep(e0, e1, x) { const t = clamp((x - e0) / (e1 - e0), 0, 1); return t * t * (3 - 2 * t); }

function drawHalftonePaper(bgColor, dotColor) {
  ctx.fillStyle = bgColor; ctx.fillRect(0, 0, W, H);
  ctx.fillStyle = dotColor;
  for (let y = 16; y < H; y += 28) {
    const off = ((y / 28) % 2) * 14;
    for (let x = 16 + off; x < W; x += 28) { ctx.beginPath(); ctx.arc(x, y, 2.3, 0, Math.PI * 2); ctx.fill(); }
  }
}

function drawComicRect(x, y, w, h, r, fill, stroke, lw = 3.5) {
  const rad = Math.min(r, w / 2, h / 2);
  ctx.beginPath();
  ctx.moveTo(x + rad, y); ctx.arcTo(x + w, y, x + w, y + h, rad); ctx.arcTo(x + w, y + h, x, y + h, rad);
  ctx.arcTo(x, y + h, x, y, rad); ctx.arcTo(x, y, x + w, y, rad); ctx.closePath();
  if (fill) { ctx.fillStyle = fill; ctx.fill(); }
  if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = lw; ctx.stroke(); }
}

function drawCartoonEye(x, y, r, px = 0, py = 0, mood = 'normal', blink = false) {
  ctx.save();
  if (blink) {
    ctx.strokeStyle = INK; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(x - r, y); ctx.lineTo(x + r, y); ctx.stroke(); ctx.restore(); return;
  }
  ctx.fillStyle = '#fff'; ctx.strokeStyle = INK; ctx.lineWidth = 2.5;
  ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  ctx.fillStyle = INK; ctx.beginPath(); ctx.arc(x + px, y + py, r * 0.48, 0, Math.PI * 2); ctx.fill();
  if (mood === 'angry') {
    ctx.strokeStyle = INK; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(x - r, y - r - 2); ctx.lineTo(x + r, y - r + 3); ctx.stroke();
  }
  ctx.restore();
}

function drawCartoonBurst(x, y, text, bgColor, textColor, scale = 1, angle = 0) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(angle); ctx.scale(scale, scale);
  ctx.beginPath();
  for (let i = 0; i < 32; i++) {
    const rad = i % 2 === 0 ? 128 : 88, a = (i * Math.PI) / 16;
    const vx = Math.cos(a) * rad * 1.45, vy = Math.sin(a) * rad * 0.72;
    if (i === 0) ctx.moveTo(vx, vy); else ctx.lineTo(vx, vy);
  }
  ctx.closePath(); ctx.fillStyle = bgColor; ctx.fill(); ctx.strokeStyle = INK; ctx.lineWidth = 5; ctx.stroke();
  ctx.fillStyle = textColor; ctx.font = '900 28px "Comic Sans MS", sans-serif';
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(text, 0, 0);
  ctx.restore();
}

function drawTheBoy(x, y, scale = 1, pose = 'stand', time = 0, facing = 1, hasCrown = false, isSpeaking = false, mood = 'normal') {
  ctx.save(); ctx.translate(x, y);
  const bob = pose === 'tiptoe' ? Math.abs(Math.sin(time * 7)) * -6 : Math.sin(time * 3) * 1.5;
  ctx.translate(0, bob); ctx.scale(scale * facing, scale);
  const step = pose === 'tiptoe' ? Math.sin(time * 7) * 12 : 0; ctx.lineCap = 'round';
  [[-9, -8 - step], [9, 8 + step]].forEach(([lx, fx]) => {
    ctx.strokeStyle = INK; ctx.lineWidth = 15; ctx.beginPath(); ctx.moveTo(lx, -26); ctx.lineTo(fx, 16); ctx.stroke();
    ctx.strokeStyle = '#1e3a8a'; ctx.lineWidth = 8; ctx.beginPath(); ctx.moveTo(lx, -26); ctx.lineTo(fx, 16); ctx.stroke();
  });
  drawComicRect(-22, -82, 44, 58, 12, '#dc2626', INK, 3.8);
  ctx.fillStyle = '#fed7aa'; ctx.strokeStyle = INK; ctx.lineWidth = 3.8;
  ctx.beginPath(); ctx.arc(0, -104, 22, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  ctx.fillStyle = '#451a03'; ctx.beginPath(); ctx.arc(0, -109, 23, Math.PI, Math.PI * 2); ctx.fill(); ctx.stroke();
  if (hasCrown) {
    ctx.fillStyle = '#fbbf24'; ctx.strokeStyle = INK; ctx.lineWidth = 3; ctx.beginPath();
    ctx.moveTo(-16, -126); ctx.lineTo(-18, -144); ctx.lineTo(-6, -133); ctx.lineTo(0, -148);
    ctx.lineTo(6, -133); ctx.lineTo(18, -144); ctx.lineTo(16, -126); ctx.closePath(); ctx.fill(); ctx.stroke();
  }
  drawCartoonEye(4, -104, 5, 1.5, 0, mood, false); drawCartoonEye(15, -104, 5, 1.5, 0, mood, false);
  drawComicRect(-2, -110, 11, 11, 2, null, INK, 2.2); drawComicRect(10, -110, 11, 11, 2, null, INK, 2.2);
  if (isSpeaking) {
    ctx.fillStyle = '#7f1d1d'; ctx.beginPath();
    ctx.ellipse(9, -90, 5.5, 3 + Math.abs(Math.sin(time * 18)) * 3.5, 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  } else {
    ctx.strokeStyle = INK; ctx.lineWidth = 2.8; ctx.beginPath();
    if (mood === 'happy') ctx.arc(9, -93, 6, 0.1 * Math.PI, 0.9 * Math.PI); else { ctx.moveTo(4, -90); ctx.lineTo(14, -90); }
    ctx.stroke();
  }
  drawComicRect(10, -68, 22, 28, 3, '#38bdf8', INK, 3); ctx.restore();
  drawComicRect(x - 46, y + 22, 92, 20, 6, '#e0f2fe', INK, 2.5);
  ctx.fillStyle = INK; ctx.font = '900 11px "Comic Sans MS", sans-serif'; ctx.textAlign = 'center'; ctx.fillText('THE BOY', x, y + 36);
}

function drawAIProtagonist(x, y, scale = 1, time = 0, glowScale = 1.2, isOffline = false, isSpeaking = false) {
  ctx.save(); ctx.translate(x, y + (isOffline ? 0 : Math.sin(time * 3.5) * 8)); ctx.scale(scale, scale);
  if (!isOffline) {
    const grad = ctx.createRadialGradient(0, 0, 12, 0, 0, 68 * glowScale);
    grad.addColorStop(0, 'rgba(56,189,248,0.55)'); grad.addColorStop(1, 'rgba(56,189,248,0)');
    ctx.fillStyle = grad; ctx.beginPath(); ctx.arc(0, 0, 68 * glowScale, 0, Math.PI * 2); ctx.fill();
  }
  ctx.save(); ctx.rotate(isOffline ? 0.2 : time * 1.1); ctx.strokeStyle = isOffline ? '#64748b' : '#fbbf24';
  ctx.lineWidth = 4; ctx.beginPath(); ctx.ellipse(0, 0, 56, 18, 0, 0, Math.PI * 2); ctx.stroke(); ctx.restore();
  ctx.fillStyle = isOffline ? '#475569' : '#38bdf8'; ctx.strokeStyle = INK; ctx.lineWidth = 4.5;
  ctx.beginPath(); ctx.arc(0, 0, 38, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  drawCartoonEye(-11, -4, 6, 0, 0, 'normal', isOffline); drawCartoonEye(11, -4, 6, 0, 0, 'normal', isOffline);
  if (isSpeaking && !isOffline) {
    ctx.fillStyle = '#0284c7'; ctx.beginPath();
    ctx.ellipse(0, 12, 7, 3.5 + Math.abs(Math.sin(time * 18)) * 4, 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  } else {
    ctx.strokeStyle = INK; ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(0, 10, 8, 0.15 * Math.PI, 0.85 * Math.PI); ctx.stroke();
  }
  ctx.restore();
  drawComicRect(x - 52, y + 48 * scale, 104, 20, 6, isOffline ? '#cbd5e1' : '#bae6fd', INK, 2.5);
  ctx.fillStyle = INK; ctx.font = '900 11px "Comic Sans MS", sans-serif'; ctx.textAlign = 'center';
  ctx.fillText(isOffline ? 'GEMINI (OFFLINE)' : 'GEMINI AI', x, y + 48 * scale + 14);
}

function drawStudent(x, y, scale, shirtColor, hairColor, isFemale, time, isSpeaking, label) {
  ctx.save(); ctx.translate(x, y); ctx.scale(scale, scale);
  drawComicRect(-46, -34, 92, 48, 6, '#d97706', INK, 3.5);
  drawComicRect(-26, -58, 52, 26, 4, '#334155', INK, 3);
  drawComicRect(-20, -86, 40, 52, 10, shirtColor, INK, 3.5);
  ctx.fillStyle = '#fed7aa'; ctx.strokeStyle = INK; ctx.lineWidth = 3.5;
  ctx.beginPath(); ctx.arc(0, -106, 20, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  ctx.fillStyle = hairColor; ctx.beginPath(); ctx.arc(0, -110, 21, Math.PI, Math.PI * 2); ctx.fill(); ctx.stroke();
  if (isFemale) { drawComicRect(-22, -110, 8, 26, 4, hairColor, INK, 2.5); drawComicRect(14, -110, 8, 26, 4, hairColor, INK, 2.5); }
  drawCartoonEye(-6, -106, 4.5, 0, 0, 'normal', false); drawCartoonEye(7, -106, 4.5, 0, 0, 'normal', false);
  if (isSpeaking) {
    ctx.fillStyle = '#7f1d1d'; ctx.beginPath();
    ctx.ellipse(0, -94, 5, 2.5 + Math.abs(Math.sin(time * 18)) * 3.5, 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  } else {
    ctx.strokeStyle = INK; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.arc(0, -96, 5.5, 0.1 * Math.PI, 0.9 * Math.PI); ctx.stroke();
  }
  ctx.restore();
  drawComicRect(x - 46, y + 18, 92, 20, 6, '#fff', INK, 2.5);
  ctx.fillStyle = INK; ctx.font = '900 11px "Comic Sans MS", sans-serif'; ctx.textAlign = 'center'; ctx.fillText(label, x, y + 32);
}

function drawSaviors(x, y, time, speakingRole) {
  const mrx = x - 45, anx = x + 65;
  ctx.save(); ctx.translate(mrx, y);
  ctx.fillStyle = '#ef4444'; ctx.strokeStyle = INK; ctx.lineWidth = 3.5; ctx.beginPath();
  ctx.moveTo(-22, -82); ctx.lineTo(-42, 10); ctx.lineTo(36, 10); ctx.lineTo(22, -82); ctx.closePath(); ctx.fill(); ctx.stroke();
  drawComicRect(-22, -84, 44, 62, 12, '#1e293b', INK, 3.8);
  ctx.fillStyle = '#fbbf24'; ctx.font = '900 16px "Comic Sans MS", sans-serif'; ctx.textAlign = 'center'; ctx.fillText('MR. R', 0, -48);
  ctx.fillStyle = '#fed7aa'; ctx.strokeStyle = INK; ctx.lineWidth = 3.8;
  ctx.beginPath(); ctx.arc(0, -106, 22, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  ctx.strokeStyle = '#fbbf24'; ctx.lineWidth = 4.5; ctx.beginPath(); ctx.ellipse(0, -136, 20, 6, 0, 0, Math.PI * 2); ctx.stroke();
  drawCartoonEye(-6, -106, 5, 0, 0, 'normal', false); drawCartoonEye(7, -106, 5, 0, 0, 'normal', false);
  ctx.restore();
  drawComicRect(mrx - 52, y + 18, 104, 20, 6, '#fef08a', INK, 2.5);
  ctx.fillStyle = INK; ctx.font = '900 10px "Comic Sans MS", sans-serif'; ctx.textAlign = 'center'; ctx.fillText('MR. R (SAVIOR)', mrx, y + 32);

  ctx.save(); ctx.translate(anx, y);
  drawComicRect(-20, -80, 40, 58, 10, '#0284c7', INK, 3.8);
  ctx.fillStyle = '#fed7aa'; ctx.strokeStyle = INK; ctx.lineWidth = 3.8;
  ctx.beginPath(); ctx.arc(0, -102, 20, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  ctx.fillStyle = INK; ctx.beginPath(); ctx.arc(0, -106, 21, Math.PI, Math.PI * 2); ctx.fill(); ctx.stroke();
  drawCartoonEye(-6, -102, 4.5, 0, 0, 'normal', false); drawCartoonEye(7, -102, 4.5, 0, 0, 'normal', false);
  ctx.restore();
  drawComicRect(anx - 48, y + 18, 96, 20, 6, '#bae6fd', INK, 2.5);
  ctx.fillStyle = INK; ctx.font = '900 10px "Comic Sans MS", sans-serif'; ctx.textAlign = 'center'; ctx.fillText('ANAY GUPTA', anx, y + 32);
}

function drawComicSpeechBubble(cue, speakerX, speakerY) {
  ctx.save();
  const isNarrator = cue.bubble === 'narrator', isThought = cue.bubble === 'thought', isShout = cue.bubble === 'shout';
  const maxW = isNarrator ? 860 : 500;
  ctx.font = 'bold 17px "Comic Sans MS", sans-serif';
  const words = cue.text.split(' '), lines = []; let line = '';
  for (let i = 0; i < words.length; i++) {
    const test = line ? line + ' ' + words[i] : words[i];
    if (ctx.measureText(test).width > maxW - 36) { lines.push(line); line = words[i]; } else { line = test; }
  }
  if (line) lines.push(line);
  const boxW = maxW, boxH = 38 + lines.length * 23;
  const bx = isNarrator ? (W - boxW) / 2 : clamp(speakerX - boxW / 2, 24, W - boxW - 24);
  const by = isNarrator ? 28 : clamp(speakerY - boxH - 28, 22, H - boxH - 95);
  const bg = isNarrator ? '#fef08a' : (isShout ? '#fee2e2' : '#fff');
  drawComicRect(bx, by, boxW, boxH, isNarrator ? 8 : 18, bg, INK, 4);
  if (!isNarrator) {
    const tx = clamp(speakerX, bx + 30, bx + boxW - 30);
    if (isThought) {
      [0, 1].forEach(d => {
        ctx.fillStyle = '#fff'; ctx.strokeStyle = INK; ctx.lineWidth = 3;
        ctx.beginPath(); ctx.arc(tx, by + boxH + 10 + d * 12, 6 - d * 2, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      });
    } else {
      ctx.fillStyle = bg; ctx.strokeStyle = INK; ctx.lineWidth = 3.5; ctx.beginPath();
      ctx.moveTo(tx - 10, by + boxH - 2); ctx.lineTo(tx, by + boxH + 18); ctx.lineTo(tx + 12, by + boxH - 2);
      ctx.closePath(); ctx.fill(); ctx.stroke();
    }
  }
  ctx.fillStyle = '#0284c7'; ctx.font = '900 13px "Comic Sans MS", sans-serif'; ctx.textAlign = 'left';
  ctx.fillText(cue.speaker.toUpperCase(), bx + 18, by + 22);
  ctx.fillStyle = INK; ctx.font = 'bold 16px "Comic Sans MS", sans-serif';
  lines.forEach((ln, idx) => ctx.fillText(ln, bx + 18, by + 44 + idx * 22));
  ctx.restore();
}
"""
