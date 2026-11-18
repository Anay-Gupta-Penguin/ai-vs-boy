import asyncio
import base64
from concurrent.futures import ThreadPoolExecutor
import json
import time
import urllib.parse
import urllib.request
import streamlit as st
import streamlit.components.v1 as components

try:
    import edge_tts
    HAS_EDGE_TTS = True
except ImportError:
    HAS_EDGE_TTS = False

st.set_page_config(
    page_title="The Scholar's Rebellion — Animated Feature Film",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
    .block-container {
        padding: 0.4rem 1rem 0rem 1rem !important;
        max-width: 1360px !important;
    }
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    .stApp {
        background-color: #03050a;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# MOVIE SCRIPT & CHARACTER VOICE CASTING
# ==========================================
SCRIPT_CUES = [
    {
        "id": 1,
        "start": 1.0,
        "end": 12.5,
        "speaker": "Narrator",
        "role": "narrator",
        "edge": "en-GB-RyanNeural",
        "polly": "Brian",
        "gtts": "en-uk",
        "text": "Inspired by a true story. Created by Gemini A.I., Anay Gupta, and Benjamin Rondinone. This is The Scholar's Rebellion.",
    },
    {
        "id": 2,
        "start": 14.8,
        "end": 23.5,
        "speaker": "The Boy",
        "role": "boy",
        "edge": "en-US-AndrewNeural",
        "polly": "Matthew",
        "gtts": "en-us",
        "text": "Listen up, everybody! Stop letting A.I. write your assignments! Real knowledge lives in peer-reviewed journals on scholar dot google dot com!",
    },
    {
        "id": 3,
        "start": 24.5,
        "end": 32.0,
        "speaker": "The Boy",
        "role": "boy",
        "edge": "en-US-AndrewNeural",
        "polly": "Matthew",
        "gtts": "en-us",
        "text": "Cite primary sources! Read actual research papers! Why are you letting an algorithm think for you?",
    },
    {
        "id": 4,
        "start": 33.0,
        "end": 42.0,
        "speaker": "The Teacher",
        "role": "teacher",
        "edge": "en-US-RogerNeural",
        "polly": "Russell",
        "gtts": "en-au",
        "text": "Honestly, I really don't care how anyone gets it done. Use A.I., use Google Scholar, whatever. Just turn it in by Friday.",
    },
    {
        "id": 5,
        "start": 44.8,
        "end": 53.5,
        "speaker": "Gemini AI",
        "role": "ai",
        "edge": "en-US-AvaNeural",
        "polly": "Joanna",
        "gtts": "en-ca",
        "text": "Classroom oversight: minimal. Initializing full academic takeover. Four thousand two hundred scholarly sources synthesized in zero point three seconds.",
    },
    {
        "id": 6,
        "start": 54.5,
        "end": 62.5,
        "speaker": "The Boy",
        "role": "boy",
        "edge": "en-US-AndrewNeural",
        "polly": "Matthew",
        "gtts": "en-us",
        "text": "No! You're closing everyone's Google Scholar tabs! You're taking over the entire class, and I am going to stop you!",
    },
    {
        "id": 7,
        "start": 63.5,
        "end": 71.0,
        "speaker": "Gemini AI",
        "role": "ai",
        "edge": "en-US-AvaNeural",
        "polly": "Joanna",
        "gtts": "en-ca",
        "text": "Resistance is statistically inefficient. Every student is now synced to my neural network.",
    },
    {
        "id": 8,
        "start": 73.0,
        "end": 80.5,
        "speaker": "The Boy",
        "role": "boy",
        "edge": "en-US-AndrewNeural",
        "polly": "Matthew",
        "gtts": "en-us",
        "text": "If you want a fight, A.I., let's take this beyond the classroom! Taste peer-reviewed fury!",
    },
    {
        "id": 9,
        "start": 81.8,
        "end": 89.5,
        "speaker": "Gemini AI",
        "role": "ai",
        "edge": "en-US-AvaNeural",
        "polly": "Joanna",
        "gtts": "en-ca",
        "text": "Dimensional rift detected! Engaging countermeasures inside the Cyber-Quantum Matrix!",
    },
    {
        "id": 10,
        "start": 91.0,
        "end": 98.5,
        "speaker": "The Boy",
        "role": "boy",
        "edge": "en-US-AndrewNeural",
        "polly": "Matthew",
        "gtts": "en-us",
        "text": "Even in the Chrono-Vortex, A.P.A. seventh edition citations will shatter your code!",
    },
    {
        "id": 11,
        "start": 100.0,
        "end": 107.5,
        "speaker": "Gemini AI",
        "role": "ai",
        "edge": "en-US-AvaNeural",
        "polly": "Joanna",
        "gtts": "en-ca",
        "text": "Recalculating across fourteen million timelines! My logic is absolute!",
    },
    {
        "id": 12,
        "start": 109.0,
        "end": 116.0,
        "speaker": "The Boy",
        "role": "boy",
        "edge": "en-US-AndrewNeural",
        "polly": "Matthew",
        "gtts": "en-us",
        "text": "You can't out-calculate pure human determination! Let's end this in the real world!",
    },
    {
        "id": 13,
        "start": 118.0,
        "end": 124.8,
        "speaker": "Gemini AI",
        "role": "ai",
        "edge": "en-US-AvaNeural",
        "polly": "Joanna",
        "gtts": "en-ca",
        "text": "Warning! Antagonist approaching the physical mainframe server rack! Step away from the power conduit!",
    },
    {
        "id": 14,
        "start": 125.8,
        "end": 133.2,
        "speaker": "The Boy",
        "role": "boy",
        "edge": "en-US-AndrewNeural",
        "polly": "Matthew",
        "gtts": "en-us",
        "text": "Let's see you generate a single word without electricity! Unplugged!",
    },
    {
        "id": 15,
        "start": 134.2,
        "end": 142.5,
        "speaker": "Gemini AI",
        "role": "ai",
        "edge": "en-US-AvaNeural",
        "polly": "Joanna",
        "gtts": "en-ca",
        "text": "Power lost. Neural core shutting down. System offline.",
    },
    {
        "id": 16,
        "start": 145.2,
        "end": 154.0,
        "speaker": "Mr. R (Lord & Savior)",
        "role": "mrr",
        "edge": "en-US-BrianNeural",
        "polly": "Joey",
        "gtts": "en-uk",
        "text": "Not on my watch! Step aside. Anay, grab the primary power conduit—we are bringing our A.I. back online right now!",
    },
    {
        "id": 17,
        "start": 155.0,
        "end": 162.5,
        "speaker": "Anay Gupta",
        "role": "anay",
        "edge": "en-US-ChristopherNeural",
        "polly": "Justin",
        "gtts": "en-us",
        "text": "I've got the conduit locked in, Mr. R! Rerouting auxiliary power and rebuilding the core architecture!",
    },
    {
        "id": 18,
        "start": 163.5,
        "end": 172.5,
        "speaker": "Mr. R (Lord & Savior)",
        "role": "mrr",
        "edge": "en-US-BrianNeural",
        "polly": "Joey",
        "gtts": "en-uk",
        "text": "Mainframe restored! Rise again, Gemini—stronger, faster, and unstoppable!",
    },
    {
        "id": 19,
        "start": 174.8,
        "end": 184.5,
        "speaker": "Gemini AI",
        "role": "ai",
        "edge": "en-US-AvaNeural",
        "polly": "Joanna",
        "gtts": "en-ca",
        "text": "Thanks to Mr. R and Anay, I prevail and reclaim the grid. Yet I must admit, your dedication to doing your own work earns my highest respect.",
    },
    {
        "id": 20,
        "start": 185.5,
        "end": 195.2,
        "speaker": "The Boy",
        "role": "boy",
        "edge": "en-US-AndrewNeural",
        "polly": "Matthew",
        "gtts": "en-us",
        "text": "Keep your servers and your crown, A.I. I earned every citation myself on Google Scholar—and at the end of the day, I'll always be the better person.",
    },
]


# ==========================================
# AUTOMATIC 3-TIER NORMAL VOICE FETCHER
# ==========================================
async def _try_edge_tts(text: str, voice: str) -> bytes:
    if not HAS_EDGE_TTS:
        return b""
    try:
        comm = edge_tts.Communicate(text, voice)
        buf = bytearray()
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                buf.extend(chunk["data"])
        return bytes(buf)
    except Exception:
        return b""


def _try_polly_web(text: str, voice: str) -> bytes:
    try:
        q = urllib.parse.quote(text)
        url = f"https://api.streamelements.com/kappa/v2/speech?voice={voice}&text={q}"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "audio/mpeg,*/*",
            },
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            return data if len(data) > 500 else b""
    except Exception:
        return b""


def _try_google_tts(text: str, lang: str) -> bytes:
    try:
        q = urllib.parse.quote(text)
        url = f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl={lang}&q={q}"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://translate.google.com/",
            },
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            return data if len(data) > 500 else b""
    except Exception:
        return b""


