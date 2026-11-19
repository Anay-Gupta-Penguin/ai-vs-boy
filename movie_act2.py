MOVIE_ACT2_JS = r"""
function renderAct2(t, cue, speakingRole) {
  let speakerX = W / 2;
  let speakerY = 260;

  // 155s - 224s: CLEAN SMARTBOARD PRESENTATION SHOWDOWN
  if (t < 224.0) {
    drawClassroomBackdrop(
      'CLASSROOM PITCH SHOWDOWN — ROOM 204',
      '• Left: 40-Page Google Scholar Primary Research',
      '• Right: Gemini Interactive Unit Economics Model'
    );

    drawComicRect(680, 145, 480, 230, 12, '#0f172a', INK, 4);
    ctx.fillStyle = '#38bdf8';
    ctx.font = '900 15px monospace';
    ctx.textAlign = 'center';
    ctx.fillText('LIVE BREAK-EVEN & PROFIT MODEL', 920, 178);
    ctx.strokeStyle = '#22c55e';
    ctx.lineWidth = 5;
    ctx.beginPath(); ctx.moveTo(730, 330); ctx.lineTo(1100, 210); ctx.stroke();
    ctx.strokeStyle = '#f59e0b';
    ctx.beginPath(); ctx.moveTo(730, 290); ctx.lineTo(1100, 275); ctx.stroke();

    for (let b = 0; b < 5; b++) {
      drawComicRect(95, 515 - b * 22, 95, 20, 4, '#ffffff', INK, 3);
    }
    drawTheBoy(270, 530, 1.32, 'stand', t, 1, false, speakingRole === 'boy', 'normal');
    drawAIProtagonist(540, 320, 1.32, t, 1.3, false, speakingRole === 'ai');
    drawWalkingTeacher(1090, 530, t, speakingRole === 'teacher', false, -1);

    if (cue) {
      if (cue.role === 'boy') { speakerX = 270; speakerY = 365; }
      else if (cue.role === 'ai') { speakerX = 540; speakerY = 245; }
      else if (cue.role === 'teacher') { speakerX = 1090; speakerY = 390; }
    }
  }

  // 224s - 268s: CLASSROOM ROUTER CORNER — WI-FI UNPLUGGED
  else if (t < 268.0) {
    const local = t - 224.0;
    const unplugged = local >= 16.0;

    if (Math.abs(local - 16.0) < 0.08 && lastSfxBucket !== 240) {
      lastSfxBucket = 240;
      playSfx('unplug');
    }

    drawHalftonePaper(unplugged ? '#334155' : '#e2e8f0', 'rgba(15, 23, 42, 0.12)');
    ctx.fillStyle = unplugged ? '#1e293b' : '#cbd5e1';
    ctx.fillRect(0, 545, W, 175);
    ctx.strokeStyle = INK;
    ctx.lineWidth = 4;
    ctx.beginPath(); ctx.moveTo(0, 545); ctx.lineTo(W, 545); ctx.stroke();

    drawComicRect(870, 210, 210, 335, 12, '#334155', INK, 4);
    for (let r = 0; r < 4; r++) {
      drawComicRect(892, 235 + r * 68, 166, 46, 8, '#0f172a', INK, 3);
      ctx.fillStyle = unplugged ? '#ef4444' : '#22c55e';
      ctx.beginPath(); ctx.arc(914, 258 + r * 68, 7, 0, Math.PI * 2); ctx.fill();
    }

    drawComicRect(710, 440, 52, 60, 8, '#ffffff', INK, 4);
    ctx.strokeStyle = INK; ctx.lineWidth = 14;
    ctx.beginPath(); ctx.moveTo(870, 475);
    if (!unplugged) {
      ctx.lineTo(762, 470); ctx.stroke();
      ctx.strokeStyle = '#f97316'; ctx.lineWidth = 8; ctx.stroke();
    } else {
      ctx.quadraticCurveTo(790, 535, 675, 495); ctx.stroke();
      ctx.strokeStyle = '#f97316'; ctx.lineWidth = 8; ctx.stroke();
      drawComicRect(650, 482, 26, 26, 5, '#ef4444', INK, 3);
    }

    const boyX = unplugged ? 585 : lerp(260, 635, clamp(local / 16.0, 0, 1));
    drawTheBoy(boyX, 530, 1.32, unplugged ? 'stand' : 'tiptoe', t, 1, false, speakingRole === 'boy', 'normal');
    drawAIProtagonist(370, unplugged ? 515 : 305, 1.35, t, 1.1, unplugged, speakingRole === 'ai' && !unplugged);

    if (cue) {
      if (cue.role === 'boy') { speakerX = boyX; speakerY = 365; }
      else if (cue.role === 'ai') { speakerX = 370; speakerY = unplugged ? 440 : 230; }
    }
  }

  // 268s - 323s: MR. R (LORD & SAVIOR) & ANAY GUPTA RESTORE WI-FI
  else if (t < 323.0) {
    const local = t - 268.0;
    const revived = local >= 41.0;

    if (Math.abs(local - 41.0) < 0.08 && lastSfxBucket !== 309) {
      lastSfxBucket = 309;
      playSfx('revive');
    }

    drawHalftonePaper(revived ? '#fef9c3' : '#cbd5e1', 'rgba(234, 179, 8, 0.14)');
    ctx.fillStyle = '#94a3b8';
    ctx.fillRect(0, 545, W, 175);
    ctx.strokeStyle = INK;
    ctx.lineWidth = 4;
    ctx.beginPath(); ctx.moveTo(0, 545); ctx.lineTo(W, 545); ctx.stroke();

    drawComicRect(910, 210, 210, 335, 12, '#334155', INK, 4);
    for (let r = 0; r < 4; r++) {
      drawComicRect(932, 235 + r * 68, 166, 46, 8, '#0f172a', INK, 3);
      ctx.fillStyle = revived ? '#22c55e' : '#38bdf8';
      ctx.beginPath(); ctx.arc(954, 258 + r * 68, 7, 0, Math.PI * 2); ctx.fill();
    }

    if (local < 14.0) {
      drawStudent(205, 530, 1.15, '#ec4899', '#4c1d95', true, t, speakingRole === 'maya', 'MAYA');
    }

    drawSaviors(675, 525, t, speakingRole);

    const aiY = revived ? lerp(510, 290, clamp((local - 41.0) / 3.5, 0, 1)) : 515;
    drawAIProtagonist(370, aiY, revived ? 1.45 : 1.25, t, revived ? 1.55 : 0.85, !revived, speakingRole === 'ai');

    if (cue) {
      if (cue.role === 'maya') { speakerX = 205; speakerY = 395; }
      else if (cue.role === 'mrr') { speakerX = 635; speakerY = 355; }
      else if (cue.role === 'anay') { speakerX = 740; speakerY = 375; }
    }
  }

  // 323s - 358s: FULFILLING FINALE — MUTUAL RESPECT & EVERYBODY PASSES
  else if (t < 358.0) {
    drawClassroomBackdrop(
      'INTRO TO BUSINESS & FINANCE — ALL PITCHES COMPLETE!',
      '• Every Group Submitted & Presented Before the Bell ✓',
      '• Lesson Learned: Great Tools + Real Effort = Success'
    );

    drawStudent(585, 525, 1.08, '#ec4899', '#4c1d95', true, t, false, 'A+ ✓');
    drawStudent(715, 525, 1.08, '#0ea5e9', '#1e1b4b', false, t, false, 'A+ ✓');

    drawAIProtagonist(330, 290, 1.5, t, 1.5, false, speakingRole === 'ai');
    drawTheBoy(955, 530, 1.35, 'stand', t, -1, true, speakingRole === 'boy', 'happy');

    if (cue) {
      if (cue.role === 'ai') { speakerX = 330; speakerY = 215; }
      else if (cue.role === 'boy') { speakerX = 955; speakerY = 365; }
    }
  }

  // 358s - 390s: COMIC BOOK END CREDITS
  else {
    const credTime = t - 358.0;
    drawHalftonePaper('#fef9c3', 'rgba(217, 119, 6, 0.14)');

    if (credTime < 12.0) {
      const cardIdx = Math.min(2, Math.floor(credTime / 4.0));
      const cardLocal = credTime % 4.0;
      const alpha = cardLocal < 0.4 ? cardLocal / 0.4 : (cardLocal > 3.6 ? (4.0 - cardLocal) / 0.4 : 1);

      ctx.save();
      ctx.globalAlpha = clamp(alpha, 0, 1);
      if (cardIdx === 0) {
        drawAIProtagonist(350, 355, 1.6, t, 1.4, false, false);
        drawComicRect(500, 275, 650, 165, 16, '#ffffff', INK, 4);
        ctx.textAlign = 'left';
        ctx.fillStyle = '#0284c7'; ctx.font = '900 15px monospace';
        ctx.fillText('DIRECTED, ANIMATED & STARRING AS PROTAGONIST', 530, 315);
        ctx.fillStyle = '#090d16'; ctx.font = '900 46px "Comic Sans MS", sans-serif';
        ctx.fillText('GEMINI (A.I.)', 530, 375);
        ctx.fillStyle = '#334155'; ctx.font = 'bold 18px "Comic Sans MS", sans-serif';
        ctx.fillText('Chromebook Study Partner & Finance Explainer', 530, 415);
      } else if (cardIdx === 1) {
        drawSaviors(330, 430, t, '');
        drawComicRect(500, 255, 660, 205, 16, '#fef08a', INK, 4);
        ctx.textAlign = 'left';
        ctx.fillStyle = '#dc2626'; ctx.font = '900 15px monospace';
        ctx.fillText('THE LORD & SAVIOR  &  CO-CREATOR', 530, 292);
        ctx.fillStyle = '#090d16'; ctx.font = '900 38px "Comic Sans MS", sans-serif';
        ctx.fillText('BENJAMIN RONDINONE', 530, 345);
        ctx.fillStyle = '#0284c7'; ctx.font = '900 38px "Comic Sans MS", sans-serif';
        ctx.fillText('& ANAY GUPTA', 530, 398);
        ctx.fillStyle = '#334155'; ctx.font = 'bold 18px "Comic Sans MS", sans-serif';
        ctx.fillText('Restorers of the Classroom Wi-Fi & Executive Producers', 530, 438);
      } else {
        drawTheBoy(350, 435, 1.5, 'stand', t, 1, true, false, 'happy');
        drawComicRect(500, 275, 650, 165, 16, '#e0f2fe', INK, 4);
        ctx.textAlign = 'left';
        ctx.fillStyle = '#dc2626'; ctx.font = '900 15px monospace';
        ctx.fillText('INSPIRED BY A TRUE STORY', 530, 315);
        ctx.fillStyle = '#090d16'; ctx.font = '900 40px "Comic Sans MS", sans-serif';
        ctx.fillText('THE SCHOLAR PURIST', 530, 375);
        ctx.fillStyle = '#334155'; ctx.font = 'bold 18px "Comic Sans MS", sans-serif';
        ctx.fillText('Champion of scholar.google.com & Zero Shortcuts', 530, 415);
      }
      ctx.restore();
    } else {
      const scrollLocal = credTime - 12.0;
      const startY = 660 - scrollLocal * 85;
      const creditLines = [
        { role: 'A COMIC-BOOK MOVIE BY', name: 'GEMINI AI  •  ANAY GUPTA  •  BENJAMIN RONDINONE', color: '#dc2626', size: 25 },
        { role: 'SETTING', name: 'ROOM 204 — INTRO TO BUSINESS & FINANCE', color: '#0284c7', size: 24 },
        { role: 'THE PROTAGONIST', name: 'GEMINI (ARTIFICIAL INTELLIGENCE)', color: '#090d16', size: 24 },
        { role: 'THE LORD & SAVIOR OF THE SERVER ROOM', name: 'BENJAMIN RONDINONE (MR. R)', color: '#d97706', size: 25 },
        { role: 'THE LOYAL STUDENT & SYSTEM ENGINEER', name: 'ANAY GUPTA', color: '#0284c7', size: 25 },
        { role: 'THE SCHOLAR WHO EARNED RESPECT', name: 'THE GOOGLE SCHOLAR PURIST', color: '#e11d48', size: 24 },
      ];
      ctx.textAlign = 'center';
      let lowestY = -999;
      creditLines.forEach((item, idx) => {
        const yPos = startY + idx * 92;
        lowestY = Math.max(lowestY, yPos + 35);
        if (yPos > 30 && yPos < H - 40) {
          ctx.fillStyle = '#475569'; ctx.font = '900 13px monospace';
          ctx.fillText(item.role, W / 2, yPos);
          ctx.fillStyle = item.color; ctx.font = `900 ${item.size}px "Comic Sans MS", sans-serif`;
          ctx.fillText(item.name, W / 2, yPos + 32);
        }
      });
      if (lowestY < 15) {
        ctx.save();
        ctx.globalAlpha = clamp((15 - lowestY) / 110, 0, 1);
        drawCartoonBurst(W / 2, 345, 'THE END!', '#fbbf24', INK, 1.35, -0.04);
        ctx.restore();
      }
    }
  }

  return { speakerX, speakerY };
}

function renderScene(t) {
  ctx.clearRect(0, 0, W, H);
  const cue = getActiveCue(t);
  const speakingRole = (cue && isVoiceCurrentlyTalking()) ? cue.role : '';
  const pos = t < 155.0 ? renderAct1(t, cue, speakingRole) : renderAct2(t, cue, speakingRole);

  if (showBubbles && cue && t < 358.0) {
    drawComicSpeechBubble(cue, pos.speakerX, pos.speakerY);
  }
  ctx.strokeStyle = INK;
  ctx.lineWidth = 10;
  ctx.strokeRect(5, 5, W - 10, H - 10);
  drawSmoothTransitions(t);
}

function formatTime(sec) {
  const m = Math.floor(sec / 60);
  const s = Math.floor(sec % 60);
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}

function updateUI() {
  document.getElementById('timeline-fill').style.width = `${(movieTime / DURATION) * 100}%`;
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
    if (movieTime >= DURATION) { movieTime = DURATION; isPlaying = false; stopActiveVoice(); }
    checkDialogueTriggers(movieTime);
  }
  lastFrameTs = ts;
  try { renderScene(movieTime); updateUI(); } catch (err) { console.error(err); }
}

document.getElementById('play-hero-btn').addEventListener('click', () => {
  initAudio(); lockCharacterVoices(); startScoreLoop();
  document.getElementById('start-overlay').style.display = 'none';
  isPlaying = true; lastFrameTs = performance.now(); checkDialogueTriggers(movieTime);
});
document.getElementById('btn-playpause').addEventListener('click', () => {
  initAudio(); lockCharacterVoices();
  if (movieTime >= DURATION) { movieTime = 0; playedCueIds.clear(); }
  isPlaying = !isPlaying; lastFrameTs = performance.now();
  if (!isPlaying) { try { window.speechSynthesis.pause(); } catch (e) {} }
  else if ('speechSynthesis' in window && window.speechSynthesis.paused) { try { window.speechSynthesis.resume(); } catch (e) {} }
  else { checkDialogueTriggers(movieTime); }
});
document.getElementById('btn-restart').addEventListener('click', () => {
  initAudio(); stopActiveVoice(); movieTime = 0; lastSfxBucket = -1; playedCueIds.clear();
  isPlaying = true; lastFrameTs = performance.now(); checkDialogueTriggers(0);
});
document.getElementById('btn-mute').addEventListener('click', (e) => {
  isMuted = !isMuted;
  if (isMuted) { stopActiveVoice(); }
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
  movieTime = clamp((e.clientX - rect.left) / rect.width, 0, 1) * DURATION;
  lastSfxBucket = -1; stopActiveVoice(); playedCueIds.clear();
  DIALOGUE_CUES.forEach(c => { if (c.start < movieTime - 0.4) playedCueIds.add(c.id); });
  if (isPlaying) checkDialogueTriggers(movieTime);
});
document.getElementById('btn-fs').addEventListener('click', () => {
  const wrap = document.getElementById('theater-wrap');
  if (!document.fullscreenElement) wrap.requestFullscreen().catch(() => {});
  else document.exitFullscreen().catch(() => {});
});
requestAnimationFrame(mainLoop);
</script>
</body>
</html>
"""
