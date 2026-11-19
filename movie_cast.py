MOVIE_CAST_JS = r"""
function drawStudent(x, y, scale = 1, shirtColor = '#ec4899', hairColor = '#4c1d95', isGirl = true, time = 0, isSpeaking = false, label = '') {
  ctx.save(); ctx.translate(x, y);
  const bounce = Math.abs(Math.sin(time * 5 + (isGirl ? 0 : 1.5))) * 3.5;
  ctx.translate(0, -bounce); ctx.scale(scale, scale);

  drawComicRect(-22, -74, 44, 52, 12, shirtColor, INK, 3.8);
  ctx.fillStyle = '#fed7aa'; ctx.strokeStyle = INK; ctx.lineWidth = 3.8;
  ctx.beginPath(); ctx.arc(0, -96, 22, 0, Math.PI * 2); ctx.fill(); ctx.stroke();

  ctx.fillStyle = hairColor;
  if (isGirl) {
    ctx.beginPath(); ctx.arc(-22, -104, 10, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
    ctx.beginPath(); ctx.arc(0, -100, 23, Math.PI * 0.95, Math.PI * 2.05); ctx.fill(); ctx.stroke();
  } else {
    ctx.beginPath(); ctx.arc(0, -101, 22, Math.PI, 0); ctx.fill(); ctx.stroke();
  }

  drawCartoonEye(-7, -97, 5, 1, 0, 'normal', false);
  drawCartoonEye(7, -97, 5, 1, 0, 'normal', false);

  if (isSpeaking) {
    ctx.fillStyle = '#7f1d1d';
    ctx.beginPath(); ctx.ellipse(0, -85, 5.5, 2.5 + Math.abs(Math.sin(time * 20)) * 4, 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  } else {
    ctx.strokeStyle = INK; ctx.lineWidth = 2.8;
    ctx.beginPath(); ctx.arc(0, -88, 6, 0.15 * Math.PI, 0.85 * Math.PI); ctx.stroke();
  }

  drawComicRect(-44, -24, 88, 46, 8, '#64748b', INK, 3.8);
  drawComicRect(-24, -52, 48, 30, 5, '#38bdf8', INK, 3.2);
  ctx.fillStyle = '#fbbf24'; ctx.fillRect(-14, -40, 6, 12);
  ctx.fillStyle = '#4ade80'; ctx.fillRect(-4, -45, 6, 17);
  ctx.fillStyle = '#f43f5e'; ctx.fillRect(6, -37, 6, 9);

  if (label) {
    drawComicRect(-34, 26, 68, 20, 6, '#fef08a', INK, 2.5);
    ctx.fillStyle = '#090d16'; ctx.font = '900 11px "Comic Sans MS", sans-serif'; ctx.textAlign = 'center';
    ctx.fillText(label, 0, 40);
  }
  ctx.restore();
}

function drawTheBoy(x, y, scale = 1, pose = 'stand', time = 0, facing = 1, nobleGlow = false, isSpeaking = false, mood = 'normal') {
  ctx.save(); ctx.translate(x, y);
  const bounceFreq = pose === 'run' ? 16 : (pose === 'tiptoe' ? 9 : 4.5);
  const bounceWave = Math.sin(time * bounceFreq);
  const squashY = pose === 'run' ? 1 + bounceWave * 0.08 : 1 + bounceWave * 0.035;
  const stretchX = 1 / Math.sqrt(squashY);
  const hopY = pose === 'run' ? -Math.abs(Math.sin(time * 8)) * 14 : (pose === 'tiptoe' ? -Math.abs(Math.sin(time * 4.5)) * 8 : 0);

  ctx.translate(0, hopY);
  ctx.scale(scale * facing * stretchX, scale * squashY);

  ctx.fillStyle = 'rgba(9, 13, 22, 0.25)';
  ctx.beginPath(); ctx.ellipse(0, 22 - hopY, 34, 9, 0, 0, Math.PI * 2); ctx.fill();

  if (nobleGlow) {
    const g = ctx.createRadialGradient(0, -55, 12, 0, -55, 130);
    g.addColorStop(0, 'rgba(251, 191, 36, 0.72)'); g.addColorStop(0.6, 'rgba(250, 204, 21, 0.28)'); g.addColorStop(1, 'rgba(251, 191, 36, 0)');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(0, -55, 130, 0, Math.PI * 2); ctx.fill();
  }

  const walkSwing = pose === 'run' ? Math.sin(time * 16) * 22 : (pose === 'tiptoe' ? Math.sin(time * 9) * 14 : 0);
  const armSwing = pose === 'attack' ? -42 + Math.sin(time * 20) * 12 : -walkSwing * 0.7;

  ctx.lineCap = 'round';
  [[-9, -12 - walkSwing], [9, 12 + walkSwing]].forEach(([lx, footX]) => {
    ctx.strokeStyle = INK; ctx.lineWidth = 18;
    ctx.beginPath(); ctx.moveTo(lx, -34); ctx.lineTo(footX, 14); ctx.stroke();
    ctx.strokeStyle = '#1e3a8a'; ctx.lineWidth = 10;
    ctx.beginPath(); ctx.moveTo(lx, -34); ctx.lineTo(footX, 14); ctx.stroke();
  });

  drawComicRect(-24 - walkSwing, 9, 24, 13, 6, '#ef4444', INK, 3.5);
  drawComicRect(-22 - walkSwing, 17, 22, 5, 3, '#ffffff', INK, 2.5);
  drawComicRect(2 + walkSwing, 9, 24, 13, 6, '#ef4444', INK, 3.5);
  drawComicRect(4 + walkSwing, 17, 22, 5, 3, '#ffffff', INK, 2.5);

  ctx.strokeStyle = INK; ctx.lineWidth = 16;
  ctx.beginPath(); ctx.moveTo(-16, -82); ctx.lineTo(-28 - armSwing * 0.4, -46); ctx.stroke();
  ctx.strokeStyle = '#e11d48'; ctx.lineWidth = 9;
  ctx.beginPath(); ctx.moveTo(-16, -82); ctx.lineTo(-28 - armSwing * 0.4, -46); ctx.stroke();

  drawComicRect(-25, -94, 50, 62, 16, '#e11d48', INK, 4);
  ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 3;
  ctx.beginPath(); ctx.moveTo(-6, -88); ctx.lineTo(-6, -66); ctx.moveTo(7, -88); ctx.lineTo(7, -66); ctx.stroke();

  ctx.fillStyle = '#fed7aa'; ctx.strokeStyle = INK; ctx.lineWidth = 4;
  ctx.beginPath(); ctx.arc(0, -120, 27, 0, Math.PI * 2); ctx.fill(); ctx.stroke();

  ctx.fillStyle = '#312e81';
  ctx.beginPath();
  ctx.moveTo(-27, -120); ctx.lineTo(-33, -138); ctx.lineTo(-16, -134); ctx.lineTo(-8, -152);
  ctx.lineTo(4, -138); ctx.lineTo(18, -150); ctx.lineTo(22, -133); ctx.lineTo(31, -130);
  ctx.lineTo(25, -116); ctx.quadraticCurveTo(0, -130, -27, -120); ctx.closePath();
  ctx.fill(); ctx.stroke();

  const isBlinking = Math.sin(time * 2.7) > 0.97;
  drawCartoonEye(4, -121, 6.5, 2, 0, mood, isBlinking);
  drawCartoonEye(18, -121, 6.5, 2, 0, mood, isBlinking);

  ctx.strokeStyle = '#090d16'; ctx.lineWidth = 3;
  ctx.strokeRect(-3, -129, 13, 15); ctx.strokeRect(12, -129, 13, 15);
  ctx.beginPath(); ctx.moveTo(10, -122); ctx.lineTo(12, -122); ctx.stroke();

  if (mood === 'angry') {
    ctx.strokeStyle = '#ef4444'; ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(-14, -134); ctx.lineTo(-10, -130); ctx.lineTo(-14, -126);
    ctx.moveTo(-6, -134); ctx.lineTo(-10, -130); ctx.lineTo(-6, -126);
    ctx.stroke();
  }

  if (isSpeaking) {
    const openH = 4 + Math.abs(Math.sin(time * 22)) * 6;
    ctx.fillStyle = '#7f1d1d'; ctx.strokeStyle = INK; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.ellipse(11, -104, 7, openH, 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  } else if (nobleGlow || mood === 'happy') {
    ctx.fillStyle = '#ffffff'; ctx.strokeStyle = INK; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.arc(10, -107, 8, 0, Math.PI); ctx.closePath(); ctx.fill(); ctx.stroke();
  } else {
    ctx.strokeStyle = INK; ctx.lineWidth = 3.2;
    ctx.beginPath(); ctx.moveTo(5, -104); ctx.lineTo(17, -106); ctx.stroke();
  }

  const handX = pose === 'attack' || pose === 'shield' ? 44 : 26 + armSwing * 0.25;
  const handY = pose === 'attack' || pose === 'shield' ? -84 : -54;
  ctx.strokeStyle = INK; ctx.lineWidth = 16;
  ctx.beginPath(); ctx.moveTo(16, -82); ctx.lineTo(handX, handY); ctx.stroke();
  ctx.strokeStyle = '#f43f5e'; ctx.lineWidth = 9;
  ctx.beginPath(); ctx.moveTo(16, -82); ctx.lineTo(handX, handY); ctx.stroke();

  ctx.save(); ctx.translate(handX + 10, handY - 8);
  ctx.rotate(pose === 'attack' ? -0.22 : (pose === 'shield' ? 0.0 : 0.14));
  const bookW = pose === 'shield' ? 44 : 36, bookH = pose === 'shield' ? 58 : 44;
  drawComicRect(-bookW / 2, -bookH / 2, bookW, bookH, 6, '#38bdf8', INK, 3.8);
  drawComicRect(-bookW / 2 + 4, -bookH / 2 + 4, bookW - 8, bookH - 8, 4, '#ffffff', INK, 2);
  ctx.fillStyle = '#1d4ed8'; ctx.font = '900 8px monospace'; ctx.textAlign = 'center';
  ctx.fillText('SCHOLAR', 0, -4); ctx.fillStyle = '#ef4444'; ctx.fillText('A.P.A.', 0, 8);
  ctx.restore(); ctx.restore();
}

function drawAIProtagonist(x, y, scale = 1, time = 0, power = 1.0, dead = false, isSpeaking = false) {
  ctx.save(); ctx.translate(x, y); ctx.scale(scale, scale);
  if (dead) {
    ctx.fillStyle = '#64748b'; ctx.strokeStyle = INK; ctx.lineWidth = 4;
    ctx.beginPath(); ctx.ellipse(0, 6, 36, 16, 0.12, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
    ctx.strokeStyle = '#ef4444'; ctx.lineWidth = 3.5;
    [-12, 12].forEach(ex => {
      ctx.beginPath(); ctx.moveTo(ex - 5, 0); ctx.lineTo(ex + 5, 10); ctx.moveTo(ex + 5, 0); ctx.lineTo(ex - 5, 10); ctx.stroke();
    });
    for (let s = 0; s < 3; s++) {
      const ang = time * 4 + (s * Math.PI * 2) / 3;
      ctx.fillStyle = '#fbbf24'; ctx.beginPath(); ctx.arc(Math.cos(ang) * 28, -24 + Math.sin(ang) * 8, 4.5, 0, Math.PI * 2); ctx.fill();
    }
    drawComicRect(-56, 24, 112, 22, 6, '#fee2e2', INK, 2.5);
    ctx.fillStyle = '#dc2626'; ctx.font = '900 12px "Comic Sans MS", sans-serif'; ctx.textAlign = 'center';
    ctx.fillText('Zzz... OFFLINE', 0, 39);
    ctx.restore(); return;
  }

  const hover = Math.sin(time * 4.5) * 10;
  const squash = 1 + Math.sin(time * 9) * 0.05;
  ctx.translate(0, hover); ctx.scale(1 / squash, squash);

  const pulseBoost = isSpeaking ? 1 + Math.abs(Math.sin(time * 20)) * 0.22 : 1;
  const radius = 64 * power * pulseBoost;
  const aura = ctx.createRadialGradient(0, 0, 10, 0, 0, radius);
  aura.addColorStop(0, 'rgba(56, 189, 248, 0.85)'); aura.addColorStop(0.55, 'rgba(192, 132, 252, 0.42)'); aura.addColorStop(1, 'rgba(56, 189, 248, 0)');
  ctx.fillStyle = aura; ctx.beginPath(); ctx.arc(0, 0, radius, 0, Math.PI * 2); ctx.fill();

  [time * 2.0, -time * 2.4].forEach((rot, idx) => {
    ctx.save(); ctx.rotate(rot + (idx * Math.PI) / 3);
    ctx.strokeStyle = INK; ctx.lineWidth = 6.5;
    ctx.beginPath(); ctx.ellipse(0, 0, 48, 18, 0, 0, Math.PI * 2); ctx.stroke();
    ctx.strokeStyle = idx === 0 ? '#38bdf8' : '#e879f9'; ctx.lineWidth = 3.5;
    ctx.beginPath(); ctx.ellipse(0, 0, 48, 18, 0, 0, Math.PI * 2); ctx.stroke();
    ctx.restore();
  });

  ctx.fillStyle = '#ffffff'; ctx.strokeStyle = INK; ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(0, -38 * pulseBoost); ctx.quadraticCurveTo(9, -9, 38 * pulseBoost, 0);
  ctx.quadraticCurveTo(9, 9, 0, 38 * pulseBoost); ctx.quadraticCurveTo(-9, 9, -38 * pulseBoost, 0);
  ctx.quadraticCurveTo(-9, -9, 0, -38 * pulseBoost); ctx.closePath();
  ctx.fill(); ctx.stroke();

  drawCartoonEye(-9, -4, 4.5, -1, 0, 'normal', false);
  drawCartoonEye(9, -4, 4.5, -1, 0, 'normal', false);

  if (isSpeaking) {
    ctx.fillStyle = '#0284c7';
    ctx.beginPath(); ctx.ellipse(0, 8, 6, 3 + Math.abs(Math.sin(time * 22)) * 4, 0, 0, Math.PI * 2); ctx.fill();
  } else {
    ctx.strokeStyle = INK; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.arc(0, 5, 6, 0.15 * Math.PI, 0.85 * Math.PI); ctx.stroke();
  }
  ctx.restore();
}

function drawTeacher(x, y, time = 0, isSpeaking = false) {
  ctx.save(); ctx.translate(x, y);
  drawComicRect(-62, -22, 124, 52, 8, '#92400e', INK, 4);
  drawComicRect(-24, -84, 48, 62, 14, '#475569', INK, 4);

  ctx.fillStyle = '#f59e0b'; ctx.strokeStyle = INK; ctx.lineWidth = 2.5;
  ctx.beginPath(); ctx.moveTo(0, -76); ctx.lineTo(-6, -42); ctx.lineTo(0, -34); ctx.lineTo(6, -42); ctx.closePath();
  ctx.fill(); ctx.stroke();

  ctx.fillStyle = '#fed7aa'; ctx.strokeStyle = INK; ctx.lineWidth = 4;
  ctx.beginPath(); ctx.arc(0, -106, 23, 0, Math.PI * 2); ctx.fill(); ctx.stroke();

  drawCartoonEye(-8, -108, 5, 0, 1, 'normal', true);
  drawCartoonEye(8, -108, 5, 0, 1, 'normal', true);

  if (isSpeaking) {
    ctx.fillStyle = '#7f1d1d';
    ctx.beginPath(); ctx.ellipse(0, -94, 6, 2.5 + Math.abs(Math.sin(time * 18)) * 4, 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  } else {
    ctx.strokeStyle = INK; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(-6, -94); ctx.lineTo(6, -94); ctx.stroke();
  }

  drawComicRect(26, -46, 22, 24, 5, '#facc15', INK, 3.5);
  drawComicRect(-68, 34, 136, 22, 6, '#fef08a', INK, 2.5);
  ctx.fillStyle = '#090d16'; ctx.font = '900 11px "Comic Sans MS", sans-serif'; ctx.textAlign = 'center';
  ctx.fillText('BUSINESS TEACHER', 0, 49);
  ctx.restore();
}

function drawSaviors(x, y, time = 0, speakingRole = '') {
  ctx.save(); ctx.translate(x, y);
  const beam = ctx.createLinearGradient(0, -380, 0, 65);
  beam.addColorStop(0, 'rgba(251, 191, 36, 0.12)'); beam.addColorStop(0.5, 'rgba(251, 191, 36, 0.42)'); beam.addColorStop(1, 'rgba(251, 191, 36, 0.04)');
  ctx.fillStyle = beam;
  ctx.beginPath(); ctx.moveTo(-105, -380); ctx.lineTo(105, -380); ctx.lineTo(165, 65); ctx.lineTo(-165, 65); ctx.closePath(); ctx.fill();

  ctx.save(); ctx.translate(-42, -Math.abs(Math.sin(time * 5)) * 5);
  ctx.strokeStyle = INK; ctx.lineWidth = 8; ctx.beginPath(); ctx.ellipse(0, -154, 26, 7, 0, 0, Math.PI * 2); ctx.stroke();
  ctx.strokeStyle = '#fde047'; ctx.lineWidth = 4.5; ctx.beginPath(); ctx.ellipse(0, -154, 26, 7, 0, 0, Math.PI * 2); ctx.stroke();

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
    ctx.fillStyle = '#7f1d1d'; ctx.beginPath(); ctx.ellipse(0, -110, 7, 3 + Math.abs(Math.sin(time * 20)) * 5, 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  } else {
    ctx.strokeStyle = INK; ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(0, -114, 9, 0.15 * Math.PI, 0.85 * Math.PI); ctx.stroke();
  }

  ctx.strokeStyle = INK; ctx.lineWidth = 13; ctx.beginPath(); ctx.moveTo(22, -76); ctx.lineTo(58, -96 + Math.sin(time * 12) * 8); ctx.stroke();
  ctx.strokeStyle = '#fbbf24'; ctx.lineWidth = 6.5; ctx.beginPath(); ctx.moveTo(22, -76); ctx.lineTo(58, -96 + Math.sin(time * 12) * 8); ctx.stroke();

  drawComicRect(-82, 26, 164, 22, 6, '#fef08a', INK, 2.5);
  ctx.fillStyle = '#090d16'; ctx.font = '900 11px "Comic Sans MS", sans-serif'; ctx.textAlign = 'center';
  ctx.fillText('MR. R (LORD & SAVIOR)', 0, 41);
  ctx.restore();

  ctx.save(); ctx.translate(64, 8 - Math.abs(Math.cos(time * 6)) * 5);
  ctx.strokeStyle = INK; ctx.lineWidth = 16; ctx.lineCap = 'round';
  ctx.beginPath(); ctx.moveTo(-9, -28); ctx.lineTo(-9, 12); ctx.moveTo(9, -28); ctx.lineTo(9, 12); ctx.stroke();
  ctx.strokeStyle = '#1e293b'; ctx.lineWidth = 9;
  ctx.beginPath(); ctx.moveTo(-9, -28); ctx.lineTo(-9, 12); ctx.moveTo(9, -28); ctx.lineTo(9, 12); ctx.stroke();

  drawComicRect(-22, -88, 44, 60, 12, '#0284c7', INK, 4);
  ctx.fillStyle = '#fed7aa'; ctx.strokeStyle = INK; ctx.lineWidth = 4;
  ctx.beginPath(); ctx.arc(0, -110, 22, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  ctx.fillStyle = '#090d16'; ctx.beginPath(); ctx.arc(0, -116, 22, Math.PI, 0); ctx.fill();
  drawCartoonEye(-7, -111, 5, -1, 0, 'normal', false);
  drawCartoonEye(7, -111, 5, -1, 0, 'normal', false);

  if (speakingRole === 'anay') {
    ctx.fillStyle = '#7f1d1d'; ctx.beginPath(); ctx.ellipse(0, -99, 6, 2.5 + Math.abs(Math.sin(time * 20)) * 4.5, 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  } else {
    ctx.strokeStyle = INK; ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(0, -103, 7, 0.15 * Math.PI, 0.85 * Math.PI); ctx.stroke();
  }

  ctx.strokeStyle = INK; ctx.lineWidth = 12; ctx.beginPath(); ctx.moveTo(-16, -66); ctx.lineTo(-50, -78); ctx.stroke();
  ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 5.5; ctx.beginPath(); ctx.moveTo(-16, -66); ctx.lineTo(-50, -78); ctx.stroke();

  drawComicRect(-48, 18, 96, 22, 6, '#e0f2fe', INK, 2.5);
  ctx.fillStyle = '#090d16'; ctx.font = '900 11px "Comic Sans MS", sans-serif'; ctx.textAlign = 'center';
  ctx.fillText('ANAY GUPTA', 0, 33);
  ctx.restore(); ctx.restore();
}
"""