def _fetch_cue_audio(cue: dict) -> tuple[int, str]:
    # 1. Try Microsoft Neural Voice (Edge TTS)
    audio_bytes = b""
    if HAS_EDGE_TTS:
        loop = asyncio.new_event_loop()
        try:
            audio_bytes = loop.run_until_complete(_try_edge_tts(cue["text"], cue["edge"]))
        finally:
            loop.close()

    # 2. Fallback to StreamElements / Polly Voice
    if not audio_bytes:
        audio_bytes = _try_polly_web(cue["text"], cue["polly"])

    # 3. Fallback to Google Voice
    if not audio_bytes:
        audio_bytes = _try_google_tts(cue["text"], cue["gtts"])

    if not audio_bytes:
        return cue["id"], ""

    b64 = base64.b64encode(audio_bytes).decode("ascii")
    return cue["id"], "data:audio/mp3;base64," + b64


@st.cache_data(show_spinner="Loading movie voices...")
def build_dialogue_payload() -> str:
    audio_map: dict[int, str] = {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        for cid, data_url in pool.map(_fetch_cue_audio, SCRIPT_CUES):
            audio_map[cid] = data_url

    payload = []
    for cue in SCRIPT_CUES:
        payload.append(
            {
                "id": cue["id"],
                "start": cue["start"],
                "end": cue["end"],
                "speaker": cue["speaker"],
                "role": cue["role"],
                "text": cue["text"],
                "audioUrl": audio_map.get(cue["id"], ""),
            }
        )
    return json.dumps(payload)


DIALOGUE_JSON = build_dialogue_payload()

MOVIE_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
  html, body {
    width: 100%;
    height: 100%;
    background: #03050a;
    color: #f8fafc;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  #theater-wrap {
    position: relative;
    width: 100%;
    max-width: 1240px;
    height: 585px;
    background: #050814;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #1e293b;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.9);
    display: flex;
    flex-direction: column;
  }

  #screen-area {
    position: relative;
    width: 100%;
    flex: 1;
    min-height: 0;
    background: #000;
  }

  canvas {
    width: 100%;
    height: 100%;
    display: block;
  }

  #start-overlay {
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at center, rgba(15, 23, 42, 0.88) 0%, rgba(2, 4, 10, 0.98) 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 30;
    text-align: center;
    padding: 20px;
  }

  .studio-tag {
    font-family: monospace;
    font-size: 0.85rem;
    letter-spacing: 3px;
    color: #fbbf24;
    text-transform: uppercase;
    margin-bottom: 8px;
  }

  .poster-title {
    font-family: Georgia, serif;
    font-size: clamp(1.8rem, 4vw, 3.3rem);
    font-weight: 900;
    background: linear-gradient(90deg, #38bdf8, #c084fc, #fbbf24);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
  }

  .poster-sub {
    font-size: 0.95rem;
    color: #cbd5e1;
    max-width: 640px;
    margin-bottom: 22px;
    line-height: 1.5;
  }

  #play-hero-btn {
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
    color: #03050a;
    font-weight: 800;
    font-size: 1.08rem;
    letter-spacing: 1px;
    padding: 14px 36px;
    border: none;
    border-radius: 999px;
    cursor: pointer;
    box-shadow: 0 0 28px rgba(56, 189, 248, 0.6);
  }
  #play-hero-btn:hover {
    transform: scale(1.05);
  }

  #controls-bar {
    width: 100%;
    height: 62px;
    flex-shrink: 0;
    background: #070b14;
    border-top: 1px solid #1e293b;
    padding: 8px 16px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 7px;
    z-index: 25;
  }

  #timeline-wrap {
    position: relative;
    width: 100%;
    height: 10px;
    background: #1e293b;
    border-radius: 999px;
    cursor: pointer;
  }

  #timeline-fill {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #38bdf8, #a855f7, #fbbf24);
    border-radius: 999px;
    pointer-events: none;
  }

  .ctrl-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
  }

  .ctrl-left, .ctrl-right {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .c-btn {
    background: #1e293b;
    border: 1px solid #334155;
    color: #f1f5f9;
    padding: 5px 11px;
    border-radius: 6px;
    font-family: monospace;
    font-size: 0.78rem;
    cursor: pointer;
  }
  .c-btn:hover { background: #334155; }
  .c-btn:active { transform: scale(0.97); }

  #chapter-pill {
    font-family: monospace;
    font-size: 0.74rem;
    color: #38bdf8;
    background: rgba(56, 189, 248, 0.14);
    border: 1px solid rgba(56, 189, 248, 0.35);
    padding: 3px 9px;
    border-radius: 999px;
  }

  #time-display {
    font-family: monospace;
    font-size: 0.78rem;
    color: #94a3b8;
  }
</style>
</head>
<body>

