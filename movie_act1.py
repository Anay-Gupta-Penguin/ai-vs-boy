MOVIE_ACT1_JS = r"""
function drawAICopyPasteSquad(centerX, baseY, t, isPanicking, isSpeaking) {
  // 7 students clustered at desks: 4 in back row, 3 in front row
  const backRow = [
    { dx: -150, shirt: '#a855f7', hair: '#1e1b4b', fem: true },
    { dx: -50,  shirt: '#ec4899', hair: '#451a03', fem: false },
    { dx: 50,   shirt: '#f97316', hair: '#090d16', fem: true },
    { dx: 150,  shirt: '#eab308', hair: '#713f12', fem: false },
  ];
  const frontRow = [
    { dx: -105, shirt: '#8b5cf6', hair: '#090d16', fem: false },
    { dx: 0,    shirt: '#f43f5e', hair: '#4c1d95', fem: true },
    { dx: 105,  shirt: '#06b6d4', hair: '#1e293b', fem: false },
  ];

  // Back row (4 students)
  backRow.forEach((s, idx) => {
    const jitter = isPanicking ? Math.sin(t * 24 + idx) * 3 : 0;
    drawStudent(centerX + s.dx + jitter, baseY - 48, 0.76, s.shirt, s.hair, s.fem, t + idx, isSpeaking && idx === 1, 'AI TAB');
  });

  // Front row (3 students)
  frontRow.forEach((s, idx) => {
    const jitter = isPanicking ? Math.cos(t * 26 + idx) * 3.5 : 0;
    drawStudent(centerX + s.dx + jitter, baseY + 12, 0.84, s.shirt, s.hair, s.fem, t + idx + 2, isSpeaking && idx === 1, isPanicking ? 'ALMOST DONE!' : 'CTRL+C/V');
  });

  // Floating Copy-Paste / Panic Banner above the 7-person AI Squad
  const bannerW = 330;
  const bannerBg = isPanicking ? '#fee2e2' : '#e0f2fe';
  const bannerText = isPanicking ? 'PANIC TAB-SWITCH: "IM ALMOST DONE!!"' : 'AI SQUAD (7): CTRL+C -> CTRL+V';
  drawComicRect(centerX - bannerW / 2, baseY - 178, bannerW, 30, 8, bannerBg, INK, 3);
  ctx.fillStyle = isPanicking ? '#dc2626' : '#0284c7';
  ctx.font = '900 12px "Comic Sans MS", sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText(bannerText, centerX, baseY - 158);
}

function renderAct1(t, cue, speakingRole) {
  let speakerX = W / 2;
  let speakerY = 260;

  // 0s - 18s: COMIC BOOK TITLE CARD & NARRATOR INTRO
  if (t < 18.0) {
    drawHalftonePaper('#fef9c3', 'rgba(217, 119, 6, 0.14)');
    drawCartoonBurst(W / 2, 330, "THE SCHOLAR'S REBELLION", '#38bdf8', INK, 1.55, -0.02);

    drawComicRect(W / 2 - 340, 445, 680, 56, 12, '#ffffff', INK, 4);
    ctx.fillStyle = INK;
    ctx.font = '900 18px "Comic Sans MS", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('ROOM 204: INTRO TO BUSINESS & FINANCE', W / 2, 480);

    drawTheBoy(210, 545, 1.22, 'stand', t, 1, false, false, 'normal');
    drawAIProtagonist(1070, 355, 1.25, t, 1.25, false, false);
  }

  // 18s - 83s: REALISTIC CLASSROOM — 2 DOING OWN THING (NO AI), ANAY & BOY WORKING, 7 COPY-PASTING AI
  else if (t < 83.0) {
    drawClassroomBackdrop(
      'TODAY: MINI STARTUP PITCH',
      '• Build Pricing & Profit Margin From Scratch',
      '• Due Before the Bell — No Blind Copy-Pasting!'
    );

    // 1. Couple of random classmates doing their own thing (NOT using AI)
    drawStudent(110, 535, 0.88, '#10b981', '#1e1b4b', true, t, speakingRole === 'maya', 'MAYA (NO AI)');
    drawStudent(225, 535, 0.88, '#3b82f6', '#451a03', false, t, speakingRole === 'sam', 'SAM (NO AI)');
    drawComicRect(82, 368, 170, 26, 6, '#dcfce7', INK, 2.5);
    ctx.fillStyle = '#15803d'; ctx.font = '900 11px "Comic Sans MS", sans-serif'; ctx.textAlign = 'center';
    ctx.fillText('DOING OWN THING (NO AI)', 167, 385);

    // 2. The 2 students genuinely doing work: Anay & The Boy
    drawStudent(380, 535, 0.96, '#0284c7', '#090d16', false, t, speakingRole === 'anay', 'ANAY (REAL WORK)');
    for (let b = 0; b < 3; b++) {
      drawComicRect(465, 522 - b * 18, 68, 16, 4, '#ffffff', INK, 2.5);
    }
    drawTheBoy(575, 535, 1.08, 'stand', t, 1, false, speakingRole === 'boy', 'angry');

    // 3. Small chunk of 7 students blatantly copy-pasting AI
    const isPanicking = t >= 69.0 || speakingRole === 'aisquad';
    drawAICopyPasteSquad(1025, 525, t, isPanicking, speakingRole === 'aisquad');

    // 4. Business Teacher wandering around casually ("doing idk") then walking near AI squad
    const teacherX = t < 66.0
      ? 680 + Math.sin(t * 0.7) * 90
      : lerp(720, 815, smoothstep(66.0, 72.0, t));
    drawWalkingTeacher(teacherX, 530, t, speakingRole === 'teacher', true, t < 66.0 ? (Math.cos(t * 0.7) >= 0 ? 1 : -1) : 1);

    if (cue) {
      if (cue.role === 'teacher') { speakerX = teacherX; speakerY = 390; }
      else if (cue.role === 'maya' || cue.role === 'sam') { speakerX = 168; speakerY = 395; }
      else if (cue.role === 'anay') { speakerX = 380; speakerY = 395; }
      else if (cue.role === 'boy') { speakerX = 575; speakerY = 380; }
      else if (cue.role === 'aisquad') { speakerX = 1025; speakerY = 340; }
    }
  }

  // 83s - 125s: TEACHER CONFRONTS THE 7 AI COPY-PASTERS; ANAY & BOY FINISH FROM SCRATCH
  else if (t < 125.0) {
    drawClassroomBackdrop(
      '15 MINUTES LEFT — SHOW YOUR WORK!',
      '• Anay & The Boy: 100% Built From Scratch ✓',
      '• AI Squad: Panicking & Switching Tabs'
    );

    // Random classmates still chilling without AI
    drawStudent(110, 535, 0.88, '#10b981', '#1e1b4b', true, t, false, 'MAYA (NO AI)');
    drawStudent(225, 535, 0.88, '#3b82f6', '#451a03', false, t, false, 'SAM (NO AI)');

    // Anay & The Boy genuinely done
    drawStudent(380, 535, 0.96, '#0284c7', '#090d16', false, t, speakingRole === 'anay', 'ANAY (DONE ✓)');
    drawTheBoy(545, 535, 1.08, 'stand', t, 1, false, speakingRole === 'boy', 'normal');

    // Teacher standing right in front of the 7-person AI Squad
    drawWalkingTeacher(745, 530, t, speakingRole === 'teacher', false, 1);
    drawAICopyPasteSquad(1025, 525, t, true, speakingRole === 'aisquad');
    drawAIProtagonist(1025, 225, 0.95, t, 1.1, false, false);

    if (cue) {
      if (cue.role === 'teacher') { speakerX = 745; speakerY = 390; }
      else if (cue.role === 'aisquad') { speakerX = 1025; speakerY = 340; }
      else if (cue.role === 'anay') { speakerX = 380; speakerY = 395; }
      else if (cue.role === 'boy') { speakerX = 545; speakerY = 380; }
    }
  }

  // 125s - 155s: THE CHALLENGE — SCHOLAR PURIST VS. GEMINI AI
  else {
    drawHalftonePaper('#e0f2fe', 'rgba(2, 132, 199, 0.14)');
    ctx.fillStyle = '#bae6fd';
    ctx.fillRect(0, 545, W, 175);
    ctx.strokeStyle = INK;
    ctx.lineWidth = 4;
    ctx.beginPath(); ctx.moveTo(0, 545); ctx.lineTo(W, 545); ctx.stroke();

    drawCartoonBurst(W / 2, 230, 'CHALLENGE!', '#fbbf24', INK, 1.15, 0.03);

    drawTheBoy(330, 530, 1.36, 'stand', t, 1, false, speakingRole === 'boy', 'angry');
    drawAIProtagonist(940, 325, 1.42, t, 1.45, false, speakingRole === 'ai');

    if (cue) {
      if (cue.role === 'boy') { speakerX = 330; speakerY = 365; }
      else if (cue.role === 'ai') { speakerX = 940; speakerY = 240; }
    }
  }

  return { speakerX, speakerY };
}
"""
