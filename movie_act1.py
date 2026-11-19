MOVIE_ACT1_JS = r"""
const particles = [];
for (let i = 0; i < 65; i++) {
  particles.push({
    x: Math.random() * W,
    y: Math.random() * H,
    vx: (Math.random() - 0.5) * 55,
    vy: (Math.random() - 0.5) * 55,
    r: 4 + Math.random() * 4,
    hue: [195, 45, 345, 145, 280][i % 5]
  });
}

function renderAct1(t, cue, speakingRole) {
  let speakerX = W / 2;
  let speakerY = 260;

  // 0s - 18s: CHILL COMIC COVER OPENING
  if (t < 18.0) {
    drawHalftonePaper('#fef08a', 'rgba(234, 88, 12, 0.14)');
    particles.forEach(p => {
      const px = (p.x + t * p.vx + W * 10) % W;
      const py = (p.y + t * p.vy + H * 10) % H;
      ctx.fillStyle = `hsla(${p.hue}, 85%, 60%, 0.85)`;
      ctx.strokeStyle = INK;
      ctx.lineWidth = 2;
      ctx.beginPath(); ctx.arc(px, py, p.r, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
    });

    drawTheBoy(210, 525, 1.35, 'stand', t, 1, false, false, 'normal');
    drawAIProtagonist(1070, 345, 1.42, t, 1.25, false, false);

    drawComicRect(W / 2 - 270, 175, 540, 38, 10, '#0284c7', INK, 4);
    ctx.textAlign = 'center';
    ctx.fillStyle = '#ffffff';
    ctx.font = '900 16px "Comic Sans MS", sans-serif';
    ctx.fillText('GEMINI AI  •  ANAY GUPTA  •  BENJAMIN RONDINONE', W / 2, 200);

    ctx.save();
    ctx.translate(W / 2, 315);
    ctx.font = '900 60px "Comic Sans MS", sans-serif';
    ctx.lineWidth = 12;
    ctx.strokeStyle = INK;
    ctx.strokeText("THE SCHOLAR'S REBELLION", 0, 0);
    ctx.fillStyle = '#38bdf8';
    ctx.fillText("THE SCHOLAR'S REBELLION", 0, 0);
    ctx.restore();

    drawComicRect(W / 2 - 335, 365, 670, 44, 12, '#ffffff', INK, 4);
    ctx.fillStyle = '#090d16';
    ctx.font = '900 18px "Comic Sans MS", sans-serif';
    ctx.fillText('Room 204: Intro to Business & Finance — A True Classroom Story', W / 2, 393);
  }

  // 18s - 83s: ACTUAL CLASSROOM VIBE — HANGING OUT, TEACHER WALKING & BANTER
  else if (t < 83.0) {
    const local = t - 18.0;
    drawClassroomBackdrop(
      'INTRO TO BUSINESS & FINANCE — UNIT 4',
      '• Build a Mini Startup Pitch (Pricing & Profit Margin)',
      '• Show Supply & Demand Curve — Due Before Bell'
    );

    drawStudent(470, 525, 1.12, '#ec4899', '#4c1d95', true, t, speakingRole === 'maya', 'MAYA');
    drawStudent(650, 525, 1.12, '#0ea5e9', '#1e1b4b', false, t, speakingRole === 'sam', 'SAM');
    drawStudent(825, 525, 1.12, '#22c55e', '#0f172a', false, t, false, 'ANAY');

    if (local > 11) {
      drawChromebookScreen(750, 235, 'game', t);
    }

    let teacherX = 1110;
    let walking = false;
    let facing = -1;
    if (local >= 24.0 && local < 30.0) {
      teacherX = lerp(1110, 955, (local - 24.0) / 6.0);
      walking = true;
    } else if (local >= 30.0 && local < 51.0) {
      teacherX = 955;
    } else if (local >= 51.0) {
      teacherX = lerp(955, 1110, clamp((local - 51.0) / 6.0, 0, 1));
      walking = local < 57.0;
      facing = walking ? 1 : -1;
    }
    drawWalkingTeacher(teacherX, 530, t, speakingRole === 'teacher', walking, facing);

    for (let b = 0; b < 4; b++) {
      drawComicRect(92, 518 - b * 22, 86, 20, 4, b % 2 === 0 ? '#3b82f6' : '#64748b', INK, 3);
    }
    drawTheBoy(255, 530, 1.25, 'stand', t, 1, false, speakingRole === 'boy', 'normal');

    if (cue) {
      if (cue.role === 'teacher') { speakerX = teacherX; speakerY = 390; }
      else if (cue.role === 'maya') { speakerX = 470; speakerY = 395; }
      else if (cue.role === 'sam') { speakerX = 650; speakerY = 395; }
      else if (cue.role === 'boy') { speakerX = 255; speakerY = 365; }
    }
  }

  // 83s - 125s: SMOOTH, CHILL SHIFT INTO WORK MODE USING GEMINI
  else if (t < 125.0) {
    drawClassroomBackdrop(
      'INTRO TO BUSINESS & FINANCE — WORK TIME',
      '• Break-Even Formula: Fixed Costs / (Price - Variable Cost)',
      '• Upload Pitch Deck to Google Classroom'
    );

    drawComicRect(640, 180, 290, 36, 9, '#dcfce7', INK, 3);
    ctx.fillStyle = '#15803d';
    ctx.font = '900 14px "Comic Sans MS", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('15 MINS LEFT • LOCKED IN', 785, 203);

    drawStudent(460, 525, 1.14, '#22c55e', '#0f172a', false, t, speakingRole === 'anay', 'ANAY');
    drawStudent(635, 525, 1.14, '#ec4899', '#4c1d95', true, t, speakingRole === 'maya', 'MAYA');
    drawStudent(810, 525, 1.14, '#0ea5e9', '#1e1b4b', false, t, speakingRole === 'sam', 'SAM');

    drawAIProtagonist(635, 365, 0.72, t, 1.15, false, false);
    drawChromebookScreen(1055, 395, 'gemini', t);

    drawTheBoy(225, 530, 1.25, 'stand', t, 1, false, false, 'normal');

    if (cue) {
      if (cue.role === 'anay') { speakerX = 460; speakerY = 395; }
      else if (cue.role === 'maya') { speakerX = 635; speakerY = 395; }
      else if (cue.role === 'sam') { speakerX = 810; speakerY = 395; }
    }
  }

  // 125s - 155s: GROUNDED, RESPECTFUL RIVALRY IN CLASS
  else {
    drawClassroomBackdrop(
      'INTRO TO BUSINESS & FINANCE — PRESENTATIONS',
      '• Group 1 (Maya, Sam, Anay): SUBMITTED ✓',
      '• Group 2 (Google Scholar Solo): IN PROGRESS'
    );

    drawStudent(780, 525, 1.1, '#ec4899', '#4c1d95', true, t, false, 'DONE ✓');
    drawStudent(930, 525, 1.1, '#0ea5e9', '#1e1b4b', false, t, false, 'DONE ✓');

    drawTheBoy(270, 530, 1.32, 'stand', t, 1, false, speakingRole === 'boy', 'normal');
    drawAIProtagonist(560, 320, 1.35, t, 1.3, false, speakingRole === 'ai');

    if (cue) {
      if (cue.role === 'boy') { speakerX = 270; speakerY = 365; }
      else if (cue.role === 'ai') { speakerX = 560; speakerY = 245; }
    }
  }

  return { speakerX, speakerY };
}
"""
