MOVIE_ACT1_JS = r"""
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

  // 18s - 83s: CLASSROOM ASSIGNMENT, CHROMEBOOK DINO & APA PURIST
  else if (t < 83.0) {
    drawClassroomBackdrop(
      'TODAY: MINI STARTUP PITCH',
      '• Pricing Strategy & Profit Margin',
      '• Supply & Demand — Due Before the Bell!'
    );

    const teacherWalking = t >= 43.0 && t <= 68.0;
    const teacherX = teacherWalking ? lerp(1080, 560, smoothstep(43.0, 52.0, t)) : 1080;
    drawWalkingTeacher(teacherX, 530, t, speakingRole === 'teacher', teacherWalking, -1);

    drawStudent(235, 530, 1.05, '#ec4899', '#4c1d95', true, t, speakingRole === 'maya', 'MAYA');
    drawStudent(390, 530, 1.05, '#0ea5e9', '#1e1b4b', false, t, speakingRole === 'sam', 'SAM');

    if (t >= 30.0 && t <= 68.0) {
      drawChromebookScreen(312, 275, 'game', t);
    }

    for (let b = 0; b < 4; b++) {
      drawComicRect(710, 515 - b * 20, 88, 18, 4, '#ffffff', INK, 3);
    }
    drawTheBoy(855, 530, 1.26, 'stand', t, -1, false, speakingRole === 'boy', 'angry');

    if (cue) {
      if (cue.role === 'teacher') { speakerX = teacherX; speakerY = 390; }
      else if (cue.role === 'maya') { speakerX = 235; speakerY = 395; }
      else if (cue.role === 'sam') { speakerX = 390; speakerY = 395; }
      else if (cue.role === 'boy') { speakerX = 855; speakerY = 370; }
    }
  }

  // 83s - 125s: ANAY & GEMINI HELP MAYA & SAM BUILD THEIR PITCH
  else if (t < 125.0) {
    drawClassroomBackdrop(
      '15 MINUTES LEFT — LOCK IN & BUILD!',
      '• Break-Even Pricing & Customer Acquisition Cost',
      '• Submit Slides to Google Classroom'
    );

    drawStudent(215, 530, 1.05, '#ec4899', '#4c1d95', true, t, speakingRole === 'maya', 'MAYA');
    drawStudent(365, 530, 1.05, '#0ea5e9', '#1e1b4b', false, t, speakingRole === 'sam', 'SAM');
    drawStudent(515, 530, 1.05, '#0284c7', '#090d16', false, t, speakingRole === 'anay', 'ANAY');

    drawAIProtagonist(365, 255, 1.18, t, 1.35, false, speakingRole === 'ai');
    drawChromebookScreen(835, 360, 'pitch', t);
    drawTheBoy(1110, 530, 1.24, 'stand', t, -1, false, false, 'normal');

    if (cue) {
      if (cue.role === 'anay') { speakerX = 515; speakerY = 395; }
      else if (cue.role === 'maya') { speakerX = 215; speakerY = 395; }
      else if (cue.role === 'sam') { speakerX = 365; speakerY = 395; }
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