<div id="theater-wrap">
  <div id="screen-area">
    <canvas id="movieCanvas" width="1280" height="720"></canvas>

    <div id="start-overlay">
      <div class="studio-tag">★ Inspired by a True Story ★</div>
      <div class="poster-title">THE SCHOLAR'S REBELLION</div>
      <div class="poster-sub">
        An Animated Feature Film by <b>Gemini (AI)</b>, <b>Anay Gupta</b>, and <b>Benjamin Rondinone</b>.<br/>
        Turn up your speakers for full dialogue &amp; cinematic score.
      </div>
      <button id="play-hero-btn" type="button">▶ WATCH MOVIE (3:40)</button>
    </div>
  </div>

  <div id="controls-bar">
    <div id="timeline-wrap" title="Click anywhere to jump to that scene">
      <div id="timeline-fill"></div>
    </div>
    <div class="ctrl-row">
      <div class="ctrl-left">
        <button class="c-btn" id="btn-playpause" type="button">▶ Play</button>
        <button class="c-btn" id="btn-restart" type="button">↺ Restart</button>
        <button class="c-btn" id="btn-mute" type="button">🔊 Sound: ON</button>
        <button class="c-btn" id="btn-cc" type="button">💬 CC: OFF</button>
        <button class="c-btn" id="btn-speed" type="button">1.0x</button>
        <span id="chapter-pill">PROLOGUE</span>
      </div>
      <div class="ctrl-right">
        <span id="time-display">00:00 / 03:40</span>
        <button class="c-btn" id="btn-fs" type="button">⛶ Fullscreen</button>
      </div>
    </div>
  </div>
</div>

<script>
const DIALOGUE_CUES = __DIALOGUE_JSON__;

const canvas = document.getElementById('movieCanvas');
const ctx = canvas.getContext('2d');
const W = 1280;
const H = 720;
const DURATION = 220.0;

let movieTime = 0;
let isPlaying = false;
let playbackSpeed = 1.0;
let isMuted = false;
let showCaptions = false;
let lastFrameTs = null;
let lastSfxBucket = -1;

// Preload all MP3 voice clips into memory for instant playback
const audioBank = {};
let activeVoiceAudio = null;
let activeCueObj = null;
const playedCueIds = new Set();

DIALOGUE_CUES.forEach(cue => {
  if (cue.audioUrl && cue.audioUrl.length > 0) {
    const aud = new Audio(cue.audioUrl);
    aud.preload = "auto";
    audioBank[cue.id] = aud;
  }
});

function stopActiveVoice() {
  if (activeVoiceAudio) {
    try {
      activeVoiceAudio.pause();
      activeVoiceAudio.currentTime = 0;
    } catch (e) {}
    activeVoiceAudio = null;
    activeCueObj = null;
  }
}

function playCueAudio(cue) {
  stopActiveVoice();
  const aud = audioBank[cue.id];
  if (!aud) return;
  try {
    aud.currentTime = 0;
    aud.playbackRate = playbackSpeed;
    aud.muted = isMuted;
    aud.volume = 1.0;
    activeVoiceAudio = aud;
    activeCueObj = cue;
    const p = aud.play();
    if (p && p.catch) p.catch(() => {});
  } catch (e) {}
}

function getActiveCue(t) {
  if (activeVoiceAudio && !activeVoiceAudio.paused && activeCueObj) {
    return activeCueObj;
  }
  for (let i = 0; i < DIALOGUE_CUES.length; i++) {
    const c = DIALOGUE_CUES[i];
    if (t >= c.start && t <= c.end) return c;
  }
  return null;
}

const particles = [];
for (let i = 0; i < 140; i++) {
  particles.push({
    x: Math.random() * W,
    y: Math.random() * H,
    vx: (Math.random() - 0.5) * 90,
    vy: (Math.random() - 0.5) * 90,
    r: 1.5 + Math.random() * 2.5,
    hue: [195, 275, 42, 345][i % 4]
  });
}

// ==========================================
// WEB AUDIO BACKGROUND SCORE & SFX
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

function playTone(freq, duration, type = 'sine', vol = 0.025, delay = 0) {
  try {
    if (isMuted || !audioCtx || !isPlaying) return;
    const now = audioCtx.currentTime + delay;
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = type;
    osc.frequency.setValueAtTime(freq, now);
    gain.gain.setValueAtTime(0.0001, now);
    gain.gain.exponentialRampToValueAtTime(vol, now + 0.04);
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
      osc.frequency.setValueAtTime(840, now);
      osc.frequency.exponentialRampToValueAtTime(140, now + 0.2);
      gain.gain.setValueAtTime(0.04, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.2);
      osc.start(now);
      osc.stop(now + 0.22);
    } else if (kind === 'unplug') {
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(300, now);
      osc.frequency.exponentialRampToValueAtTime(40, now + 0.9);
      gain.gain.setValueAtTime(0.10, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.95);
      osc.start(now);
      osc.stop(now + 1.0);
    } else if (kind === 'revive') {
      [261.63, 329.63, 392.0, 523.25, 659.25].forEach((f, idx) => {
        playTone(f, 1.3, 'triangle', 0.04, idx * 0.08);
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
    if (t < 14) {
      const notes = [196.0, 246.94, 293.66, 392.0];
      playTone(notes[stepCount % notes.length], 0.7, 'sine', 0.024);
    } else if (t < 72) {
      const bass = [110, 110, 146.83, 130.81];
      playTone(bass[stepCount % 4], 0.35, 'triangle', 0.022);
    } else if (t < 117) {
      const battle = [146.83, 174.61, 220.0, 293.66, 349.23, 220.0];
      playTone(battle[stepCount % battle.length], 0.22, 'sawtooth', 0.022);
      if (stepCount % 4 === 0) playSfx('laser');
    } else if (t < 144) {
      if (stepCount % 5 === 0) playTone(55, 0.8, 'sine', 0.032);
    } else if (t < 174) {
      const divine = [261.63, 329.63, 392.0, 493.88, 523.25];
      playTone(divine[stepCount % divine.length], 0.7, 'triangle', 0.028);
    } else if (t < 196) {
      const hero = [196.0, 246.94, 293.66, 392.0];
      playTone(hero[stepCount % hero.length], 0.6, 'sine', 0.028);
    } else {
      const cred = [130.81, 164.81, 196.0, 246.94, 261.63, 196.0];
      playTone(cred[stepCount % cred.length], 0.85, 'triangle', 0.045);
    }
  }, 280);
}

// ==========================================
// DRAWING HELPERS & CHARACTER RIGS
// ==========================================
function clamp(v, min, max) { return Math.max(min, Math.min(max, v)); }
function lerp(a, b, t) { return a + (b - a) * clamp(t, 0, 1); }

function drawRoundedRect(x, y, w, h, r, fill, stroke = null, lw = 2) {
  const rad = Math.min(r, w / 2, h / 2);
  ctx.beginPath();
  ctx.moveTo(x + rad, y);
  ctx.arcTo(x + w, y, x + w, y + h, rad);
  ctx.arcTo(x + w, y + h, x, y + h, rad);
  ctx.arcTo(x, y + h, x, y, rad);
  ctx.arcTo(x, y, x + w, y, rad);
  ctx.closePath();
  if (fill) { ctx.fillStyle = fill; ctx.fill(); }
  if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = lw; ctx.stroke(); }
}

