MOVIE_ACT1_JS = r"""
function drawFastFiveExceptions(centerX, baseY, t, isSpeaking) {
  // 5 students who finished fast WITHOUT AI and are now chilling/fooling around
  const spots = [
    { dx: -52, dy: -46, shirt: '#10b981', hair: '#1e1b4b', fem: true },
    { dx:  52, dy: -46, shirt: '#3b82f6', hair: '#451a03', fem: false },
    { dx: -76, dy:  16, shirt: '#14b8a6', hair: '#090d16', fem: false },
    { dx:   0, dy:  16, shirt: '#22c55e', hair: '#713f12', fem: true },
    { dx:  76, dy:  16, shirt: '#0ea5e9', hair: '#1e293b', fem: false },
  ];

  spots.forEach((s, idx) => {
    const chillBob = Math.sin(t * 4 + idx) * 2.5;
    drawStudent(centerX + s.dx, baseY + s.dy + chillBob, 0.68, s.shirt, s.hair, s.fem, t + idx, isSpeaking && idx === 0, 'DONE ✓');
  });

  drawComicRect(centerX - 115, baseY - 156, 230, 28, 7, '#dcfce7', INK, 2.8);
  ctx.fillStyle = '#15803d';
  ctx.font = '900 11px "Comic Sans MS", sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('5 EXCEPTIONS: DONE (NO AI) & CHILL', centerX, baseY - 138);
}

function drawTwentyStudentCrowd(centerX, baseY, t, isFocusedAI, isSpeaking) {
  // Exact 20 students arranged in 3 rows (7 + 7 + 6 = 20)
  const palette = ['#a855f7', '#ec4899', '#f97316', '#eab308', '#8b5cf6', '#f43f5e', '#06b6d4', '#6366f1'];
  const hairs = ['#090d16', '#1e1b4b', '#451a03', '#713f12', '#4c1d95', '#1e293b'];
  const rows = [
    { count: 7, dy: -74, scale: 0.56, spread: 74 },
    { count: 7, dy: -22, scale: 0.62, spread: 78 },
    { count: 6, dy:  32, scale: 0.68, spread: 84 },
  ];

  let studentIdx = 0;
  rows.forEach((row, rIdx) => {
    const startX = centerX - ((row.count - 1) * row.spread) / 2;
    for (let c = 0; c < row.count; c++) {
      const sx = startX + c * row.spread;
      const shirt = palette[studentIdx % palette.length];
      const hair = hairs[studentIdx % hairs.length];
      const fem = studentIdx % 2 === 0;

      // Fooling around = bouncy chatting; Focused-ish AI = calm, steady slight lean
      const motionY = isFocusedAI ? Math.sin(t * 2 + studentIdx) * 0.8 : Math.sin(t * 6 + studentIdx * 1.3) * 3.5;
      const badge = isFocusedAI ? (rIdx === 2 ? 'CALM AI ✓' : 'AI COPY') : 'CHILLING';
      drawStudent(sx, baseY + row.dy + motionY, row.scale, shirt, hair, fem, t + studentIdx, isSpeaking && studentIdx === 16, badge);
      studentIdx++;
    }
  });

  // Banner showing the transition from fooling around -> calm last-minute AI mode
  const bannerW = 470;
  const bannerBg = isFocusedAI ? '#e0f2fe' : '#fef08a';
  const bannerText = isFocusedAI
    ? '20 STUDENTS: FOCUSED-ISH... CALMLY USING AI AT LAST MINUTE'
    : '20 STUDENTS: FOOLING AROUND (WAITING TILL LAST MINUTE)';
  drawComicRect(centerX - bannerW / 2, baseY - 178, bannerW, 30, 8, bannerBg, INK, 3);
  ctx.fillStyle = isFocusedAI ? '#0284c7' : '#b45309';
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

  // 18s - 83s: 5 FAST EXCEPTIONS (NO AI), ANAY & BOY GRINDING, 20 FOOLING AROUND
  else if (t < 83.0) {
    drawClassroomBackdrop(
      'TODAY: MINI STARTUP PITCH',
      '• 5 Fast Finishers: Done Without AI | Anay & Boy: Grinding',
      '• 20 Students: Fooling Around & Waiting Till Last Minute'
    );

    // Left: 5 fast exceptions who finished without AI and are now fooling around/chilling
    drawFastFiveExceptions(135, 525, t, speakingRole === 'fast5');

    // Center-left: The 2 steady workers (Anay & The Boy)
    drawStudent(335, 535, 0.94, '#0284c7', '#090d16', false, t, speakingRole === 'anay', 'ANAY (NO AI)');
    for (let b = 0; b < 3; b++) {
      drawComicRect(410, 522 - b * 18, 62, 16, 4, '#ffffff', INK, 2.5);
    }
    drawTheBoy(512, 535, 1.04, 'stand', t, 1, false, speakingRole === 'boy', 'angry');

    // Right: All 20 procrastinating students fooling around before last-minute AI mode
    drawTwentyStudentCrowd(965, 525, t, false, speakingRole === 'aisquad');

    // Wandering Business Teacher
    const teacherX = 635 + Math.sin(t * 0.65) * 65;
    drawWalkingTeacher(teacherX, 530, t, speakingRole === 'teacher', true, Math.cos(t * 0.65) >= 0 ? 1 : -1);

    if (cue) {
      if (cue.role === 'teacher') { speakerX = teacherX; speakerY = 390; }
      else if (cue.role === 'fast5') { speakerX = 135; speakerY = 385; }
      else if (cue.role === 'anay') { speakerX = 335; speakerY = 395; }
      else if (cue.role === 'boy') { speakerX = 512; speakerY = 380; }
      else if (cue.role === 'aisquad') { speakerX = 965; speakerY = 340; }
    }
  }

  // 83s - 125s: LAST MINUTE — THE 20 SLIP INTO FOCUSED-ISH CALM AI MODE & FINISH
  else if (t < 125.0) {
    drawClassroomBackdrop(
      'LAST 10 MINUTES — DEADLINE APPROACHING!',
      '• Anay & The Boy: Finished From Scratch ✓',
      '• 20 Students: Slowly Slip Into Calm AI Copy-Paste Mode'
    );

    drawFastFiveExceptions(135, 525, t, false);

    drawStudent(335, 535, 0.94, '#0284c7', '#090d16', false, t, speakingRole === 'anay', 'ANAY (DONE ✓)');
    drawTheBoy(505, 535, 1.04, 'stand', t, 1, false, speakingRole === 'boy', 'normal');

    drawWalkingTeacher(635, 530, t, speakingRole === 'teacher', false, 1);

    // The 20 students are now in their calm "focused-ish" AI phase
    drawTwentyStudentCrowd(965, 525, t, true, speakingRole === 'aisquad');
    drawAIProtagonist(965, 225, 0.92, t, 1.15, false, false);

    if (cue) {
      if (cue.role === 'teacher') { speakerX = 635; speakerY = 390; }
      else if (cue.role === 'aisquad') { speakerX = 965; speakerY = 340; }
      else if (cue.role === 'anay') { speakerX = 335; speakerY = 395; }
      else if (cue.role === 'boy') { speakerX = 505; speakerY = 380; }
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
