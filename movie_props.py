MOVIE_PROPS_JS = r"""
let movieTime = 0;
let isPlaying = false;
let playbackSpeed = 1.0;
let isMuted = false;
let showBubbles = true;
let lastFrameTs = null;
let lastSfxBucket = -1;

let activeCueObj = null;
let isSpeechSpeaking = false;
const playedCueIds = new Set();
const LOCKED_CAST = {};
let voicesAreLocked = false;

function lockCharacterVoices() {
  if (!('speechSynthesis' in window) || voicesAreLocked) return;
  const allVoices = window.speechSynthesis.getVoices();
  if (!allVoices || allVoices.length === 0) return;

  const enVoices = allVoices.filter(v => (v.lang || '').toLowerCase().startsWith('en'));
  const pool = enVoices.length > 0 ? enVoices : allVoices;

  const femaleRegex = /(zira|jenny|ava|aria|samantha|victoria|karen|moira|tessa|susan|hazel|catherine|female|google us english|chrome os us english)/i;
  const maleRegex = /(david|mark|guy|andrew|christopher|daniel|ryan|arthur|alex|fred|george|james|brian|roger|aaron|gordon|lee|oliver|male|uk english male)/i;

  const males = pool.filter(v => maleRegex.test(v.name) && !femaleRegex.test(v.name));
  const females = pool.filter(v => femaleRegex.test(v.name));

  const primaryMale = males[0] || pool[0];
  const secondaryMale = males[1] || primaryMale;
  const tertiaryMale = males[2] || secondaryMale;
  const primaryFemale = females[0] || pool[pool.length - 1];
  const secondaryFemale = females[1] || primaryFemale;
  const foundTrueMale = males.length > 0;

  LOCKED_CAST.boy      = { voice: primaryMale,    pitch: foundTrueMale ? 1.02 : 0.72, rate: 1.03 };
  LOCKED_CAST.narrator = { voice: secondaryMale,  pitch: foundTrueMale ? 0.90 : 0.66, rate: 1.00 };
  LOCKED_CAST.teacher  = { voice: tertiaryMale,   pitch: foundTrueMale ? 0.86 : 0.64, rate: 1.00 };
  LOCKED_CAST.sam      = { voice: secondaryMale,  pitch: foundTrueMale ? 1.10 : 0.76, rate: 1.04 };
  LOCKED_CAST.mrr      = { voice: secondaryMale,  pitch: foundTrueMale ? 0.94 : 0.68, rate: 1.02 };
  LOCKED_CAST.anay     = { voice: tertiaryMale,   pitch: foundTrueMale ? 1.04 : 0.74, rate: 1.04 };
  LOCKED_CAST.ai       = { voice: primaryFemale,  pitch: 1.08, rate: 1.04 };
  LOCKED_CAST.maya     = { voice: secondaryFemale,pitch: 1.16, rate: 1.05 };

  voicesAreLocked = true;
}

if ('speechSynthesis' in window) {
  lockCharacterVoices();
  window.speechSynthesis.onvoiceschanged = lockCharacterVoices;
  setInterval(() => {
    if (isPlaying && !isMuted && window.speechSynthesis.speaking && !window.speechSynthesis.paused) {
      window.speechSynthesis.pause();
      window.speechSynthesis.resume();
    }
  }, 9000);
}

function stopActiveVoice() {
  if ('speechSynthesis' in window) {
    try { window.speechSynthesis.cancel(); } catch (e) {}
  }
  isSpeechSpeaking = false;
  activeCueObj = null;
}

function playCueAudio(cue) {
  stopActiveVoice();
  activeCueObj = cue;
  if (isMuted || !('speechSynthesis' in window)) return;

  try {
    if (!voicesAreLocked) lockCharacterVoices();
    const utter = new SpeechSynthesisUtterance(cue.text);
    const profile = LOCKED_CAST[cue.role];
    if (profile) {
      if (profile.voice) utter.voice = profile.voice;
      utter.pitch = profile.pitch;
      utter.rate = profile.rate * playbackSpeed;
    } else {
      utter.pitch = cue.gender === 'male' ? 0.75 : 1.14;
      utter.rate = 1.03 * playbackSpeed;
    }
    utter.volume = 1.0;
    utter.onstart = () => { isSpeechSpeaking = true; };
    utter.onend = () => { isSpeechSpeaking = false; };
    utter.onerror = () => { isSpeechSpeaking = false; };
    isSpeechSpeaking = true;
    window.speechSynthesis.speak(utter);
  } catch (e) {}
}

function isVoiceCurrentlyTalking() {
  return isSpeechSpeaking && 'speechSynthesis' in window && window.speechSynthesis.speaking;
}

function getActiveCue(t) {
  if (isVoiceCurrentlyTalking() && activeCueObj) return activeCueObj;
  for (let i = 0; i < DIALOGUE_CUES.length; i++) {
    const c = DIALOGUE_CUES[i];
    if (t >= c.start && t <= c.end) return c;
  }
  return null;
}

let audioCtx = null;
let musicInterval = null;
let stepCount = 0;

function initAudio() {
  try {
    if (!audioCtx) {
      const AC = window.AudioContext || window.webkitAudioContext;
      if (AC) audioCtx = new AC();
    }
    if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume().catch(() => {});
  } catch (e) {}
}

function playTone(freq, duration, type = 'sine', vol = 0.015, delay = 0) {
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
    if (kind === 'unplug') {
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(320, now);
      osc.frequency.exponentialRampToValueAtTime(65, now + 0.65);
      gain.gain.setValueAtTime(0.05, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.7);
      osc.start(now); osc.stop(now + 0.75);
    } else if (kind === 'revive') {
      [261.63, 329.63, 392.0, 523.25].forEach((f, idx) => playTone(f, 0.9, 'triangle', 0.025, idx * 0.08));
    }
  } catch (e) {}
}

function startScoreLoop() {
  if (musicInterval) clearInterval(musicInterval);
  musicInterval = setInterval(() => {
    if (!isPlaying || isMuted || !audioCtx) return;
    stepCount++;
    const chillNotes = [261.63, 329.63, 392.0, 493.88, 392.0, 329.63];
    playTone(chillNotes[stepCount % chillNotes.length], 0.45, 'sine', 0.014);
  }, 320);
}

function drawClassroomBackdrop(boardTitle, boardLine1, boardLine2) {
  drawHalftonePaper('#f1f5f9', 'rgba(100, 116, 139, 0.12)');
  ctx.fillStyle = '#e2e8f0';
  ctx.fillRect(0, 430, W, 115);
  ctx.fillStyle = '#cbd5e1';
  ctx.fillRect(0, 545, W, 175);
  ctx.strokeStyle = INK;
  ctx.lineWidth = 4;
  ctx.beginPath(); ctx.moveTo(0, 545); ctx.lineTo(W, 545); ctx.stroke();

  [960, 1110].forEach(wx => {
    drawComicRect(wx, 125, 115, 195, 8, '#bae6fd', INK, 4);
    ctx.strokeStyle = INK; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(wx + 57, 125); ctx.lineTo(wx + 57, 320);
    ctx.moveTo(wx, 222); ctx.lineTo(wx + 115, 222); ctx.stroke();
  });

  drawComicRect(75, 125, 540, 215, 12, '#ffffff', '#64748b', 7);
  drawComicRect(75, 125, 540, 215, 12, null, INK, 4);
  ctx.fillStyle = '#0284c7';
  ctx.font = '900 19px "Comic Sans MS", sans-serif';
  ctx.textAlign = 'left';
  ctx.fillText(boardTitle, 102, 168);
  ctx.fillStyle = '#1e293b';
  ctx.font = 'bold 16px "Comic Sans MS", sans-serif';
  ctx.fillText(boardLine1, 102, 206);
  ctx.fillText(boardLine2, 102, 240);

  drawComicRect(655, 135, 120, 38, 8, '#fef08a', INK, 3.5);
  ctx.fillStyle = '#090d16';
  ctx.font = '900 15px "Comic Sans MS", sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('ROOM 204', 715, 160);
}

function drawWalkingTeacher(x, y, time = 0, isSpeaking = false, isWalking = false, facing = -1) {
  ctx.save();
  ctx.translate(x, y);
  const bob = isWalking ? -Math.abs(Math.sin(time * 8)) * 4 : 0;
  ctx.translate(0, bob);
  ctx.scale(facing, 1);

  const legSwing = isWalking ? Math.sin(time * 8) * 14 : 0;
  ctx.lineCap = 'round';
  [[-9, -10 - legSwing], [9, 10 + legSwing]].forEach(([lx, fx]) => {
    ctx.strokeStyle = INK; ctx.lineWidth = 17;
    ctx.beginPath(); ctx.moveTo(lx, -28); ctx.lineTo(fx, 18); ctx.stroke();
    ctx.strokeStyle = '#1e293b'; ctx.lineWidth = 9;
    ctx.beginPath(); ctx.moveTo(lx, -28); ctx.lineTo(fx, 18); ctx.stroke();
  });

  drawComicRect(-24, -88, 48, 62, 14, '#475569', INK, 4);
  ctx.fillStyle = '#f59e0b'; ctx.strokeStyle = INK; ctx.lineWidth = 2.5;
  ctx.beginPath(); ctx.moveTo(4, -80); ctx.lineTo(-2, -46); ctx.lineTo(4, -38); ctx.lineTo(10, -46); ctx.closePath();
  ctx.fill(); ctx.stroke();

  ctx.fillStyle = '#fed7aa'; ctx.strokeStyle = INK; ctx.lineWidth = 4;
  ctx.beginPath(); ctx.arc(0, -110, 23, 0, Math.PI * 2); ctx.fill(); ctx.stroke();

  drawCartoonEye(4, -112, 5, 2, 0, 'normal', false);
  drawCartoonEye(16, -112, 5, 2, 0, 'normal', false);

  if (isSpeaking) {
    ctx.fillStyle = '#7f1d1d';
    ctx.beginPath(); ctx.ellipse(10, -96, 6, 3 + Math.abs(Math.sin(time * 18)) * 4, 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  } else {
    ctx.strokeStyle = INK; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.arc(9, -98, 6, 0.15 * Math.PI, 0.85 * Math.PI); ctx.stroke();
  }

  const armY = isSpeaking ? -66 + Math.sin(time * 12) * 5 : -56;
  ctx.strokeStyle = INK; ctx.lineWidth = 14;
  ctx.beginPath(); ctx.moveTo(14, -74); ctx.lineTo(36, armY); ctx.stroke();
  ctx.strokeStyle = '#475569'; ctx.lineWidth = 8;
  ctx.beginPath(); ctx.moveTo(14, -74); ctx.lineTo(36, armY); ctx.stroke();
  drawComicRect(28, armY - 16, 18, 26, 4, '#d97706', INK, 3);
  ctx.restore();

  drawComicRect(x - 68, y + 26, 136, 22, 6, '#fef08a', INK, 2.5);
  ctx.fillStyle = '#090d16';
  ctx.font = '900 11px "Comic Sans MS", sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('BUSINESS TEACHER', x, y + 41);
}

function drawChromebookScreen(x, y, mode, time) {
  ctx.save();
  ctx.translate(x, y);
  drawComicRect(-115, -78, 230, 140, 10, '#334155', INK, 4);
  drawComicRect(-103, -66, 206, 116, 6, mode === 'game' ? '#0f172a' : '#1e1b4b', INK, 3);
  drawComicRect(-130, 62, 260, 15, 6, '#94a3b8', INK, 3.5);

  if (mode === 'game') {
    ctx.fillStyle = '#22c55e';
    ctx.fillRect(-95, 26, 190, 4);
    const jumpY = -Math.abs(Math.sin(time * 8)) * 32;
    drawComicRect(-68, 4 + jumpY, 18, 22, 3, '#4ade80', INK, 2);
    const obsX = 75 - ((time * 130) % 155);
    drawComicRect(obsX, 8, 14, 18, 2, '#ef4444', INK, 2);
    ctx.fillStyle = '#fde047';
    ctx.font = '900 11px monospace';
    ctx.textAlign = 'center';
    ctx.fillText('CHROMEBOOK DINO // 1,850 PTS', 0, -46);
  } else {
    ctx.fillStyle = '#38bdf8';
    ctx.font = '900 12px monospace';
    ctx.textAlign = 'center';
    ctx.fillText('GEMINI ON CHROMEBOOK', 0, -46);
    [0, 1, 2, 3].forEach(i => {
      const h = 18 + i * 11;
      drawComicRect(-66 + i * 36, 34 - h, 24, h, 3, '#4ade80', INK, 2);
    });
    drawComicRect(-78, -32, 156, 22, 5, '#fef08a', INK, 2);
    ctx.fillStyle = '#090d16';
    ctx.font = '900 11px "Comic Sans MS", sans-serif';
    ctx.fillText('PITCH DECK SUBMITTED!', 0, -17);
  }
  ctx.restore();
}

const CUT_POINTS = [18.0, 83.0, 125.0, 155.0, 224.0, 268.0, 323.0, 358.0];

function drawSmoothTransitions(t) {
  for (let i = 0; i < CUT_POINTS.length; i++) {
    const dist = Math.abs(t - CUT_POINTS[i]);
    if (dist < 0.85) {
      const alpha = (1 - smoothstep(0.0, 0.85, dist)) * 0.85;
      ctx.fillStyle = `rgba(15, 23, 42, ${alpha})`;
      ctx.fillRect(0, 0, W, H);
      break;
    }
  }
}
"""
