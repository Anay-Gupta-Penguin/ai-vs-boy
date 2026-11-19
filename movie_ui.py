MOVIE_HTML_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>The Scholar's Rebellion</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
  body {
    background: #090d16;
    color: #f8fafc;
    font-family: "Comic Sans MS", "Chalkboard SE", system-ui, sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    overflow: hidden;
  }
  #theater-wrap {
    position: relative;
    width: 100%;
    max-width: 1280px;
    aspect-ratio: 16 / 9;
    background: #0f172a;
    border: 4px solid #38bdf8;
    border-radius: 14px;
    box-shadow: 0 20px 55px rgba(0, 0, 0, 0.75);
    overflow: hidden;
  }
  canvas {
    width: 100%;
    height: 100%;
    display: block;
  }
  #start-overlay {
    position: absolute;
    inset: 0;
    background: rgba(9, 13, 22, 0.84);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 18px;
    z-index: 20;
    text-align: center;
    padding: 24px;
  }
  #start-overlay h1 {
    font-size: clamp(28px, 4vw, 52px);
    color: #38bdf8;
    text-shadow: 3px 3px 0 #090d16, -2px -2px 0 #090d16;
    letter-spacing: 1px;
  }
  #start-overlay p {
    font-size: clamp(14px, 1.6vw, 20px);
    color: #fef08a;
    max-width: 680px;
  }
  #play-hero-btn {
    background: #fbbf24;
    color: #090d16;
    border: 4px solid #090d16;
    border-radius: 14px;
    padding: 14px 34px;
    font-size: 22px;
    font-weight: 900;
    font-family: inherit;
    cursor: pointer;
    box-shadow: 0 6px 0 #090d16;
    transition: transform 0.1s ease;
  }
  #play-hero-btn:hover { transform: translateY(-2px); background: #fde047; }
  #play-hero-btn:active { transform: translateY(2px); }
  #controls-bar {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(to top, rgba(9, 13, 22, 0.95), rgba(9, 13, 22, 0.78));
    padding: 10px 16px 12px 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    z-index: 10;
  }
  #timeline-wrap {
    width: 100%;
    height: 10px;
    background: #334155;
    border-radius: 999px;
    cursor: pointer;
    overflow: hidden;
    border: 2px solid #090d16;
  }
  #timeline-fill {
    width: 0%;
    height: 100%;
    background: linear-gradient(90deg, #38bdf8, #fbbf24);
  }
  .btn-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 8px;
  }
  .btn-group {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .ctrl-btn {
    background: #1e293b;
    color: #f8fafc;
    border: 2px solid #475569;
    border-radius: 8px;
    padding: 5px 12px;
    font-size: 13px;
    font-weight: 800;
    font-family: inherit;
    cursor: pointer;
  }
  .ctrl-btn:hover { background: #334155; border-color: #38bdf8; }
  #time-display {
    font-family: monospace;
    font-size: 14px;
    font-weight: 700;
    color: #fef08a;
  }
</style>
</head>
<body>
<div id="theater-wrap">
  <canvas id="movie-canvas" width="1280" height="720"></canvas>
  <div id="start-overlay">
    <h1>THE SCHOLAR'S REBELLION</h1>
    <p>Room 204: Intro to Business &amp; Finance • A True Classroom Comic Story</p>
    <button id="play-hero-btn">▶ WATCH MOVIE (6:30)</button>
  </div>
  <div id="controls-bar">
    <div id="timeline-wrap" title="Click anywhere to seek">
      <div id="timeline-fill"></div>
    </div>
    <div class="btn-row">
      <div class="btn-group">
        <button id="btn-playpause" class="ctrl-btn">▶ Play</button>
        <button id="btn-restart" class="ctrl-btn">↺ Restart</button>
        <span id="time-display">00:00 / 06:30</span>
      </div>
      <div class="btn-group">
        <button id="btn-mute" class="ctrl-btn">🔊 Sound: ON</button>
        <button id="btn-cc" class="ctrl-btn">💬 Bubbles: ON</button>
        <button id="btn-speed" class="ctrl-btn">1.0x</button>
        <button id="btn-fs" class="ctrl-btn">⛶ Fullscreen</button>
      </div>
    </div>
  </div>
</div>
<script>
"""
