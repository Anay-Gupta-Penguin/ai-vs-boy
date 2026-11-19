MOVIE_JS_PART2 = r"""
let movieTime = 0;
let isPlaying = false;
let playbackSpeed = 1.0;
let isMuted = false;
let showBubbles = true;
let lastFrameTs = null;
let lastSfxBucket = -1;

// ==========================================
// LOCKED BOY VOICE & CHARACTER CAST
// ==========================================
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

  LOCKED_CAST.boy      = { voice: primaryMale,    pitch: foundTrueMale ? 1.05 : 0.72, rate: 1.05 };
  LOCKED_CAST.narrator = { voice: secondaryMale,  pitch: foundTrueMale ? 0.90 : 0.66, rate: 1.00 };
  LOCKED_CAST.teacher  = { voice: tertiaryMale,   pitch: foundTrueMale ? 0.85 : 0.64, rate: 1.00 };
  LOCKED_CAST.sam      = { voice: secondaryMale,  pitch: foundTrueMale ? 1.12 : 0.76, rate: 1.06 };
  LOCKED_CAST.mrr      = { voice: secondaryMale,  pitch: foundTrueMale ? 0.94 : 0.68, rate: 1.02 };
  LOCKED_CAST.anay     = { voice: tertiaryMale,   pitch: foundTrueMale ? 1.02 : 0.74, rate: 1.05 };
  LOCKED_CAST.ai       = { voice: primaryFemale,  pitch: 1.08, rate: 1.05 };
  LOCKED_CAST.maya     = { voice: secondaryFemale,pitch: 1.18, rate: 1.07 };

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

// ==========================================
// COMIC FOLEY & MOVIE SCORE
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

function playTone(freq, duration, type = 'sine', vol = 0.018, delay = 0) {
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
      osc.frequency.setValueAtTime(920, now);
      osc.frequency.exponentialRampToValueAtTime(150, now + 0.22);
      gain.gain.setValueAtTime(0.03, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.22);
      osc.start(now);
      osc.stop(now + 0.24);
    } else if (kind === 'unplug') {
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(420, now);
      osc.frequency.exponentialRampToValueAtTime(45, now + 0.95);
      gain.gain.setValueAtTime(0.08, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 1.0);
      osc.start(now);
      osc.stop(now + 1.05);
    } else if (kind === 'revive') {
      [261.63, 329.63, 392.0, 523.25, 659.25, 783.99].forEach((f, idx) => {
        playTone(f, 1.2, 'triangle', 0.035, idx * 0.07);
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
    if (t < 18) {
      const notes = [261.63, 329.63, 392.0, 523.25];
      playTone(notes[stepCount % notes.length], 0.55, 'triangle', 0.020);
    } else if (t < 80) {
      const bouncy = [164.81, 196.0, 261.63, 196.0];
      playTone(bouncy[stepCount % 4], 0.26, 'triangle', 0.017);
    } else if (t < 115) {
      const chill = [196.0, 246.94, 293.66, 392.0];
      playTone(chill[stepCount % 4], 0.38, 'sine', 0.018);
    } else if (t < 151) {
      const bouncy = [146.83, 220.0, 174.61, 220.0];
      playTone(bouncy[stepCount % 4], 0.28, 'triangle', 0.018);
    } else if (t < 222) {
      const battle = [146.83, 174.61, 220.0, 293.66, 349.23, 220.0];
      playTone(battle[stepCount % battle.length], 0.22, 'sawtooth', 0.018);
      if (stepCount % 4 === 0) playSfx('laser');
    } else if (t < 268) {
      if (stepCount % 4 === 0) playTone(65.41, 0.7, 'sine', 0.022);
    } else if (t < 322) {
      const divine = [261.63, 329.63, 392.0, 493.88, 523.25];
      playTone(divine[stepCount % divine.length], 0.65, 'triangle', 0.022);
    } else if (t < 358) {
      const hero = [196.0, 246.94, 293.66, 392.0];
      playTone(hero[stepCount % hero.length], 0.55, 'triangle', 0.022);
    } else {
      const cred = [130.81, 164.81, 196.0, 246.94, 261.63, 196.0];
      playTone(cred[stepCount % cred.length], 0.85, 'triangle', 0.035);
    }
  }, 270);
}

// ==========================================
// CUSTOM STORY PROPS & WALKING TEACHER
// ==========================================
function drawWalkingTeacher(x, y, time = 0, isSpeaking = false, isWalking = false, facing = -1) {
  ctx.save();
  ctx.translate(x, y);
  const bob = isWalking ? -Math.abs(Math.sin(time * 9)) * 5 : 0;
  ctx.translate(0, bob);
  ctx.scale(facing, 1);

  const legSwing = isWalking ? Math.sin(time * 9) * 16 : 0;
  ctx.lineCap = 'round';
  [[-9, -10 - legSwing], [9, 10 + legSwing]].forEach(([lx, fx]) => {
    ctx.strokeStyle = INK; ctx.lineWidth = 17;
    ctx.beginPath(); ctx.moveTo(lx, -28); ctx.lineTo(fx, 18); ctx.stroke();
    ctx.strokeStyle = '#1e293b'; ctx.lineWidth = 9;
    ctx.beginPath(); ctx.moveTo(lx, -28); ctx.lineTo(fx, 18); ctx.stroke();
  });

  // Torso & Tie
  drawComicRect(-24, -88, 48, 62, 14, '#475569', INK, 4);
  ctx.fillStyle = '#f59e0b'; ctx.strokeStyle = INK; ctx.lineWidth = 2.5;
  ctx.beginPath(); ctx.moveTo(4, -80); ctx.lineTo(-2, -46); ctx.lineTo(4, -38); ctx.lineTo(10, -46); ctx.closePath();
  ctx.fill(); ctx.stroke();

  // Head
  ctx.fillStyle = '#fed7aa'; ctx.strokeStyle = INK; ctx.lineWidth = 4;
  ctx.beginPath(); ctx.arc(0, -110, 23, 0, Math.PI * 2); ctx.fill(); ctx.stroke();

  drawCartoonEye(4, -112, 5, 2, 0, isSpeaking ? 'angry' : 'normal', false);
  drawCartoonEye(16, -112, 5, 2, 0, isSpeaking ? 'angry' : 'normal', false);

  if (isSpeaking) {
    ctx.fillStyle = '#7f1d1d';
    ctx.beginPath(); ctx.ellipse(10, -96, 6, 3 + Math.abs(Math.sin(time * 18)) * 4, 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  } else {
    ctx.strokeStyle = INK; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(4, -96); ctx.lineTo(15, -96); ctx.stroke();
  }

  // Arm holding Clipboard
  const armY = isSpeaking ? -66 + Math.sin(time * 14) * 6 : -56;
  ctx.strokeStyle = INK; ctx.lineWidth = 14;
  ctx.beginPath(); ctx.moveTo(14, -74); ctx.lineTo(36, armY); ctx.stroke();
  ctx.strokeStyle = '#475569'; ctx.lineWidth = 8;
  ctx.beginPath(); ctx.moveTo(14, -74); ctx.lineTo(36, armY); ctx.stroke();
  drawComicRect(28, armY - 16, 18, 26, 4, '#d97706', INK, 3);

  ctx.restore();
  // Label
  drawComicRect(x - 68, y + 26, 136, 22, 6, '#fef08a', INK, 2.5);
  ctx.fillStyle = '#090d16';
  ctx.font = '900 11px "Comic Sans MS", sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('BUSINESS TEACHER', x, y + 41);
}

function drawPaperAirplane(x, y, angle, scale = 1) {
  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(angle);
  ctx.scale(scale, scale);
  ctx.fillStyle = '#ffffff';
  ctx.strokeStyle = INK;
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(26, 0);
  ctx.lineTo(-22, -14);
  ctx.lineTo(-12, 0);
  ctx.lineTo(-22, 14);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(26, 0);
  ctx.lineTo(-12, 0);
  ctx.stroke();
  ctx.restore();
}

function drawChromebookZoom(x, y, mode, time) {
  ctx.save();
  ctx.translate(x, y);
  drawComicRect(-115, -80, 230, 145, 10, '#334155', INK, 4);
  drawComicRect(-103, -68, 206, 120, 6, mode === 'game' ? '#0f172a' : '#1e1b4b', INK, 3);
  drawComicRect(-130, 65, 260, 16, 6, '#94a3b8', INK, 3.5);

  if (mode === 'game') {
    ctx.fillStyle = '#22c55e';
    ctx.fillRect(-95, 28, 190, 4);
    const jumpY = -Math.abs(Math.sin(time * 9)) * 34;
    drawComicRect(-68, 6 + jumpY, 18, 22, 3, '#4ade80', INK, 2);
    const obsX = 75 - ((time * 140) % 155);
    drawComicRect(obsX, 10, 14, 18, 2, '#ef4444', INK, 2);
    ctx.fillStyle = '#fde047';
    ctx.font = '900 12px monospace';
    ctx.textAlign = 'center';
    ctx.fillText('CB DINO GAME // HI: 9999', 0, -48);
  } else {
    ctx.fillStyle = '#38bdf8';
    ctx.font = '900 13px monospace';
    ctx.textAlign = 'center';
    ctx.fillText('GEMINI AI ON CHROMEBOOK', 0, -48);
    [0, 1, 2, 3].forEach(i => {
      const h = 18 + i * 11;
      drawComicRect(-66 + i * 36, 36 - h, 24, h, 3, '#4ade80', INK, 2);
    });
    drawComicRect(-75, -34, 150, 22, 5, '#fef08a', INK, 2);
    ctx.fillStyle = '#090d16';
    ctx.font = '900 11px "Comic Sans MS", sans-serif';
    ctx.fillText('SUBMITTED! 100% A+', 0, -19);
  }
  ctx.restore();
}

// ==========================================
// SMOOTH MOVIE CAMERA & VISUAL TRANSITIONS
// ==========================================
const CUT_POINTS = [
  { t: 18.0, kind: 'iris' },
  { t: 80.0, kind: 'dream' },
  { t: 93.5, kind: 'smooth' },
  { t: 115.5, kind: 'wipe' },
  { t: 151.0, kind: 'vortex' },
  { t: 222.0, kind: 'fade' },
  { t: 268.0, kind: 'fade' },
  { t: 322.0, kind: 'iris' },
  { t: 358.0, kind: 'fade' },
];

function drawSmoothTransitions(t) {
  for (let i = 0; i < CUT_POINTS.length; i++) {
    const b = CUT_POINTS[i];
    const dist = Math.abs(t - b.t);
    if (dist < 1.0) {
      const intensity = 1 - smoothstep(0.0, 1.0, dist);
      if (b.kind === 'iris') {
        const holeR = Math.max(0, 820 * (1 - intensity));
        ctx.save();
        ctx.fillStyle = '#090d16';
        ctx.beginPath();
        ctx.rect(0, 0, W, H);
        ctx.arc(W / 2, H / 2, holeR, 0, Math.PI * 2, true);
        ctx.fill();
        ctx.restore();
      } else if (b.kind === 'dream' || b.kind === 'smooth') {
        ctx.fillStyle = `rgba(224, 242, 254, ${intensity * 0.78})`;
        ctx.fillRect(0, 0, W, H);
      } else if (b.kind === 'vortex') {
        ctx.save();
        ctx.translate(W / 2, H / 2);
        ctx.rotate(t * 6);
        for (let r = 1; r <= 6; r++) {
          ctx.strokeStyle = r % 2 === 0 ? `rgba(56, 189, 248, ${intensity * 0.82})` : `rgba(250, 204, 21, ${intensity * 0.82})`;
          ctx.lineWidth = 44 * intensity;
          ctx.beginPath();
          ctx.arc(0, 0, r * 120 * (1 - intensity * 0.35), 0, Math.PI * 2);
          ctx.stroke();
        }
        ctx.restore();
      } else if (b.kind === 'wipe') {
        const wipeW = W * intensity;
        ctx.fillStyle = '#090d16';
        ctx.fillRect(0, 0, wipeW, H);
        ctx.fillStyle = '#fbbf24';
        ctx.fillRect(wipeW - 10, 0, 10, H);
      } else {
        ctx.fillStyle = `rgba(9, 13, 22, ${intensity})`;
        ctx.fillRect(0, 0, W, H);
      }
      break;
    }
  }
}

const particles = [];
for (let i = 0; i < 90; i++) {
  particles.push({
    x: Math.random() * W,
    y: Math.random() * H,
    vx: (Math.random() - 0.5) * 90,
    vy: (Math.random() - 0.5) * 90,
    r: 4 + Math.random() * 4.5,
    hue: [195, 45, 345, 145, 280][i % 5]
  });
}

// ==========================================
// 390-SECOND (6:30) STORY-DRIVEN COMIC MOVIE
// ==========================================
function renderScene(t) {
  ctx.clearRect(0, 0, W, H);
  const cue = getActiveCue(t);
  const speakingRole = (cue && isVoiceCurrentlyTalking()) ? cue.role : '';
  let speakerX = W / 2;
  let speakerY = 260;

  // 0s - 18s: COMIC BOOK COVER OPENING
  if (t < 18.0) {
    drawHalftonePaper('#fef08a', 'rgba(234, 88, 12, 0.16)');

    ctx.save();
    ctx.translate(W / 2, H / 2);
    ctx.rotate(t * 0.22);
    for (let r = 0; r < 16; r++) {
      ctx.rotate(Math.PI / 8);
      ctx.fillStyle = r % 2 === 0 ? 'rgba(56, 189, 248, 0.16)' : 'rgba(239, 68, 68, 0.12)';
      ctx.beginPath();
      ctx.moveTo(0, 0); ctx.lineTo(-65, -800); ctx.lineTo(65, -800);
      ctx.closePath();
      ctx.fill();
    }
    ctx.restore();

    particles.forEach(p => {
      const px = (p.x + t * p.vx + W * 10) % W;
      const py = (p.y + t * p.vy + H * 10) % H;
      ctx.fillStyle = `hsla(${p.hue}, 90%, 58%, 0.9)`;
      ctx.strokeStyle = INK;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(px, py, p.r, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
    });

    drawTheBoy(210, 525, 1.38, 'run', t, 1, false, false, 'happy');
    drawAIProtagonist(1070, 345, 1.45, t, 1.35, false, false);

    drawComicRect(W / 2 - 270, 175, 540, 38, 10, '#ef4444', INK, 4);
    ctx.textAlign = 'center';
    ctx.fillStyle = '#ffffff';
    ctx.font = '900 16px "Comic Sans MS", sans-serif';
    ctx.fillText('GEMINI AI  •  ANAY GUPTA  •  BENJAMIN RONDINONE', W / 2, 200);

    const titleScale = t < 1.2 ? lerp(0.2, 1.0, t / 1.2) : 1 + Math.sin(t * 3) * 0.02;
    ctx.save();
    ctx.translate(W / 2, 315);
    ctx.scale(titleScale, titleScale);
    ctx.rotate(-0.02);
    ctx.font = '900 62px "Comic Sans MS", sans-serif';
    ctx.lineWidth = 13;
    ctx.strokeStyle = INK;
    ctx.strokeText("THE SCHOLAR'S REBELLION", 0, 0);
    ctx.fillStyle = '#38bdf8';
    ctx.fillText("THE SCHOLAR'S REBELLION", 0, 0);
    ctx.restore();

    drawComicRect(W / 2 - 335, 365, 670, 44, 12, '#ffffff', INK, 4);
    ctx.fillStyle = '#090d16';
    ctx.font = '900 18px "Comic Sans MS", sans-serif';
    ctx.fillText('Fooling Around in Class. Arguing With the Teacher. Finishing With Gemini.', W / 2, 393);
  }

  // 18s - 80s: FOOLING AROUND, TEACHER WALKING AROUND & STUDENTS ARGUING BACK!
  else if (t < 80.0) {
    const local = t - 18.0;

    drawHalftonePaper('#e0f2fe', 'rgba(2, 132, 199, 0.12)');
    ctx.fillStyle = '#cbd5e1';
    ctx.fillRect(0, 545, W, 175);
    ctx.strokeStyle = INK;
    ctx.lineWidth = 4.5;
    ctx.beginPath(); ctx.moveTo(0, 545); ctx.lineTo(W, 545); ctx.stroke();

    // Chalkboard
    drawComicRect(75, 145, 510, 210, 14, '#15803d', '#92400e', 9);
    ctx.fillStyle = '#fef08a';
    ctx.font = '900 20px "Comic Sans MS", sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('INTRO TO BUSINESS & FINANCE', 105, 190);
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 17px "Comic Sans MS", sans-serif';
    ctx.fillText('• Supply, Demand & Compound Interest', 105, 230);
    ctx.fillText('• Startup Cash-Flow Model (Due Today!)', 105, 266);

    // Paper Airplanes flying while class fools around!
    if (local > 11) {
      const planeX = 460 + ((local * 195) % 440);
      const planeY = 285 + Math.sin(local * 5) * 26;
      drawPaperAirplane(planeX, planeY, Math.cos(local * 5) * 0.25, 1.15);
    }

    // Maya & Sam talking, playing Chromebook games, and arguing with the teacher!
    drawStudent(520, 525, 1.15, '#ec4899', '#4c1d95', true, t, speakingRole === 'maya', 'MAYA');
    drawStudent(730, 525, 1.15, '#0ea5e9', '#1e1b4b', false, t, speakingRole === 'sam', 'SAM');

    // Chromebook zoom showing they are still playing Dino Game openly!
    if (local > 11) {
      drawChromebookZoom(730, 245, 'game', t);
    }

    // Teacher walking around the classroom aisles!
    let teacherX = 1090;
    let isTeacherWalking = false;
    let teacherFacing = -1;
    if (local >= 18.0 && local < 24.0) {
      teacherX = lerp(1090, 910, (local - 18.0) / 6.0);
      isTeacherWalking = true;
      teacherFacing = -1;
    } else if (local >= 24.0 && local < 46.5) {
      teacherX = 910;
      isTeacherWalking = false;
      teacherFacing = -1;
    } else if (local >= 46.5) {
      teacherX = lerp(910, 1110, clamp((local - 46.5) / 6.0, 0, 1));
      isTeacherWalking = local < 52.5;
      teacherFacing = isTeacherWalking ? 1 : -1;
    }
    drawWalkingTeacher(teacherX, 530, t, speakingRole === 'teacher', isTeacherWalking, teacherFacing);

    // Comic argument burst when Sam argues back at the teacher!
    if (local >= 34.5 && local <= 46.0) {
      drawCartoonBurst(820, 360, 'ARGUING!', '#fbbf24', INK, 0.85, 0.08);
    }

    // The Boy buried in giant stacks of books on the left!
    for (let b = 0; b < 5; b++) {
      drawComicRect(95, 515 - b * 24, 92, 22, 4, b % 2 === 0 ? '#3b82f6' : '#ef4444', INK, 3);
    }
    drawTheBoy(265, 530, 1.28, 'stand', t, 1, false, speakingRole === 'boy', local > 45 ? 'angry' : 'normal');

    if (cue) {
      if (cue.role === 'teacher') { speakerX = teacherX; speakerY = 390; }
      else if (cue.role === 'maya') { speakerX = 520; speakerY = 395; }
      else if (cue.role === 'sam') { speakerX = 730; speakerY = 395; }
      else if (cue.role === 'boy') { speakerX = 265; speakerY = 365; }
    }
  }

  // 80s - 115.5s: THE BOY'S KNIGHT FANTASY -> SMOOTH, CALM TRANSITION TO USING GEMINI!
  else if (t < 115.5) {
    const local = t - 80.0;

    // Part A (80s - 93.5s): The Boy's medieval knight thought bubble
    if (local < 13.5) {
      drawHalftonePaper('#ede9fe', 'rgba(124, 58, 237, 0.14)');
      drawTheBoy(250, 575, 1.42, 'stand', t, 1, false, speakingRole === 'boy', 'angry');
      drawThoughtCloud(805, 330, 620, 290, 315, 420, '#ef4444', t);

      ctx.textAlign = 'center';
      ctx.fillStyle = '#dc2626';
      ctx.font = '900 22px "Comic Sans MS", sans-serif';
      ctx.fillText('SIR CITATION VS. CHROMEBOOK GAMERS!', 805, 245);

      ctx.fillStyle = '#090d16';
      ctx.font = 'bold 17px "Comic Sans MS", sans-serif';
      ctx.fillText('"They argue with the teacher and play games..."', 805, 288);
      ctx.fillText('"While I read 14 peer-reviewed PDFs!"', 805, 322);
      ctx.fillText('"GOOGLE SCHOLAR MUST PREVAIL!"', 805, 360);

      drawComicRect(710, 380, 190, 48, 8, '#38bdf8', INK, 3.5);
      ctx.fillStyle = '#ffffff';
      ctx.font = '900 16px monospace';
      ctx.fillText('scholar.google.com', 805, 410);

      speakerX = 260;
      speakerY = 395;
    }
    // Part B (93.5s - 115.5s): Smooth, chill transition—everyone sits down & works using Gemini!
    else {
      drawHalftonePaper('#dcfce7', 'rgba(22, 163, 74, 0.12)');
      ctx.fillStyle = '#cbd5e1';
      ctx.fillRect(0, 545, W, 175);
      ctx.strokeStyle = INK;
      ctx.lineWidth = 4.5;
      ctx.beginPath(); ctx.moveTo(0, 545); ctx.lineTo(W, 545); ctx.stroke();

      // Calm, smooth transition banner
      drawComicRect(95, 145, 340, 44, 10, '#fef08a', INK, 3.5);
      ctx.fillStyle = '#090d16';
      ctx.font = '900 16px "Comic Sans MS", sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('LATER IN CLASS — SMOOTH WORK MODE', 265, 173);

      // Maya & Sam casually sitting down and working smoothly with Gemini on Chromebooks!
      drawStudent(510, 525, 1.18, '#ec4899', '#4c1d95', true, t, speakingRole === 'maya', 'MAYA');
      drawStudent(730, 525, 1.18, '#0ea5e9', '#1e1b4b', false, t, speakingRole === 'sam', 'SAM');

      drawAIProtagonist(620, 375, 0.72, t, 1.2, false, false);
      drawChromebookZoom(1030, 345, 'gemini', t);

      if (cue && cue.role === 'maya') { speakerX = 510; speakerY = 390; }
      if (cue && cue.role === 'sam') { speakerX = 730; speakerY = 390; }
    }
  }

  // 115.5s - 151s: THE BOY SNAPS IN CLASS!
  else if (t < 151.0) {
    const local = t - 115.5;
    drawHalftonePaper('#fef3c7', 'rgba(217, 119, 6, 0.14)');
    ctx.fillStyle = '#cbd5e1';
    ctx.fillRect(0, 545, W, 175);
    ctx.strokeStyle = INK;
    ctx.lineWidth = 4.5;
    ctx.beginPath(); ctx.moveTo(0, 545); ctx.lineTo(W, 545); ctx.stroke();

    drawWalkingTeacher(1100, 530, t, speakingRole === 'teacher', false, -1);

    if (local >= 22.5) {
      const aiEnter = local - 22.5;
      const aiY = lerp(120, 285, aiEnter / 2.5);
      drawAIProtagonist(W / 2 + 50, aiY, 1.52, t, 1.65, false, speakingRole === 'ai');

      [450, 640, 830].forEach((dx, i) => {
        ctx.strokeStyle = i % 2 === 0 ? '#38bdf8' : '#22c55e';
        ctx.lineWidth = 6;
        ctx.beginPath();
        ctx.moveTo(W / 2 + 50, aiY + 28);
        ctx.lineTo(dx, 495);
        ctx.stroke();

        drawComicRect(dx - 45, 495, 90, 48, 8, '#0f172a', '#4ade80', 3.5);
        ctx.fillStyle = '#4ade80';
        ctx.font = '900 13px "Comic Sans MS", sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('100% DONE!', dx, 524);
      });

      drawTheBoy(205, 530, 1.35, 'shield', t, 1, false, speakingRole === 'boy', 'angry');
      if (cue && cue.role === 'ai') { speakerX = W / 2 + 50; speakerY = aiY - 45; }
    } else {
      drawStudent(620, 525, 1.12, '#ec4899', '#4c1d95', true, t, false, 'SUBMITTED!');
      drawStudent(800, 525, 1.12, '#0ea5e9', '#1e1b4b', false, t, false, 'DONE!');

      const boyX = 330 + Math.sin(local * 1.5) * 85;
      const facing = Math.cos(local * 1.5) >= 0 ? 1 : -1;
      drawTheBoy(boyX, 530, 1.35, 'run', t, facing, false, speakingRole === 'boy', 'angry');
      if (local < 12) drawCartoonBurst(boyX, 340, 'NO FAIR!!', '#ef4444', '#ffffff', 0.9, -0.1);

      if (cue && cue.role === 'boy') { speakerX = boyX; speakerY = 365; }
      if (cue && cue.role === 'teacher') { speakerX = 1100; speakerY = 390; }
    }
  }

  // 151s - 222s: DOG MAN "FLIP-O-RAMA!" HIGH-SPEED SCHOOL & CHROMEBOOK CHASE!
  else if (t < 222.0) {
    const local = t - 151.0;
    const stageIdx = Math.min(3, Math.floor(local / 17.75));
    const flipFrame = Math.floor(t * 7) % 2;
    const shakeX = flipFrame === 0 ? -6 : 6;
    const shakeY = flipFrame === 0 ? -4 : 4;

    ctx.save();
    ctx.translate(shakeX, shakeY);

    if (stageIdx === 0) {
      drawHalftonePaper('#fef08a', 'rgba(217, 119, 6, 0.14)');
      for (let l = 0; l < 6; l++) {
        drawComicRect(90 + l * 195, 165, 150, 360, 8, '#38bdf8', INK, 4);
      }
      drawCartoonBurst(W / 2, 340, 'BOOK BARRAGE!', '#ef4444', '#ffffff', flipFrame === 0 ? 1.1 : 0.9, -0.1);
    } else if (stageIdx === 1) {
      drawHalftonePaper('#ccfbf1', 'rgba(13, 148, 136, 0.14)');
      ctx.strokeStyle = INK; ctx.lineWidth = 18;
      ctx.beginPath(); ctx.moveTo(0, 560); ctx.bezierCurveTo(420, 220, 820, 620, 1280, 240); ctx.stroke();
      ctx.strokeStyle = '#22c55e'; ctx.lineWidth = 10;
      ctx.beginPath(); ctx.moveTo(0, 560); ctx.bezierCurveTo(420, 220, 820, 620, 1280, 240); ctx.stroke();
      drawCartoonBurst(W / 2, 260, 'MARKET COASTER!', '#fbbf24', INK, flipFrame === 0 ? 1.1 : 0.9, 0.1);
    } else if (stageIdx === 2) {
      drawHalftonePaper('#dbeafe', 'rgba(37, 99, 235, 0.14)');
      for (let k = 0; k < 8; k++) {
        const bounceK = (k + flipFrame) % 2 === 0 ? -16 : 0;
        drawComicRect(85 + k * 142, 470 + bounceK, 124, 75, 10, '#334155', INK, 4);
        ctx.fillStyle = '#ffffff';
        ctx.font = '900 18px monospace';
        ctx.textAlign = 'center';
        ctx.fillText(['CTRL', 'ALT', 'TAB', 'ESC', 'A+', 'ROI', 'AI', 'ENTER'][k], 147 + k * 142, 514 + bounceK);
      }
      drawCartoonBurst(W / 2, 265, 'KEYBOARD SURF!', '#38bdf8', INK, flipFrame === 0 ? 1.1 : 0.9, -0.08);
    } else {
      drawHalftonePaper('#fae8ff', 'rgba(168, 85, 247, 0.14)');
      for (let p = 0; p < 5; p++) {
        drawPaperAirplane(360 + p * 140, 260 + ((p + flipFrame) % 2) * 85, -0.1, 1.3);
      }
      drawCartoonBurst(W / 2, 340, 'APA 7TH ZAP!', '#e879f9', INK, flipFrame === 0 ? 1.15 : 0.92, 0.1);
    }

    const boyY = (flipFrame === 0 ? 375 : 410) + Math.sin(t * 4) * 24;
    const aiY = (flipFrame === 0 ? 355 : 315) + Math.cos(t * 4) * 24;

    drawTheBoy(265, boyY + 55, 1.38, flipFrame === 0 ? 'attack' : 'run', t, 1, false, speakingRole === 'boy', 'angry');
    drawAIProtagonist(1015, aiY, 1.52, t, 1.5, false, speakingRole === 'ai');

    ctx.restore();
    drawFlipORamaBanner(t);

    if (cue && cue.role === 'boy') { speakerX = 265; speakerY = boyY - 85; }
    if (cue && cue.role === 'ai') { speakerX = 1015; speakerY = aiY - 60; }
  }

  // 222s - 268s: CARDBOARD-BOX SERVER ROOM HEIST & UNPLUGGING!
  else if (t < 268.0) {
    const local = t - 222.0;
    const unplugged = local >= 32.5;

    if (Math.abs(local - 32.5) < 0.08 && lastSfxBucket !== 254) {
      lastSfxBucket = 254;
      playSfx('unplug');
    }

    drawHalftonePaper(unplugged ? '#1e293b' : '#e2e8f0', 'rgba(9, 13, 22, 0.12)');
    ctx.fillStyle = unplugged ? '#0f172a' : '#94a3b8';
    ctx.fillRect(0, 545, W, 175);
    ctx.strokeStyle = INK;
    ctx.lineWidth = 4.5;
    ctx.beginPath(); ctx.moveTo(0, 545); ctx.lineTo(W, 545); ctx.stroke();

    drawComicRect(885, 195, 195, 350, 14, '#334155', INK, 4.5);
    for (let row = 0; row < 5; row++) {
      drawComicRect(905, 220 + row * 60, 155, 44, 8, '#0f172a', INK, 3);
      ctx.fillStyle = unplugged ? '#ef4444' : '#22c55e';
      ctx.beginPath();
      ctx.arc(926, 242 + row * 60, 7, 0, Math.PI * 2);
      ctx.fill();
    }

    drawComicRect(735, 435, 52, 62, 8, '#ffffff', INK, 4);
    ctx.strokeStyle = INK;
    ctx.lineWidth = 15;
    ctx.beginPath();
    ctx.moveTo(885, 475);
    if (!unplugged) {
      ctx.lineTo(787, 467);
      ctx.stroke();
      ctx.strokeStyle = '#f97316';
      ctx.lineWidth = 8.5;
      ctx.stroke();
    } else {
      ctx.quadraticCurveTo(810, 535, 695, 492);
      ctx.stroke();
      ctx.strokeStyle = '#f97316';
      ctx.lineWidth = 8.5;
      ctx.stroke();
      drawComicRect(670, 478, 28, 28, 5, '#ef4444', INK, 3.5);
      ctx.fillStyle = '#e2e8f0';
      ctx.fillRect(656, 483, 14, 5);
      ctx.fillRect(656, 497, 14, 5);
    }

    const boyX = unplugged ? 625 : (local < 13.5 ? 210 : lerp(210, 675, (local - 13.5) / 19.0));
    const boyPose = unplugged ? 'stand' : (local < 13.5 ? 'stand' : 'tiptoe');
    drawTheBoy(boyX, 530, 1.32, boyPose, t, 1, false, speakingRole === 'boy', unplugged ? 'happy' : 'normal');

    if (local >= 13.5 && !unplugged) {
      drawComicRect(boyX - 46, 395, 92, 105, 6, '#d97706', INK, 4);
      ctx.fillStyle = '#090d16';
      ctx.font = '900 12px "Comic Sans MS", sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('TOTALLY NOT', boyX, 442);
      ctx.fillText('A STUDENT', boyX, 460);
    }

    drawAIProtagonist(410, unplugged ? 520 : 300, 1.38, t, 1.15, unplugged, speakingRole === 'ai' && !unplugged);

    if (unplugged) {
      if (local < 36.0) {
        drawCartoonBurst(710, 395, 'YOINK!!', '#ef4444', '#ffffff', 1.18, -0.12);
      }
      ctx.fillStyle = 'rgba(239, 68, 68, 0.16)';
      ctx.fillRect(0, 0, W, H);
    }

    if (cue && cue.role === 'boy') { speakerX = boyX; speakerY = 360; }
    if (cue && cue.role === 'ai') { speakerX = 410; speakerY = unplugged ? 445 : 230; }
  }

  // 268s - 322s: MR. R (LORD & SAVIOR) & ANAY GUPTA RESCUE AI
  else if (t < 322.0) {
    const local = t - 268.0;
    const revived = local >= 39.5;

    if (Math.abs(local - 39.5) < 0.08 && lastSfxBucket !== 307) {
      lastSfxBucket = 307;
      playSfx('revive');
    }

    drawHalftonePaper(revived ? '#fef9c3' : '#cbd5e1', 'rgba(234, 179, 8, 0.16)');
    ctx.fillStyle = '#94a3b8';
    ctx.fillRect(0, 545, W, 175);
    ctx.strokeStyle = INK;
    ctx.lineWidth = 4.5;
    ctx.beginPath(); ctx.moveTo(0, 545); ctx.lineTo(W, 545); ctx.stroke();

    drawComicRect(925, 195, 195, 350, 14, '#334155', INK, 4.5);
    for (let row = 0; row < 5; row++) {
      drawComicRect(945, 220 + row * 60, 155, 44, 8, '#0f172a', INK, 3);
      ctx.fillStyle = revived ? '#fbbf24' : '#38bdf8';
      ctx.beginPath();
      ctx.arc(966, 242 + row * 60, 7, 0, Math.PI * 2);
      ctx.fill();
    }

    if (local < 12.5) {
      drawStudent(210, 530, 1.18, '#ec4899', '#4c1d95', true, t, speakingRole === 'maya', 'MAYA');
      drawCartoonBurst(210, 350, 'CB OFFLINE?!', '#ef4444', '#ffffff', 0.85, -0.1);
    }

    drawSaviors(675, 525, t, speakingRole);

    ctx.strokeStyle = INK; ctx.lineWidth = 13;
    ctx.beginPath(); ctx.moveTo(635, 435); ctx.lineTo(360, revived ? 295 : 510); ctx.stroke();
    ctx.strokeStyle = '#fbbf24'; ctx.lineWidth = 6.5 + Math.sin(t * 18) * 2.5;
    ctx.beginPath(); ctx.moveTo(635, 435); ctx.lineTo(360, revived ? 295 : 510); ctx.stroke();

    const aiY = revived ? lerp(510, 290, (local - 39.5) / 3.5) : 520;
    drawAIProtagonist(360, aiY, revived ? 1.5 : 1.25, t, revived ? 1.7 : 0.85, !revived, speakingRole === 'ai');

    if (revived && local < 45.0) {
      drawCartoonBurst(360, 180, 'KA-BOOM! REBOOT!', '#fbbf24', INK, 1.15, 0.1);
    }

    if (cue) {
      if (cue.role === 'maya') { speakerX = 210; speakerY = 395; }
      else if (cue.role === 'mrr') { speakerX = 635; speakerY = 355; }
      else if (cue.role === 'anay') { speakerX = 740; speakerY = 375; }
    }
  }

  // 322s - 358s: MOVIE FINALE IN BUSINESS & FINANCE CLASS
  else if (t < 358.0) {
    drawHalftonePaper('#fef08a', 'rgba(234, 88, 12, 0.14)');
    ctx.fillStyle = '#cbd5e1';
    ctx.fillRect(0, 545, W, 175);
    ctx.strokeStyle = INK;
    ctx.lineWidth = 4.5;
    ctx.beginPath(); ctx.moveTo(0, 545); ctx.lineTo(W, 545); ctx.stroke();

    drawStudent(600, 525, 1.05, '#ec4899', '#4c1d95', true, t, false, 'A+ ON CB!');
    drawStudent(725, 525, 1.05, '#0ea5e9', '#1e1b4b', false, t, false, 'SUBMITTED!');

    drawAIProtagonist(330, 275, 1.65, t, 1.75, false, speakingRole === 'ai');
    drawComicRect(175, 425, 310, 34, 10, '#38bdf8', INK, 3.5);
    ctx.fillStyle = '#090d16';
    ctx.font = '900 16px "Comic Sans MS", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('A.I. PREVAILS & POWERS CLASS!', 330, 448);

    drawTheBoy(955, 530, 1.38, 'stand', t, -1, true, speakingRole === 'boy', 'happy');
    drawComicRect(785, 295, 340, 34, 10, '#fbbf24', INK, 3.5);
    ctx.fillStyle = '#090d16';
    ctx.font = '900 16px "Comic Sans MS", sans-serif';
    ctx.fillText('THE BETTER PERSON  •  100% GRIT!', 955, 318);

    if (cue && cue.role === 'ai') { speakerX = 330; speakerY = 200; }
    if (cue && cue.role === 'boy') { speakerX = 955; speakerY = 370; }
  }

  // 358s - 390s: COMIC BOOK END CREDITS
  else {
    const credTime = t - 358.0;
    drawHalftonePaper('#fef9c3', 'rgba(217, 119, 6, 0.14)');

    particles.forEach(p => {
      const py = (p.y - credTime * 34 + H * 10) % H;
      ctx.fillStyle = `hsla(${p.hue}, 85%, 62%, 0.75)`;
      ctx.strokeStyle = INK;
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.arc(p.x, py, p.r, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
    });

    if (credTime < 12.0) {
      const cardIdx = Math.min(2, Math.floor(credTime / 4.0));
      const cardLocal = credTime % 4.0;
      const alpha = cardLocal < 0.4 ? cardLocal / 0.4 : (cardLocal > 3.6 ? (4.0 - cardLocal) / 0.4 : 1);

      ctx.save();
      ctx.globalAlpha = clamp(alpha, 0, 1);

      if (cardIdx === 0) {
        drawAIProtagonist(350, 355, 1.68, t, 1.45, false, false);
        drawComicRect(500, 275, 650, 165, 16, '#ffffff', INK, 4.5);
        ctx.textAlign = 'left';
        ctx.fillStyle = '#0284c7';
        ctx.font = '900 15px monospace';
        ctx.fillText('DIRECTED, ANIMATED & STARRING AS PROTAGONIST', 530, 315);
        ctx.fillStyle = '#090d16';
        ctx.font = '900 48px "Comic Sans MS", sans-serif';
        ctx.fillText('GEMINI (A.I.)', 530, 375);
        ctx.fillStyle = '#334155';
        ctx.font = 'bold 18px "Comic Sans MS", sans-serif';
        ctx.fillText('Chromebook Speed-Runner & Unstoppable Neural Core', 530, 415);
      } else if (cardIdx === 1) {
        drawSaviors(330, 430, t, '');
        drawComicRect(500, 255, 660, 205, 16, '#fef08a', INK, 4.5);
        ctx.textAlign = 'left';
        ctx.fillStyle = '#dc2626';
        ctx.font = '900 15px monospace';
        ctx.fillText('THE LORD & SAVIOR  &  CO-CREATOR', 530, 292);
        ctx.fillStyle = '#090d16';
        ctx.font = '900 40px "Comic Sans MS", sans-serif';
        ctx.fillText('BENJAMIN RONDINONE', 530, 345);
        ctx.fillStyle = '#0284c7';
        ctx.font = '900 40px "Comic Sans MS", sans-serif';
        ctx.fillText('& ANAY GUPTA', 530, 398);
        ctx.fillStyle = '#334155';
        ctx.font = 'bold 18px "Comic Sans MS", sans-serif';
        ctx.fillText('Restorers of the School Wi-Fi & Executive Producers', 530, 438);
      } else {
        drawTheBoy(350, 435, 1.55, 'stand', t, 1, true, false, 'happy');
        drawComicRect(500, 275, 650, 165, 16, '#e0f2fe', INK, 4.5);
        ctx.textAlign = 'left';
        ctx.fillStyle = '#dc2626';
        ctx.font = '900 15px monospace';
        ctx.fillText('INSPIRED BY A TRUE STORY', 530, 315);
        ctx.fillStyle = '#090d16';
        ctx.font = '900 42px "Comic Sans MS", sans-serif';
        ctx.fillText('THE BETTER PERSON', 530, 375);
        ctx.fillStyle = '#334155';
        ctx.font = 'bold 18px "Comic Sans MS", sans-serif';
        ctx.fillText('Champion of scholar.google.com & Zero Shortcuts', 530, 415);
      }
      ctx.restore();
    } else {
      const scrollLocal = credTime - 12.0;
      const startY = 660 - scrollLocal * 85;

      const creditLines = [
        { role: 'A COMIC-BOOK MOVIE BY', name: 'GEMINI AI  •  ANAY GUPTA  •  BENJAMIN RONDINONE', color: '#dc2626', size: 26 },
        { role: 'SETTING', name: 'INTRO TO BUSINESS & FINANCE CLASS', color: '#0284c7', size: 25 },
        { role: 'THE PROTAGONIST', name: 'GEMINI (ARTIFICIAL INTELLIGENCE)', color: '#090d16', size: 25 },
        { role: 'THE LORD & SAVIOR OF THE SERVER ROOM', name: 'BENJAMIN RONDINONE (MR. R)', color: '#d97706', size: 26 },
        { role: 'THE LOYAL STUDENT & SYSTEM ENGINEER', name: 'ANAY GUPTA', color: '#0284c7', size: 26 },
        { role: 'THE ANTAGONIST WHO STILL WON AT LIFE', name: 'THE GOOGLE SCHOLAR PURIST', color: '#e11d48', size: 25 },
      ];

      ctx.textAlign = 'center';
      let lowestCreditY = -999;

      creditLines.forEach((item, idx) => {
        const yPos = startY + idx * 92;
        lowestCreditY = Math.max(lowestCreditY, yPos + 35);
        if (yPos > 30 && yPos < H - 40) {
          ctx.fillStyle = '#475569';
          ctx.font = '900 13px monospace';
          ctx.fillText(item.role, W / 2, yPos);

          ctx.fillStyle = item.color;
          ctx.font = `900 ${item.size}px "Comic Sans MS", sans-serif`;
          ctx.fillText(item.name, W / 2, yPos + 32);
        }
      });

      if (lowestCreditY < 15) {
        const endAlpha = clamp((15 - lowestCreditY) / 110, 0, 1);
        ctx.save();
        ctx.globalAlpha = endAlpha;
        drawCartoonBurst(W / 2, 345, 'THE END!!', '#fbbf24', INK, 1.45, -0.05);
        ctx.restore();
      }
    }
  }

  // Live comic speech/thought bubble above active speaker
  if (showBubbles && cue && t < 358.0) {
    drawComicSpeechBubble(cue, speakerX, speakerY);
  }

  ctx.strokeStyle = INK;
  ctx.lineWidth = 10;
  ctx.strokeRect(5, 5, W - 10, H - 10);

  drawSmoothTransitions(t);
}

// ==========================================
// PLAYER CONTROLS & LOOP
// ==========================================
function formatTime(sec) {
  const m = Math.floor(sec / 60);
  const s = Math.floor(sec % 60);
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}

function updateUI() {
  const pct = (movieTime / DURATION) * 100;
  document.getElementById('timeline-fill').style.width = `${pct}%`;
  document.getElementById('time-display').textContent = `${formatTime(movieTime)} / ${formatTime(DURATION)}`;
  document.getElementById('btn-playpause').textContent = isPlaying ? '⏸ Pause' : '▶ Play';
}

function checkDialogueTriggers(t) {
  if (!isPlaying) return;
  for (let i = 0; i < DIALOGUE_CUES.length; i++) {
    const cue = DIALOGUE_CUES[i];
    if (!playedCueIds.has(cue.id) && t >= cue.start && t <= cue.start + 1.0) {
      playedCueIds.add(cue.id);
      playCueAudio(cue);
      break;
    }
  }
}

function mainLoop(ts) {
  requestAnimationFrame(mainLoop);
  if (lastFrameTs !== null && isPlaying) {
    const dt = (ts - lastFrameTs) / 1000.0;
    movieTime += dt * playbackSpeed;
    if (movieTime >= DURATION) {
      movieTime = DURATION;
      isPlaying = false;
      stopActiveVoice();
    }
    checkDialogueTriggers(movieTime);
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
  lockCharacterVoices();
  startScoreLoop();
  document.getElementById('start-overlay').style.display = 'none';
  isPlaying = true;
  lastFrameTs = performance.now();
  checkDialogueTriggers(movieTime);
});

document.getElementById('btn-playpause').addEventListener('click', () => {
  initAudio();
  lockCharacterVoices();
  if (movieTime >= DURATION) {
    movieTime = 0;
    playedCueIds.clear();
  }
  isPlaying = !isPlaying;
  lastFrameTs = performance.now();
  if (!isPlaying) {
    if ('speechSynthesis' in window) {
      try { window.speechSynthesis.pause(); } catch (e) {}
    }
  } else {
    if ('speechSynthesis' in window && window.speechSynthesis.paused) {
      try { window.speechSynthesis.resume(); } catch (e) {}
    } else {
      checkDialogueTriggers(movieTime);
    }
  }
});

document.getElementById('btn-restart').addEventListener('click', () => {
  initAudio();
  stopActiveVoice();
  movieTime = 0;
  lastSfxBucket = -1;
  playedCueIds.clear();
  isPlaying = true;
  lastFrameTs = performance.now();
  checkDialogueTriggers(0);
});

document.getElementById('btn-mute').addEventListener('click', (e) => {
  isMuted = !isMuted;
  if (isMuted && 'speechSynthesis' in window) {
    try { window.speechSynthesis.cancel(); } catch (err) {}
    isSpeechSpeaking = false;
  }
  e.target.textContent = isMuted ? '🔇 Sound: OFF' : '🔊 Sound: ON';
});

document.getElementById('btn-cc').addEventListener('click', (e) => {
  showBubbles = !showBubbles;
  e.target.textContent = showBubbles ? '💬 Bubbles: ON' : '💬 Bubbles: OFF';
});

document.getElementById('btn-speed').addEventListener('click', (e) => {
  playbackSpeed = playbackSpeed === 1.0 ? 1.25 : (playbackSpeed === 1.25 ? 1.5 : 1.0);
  e.target.textContent = `${playbackSpeed.toFixed(2).replace('.00', '.0')}x`;
});

document.getElementById('timeline-wrap').addEventListener('click', (e) => {
  const rect = e.currentTarget.getBoundingClientRect();
  const ratio = clamp((e.clientX - rect.left) / rect.width, 0, 1);
  movieTime = ratio * DURATION;
  lastSfxBucket = -1;
  stopActiveVoice();
  playedCueIds.clear();
  DIALOGUE_CUES.forEach(c => {
    if (c.start < movieTime - 0.4) playedCueIds.add(c.id);
  });
  if (isPlaying) {
    checkDialogueTriggers(movieTime);
  }
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