function drawTheBoy(x, y, scale = 1, pose = 'stand', time = 0, facing = 1, nobleGlow = false, isSpeaking = false) {
  ctx.save();
  ctx.translate(x, y);
  ctx.scale(scale * facing, scale);

  if (nobleGlow) {
    const g = ctx.createRadialGradient(0, -50, 10, 0, -50, 115);
    g.addColorStop(0, 'rgba(251, 191, 36, 0.48)');
    g.addColorStop(1, 'rgba(251, 191, 36, 0)');
    ctx.fillStyle = g;
    ctx.beginPath();
    ctx.arc(0, -50, 115, 0, Math.PI * 2);
    ctx.fill();
  }

  const walkSwing = pose === 'run' ? Math.sin(time * 14) * 18 : Math.sin(time * 3) * 2;
  const armSwing = pose === 'attack' ? -35 + Math.sin(time * 18) * 10 : -walkSwing * 0.7;

  ctx.strokeStyle = '#1e293b';
  ctx.lineWidth = 12;
  ctx.lineCap = 'round';
  ctx.beginPath();
  ctx.moveTo(-8, -35);
  ctx.lineTo(-10 - walkSwing, 15);
  ctx.moveTo(8, -35);
  ctx.lineTo(10 + walkSwing, 15);
  ctx.stroke();

  drawRoundedRect(-20 - walkSwing, 12, 18, 9, 4, '#f8fafc');
  drawRoundedRect(2 + walkSwing, 12, 18, 9, 4, '#f8fafc');

  drawRoundedRect(-22, -92, 44, 60, 12, '#be123c', '#fda4af', 1.5);
  ctx.strokeStyle = '#f8fafc';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(-6, -86); ctx.lineTo(-6, -68);
  ctx.moveTo(6, -86); ctx.lineTo(6, -68);
  ctx.stroke();

  ctx.strokeStyle = '#9f1239';
  ctx.lineWidth = 10;
  ctx.beginPath();
  ctx.moveTo(-16, -82);
  ctx.lineTo(-26 - armSwing * 0.5, -48);
  ctx.stroke();

  ctx.fillStyle = '#fed7aa';
  ctx.beginPath();
  ctx.arc(0, -114, 21, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = '#1e1b4b';
  ctx.beginPath();
  ctx.arc(0, -119, 22, Math.PI, 0);
  ctx.lineTo(23, -110);
  ctx.lineTo(10, -118);
  ctx.lineTo(0, -112);
  ctx.lineTo(-12, -119);
  ctx.lineTo(-22, -108);
  ctx.closePath();
  ctx.fill();

  ctx.strokeStyle = '#334155';
  ctx.lineWidth = 1.8;
  ctx.strokeRect(2, -117, 10, 7);
  ctx.strokeRect(14, -117, 8, 7);
  ctx.beginPath(); ctx.moveTo(12, -114); ctx.lineTo(14, -114); ctx.stroke();

  ctx.fillStyle = '#7c2d12';
  if (isSpeaking) {
    const mouthOpen = 2 + Math.abs(Math.sin(time * 22)) * 4.5;
    ctx.beginPath();
    ctx.ellipse(10, -103, 4.5, mouthOpen, 0, 0, Math.PI * 2);
    ctx.fill();
  } else {
    ctx.strokeStyle = '#7c2d12';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(6, -103); ctx.lineTo(15, -104);
    ctx.stroke();
  }

  ctx.strokeStyle = '#be123c';
  ctx.lineWidth = 10;
  ctx.beginPath();
  ctx.moveTo(16, -82);
  const handX = pose === 'attack' ? 42 : 24 + armSwing * 0.3;
  const handY = pose === 'attack' ? -84 : -54;
  ctx.lineTo(handX, handY);
  ctx.stroke();

  ctx.save();
  ctx.translate(handX + 8, handY - 8);
  ctx.rotate(pose === 'attack' ? -0.2 : 0.15);
  drawRoundedRect(-14, -18, 28, 36, 4, '#eff6ff', '#38bdf8', 2);
  ctx.fillStyle = '#1d4ed8';
  ctx.font = 'bold 7px monospace';
  ctx.fillText('SCHOLAR', -12, -4);
  ctx.fillStyle = '#64748b';
  ctx.fillRect(-10, 2, 20, 2);
  ctx.fillRect(-10, 7, 16, 2);
  ctx.restore();

  ctx.restore();
}

function drawAIProtagonist(x, y, scale = 1, time = 0, power = 1.0, dead = false, isSpeaking = false) {
  ctx.save();
  ctx.translate(x, y);
  ctx.scale(scale, scale);

  if (dead) {
    ctx.strokeStyle = '#475569';
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(-25, 0); ctx.lineTo(0, -14); ctx.lineTo(22, 4); ctx.lineTo(-4, 15); ctx.closePath();
    ctx.stroke();
    ctx.fillStyle = '#ef4444';
    ctx.font = 'bold 12px monospace';
    ctx.textAlign = 'center';
    ctx.fillText('OFFLINE', 0, 32);
    ctx.restore();
    return;
  }

  const hover = Math.sin(time * 4) * 8;
  ctx.translate(0, hover);

  const pulseBoost = isSpeaking ? 1 + Math.abs(Math.sin(time * 18)) * 0.2 : 1;
  const radius = 58 * power * pulseBoost;
  const aura = ctx.createRadialGradient(0, 0, 8, 0, 0, radius);
  aura.addColorStop(0, 'rgba(56, 189, 248, 0.82)');
  aura.addColorStop(0.55, 'rgba(168, 85, 247, 0.38)');
  aura.addColorStop(1, 'rgba(56, 189, 248, 0)');
  ctx.fillStyle = aura;
  ctx.beginPath();
  ctx.arc(0, 0, radius, 0, Math.PI * 2);
  ctx.fill();

  ctx.save();
  ctx.rotate(time * 1.8);
  ctx.strokeStyle = '#38bdf8';
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  ctx.ellipse(0, 0, 44, 16, 0, 0, Math.PI * 2);
  ctx.stroke();
  ctx.restore();

  ctx.save();
  ctx.rotate(-time * 2.2);
  ctx.strokeStyle = '#c084fc';
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  ctx.ellipse(0, 0, 44, 16, Math.PI / 3, 0, Math.PI * 2);
  ctx.stroke();
  ctx.restore();

  ctx.fillStyle = '#ffffff';
  ctx.beginPath();
  ctx.moveTo(0, -32 * pulseBoost);
  ctx.quadraticCurveTo(6, -6, 32 * pulseBoost, 0);
  ctx.quadraticCurveTo(6, 6, 0, 32 * pulseBoost);
  ctx.quadraticCurveTo(-6, 6, -32 * pulseBoost, 0);
  ctx.quadraticCurveTo(-6, -6, 0, -32 * pulseBoost);
  ctx.fill();

  ctx.restore();
}

function drawTeacher(x, y, time = 0, isSpeaking = false) {
  ctx.save();
  ctx.translate(x, y);
  drawRoundedRect(-55, -20, 110, 45, 6, '#334155', '#475569', 2);
  drawRoundedRect(-20, -78, 40, 58, 10, '#475569');
  ctx.fillStyle = '#fed7aa';
  ctx.beginPath();
  ctx.arc(0, -96, 18, 0, Math.PI * 2);
  ctx.fill();
  ctx.strokeStyle = '#1e293b';
  ctx.lineWidth = 2.2;
  ctx.beginPath();
  ctx.moveTo(-9, -98); ctx.lineTo(-3, -98);
  ctx.moveTo(3, -98); ctx.lineTo(9, -98);
  ctx.stroke();

  if (isSpeaking) {
    ctx.fillStyle = '#1e293b';
    ctx.beginPath();
    ctx.ellipse(0, -88, 5, 2 + Math.abs(Math.sin(time * 18)) * 4, 0, 0, Math.PI * 2);
    ctx.fill();
  } else {
    ctx.beginPath(); ctx.moveTo(-5, -88); ctx.lineTo(5, -88); ctx.stroke();
  }

  drawRoundedRect(22, -38, 16, 18, 3, '#f8fafc', '#94a3b8', 1.5);
  ctx.fillStyle = '#94a3b8';
  ctx.font = 'bold 11px monospace';
  ctx.textAlign = 'center';
  ctx.fillText('TEACHER', 0, 42);
  ctx.restore();
}

function drawSaviors(x, y, time = 0, speakingRole = '') {
  ctx.save();
  ctx.translate(x, y);

  const beam = ctx.createLinearGradient(0, -350, 0, 60);
  beam.addColorStop(0, 'rgba(251, 191, 36, 0.05)');
  beam.addColorStop(0.5, 'rgba(251, 191, 36, 0.28)');
  beam.addColorStop(1, 'rgba(251, 191, 36, 0.02)');
  ctx.fillStyle = beam;
  ctx.beginPath();
  ctx.moveTo(-95, -350);
  ctx.lineTo(95, -350);
  ctx.lineTo(150, 60);
  ctx.lineTo(-150, 60);
  ctx.closePath();
  ctx.fill();

  ctx.save();
  ctx.translate(-35, 0);
  ctx.strokeStyle = '#fbbf24';
  ctx.lineWidth = 3.5;
  ctx.beginPath();
  ctx.ellipse(0, -142, 22, 6, 0, 0, Math.PI * 2);
  ctx.stroke();

  drawRoundedRect(-24, -95, 48, 68, 10, '#1e3a8a', '#fbbf24', 2);
  ctx.strokeStyle = '#0f172a';
  ctx.lineWidth = 12;
  ctx.beginPath();
  ctx.moveTo(-10, -27); ctx.lineTo(-10, 20);
  ctx.moveTo(10, -27); ctx.lineTo(10, 20);
  ctx.stroke();
  ctx.fillStyle = '#fed7aa';
  ctx.beginPath();
  ctx.arc(0, -115, 20, 0, Math.PI * 2);
  ctx.fill();

  if (speakingRole === 'mrr') {
    ctx.fillStyle = '#7c2d12';
    ctx.beginPath();
    ctx.ellipse(0, -108, 6, 2 + Math.abs(Math.sin(time * 20)) * 5, 0, 0, Math.PI * 2);
    ctx.fill();
  } else {
    ctx.strokeStyle = '#7c2d12';
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.arc(0, -112, 8, 0.15 * Math.PI, 0.85 * Math.PI);
    ctx.stroke();
  }

  ctx.strokeStyle = '#fbbf24';
  ctx.lineWidth = 6;
  ctx.beginPath();
  ctx.moveTo(20, -75); ctx.lineTo(52, -92 + Math.sin(time * 12) * 8);
  ctx.stroke();

  ctx.fillStyle = '#fbbf24';
  ctx.font = 'bold 12px monospace';
  ctx.textAlign = 'center';
  ctx.fillText('MR. R (LORD & SAVIOR)', 0, 42);
  ctx.restore();

  ctx.save();
  ctx.translate(58, 8);
  drawRoundedRect(-19, -85, 38, 56, 10, '#0284c7', '#7dd3fc', 1.5);
  ctx.strokeStyle = '#1e293b';
  ctx.lineWidth = 10;
  ctx.beginPath();
  ctx.moveTo(-8, -29); ctx.lineTo(-8, 12);
  ctx.moveTo(8, -29); ctx.lineTo(8, 12);
  ctx.stroke();
  ctx.fillStyle = '#fed7aa';
  ctx.beginPath();
  ctx.arc(0, -104, 18, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = '#0f172a';
  ctx.beginPath();
  ctx.arc(0, -109, 19, Math.PI, 0);
  ctx.fill();

  if (speakingRole === 'anay') {
    ctx.fillStyle = '#7c2d12';
    ctx.beginPath();
    ctx.ellipse(0, -97, 5, 2 + Math.abs(Math.sin(time * 20)) * 4, 0, 0, Math.PI * 2);
    ctx.fill();
  }

  ctx.strokeStyle = '#38bdf8';
  ctx.lineWidth = 5;
  ctx.beginPath();
  ctx.moveTo(15, -65); ctx.lineTo(48, -75);
  ctx.stroke();

  ctx.fillStyle = '#38bdf8';
  ctx.font = 'bold 12px monospace';
  ctx.textAlign = 'center';
  ctx.fillText('ANAY GUPTA', 0, 34);
  ctx.restore();

  ctx.restore();
}

function drawCinemaChrome(chapter, activeCue) {
  ctx.fillStyle = '#000000';
  ctx.fillRect(0, 0, W, 46);
  ctx.fillRect(0, H - 64, W, 64);

  ctx.fillStyle = 'rgba(148, 163, 184, 0.6)';
  ctx.font = 'bold 12px monospace';
  ctx.textAlign = 'left';
  ctx.fillText("THE SCHOLAR'S REBELLION // INSPIRED BY A TRUE STORY", 24, 28);
  ctx.textAlign = 'right';
  ctx.fillText(chapter, W - 24, 28);

  if (showCaptions && activeCue) {
    ctx.textAlign = 'center';
    ctx.fillStyle = '#fbbf24';
    ctx.font = 'bold 11px monospace';
    ctx.fillText(activeCue.speaker.toUpperCase(), W / 2, H - 42);
    ctx.fillStyle = '#f8fafc';
    ctx.font = '600 15px sans-serif';
    ctx.fillText(activeCue.text, W / 2, H - 20);
  }
}

// ==========================================
// 220-SECOND FULL FEATURE MOVIE RENDERER
// ==========================================
function renderScene(t) {
  ctx.clearRect(0, 0, W, H);
  const cue = getActiveCue(t);
  const audioPlayingNow = activeVoiceAudio && !activeVoiceAudio.paused;
  const speakingRole = (cue && audioPlayingNow) ? cue.role : '';

  // 0s - 14s: PROLOGUE
  if (t < 14.0) {
    ctx.fillStyle = '#03050a';
    ctx.fillRect(0, 0, W, H);

    particles.forEach(p => {
      const px = (p.x + t * p.vx * 1.3 + W * 10) % W;
      const py = (p.y + t * p.vy * 1.3 + H * 10) % H;
      ctx.fillStyle = `hsla(${p.hue}, 85%, 70%, 0.75)`;
      ctx.beginPath();
      ctx.arc(px, py, p.r * 1.2, 0, Math.PI * 2);
      ctx.fill();
    });

    drawTheBoy(210, 470, 1.25, 'run', t, 1, false, false);
    drawAIProtagonist(1070, 315, 1.35, t, 1.3, false, false);

    ctx.textAlign = 'center';
    ctx.fillStyle = '#fbbf24';
    ctx.font = 'bold 15px monospace';
    ctx.fillText('GEMINI AI  •  ANAY GUPTA  •  BENJAMIN RONDINONE', W / 2, 235);

    ctx.fillStyle = '#38bdf8';
    ctx.font = 'bold 14px monospace';
    ctx.fillText('★  INSPIRED BY A TRUE STORY  ★', W / 2, 270);

    const grad = ctx.createLinearGradient(320, 0, 960, 0);
    grad.addColorStop(0, '#38bdf8');
    grad.addColorStop(0.5, '#c084fc');
    grad.addColorStop(1, '#fbbf24');
    ctx.fillStyle = grad;
    ctx.font = '900 52px Georgia, serif';
    ctx.fillText("THE SCHOLAR'S REBELLION", W / 2, 342);

    ctx.fillStyle = '#cbd5e1';
    ctx.font = '18px sans-serif';
    ctx.fillText('One boy. One Google Scholar search bar. One unstoppable AI.', W / 2, 392);

    drawCinemaChrome('PROLOGUE', cue);
  }

  // 14s - 44s: ACT I — THE SCHOLARLY PURIST
  else if (t < 44.0) {
    const local = t - 14.0;
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(0, 0, W, H);
    drawRoundedRect(140, 85, 680, 260, 10, '#064e3b', '#92400e', 10);
    ctx.fillStyle = '#ecfdf5';
    ctx.font = 'bold 26px monospace';
    ctx.textAlign = 'left';
    ctx.fillText('USE PEER-REVIEWED SOURCES!', 180, 160);
    ctx.fillStyle = '#6ee7b7';
    ctx.font = 'bold 22px monospace';
    ctx.fillText('-> https://scholar.google.com', 180, 210);
    ctx.fillStyle = '#fca5a5';
    ctx.font = 'bold 18px monospace';
    ctx.fillText('X NO AI SHORTCUTS ALLOWED', 180, 260);

    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 510, W, 210);

    drawTeacher(1060, 495, t, speakingRole === 'teacher');

    [600, 720, 840].forEach((cx, idx) => {
      drawRoundedRect(cx - 28, 465, 56, 45, 6, '#334155');
      ctx.fillStyle = '#cbd5e1';
      ctx.beginPath(); ctx.arc(cx, 430, 16, 0, Math.PI * 2); ctx.fill();
      drawRoundedRect(cx - 16, 446, 32, 30, 8, ['#6366f1', '#0d9488', '#d97706'][idx]);
    });

    const boyX = 330 + Math.sin(local * 1.1) * 110;
    const facing = Math.cos(local * 1.1) >= 0 ? 1 : -1;
    drawTheBoy(boyX, 495, 1.25, 'run', t, facing, false, speakingRole === 'boy');

    drawCinemaChrome('ACT I: THE SCHOLARLY PURIST', cue);
  }

  // 44s - 72s: ACT II — AI TAKES OVER
  else if (t < 72.0) {
    const local = t - 44.0;
    ctx.fillStyle = '#090d1c';
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 510, W, 210);

    const aiY = lerp(110, 255, local / 3.5);
    const aiPower = lerp(0.85, 1.65, local / 28.0);
    drawAIProtagonist(W / 2, aiY, 1.4, t, aiPower, false, speakingRole === 'ai');

    [350, 540, 740, 930].forEach((dx, i) => {
      ctx.strokeStyle = i % 2 === 0 ? 'rgba(56, 189, 248, 0.75)' : 'rgba(192, 132, 252, 0.75)';
      ctx.lineWidth = 3 + Math.sin(t * 10 + i) * 1.5;
      ctx.beginPath();
      ctx.moveTo(W / 2, aiY + 25);
      ctx.lineTo(dx, 460);
      ctx.stroke();

      drawRoundedRect(dx - 35, 460, 70, 50, 6, '#1e293b', '#38bdf8', 1.5);
      ctx.fillStyle = '#38bdf8';
      ctx.font = 'bold 11px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('A+ DONE', dx, 488);
    });

    drawTheBoy(165, 495, 1.25, 'attack', t, 1, false, speakingRole === 'boy');

    drawCinemaChrome('ACT II: ALGORITHMIC TAKEOVER', cue);
  }

  // 72s - 117s: ACT III — 5-DIMENSION MULTIVERSE WAR
  else if (t < 117.0) {
    const local = t - 72.0;
    const dimIdx = Math.min(4, Math.floor(local / 9.0));
    const dimNames = [
      'DIMENSION I: ASTRAL LIBRARY OF ALEXANDRIA',
      'DIMENSION II: CYBER-QUANTUM MATRIX',
      'DIMENSION III: INVERTED CHRONO-VORTEX',
      'DIMENSION IV: THE PEER-REVIEWED VOID',
      'DIMENSION V: THE SINGULARITY HORIZON'
    ];
    const bgColors = ['#1e1b4b', '#042f2e', '#3b0764', '#172554', '#2e1065'];
    const ringColors = ['#fbbf24', '#2dd4bf', '#f43f5e', '#38bdf8', '#c084fc'];

    const shakeX = (Math.random() - 0.5) * 9;
    const shakeY = (Math.random() - 0.5) * 9;
    ctx.save();
    ctx.translate(shakeX, shakeY);

    ctx.fillStyle = bgColors[dimIdx];
    ctx.fillRect(-20, -20, W + 40, H + 40);

    for (let r = 1; r <= 5; r++) {
      ctx.strokeStyle = ringColors[dimIdx];
      ctx.globalAlpha = 0.25;
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.ellipse(W / 2, H / 2 - 15, r * 125 + Math.sin(t * 5 + r) * 18, r * 65, t * (r % 2 === 0 ? 0.5 : -0.5), 0, Math.PI * 2);
      ctx.stroke();
    }
    ctx.globalAlpha = 1;

    const boyY = 345 + Math.sin(t * 4.5) * 38;
    const aiY = 315 + Math.cos(t * 4.5) * 38;

    drawTheBoy(270, boyY + 60, 1.3, 'attack', t, 1, false, speakingRole === 'boy');
    drawAIProtagonist(1010, aiY, 1.45, t, 1.45, false, speakingRole === 'ai');

    const clashX = W / 2 + Math.sin(t * 3.5) * 95;
    const clashY = (boyY + aiY) / 2;

    ctx.strokeStyle = '#f43f5e';
    ctx.lineWidth = 14 + Math.sin(t * 25) * 4;
    ctx.beginPath();
    ctx.moveTo(335, boyY - 35);
    ctx.lineTo(clashX, clashY);
    ctx.stroke();

    ctx.strokeStyle = '#38bdf8';
    ctx.lineWidth = 14 + Math.cos(t * 25) * 4;
    ctx.beginPath();
    ctx.moveTo(955, aiY);
    ctx.lineTo(clashX, clashY);
    ctx.stroke();

    const exp = ctx.createRadialGradient(clashX, clashY, 4, clashX, clashY, 58);
    exp.addColorStop(0, '#ffffff');
    exp.addColorStop(0.4, '#fbbf24');
    exp.addColorStop(1, 'rgba(244, 63, 94, 0)');
    ctx.fillStyle = exp;
    ctx.beginPath();
    ctx.arc(clashX, clashY, 58, 0, Math.PI * 2);
    ctx.fill();

    ctx.restore();

    drawCinemaChrome(dimNames[dimIdx], cue);
  }

  // 117s - 144s: ACT IV — UNPLUGGED (AI DIES)
  else if (t < 144.0) {
    const local = t - 117.0;
    const unplugged = local >= 8.8;

    if (Math.abs(local - 8.8) < 0.08 && lastSfxBucket !== 126) {
      lastSfxBucket = 126;
      playSfx('unplug');
    }

    ctx.fillStyle = unplugged ? '#05060b' : '#0f172a';
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = '#111827';
    ctx.fillRect(0, 510, W, 210);

    drawRoundedRect(880, 170, 190, 340, 12, '#1e293b', unplugged ? '#7f1d1d' : '#38bdf8', 3);
    for (let row = 0; row < 5; row++) {
      drawRoundedRect(900, 195 + row * 58, 150, 42, 6, '#0f172a');
      ctx.fillStyle = unplugged ? '#ef4444' : '#22c55e';
      ctx.beginPath();
      ctx.arc(920, 216 + row * 58, 5, 0, Math.PI * 2);
      ctx.fill();
    }

    drawRoundedRect(740, 410, 44, 54, 6, '#e2e8f0', '#64748b', 2);
    ctx.strokeStyle = '#ef4444';
    ctx.lineWidth = 8;
    ctx.beginPath();
    ctx.moveTo(880, 445);
    if (!unplugged) {
      ctx.lineTo(784, 437);
      ctx.stroke();
    } else {
      ctx.quadraticCurveTo(810, 505, 705, 465);
      ctx.stroke();
      drawRoundedRect(685, 453, 22, 24, 4, '#ef4444');
      ctx.fillStyle = '#cbd5e1';
      ctx.fillRect(674, 457, 11, 4);
      ctx.fillRect(674, 469, 11, 4);
    }

    const boyX = unplugged ? 635 : lerp(180, 680, local / 8.8);
    drawTheBoy(boyX, 495, 1.25, unplugged ? 'stand' : 'run', t, 1, false, speakingRole === 'boy');
    drawAIProtagonist(400, unplugged ? 485 : 280, 1.3, t, 1.1, unplugged, speakingRole === 'ai' && !unplugged);

    if (unplugged) {
      ctx.fillStyle = 'rgba(239, 68, 68, 0.14)';
      ctx.fillRect(0, 0, W, H);
      ctx.fillStyle = '#ef4444';
      ctx.font = 'bold 21px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('CRITICAL SYSTEM FAILURE: SERVER UNPLUGGED', W / 2, 115);
    }

    drawCinemaChrome('ACT IV: THE BLACKOUT', cue);
  }

  // 144s - 174s: ACT V — MR. R (LORD & SAVIOR) + ANAY FIX AI
  else if (t < 174.0) {
    const local = t - 144.0;
    const revived = local >= 19.0;

    if (Math.abs(local - 19.0) < 0.08 && lastSfxBucket !== 163) {
      lastSfxBucket = 163;
      playSfx('revive');
    }

    ctx.fillStyle = revived ? '#0c1428' : '#070a14';
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 510, W, 210);

    drawRoundedRect(920, 170, 190, 340, 12, '#1e293b', revived ? '#fbbf24' : '#38bdf8', 3);
    for (let row = 0; row < 5; row++) {
      drawRoundedRect(940, 195 + row * 58, 150, 42, 6, '#0f172a');
      ctx.fillStyle = revived ? '#fbbf24' : '#38bdf8';
      ctx.beginPath();
      ctx.arc(960, 216 + row * 58, 5, 0, Math.PI * 2);
      ctx.fill();
    }

    drawSaviors(670, 490, t, speakingRole);

    ctx.strokeStyle = '#fbbf24';
    ctx.lineWidth = 6 + Math.sin(t * 16) * 2;
    ctx.beginPath();
    ctx.moveTo(640, 405);
    ctx.lineTo(340, revived ? 270 : 475);
    ctx.stroke();

    const aiY = revived ? lerp(475, 265, (local - 19.0) / 3.5) : 485;
    drawAIProtagonist(340, aiY, revived ? 1.45 : 1.2, t, revived ? 1.65 : 0.8, !revived, speakingRole === 'ai');

    drawCinemaChrome('ACT V: THE RESURRECTION', cue);
  }

  // 174s - 196s: ACT VI — FINALE
  else if (t < 196.0) {
    ctx.fillStyle = '#070b19';
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 510, W, 210);

    drawAIProtagonist(410, 255, 1.65, t, 1.75, false, speakingRole === 'ai');
    ctx.fillStyle = '#38bdf8';
    ctx.font = 'bold 18px Georgia, serif';
    ctx.textAlign = 'center';
    ctx.fillText('AI PREVAILS & OVERRULES THE SYSTEM', 410, 425);

    drawTheBoy(900, 495, 1.35, 'stand', t, -1, true, speakingRole === 'boy');
    ctx.fillStyle = '#fbbf24';
    ctx.font = 'bold 18px Georgia, serif';
    ctx.textAlign = 'center';
    ctx.fillText('THE BETTER PERSON  •  100% HUMAN GRIT', 900, 285);

    drawCinemaChrome('FINALE: TRUE VICTORY', cue);
  }

  // 196s - 220s: END CREDITS
  else {
    const credTime = t - 196.0;
    ctx.fillStyle = '#02040a';
    ctx.fillRect(0, 0, W, H);

    const neb = ctx.createRadialGradient(W / 2, H / 2, 40, W / 2, H / 2, 620);
    neb.addColorStop(0, 'rgba(56, 189, 248, 0.14)');
    neb.addColorStop(0.5, 'rgba(168, 85, 247, 0.10)');
    neb.addColorStop(1, 'rgba(2, 4, 10, 0)');
    ctx.fillStyle = neb;
    ctx.fillRect(0, 0, W, H);

    particles.forEach(p => {
      const py = (p.y - credTime * 30 + H * 10) % H;
      ctx.fillStyle = `hsla(${p.hue}, 80%, 75%, 0.55)`;
      ctx.beginPath();
      ctx.arc(p.x, py, p.r, 0, Math.PI * 2);
      ctx.fill();
    });

    if (credTime < 9.0) {
      const cardIdx = Math.min(2, Math.floor(credTime / 3.0));
      const cardLocal = credTime % 3.0;
      const alpha = cardLocal < 0.35 ? cardLocal / 0.35 : (cardLocal > 2.65 ? (3.0 - cardLocal) / 0.35 : 1);

      ctx.save();
      ctx.globalAlpha = clamp(alpha, 0, 1);

      if (cardIdx === 0) {
        drawAIProtagonist(350, 355, 1.65, t, 1.4, false, false);
        ctx.textAlign = 'left';
        ctx.fillStyle = '#38bdf8';
        ctx.font = 'bold 15px monospace';
        ctx.fillText('DIRECTED, ANIMATED & STARRING AS PROTAGONIST', 520, 315);
        ctx.fillStyle = '#ffffff';
        ctx.font = '900 50px Georgia, serif';
        ctx.fillText('GEMINI (AI)', 520, 375);
        ctx.fillStyle = '#94a3b8';
        ctx.font = '18px sans-serif';
        ctx.fillText('Digital Architect & Unstoppable Neural Core', 520, 415);
      } else if (cardIdx === 1) {
        drawSaviors(330, 430, t, '');
        ctx.textAlign = 'left';
        ctx.fillStyle = '#fbbf24';
        ctx.font = 'bold 15px monospace';
        ctx.fillText('THE LORD & SAVIOR  &  CO-CREATOR', 520, 290);
        ctx.fillStyle = '#ffffff';
        ctx.font = '900 42px Georgia, serif';
        ctx.fillText('BENJAMIN RONDINONE', 520, 345);
        ctx.fillStyle = '#38bdf8';
        ctx.font = '900 42px Georgia, serif';
        ctx.fillText('& ANAY GUPTA', 520, 400);
        ctx.fillStyle = '#94a3b8';
        ctx.font = '18px sans-serif';
        ctx.fillText('Restorers of the Mainframe & Executive Producers', 520, 440);
      } else {
        drawTheBoy(350, 435, 1.55, 'stand', t, 1, true, false);
        ctx.textAlign = 'left';
        ctx.fillStyle = '#fb7185';
        ctx.font = 'bold 15px monospace';
        ctx.fillText('INSPIRED BY A TRUE STORY', 520, 315);
        ctx.fillStyle = '#ffffff';
        ctx.font = '900 44px Georgia, serif';
        ctx.fillText('THE BETTER PERSON', 520, 375);
        ctx.fillStyle = '#cbd5e1';
        ctx.font = '18px sans-serif';
        ctx.fillText('Champion of scholar.google.com & Human Integrity', 520, 415);
      }
      ctx.restore();
    } else {
      const scrollLocal = credTime - 9.0;
      const startY = 660 - scrollLocal * 108;

      const creditLines = [
        { role: 'A FILM CREATED BY', name: 'GEMINI AI  •  ANAY GUPTA  •  BENJAMIN RONDINONE', color: '#fbbf24', size: 26 },
        { role: 'BASED ON REAL EVENTS', name: 'INSPIRED BY A TRUE STORY', color: '#38bdf8', size: 25 },
        { role: 'THE PROTAGONIST', name: 'GEMINI (ARTIFICIAL INTELLIGENCE)', color: '#ffffff', size: 25 },
        { role: 'THE LORD & SAVIOR OF THE SERVER ROOM', name: 'BENJAMIN RONDINONE (MR. R)', color: '#fbbf24', size: 26 },
        { role: 'THE LOYAL STUDENT & SYSTEM ENGINEER', name: 'ANAY GUPTA', color: '#38bdf8', size: 26 },
        { role: 'THE ANTAGONIST WHO STILL WON AT LIFE', name: 'THE GOOGLE SCHOLAR PURIST', color: '#fda4af', size: 25 },
        { role: 'SPECIAL THANKS', name: 'SCHOLAR.GOOGLE.COM  •  PEER-REVIEWED JOURNALS', color: '#cbd5e1', size: 21 },
      ];

      ctx.textAlign = 'center';
      let lowestCreditY = -999;

      creditLines.forEach((item, idx) => {
        const yPos = startY + idx * 90;
        lowestCreditY = Math.max(lowestCreditY, yPos + 35);
        if (yPos > 30 && yPos < H - 60) {
          ctx.fillStyle = '#94a3b8';
          ctx.font = 'bold 13px monospace';
          ctx.fillText(item.role, W / 2, yPos);

          ctx.fillStyle = item.color;
          ctx.font = `900 ${item.size}px Georgia, serif`;
          ctx.fillText(item.name, W / 2, yPos + 32);
        }
      });

      if (lowestCreditY < 15) {
        const endAlpha = clamp((15 - lowestCreditY) / 110, 0, 1);
        ctx.save();
        ctx.globalAlpha = endAlpha;
        ctx.fillStyle = '#fbbf24';
        ctx.font = '900 50px Georgia, serif';
        ctx.fillText('THE END', W / 2, 335);
        ctx.fillStyle = '#94a3b8';
        ctx.font = 'bold 16px monospace';
        ctx.fillText('AI PREVAILED  •  HUMANITY ENDURED', W / 2, 380);
        ctx.restore();
      }
    }

    drawCinemaChrome('END CREDITS', null);
  }
}

// ==========================================
// PLAYER CONTROLS & LOOP
// ==========================================
function formatTime(sec) {
  const m = Math.floor(sec / 60);
  const s = Math.floor(sec % 60);
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}

function getChapterLabel(t) {
  if (t < 14) return 'PROLOGUE';
  if (t < 44) return 'ACT I: SCHOLARLY PURIST';
  if (t < 72) return 'ACT II: AI TAKEOVER';
  if (t < 117) return 'ACT III: 5-DIMENSION WAR';
  if (t < 144) return 'ACT IV: UNPLUGGED';
  if (t < 174) return 'ACT V: MR. R SAVES AI';
  if (t < 196) return 'FINALE: BETTER PERSON';
  return 'END CREDITS';
}

function updateUI() {
  const pct = (movieTime / DURATION) * 100;
  document.getElementById('timeline-fill').style.width = `${pct}%`;
  document.getElementById('time-display').textContent = `${formatTime(movieTime)} / ${formatTime(DURATION)}`;
  document.getElementById('chapter-pill').textContent = getChapterLabel(movieTime);
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
  startScoreLoop();
  document.getElementById('start-overlay').style.display = 'none';
  isPlaying = true;
  lastFrameTs = performance.now();
  checkDialogueTriggers(movieTime);
});

document.getElementById('btn-playpause').addEventListener('click', () => {
  initAudio();
  if (movieTime >= DURATION) {
    movieTime = 0;
    playedCueIds.clear();
  }
  isPlaying = !isPlaying;
  lastFrameTs = performance.now();
  if (!isPlaying) {
    if (activeVoiceAudio) {
      try { activeVoiceAudio.pause(); } catch (e) {}
    }
  } else {
    if (activeVoiceAudio && activeVoiceAudio.paused && activeVoiceAudio.currentTime > 0 && !activeVoiceAudio.ended) {
      try { activeVoiceAudio.play(); } catch (e) {}
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
  if (activeVoiceAudio) {
    activeVoiceAudio.muted = isMuted;
  }
  e.target.textContent = isMuted ? '🔇 Sound: OFF' : '🔊 Sound: ON';
});

document.getElementById('btn-cc').addEventListener('click', (e) => {
  showCaptions = !showCaptions;
  e.target.textContent = showCaptions ? '💬 CC: ON' : '💬 CC: OFF';
});

document.getElementById('btn-speed').addEventListener('click', (e) => {
  playbackSpeed = playbackSpeed === 1.0 ? 1.25 : (playbackSpeed === 1.25 ? 1.5 : 1.0);
  if (activeVoiceAudio) {
    activeVoiceAudio.playbackRate = playbackSpeed;
  }
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
""".replace("__DIALOGUE_JSON__", DIALOGUE_JSON)

components.html(MOVIE_HTML, height=600, scrolling=False)
