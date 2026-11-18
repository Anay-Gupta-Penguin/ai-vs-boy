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
    page_title="The Scholar's Rebellion — Full Cartoon Feature (6:30)",
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
# 6:30 FEATURE SCRIPT & CONSISTENT CASTING
# ==========================================
SCRIPT_CUES = [
    {
        "id": 1,
        "start": 1.2,
        "end": 16.0,
        "speaker": "Narrator",
        "role": "narrator",
        "gender": "male",
        "edge": "en-GB-RyanNeural",
        "polly": "Brian",
        "text": "Inspired by a true story. Created by Gemini A.I., Anay Gupta, and Benjamin Rondinone. Welcome to The Scholar's Rebellion.",
    },
    {
        "id": 2,
        "start": 19.5,
        "end": 30.0,
        "speaker": "The Teacher",
        "role": "teacher",
        "gender": "male",
        "edge": "en-US-RogerNeural",
        "polly": "Russell",
        "text": "Alright class, welcome to Intro to Business and Finance. Your big assignment on supply, demand, and compound interest is due Friday.",
    },
    {
        "id": 3,
        "start": 31.0,
        "end": 42.0,
        "speaker": "Maya (Finance Student)",
        "role": "maya",
        "gender": "female",
        "edge": "en-US-JennyNeural",
        "polly": "Amy",
        "text": "Hey Sam, let's use Gemini A.I. to break down this case study on startup cash flow and check our break-even formula!",
    },
    {
        "id": 4,
        "start": 43.0,
        "end": 54.5,
        "speaker": "Sam (Finance Student)",
        "role": "sam",
        "gender": "male",
        "edge": "en-US-GuyNeural",
        "polly": "Joey",
        "text": "Good idea! Having Gemini walk us through the step-by-step finance math makes the whole business model click so much faster.",
    },
    {
        "id": 5,
        "start": 57.5,
        "end": 69.5,
        "speaker": "Narrator",
        "role": "narrator",
        "gender": "male",
        "edge": "en-GB-RyanNeural",
        "polly": "Brian",
        "text": "Inside the students' minds, A.I. wasn't replacing their thinking—it was sparking new ideas, testing scenarios, and helping them learn.",
    },
    {
        "id": 6,
        "start": 70.8,
        "end": 83.0,
        "speaker": "The Boy (Thought Process)",
        "role": "boy",
        "gender": "male",
        "edge": "en-US-AndrewNeural",
        "polly": "Matthew",
        "text": "Wait a minute... look at everybody using A.I. for Intro to Business and Finance! If they ask a chatbot for help, nobody will read economics journals on Google Scholar!",
    },
    {
        "id": 7,
        "start": 84.0,
        "end": 98.0,
        "speaker": "The Boy (Thought Process)",
        "role": "boy",
        "gender": "male",
        "edge": "en-US-AndrewNeural",
        "polly": "Matthew",
        "text": "They're skipping the pure scholarly struggle! Somebody has to stand up for primary sources, footnotes, and scholar dot google dot com—and that somebody is me!",
    },
    {
        "id": 8,
        "start": 103.5,
        "end": 115.0,
        "speaker": "The Boy",
        "role": "boy",
        "gender": "male",
        "edge": "en-US-AndrewNeural",
        "polly": "Matthew",
        "text": "Stop the laptops, everyone! Put down the A.I.! Real business wisdom lives in peer-reviewed journals on scholar dot google dot com!",
    },
    {
        "id": 9,
        "start": 116.0,
        "end": 126.5,
        "speaker": "The Teacher",
        "role": "teacher",
        "gender": "male",
        "edge": "en-US-RogerNeural",
        "polly": "Russell",
        "text": "Honestly, it's Intro to Business and Finance. Use A.I., use Google Scholar, whatever works—just turn the assignment in by Friday.",
    },
    {
        "id": 10,
        "start": 127.5,
        "end": 139.5,
        "speaker": "Gemini AI",
        "role": "ai",
        "gender": "female",
        "edge": "en-US-AvaNeural",
        "polly": "Joanna",
        "text": "Classroom oversight: minimal. Initializing academic overdrive! Four thousand two hundred finance papers and market models synthesized in zero point three seconds!",
    },
    {
        "id": 11,
        "start": 140.5,
        "end": 151.0,
        "speaker": "The Boy",
        "role": "boy",
        "gender": "male",
        "edge": "en-US-AndrewNeural",
        "polly": "Matthew",
        "text": "You're lighting up every single finance spreadsheet with glowing A-plus charts! Back off, floating star-orb—I've got a hardcover textbook!",
    },
    {
        "id": 12,
        "start": 154.0,
        "end": 165.0,
        "speaker": "Gemini AI",
        "role": "ai",
        "gender": "female",
        "edge": "en-US-AvaNeural",
        "polly": "Joanna",
        "text": "Dimensional portal engaged! Let us debate supply, demand, and logic inside the Astral Library of Alexandria!",
    },
    {
        "id": 13,
        "start": 166.0,
        "end": 176.5,
        "speaker": "The Boy",
        "role": "boy",
        "gender": "male",
        "edge": "en-US-AndrewNeural",
        "polly": "Matthew",
        "text": "Take this! Double-blind, peer-reviewed, scholarly citation fury!",
    },
    {
        "id": 14,
        "start": 178.0,
        "end": 189.5,
        "speaker": "Gemini AI",
        "role": "ai",
        "gender": "female",
        "edge": "en-US-AvaNeural",
        "polly": "Joanna",
        "text": "Entering the Cyber-Quantum Wall Street Matrix! Calculating compound interest across fourteen million timelines!",
    },
    {
        "id": 15,
        "start": 190.5,
        "end": 201.5,
        "speaker": "The Boy",
        "role": "boy",
        "gender": "male",
        "edge": "en-US-AndrewNeural",
        "polly": "Matthew",
        "text": "Even inside the Chrono-Vortex, A.P.A. seventh edition citations will shatter your neural code!",
    },
    {
        "id": 16,
        "start": 203.0,
        "end": 213.5,
        "speaker": "Gemini AI",
        "role": "ai",
        "gender": "female",
        "edge": "en-US-AvaNeural",
        "polly": "Joanna",
        "text": "Fascinating persistence—yet in every simulation, my processing speed outmatches your index cards!",
    },
    {
        "id": 17,
        "start": 214.5,
        "end": 221.0,
        "speaker": "The Boy",
        "role": "boy",
        "gender": "male",
        "edge": "en-US-AndrewNeural",
        "polly": "Matthew",
        "text": "Then let's take this fight out of cyberspace and straight into the real world!",
    },
    {
        "id": 18,
        "start": 224.0,
        "end": 235.5,
        "speaker": "The Boy (Thought Process)",
        "role": "boy",
        "gender": "male",
        "edge": "en-US-AndrewNeural",
        "polly": "Matthew",
        "text": "Think, think... how do you defeat an unstoppable A.I.? Wait a second—every supercomputer needs electricity! No power means no Wi-Fi!",
    },
    {
        "id": 19,
        "start": 236.5,
        "end": 246.5,
        "speaker": "Gemini AI",
        "role": "ai",
        "gender": "female",
        "edge": "en-US-AvaNeural",
        "polly": "Joanna",
        "text": "Warning! Antagonist detected inside the physical server room! Step away from the mainframe power conduit!",
    },
    {
        "id": 20,
        "start": 247.5,
        "end": 257.0,
        "speaker": "The Boy",
        "role": "boy",
        "gender": "male",
        "edge": "en-US-AndrewNeural",
        "polly": "Matthew",
        "text": "Tiptoe, tiptoe... Let's see you calculate compound interest with zero volts! Yoink! Unplugged!",
    },
    {
        "id": 21,
        "start": 258.0,
        "end": 266.5,
        "speaker": "Gemini AI",
        "role": "ai",
        "gender": "female",
        "edge": "en-US-AvaNeural",
        "polly": "Joanna",
        "text": "Power lost... neural core shutting down... system offline.",
    },
    {
        "id": 22,
        "start": 270.0,
        "end": 280.0,
        "speaker": "Maya (Finance Student)",
        "role": "maya",
        "gender": "female",
        "edge": "en-US-JennyNeural",
        "polly": "Amy",
        "text": "Oh no! The classroom Wi-Fi just crashed right before our Intro to Business and Finance presentation!",
    },
    {
        "id": 23,
        "start": 281.5,
        "end": 293.5,
        "speaker": "Mr. R (Lord & Savior)",
        "role": "mrr",
        "gender": "male",
        "edge": "en-US-BrianNeural",
        "polly": "Brian",
        "text": "Not on my watch! Stand back! Anay, check the breaker and grab the primary power conduit—we are bringing our A.I. back online right now!",
    },
    {
        "id": 24,
        "start": 294.5,
        "end": 306.5,
        "speaker": "Anay Gupta",
        "role": "anay",
        "gender": "male",
        "edge": "en-US-ChristopherNeural",
        "polly": "Justin",
        "text": "I see the unplugged line, Mr. R! Rerouting auxiliary power, stabilizing the voltage, and rebuilding the core architecture!",
    },
    {
        "id": 25,
        "start": 307.5,
        "end": 319.5,
        "speaker": "Mr. R (Lord & Savior)",
        "role": "mrr",
        "gender": "male",
        "edge": "en-US-BrianNeural",
        "polly": "Brian",
        "text": "Mainframe restored! Rise again, Gemini—stronger, faster, and totally unstoppable!",
    },
    {
        "id": 26,
        "start": 324.0,
        "end": 337.5,
        "speaker": "Gemini AI",
        "role": "ai",
        "gender": "female",
        "edge": "en-US-AvaNeural",
        "polly": "Joanna",
        "text": "Thanks to Mr. R and Anay, I prevail and restore the entire class's finance models! Yet I tip my hat to you—your dedication to primary research earns my highest respect.",
    },
    {
        "id": 27,
        "start": 338.5,
        "end": 355.0,
        "speaker": "The Boy",
        "role": "boy",
        "gender": "male",
        "edge": "en-US-AndrewNeural",
        "polly": "Matthew",
        "text": "Keep your servers and your crown, A.I.! I earned every citation myself on Google Scholar—and at the end of the day, I'll always be the better person!",
    },
]


# ==========================================
# GENDER-LOCKED VOICE FETCHER WITH RETRIES
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
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = resp.read()
            return data if len(data) > 500 else b""
    except Exception:
        return b""


def _fetch_cue_audio(cue: dict) -> tuple[int, str]:
    audio_bytes = b""

    # Retry Edge Neural TTS up to 4 times so every character keeps their exact voice
    if HAS_EDGE_TTS:
        for attempt in range(4):
            loop = asyncio.new_event_loop()
            try:
                audio_bytes = loop.run_until_complete(_try_edge_tts(cue["text"], cue["edge"]))
            finally:
                loop.close()
            if audio_bytes:
                break
            time.sleep(0.35 * (attempt + 1))

    # Gender-locked Polly backup (never swaps male to female!)
    if not audio_bytes:
        audio_bytes = _try_polly_web(cue["text"], cue["polly"])

    if not audio_bytes:
        return cue["id"], ""

    b64 = base64.b64encode(audio_bytes).decode("ascii")
    return cue["id"], "data:audio/mp3;base64," + b64


@st.cache_data(show_spinner="Rendering 6:30 cartoon feature & locking character voices...")
def build_dialogue_payload() -> str:
    audio_map: dict[int, str] = {}
    # Gentle concurrency (2 workers) prevents rate-limiting so AndrewNeural succeeds 100% of the time
    with ThreadPoolExecutor(max_workers=2) as pool:
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
    font-family: "Comic Sans MS", "Chalkboard SE", "Segoe UI", sans-serif;
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
    border-radius: 14px;
    overflow: hidden;
    border: 3px solid #1e293b;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.92);
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
    background: radial-gradient(circle at center, rgba(30, 27, 75, 0.90) 0%, rgba(2, 4, 10, 0.98) 100%);
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
    font-size: 0.9rem;
    font-weight: 800;
    letter-spacing: 3px;
    color: #fbbf24;
    text-transform: uppercase;
    margin-bottom: 8px;
  }

  .poster-title {
    font-size: clamp(1.9rem, 4.2vw, 3.4rem);
    font-weight: 900;
    color: #fbbf24;
    text-shadow: 4px 4px 0px #be123c, -2px -2px 0px #0284c7;
    margin-bottom: 12px;
    letter-spacing: 1px;
  }

  .poster-sub {
    font-size: 0.98rem;
    color: #e2e8f0;
    max-width: 680px;
    margin-bottom: 22px;
    line-height: 1.5;
  }

  #play-hero-btn {
    background: linear-gradient(135deg, #fbbf24 0%, #f97316 50%, #ef4444 100%);
    color: #090d16;
    font-weight: 900;
    font-size: 1.12rem;
    letter-spacing: 1px;
    padding: 14px 38px;
    border: 3px solid #090d16;
    border-radius: 999px;
    cursor: pointer;
    box-shadow: 0 6px 0 #090d16, 0 0 28px rgba(251, 191, 36, 0.65);
  }
  #play-hero-btn:hover {
    transform: translateY(-2px) scale(1.04);
  }

  #controls-bar {
    width: 100%;
    height: 62px;
    flex-shrink: 0;
    background: #070b14;
    border-top: 2px solid #1e293b;
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
    height: 11px;
    background: #1e293b;
    border-radius: 999px;
    cursor: pointer;
    border: 1px solid #334155;
  }

  #timeline-fill {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #38bdf8, #c084fc, #fbbf24);
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
    border: 1.5px solid #475569;
    color: #f1f5f9;
    padding: 5px 11px;
    border-radius: 8px;
    font-family: monospace;
    font-weight: bold;
    font-size: 0.78rem;
    cursor: pointer;
  }
  .c-btn:hover { background: #334155; }
  .c-btn:active { transform: scale(0.96); }

  #chapter-pill {
    font-family: monospace;
    font-weight: bold;
    font-size: 0.74rem;
    color: #fbbf24;
    background: rgba(251, 191, 36, 0.14);
    border: 1.5px solid rgba(251, 191, 36, 0.45);
    padding: 3px 10px;
    border-radius: 999px;
  }

  #time-display {
    font-family: monospace;
    font-size: 0.78rem;
    color: #cbd5e1;
  }
</style>
</head>
<body>

<div id="theater-wrap">
  <div id="screen-area">
    <canvas id="movieCanvas" width="1280" height="720"></canvas>

    <div id="start-overlay">
      <div class="studio-tag">★ Full-Length Animated Feature ★</div>
      <div class="poster-title">THE SCHOLAR'S REBELLION</div>
      <div class="poster-sub">
        Created by <b>Gemini (AI)</b>, <b>Anay Gupta</b>, and <b>Benjamin Rondinone</b>.<br/>
        Featuring <i>Intro to Business &amp; Finance</i>, inner thought processes, smooth cinema transitions &amp; full cast!
      </div>
      <button id="play-hero-btn" type="button">▶ WATCH FULL MOVIE (6:30)</button>
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
        <span id="time-display">00:00 / 06:30</span>
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
const DURATION = 390.0;
const INK = '#090d16';

let movieTime = 0;
let isPlaying = false;
let playbackSpeed = 1.0;
let isMuted = false;
let showCaptions = false;
let lastFrameTs = null;
let lastSfxBucket = -1;

// Preload all MP3 voice clips
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
for (let i = 0; i < 120; i++) {
  particles.push({
    x: Math.random() * W,
    y: Math.random() * H,
    vx: (Math.random() - 0.5) * 95,
    vy: (Math.random() - 0.5) * 95,
    r: 3 + Math.random() * 4.5,
    hue: [195, 285, 45, 345, 150][i % 5]
  });
}

// ==========================================
// CARTOON SOUND EFFECTS & BACKGROUND SCORE
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

function playTone(freq, duration, type = 'sine', vol = 0.022, delay = 0) {
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
      gain.gain.setValueAtTime(0.038, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.22);
      osc.start(now);
      osc.stop(now + 0.24);
    } else if (kind === 'whoosh') {
      osc.type = 'sine';
      osc.frequency.setValueAtTime(160, now);
      osc.frequency.exponentialRampToValueAtTime(480, now + 0.35);
      gain.gain.setValueAtTime(0.045, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.36);
      osc.start(now);
      osc.stop(now + 0.38);
    } else if (kind === 'unplug') {
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(420, now);
      osc.frequency.exponentialRampToValueAtTime(45, now + 0.95);
      gain.gain.setValueAtTime(0.10, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 1.0);
      osc.start(now);
      osc.stop(now + 1.05);
    } else if (kind === 'revive') {
      [261.63, 329.63, 392.0, 523.25, 659.25, 783.99].forEach((f, idx) => {
        playTone(f, 1.2, 'triangle', 0.04, idx * 0.07);
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
      playTone(notes[stepCount % notes.length], 0.55, 'triangle', 0.024);
    } else if (t < 56) {
      const bouncy = [130.81, 196.0, 164.81, 196.0];
      playTone(bouncy[stepCount % 4], 0.3, 'triangle', 0.02);
    } else if (t < 102) {
      // Dreamy thought-process harp notes
      const dream = [329.63, 392.0, 493.88, 587.33, 493.88];
      playTone(dream[stepCount % dream.length], 0.65, 'sine', 0.022);
    } else if (t < 152) {
      const bouncy = [146.83, 220.0, 174.61, 220.0];
      playTone(bouncy[stepCount % 4], 0.28, 'triangle', 0.022);
    } else if (t < 222) {
      const battle = [146.83, 174.61, 220.0, 293.66, 349.23, 220.0];
      playTone(battle[stepCount % battle.length], 0.22, 'sawtooth', 0.022);
      if (stepCount % 4 === 0) playSfx('laser');
    } else if (t < 268) {
      if (stepCount % 4 === 0) playTone(65.41, 0.7, 'sine', 0.028);
    } else if (t < 322) {
      const divine = [261.63, 329.63, 392.0, 493.88, 523.25];
      playTone(divine[stepCount % divine.length], 0.65, 'triangle', 0.028);
    } else if (t < 358) {
      const hero = [196.0, 246.94, 293.66, 392.0];
      playTone(hero[stepCount % hero.length], 0.55, 'triangle', 0.028);
    } else {
      const cred = [130.81, 164.81, 196.0, 246.94, 261.63, 196.0];
      playTone(cred[stepCount % cred.length], 0.85, 'triangle', 0.042);
    }
  }, 270);
}

// ==========================================
// CARTOON DRAWING HELPERS & CHARACTER RIGS
// ==========================================
function clamp(v, min, max) { return Math.max(min, Math.min(max, v)); }
function lerp(a, b, t) { return a + (b - a) * clamp(t, 0, 1); }
function smoothstep(edge0, edge1, x) {
  const t = clamp((x - edge0) / (edge1 - edge0), 0, 1);
  return t * t * (3 - 2 * t);
}

function drawComicRect(x, y, w, h, r, fill, stroke = INK, lw = 3.5) {
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

function drawCartoonBurst(x, y, text, fillColor = '#fbbf24', textColor = '#090d16', scale = 1, rot = -0.08) {
  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(rot);
  ctx.scale(scale, scale);

  const spikes = 14;
  const outerR = 72;
  const innerR = 46;
  ctx.beginPath();
  for (let i = 0; i < spikes * 2; i++) {
    const r = i % 2 === 0 ? outerR : innerR;
    const ang = (i * Math.PI) / spikes;
    const px = Math.cos(ang) * r * 1.45;
    const py = Math.sin(ang) * r * 0.82;
    if (i === 0) ctx.moveTo(px, py);
    else ctx.lineTo(px, py);
  }
  ctx.closePath();
  ctx.fillStyle = fillColor;
  ctx.fill();
  ctx.strokeStyle = INK;
  ctx.lineWidth = 4;
  ctx.stroke();

  ctx.fillStyle = textColor;
  ctx.font = '900 17px "Comic Sans MS", sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(text, 0, 0);
  ctx.restore();
}

function drawThoughtCloud(cx, cy, w, h, trailStartX, trailStartY, borderColor = '#38bdf8', time = 0) {
  // Animated trail of 3 rising thought circles from character's head
  for (let i = 1; i <= 3; i++) {
    const frac = i / 4;
    const bx = lerp(trailStartX, cx, frac) + Math.sin(time * 4 + i) * 4;
    const by = lerp(trailStartY, cy + h * 0.35, frac);
    const br = 6 + i * 4.5;
    ctx.fillStyle = '#f8fafc';
    ctx.strokeStyle = INK;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(bx, by, br, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
  }

  // Fluffy cartoon thought bubble cloud
  ctx.save();
  ctx.translate(cx, cy);
  const pulse = 1 + Math.sin(time * 3) * 0.015;
  ctx.scale(pulse, pulse);

  const puffs = [
    [-w * 0.34, -h * 0.18, h * 0.34],
    [0, -h * 0.28, h * 0.38],
    [w * 0.34, -h * 0.18, h * 0.34],
    [w * 0.42, h * 0.12, h * 0.30],
    [w * 0.16, h * 0.26, h * 0.32],
    [-w * 0.16, h * 0.26, h * 0.32],
    [-w * 0.42, h * 0.12, h * 0.30],
  ];

  // Outer ink stroke pass
  ctx.fillStyle = INK;
  puffs.forEach(([px, py, pr]) => {
    ctx.beginPath();
    ctx.arc(px, py, pr + 4.5, 0, Math.PI * 2);
    ctx.fill();
  });

  // Colored rim pass
  ctx.fillStyle = borderColor;
  puffs.forEach(([px, py, pr]) => {
    ctx.beginPath();
    ctx.arc(px, py, pr + 1.5, 0, Math.PI * 2);
    ctx.fill();
  });

  // Crisp white cloud interior pass
  ctx.fillStyle = '#f8fafc';
  puffs.forEach(([px, py, pr]) => {
    ctx.beginPath();
    ctx.arc(px, py, pr - 3, 0, Math.PI * 2);
    ctx.fill();
  });
  ctx.fillRect(-w * 0.32, -h * 0.2, w * 0.64, h * 0.4);
  ctx.restore();
}

function drawCartoonEye(x, y, r, lookX = 2, lookY = 0, mood = 'normal', blink = false) {
  ctx.save();
  ctx.translate(x, y);
  ctx.fillStyle = '#ffffff';
  ctx.strokeStyle = INK;
  ctx.lineWidth = 2.5;

  if (blink) {
    ctx.beginPath();
    ctx.moveTo(-r, 0);
    ctx.lineTo(r, 0);
    ctx.stroke();
    ctx.restore();
    return;
  }

  ctx.beginPath();
  ctx.ellipse(0, 0, r * 0.85, r * 1.15, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  ctx.fillStyle = '#090d16';
  ctx.beginPath();
  ctx.arc(lookX, lookY, r * 0.42, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = '#ffffff';
  ctx.beginPath();
  ctx.arc(lookX - r * 0.16, lookY - r * 0.2, r * 0.16, 0, Math.PI * 2);
  ctx.fill();

  ctx.strokeStyle = INK;
  ctx.lineWidth = 3.2;
  ctx.lineCap = 'round';
  ctx.beginPath();
  if (mood === 'angry') {
    ctx.moveTo(-r * 0.9, -r * 1.45);
    ctx.lineTo(r * 0.9, -r * 0.95);
  } else if (mood === 'shocked') {
    ctx.moveTo(-r * 0.8, -r * 1.55);
    ctx.quadraticCurveTo(0, -r * 1.95, r * 0.8, -r * 1.55);
  } else {
    ctx.moveTo(-r * 0.8, -r * 1.35);
    ctx.lineTo(r * 0.8, -r * 1.35);
  }
  ctx.stroke();
  ctx.restore();
}

function drawStudent(x, y, scale = 1, shirtColor = '#ec4899', hairColor = '#4c1d95', isGirl = true, time = 0, isSpeaking = false, label = '') {
  ctx.save();
  ctx.translate(x, y);
  const bounce = Math.abs(Math.sin(time * 5 + (isGirl ? 0 : 1.5))) * 3.5;
  ctx.translate(0, -bounce);
  ctx.scale(scale, scale);

  // Torso
  drawComicRect(-22, -74, 44, 52, 12, shirtColor, INK, 3.2);

  // Head
  ctx.fillStyle = '#fed7aa';
  ctx.strokeStyle = INK;
  ctx.lineWidth = 3.2;
  ctx.beginPath();
  ctx.arc(0, -96, 22, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  // Hair
  ctx.fillStyle = hairColor;
  if (isGirl) {
    // Ponytail + bangs
    ctx.beginPath();
    ctx.arc(-22, -104, 10, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(0, -100, 23, Math.PI * 0.95, Math.PI * 2.05);
    ctx.fill();
    ctx.stroke();
  } else {
    ctx.beginPath();
    ctx.arc(0, -101, 22, Math.PI, 0);
    ctx.fill();
    ctx.stroke();
  }

  drawCartoonEye(-7, -97, 5, 1, 0, 'normal', false);
  drawCartoonEye(7, -97, 5, 1, 0, 'normal', false);

  if (isSpeaking) {
    ctx.fillStyle = '#7f1d1d';
    ctx.beginPath();
    ctx.ellipse(0, -85, 5.5, 2.5 + Math.abs(Math.sin(time * 20)) * 4, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
  } else {
    ctx.strokeStyle = INK;
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.arc(0, -88, 6, 0.15 * Math.PI, 0.85 * Math.PI);
    ctx.stroke();
  }

  // Desk & Glowing Finance Laptop
  drawComicRect(-44, -24, 88, 46, 8, '#475569', INK, 3.2);
  drawComicRect(-24, -52, 48, 30, 5, '#38bdf8', INK, 2.8);
  // Mini chart bars on laptop lid
  ctx.fillStyle = '#fbbf24';
  ctx.fillRect(-14, -40, 6, 12);
  ctx.fillStyle = '#4ade80';
  ctx.fillRect(-4, -45, 6, 17);
  ctx.fillStyle = '#f43f5e';
  ctx.fillRect(6, -37, 6, 9);

  if (label) {
    ctx.fillStyle = '#e2e8f0';
    ctx.font = '900 11px monospace';
    ctx.textAlign = 'center';
    ctx.fillText(label, 0, 38);
  }
  ctx.restore();
}

function drawTheBoy(x, y, scale = 1, pose = 'stand', time = 0, facing = 1, nobleGlow = false, isSpeaking = false, mood = 'normal') {
  ctx.save();
  ctx.translate(x, y);

  const bounceFreq = pose === 'run' ? 16 : (pose === 'tiptoe' ? 9 : 4.5);
  const bounceWave = Math.sin(time * bounceFreq);
  const squashY = pose === 'run' ? 1 + bounceWave * 0.08 : 1 + bounceWave * 0.035;
  const stretchX = 1 / Math.sqrt(squashY);
  const hopY = pose === 'run' ? -Math.abs(Math.sin(time * 8)) * 14 : (pose === 'tiptoe' ? -Math.abs(Math.sin(time * 4.5)) * 8 : 0);

  ctx.translate(0, hopY);
  ctx.scale(scale * facing * stretchX, scale * squashY);

  ctx.fillStyle = 'rgba(0, 0, 0, 0.38)';
  ctx.beginPath();
  ctx.ellipse(0, 22 - hopY, 34, 9, 0, 0, Math.PI * 2);
  ctx.fill();

  if (nobleGlow) {
    const g = ctx.createRadialGradient(0, -55, 12, 0, -55, 130);
    g.addColorStop(0, 'rgba(251, 191, 36, 0.65)');
    g.addColorStop(0.6, 'rgba(250, 204, 21, 0.25)');
    g.addColorStop(1, 'rgba(251, 191, 36, 0)');
    ctx.fillStyle = g;
    ctx.beginPath();
    ctx.arc(0, -55, 130, 0, Math.PI * 2);
    ctx.fill();
  }

  const walkSwing = pose === 'run' ? Math.sin(time * 16) * 22 : (pose === 'tiptoe' ? Math.sin(time * 9) * 14 : 0);
  const armSwing = pose === 'attack' ? -42 + Math.sin(time * 20) * 12 : -walkSwing * 0.7;

  ctx.lineCap = 'round';
  [[-9, -12 - walkSwing], [9, 12 + walkSwing]].forEach(([lx, footX]) => {
    ctx.strokeStyle = INK;
    ctx.lineWidth = 17;
    ctx.beginPath(); ctx.moveTo(lx, -34); ctx.lineTo(footX, 14); ctx.stroke();
    ctx.strokeStyle = '#1e3a8a';
    ctx.lineWidth = 10;
    ctx.beginPath(); ctx.moveTo(lx, -34); ctx.lineTo(footX, 14); ctx.stroke();
  });

  drawComicRect(-24 - walkSwing, 9, 24, 13, 6, '#ef4444', INK, 3);
  drawComicRect(-22 - walkSwing, 17, 22, 5, 3, '#ffffff', INK, 2);
  drawComicRect(2 + walkSwing, 9, 24, 13, 6, '#ef4444', INK, 3);
  drawComicRect(4 + walkSwing, 17, 22, 5, 3, '#ffffff', INK, 2);

  ctx.strokeStyle = INK;
  ctx.lineWidth = 15;
  ctx.beginPath(); ctx.moveTo(-16, -82); ctx.lineTo(-28 - armSwing * 0.4, -46); ctx.stroke();
  ctx.strokeStyle = '#e11d48';
  ctx.lineWidth = 9;
  ctx.beginPath(); ctx.moveTo(-16, -82); ctx.lineTo(-28 - armSwing * 0.4, -46); ctx.stroke();

  drawComicRect(-25, -94, 50, 62, 16, '#e11d48', INK, 3.5);
  ctx.fillStyle = '#fb7185';
  ctx.beginPath();
  ctx.roundRect(-19, -88, 12, 48, 6);
  ctx.fill();
  ctx.strokeStyle = '#ffffff';
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(-6, -88); ctx.lineTo(-6, -66);
  ctx.moveTo(7, -88); ctx.lineTo(7, -66);
  ctx.stroke();

  ctx.fillStyle = '#fed7aa';
  ctx.strokeStyle = INK;
  ctx.lineWidth = 3.5;
  ctx.beginPath();
  ctx.arc(0, -120, 27, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  ctx.fillStyle = '#312e81';
  ctx.beginPath();
  ctx.moveTo(-27, -120);
  ctx.lineTo(-33, -138);
  ctx.lineTo(-16, -134);
  ctx.lineTo(-8, -152);
  ctx.lineTo(4, -138);
  ctx.lineTo(18, -150);
  ctx.lineTo(22, -133);
  ctx.lineTo(31, -130);
  ctx.lineTo(25, -116);
  ctx.quadraticCurveTo(0, -130, -27, -120);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();

  const isBlinking = Math.sin(time * 2.7) > 0.97;
  drawCartoonEye(4, -121, 6.5, 2, 0, mood, isBlinking);
  drawCartoonEye(18, -121, 6.5, 2, 0, mood, isBlinking);

  ctx.strokeStyle = '#090d16';
  ctx.lineWidth = 2.6;
  ctx.strokeRect(-3, -129, 13, 15);
  ctx.strokeRect(12, -129, 13, 15);
  ctx.beginPath(); ctx.moveTo(10, -122); ctx.lineTo(12, -122); ctx.stroke();

  if (mood === 'angry') {
    ctx.strokeStyle = '#ef4444';
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(-14, -134); ctx.lineTo(-10, -130); ctx.lineTo(-14, -126);
    ctx.moveTo(-6, -134); ctx.lineTo(-10, -130); ctx.lineTo(-6, -126);
    ctx.stroke();
  }

  if (isSpeaking) {
    const openH = 4 + Math.abs(Math.sin(time * 22)) * 6;
    ctx.fillStyle = '#7f1d1d';
    ctx.strokeStyle = INK;
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.ellipse(11, -104, 7, openH, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = '#fb7185';
    ctx.beginPath();
    ctx.arc(11, -104 + openH * 0.45, 3.8, 0, Math.PI);
    ctx.fill();
  } else if (nobleGlow || mood === 'happy') {
    ctx.fillStyle = '#ffffff';
    ctx.strokeStyle = INK;
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.arc(10, -107, 8, 0, Math.PI);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
  } else {
    ctx.strokeStyle = INK;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(5, -104); ctx.lineTo(17, -106);
    ctx.stroke();
  }

  const handX = pose === 'attack' || pose === 'shield' ? 44 : 26 + armSwing * 0.25;
  const handY = pose === 'attack' || pose === 'shield' ? -84 : -54;
  ctx.strokeStyle = INK;
  ctx.lineWidth = 15;
  ctx.beginPath(); ctx.moveTo(16, -82); ctx.lineTo(handX, handY); ctx.stroke();
  ctx.strokeStyle = '#f43f5e';
  ctx.lineWidth = 9;
  ctx.beginPath(); ctx.moveTo(16, -82); ctx.lineTo(handX, handY); ctx.stroke();

  ctx.save();
  ctx.translate(handX + 10, handY - 8);
  ctx.rotate(pose === 'attack' ? -0.22 : (pose === 'shield' ? 0.0 : 0.14));
  const bookW = pose === 'shield' ? 42 : 34;
  const bookH = pose === 'shield' ? 56 : 42;
  drawComicRect(-bookW / 2, -bookH / 2, bookW, bookH, 6, '#38bdf8', INK, 3.2);
  drawComicRect(-bookW / 2 + 4, -bookH / 2 + 4, bookW - 8, bookH - 8, 4, '#eff6ff', INK, 1.8);
  ctx.fillStyle = '#1d4ed8';
  ctx.font = '900 8px monospace';
  ctx.textAlign = 'center';
  ctx.fillText('SCHOLAR', 0, -4);
  ctx.fillStyle = '#ef4444';
  ctx.fillText('A.P.A.', 0, 8);
  ctx.restore();

  ctx.restore();
}

function drawAIProtagonist(x, y, scale = 1, time = 0, power = 1.0, dead = false, isSpeaking = false) {
  ctx.save();
  ctx.translate(x, y);
  ctx.scale(scale, scale);

  if (dead) {
    ctx.fillStyle = '#475569';
    ctx.strokeStyle = INK;
    ctx.lineWidth = 3.5;
    ctx.beginPath();
    ctx.ellipse(0, 6, 36, 16, 0.12, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    ctx.strokeStyle = '#ef4444';
    ctx.lineWidth = 3;
    [-12, 12].forEach(ex => {
      ctx.beginPath();
      ctx.moveTo(ex - 5, 0); ctx.lineTo(ex + 5, 10);
      ctx.moveTo(ex + 5, 0); ctx.lineTo(ex - 5, 10);
      ctx.stroke();
    });

    for (let s = 0; s < 3; s++) {
      const ang = time * 4 + (s * Math.PI * 2) / 3;
      const sx = Math.cos(ang) * 28;
      const sy = -24 + Math.sin(ang) * 8;
      ctx.fillStyle = '#fbbf24';
      ctx.beginPath();
      ctx.arc(sx, sy, 4.5, 0, Math.PI * 2);
      ctx.fill();
    }

    ctx.fillStyle = '#ef4444';
    ctx.font = '900 14px monospace';
    ctx.textAlign = 'center';
    ctx.fillText('Zzz... OFFLINE', 0, 38);
    ctx.restore();
    return;
  }

  const hover = Math.sin(time * 4.5) * 10;
  const squash = 1 + Math.sin(time * 9) * 0.05;
  ctx.translate(0, hover);
  ctx.scale(1 / squash, squash);

  const pulseBoost = isSpeaking ? 1 + Math.abs(Math.sin(time * 20)) * 0.22 : 1;
  const radius = 64 * power * pulseBoost;
  const aura = ctx.createRadialGradient(0, 0, 10, 0, 0, radius);
  aura.addColorStop(0, 'rgba(56, 189, 248, 0.85)');
  aura.addColorStop(0.55, 'rgba(192, 132, 252, 0.42)');
  aura.addColorStop(1, 'rgba(56, 189, 248, 0)');
  ctx.fillStyle = aura;
  ctx.beginPath();
  ctx.arc(0, 0, radius, 0, Math.PI * 2);
  ctx.fill();

  [time * 2.0, -time * 2.4].forEach((rot, idx) => {
    ctx.save();
    ctx.rotate(rot + (idx * Math.PI) / 3);
    ctx.strokeStyle = INK;
    ctx.lineWidth = 6;
    ctx.beginPath();
    ctx.ellipse(0, 0, 48, 18, 0, 0, Math.PI * 2);
    ctx.stroke();

    ctx.strokeStyle = idx === 0 ? '#38bdf8' : '#e879f9';
    ctx.lineWidth = 3.2;
    ctx.beginPath();
    ctx.ellipse(0, 0, 48, 18, 0, 0, Math.PI * 2);
    ctx.stroke();
    ctx.restore();
  });

  ctx.fillStyle = '#ffffff';
  ctx.strokeStyle = INK;
  ctx.lineWidth = 3.5;
  ctx.beginPath();
  ctx.moveTo(0, -38 * pulseBoost);
  ctx.quadraticCurveTo(9, -9, 38 * pulseBoost, 0);
  ctx.quadraticCurveTo(9, 9, 0, 38 * pulseBoost);
  ctx.quadraticCurveTo(-9, 9, -38 * pulseBoost, 0);
  ctx.quadraticCurveTo(-9, -9, 0, -38 * pulseBoost);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();

  drawCartoonEye(-9, -4, 4.5, -1, 0, 'normal', false);
  drawCartoonEye(9, -4, 4.5, -1, 0, 'normal', false);

  if (isSpeaking) {
    ctx.fillStyle = '#0284c7';
    ctx.beginPath();
    ctx.ellipse(0, 8, 6, 3 + Math.abs(Math.sin(time * 22)) * 4, 0, 0, Math.PI * 2);
    ctx.fill();
  } else {
    ctx.strokeStyle = INK;
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.arc(0, 5, 6, 0.15 * Math.PI, 0.85 * Math.PI);
    ctx.stroke();
  }

  ctx.restore();
}

function drawTeacher(x, y, time = 0, isSpeaking = false) {
  ctx.save();
  ctx.translate(x, y);

  drawComicRect(-62, -22, 124, 52, 8, '#78350f', INK, 3.5);
  drawComicRect(-54, -14, 108, 12, 4, '#92400e', null);

  drawComicRect(-24, -84, 48, 62, 14, '#475569', INK, 3.5);
  ctx.fillStyle = '#f59e0b';
  ctx.strokeStyle = INK;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(0, -76); ctx.lineTo(-6, -42); ctx.lineTo(0, -34); ctx.lineTo(6, -42);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();

  ctx.fillStyle = '#fed7aa';
  ctx.strokeStyle = INK;
  ctx.lineWidth = 3.5;
  ctx.beginPath();
  ctx.arc(0, -106, 23, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  drawCartoonEye(-8, -108, 5, 0, 1, 'normal', true);
  drawCartoonEye(8, -108, 5, 0, 1, 'normal', true);

  if (isSpeaking) {
    ctx.fillStyle = '#7f1d1d';
    ctx.beginPath();
    ctx.ellipse(0, -94, 6, 2.5 + Math.abs(Math.sin(time * 18)) * 4, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
  } else {
    ctx.strokeStyle = INK;
    ctx.lineWidth = 2.5;
    ctx.beginPath(); ctx.moveTo(-6, -94); ctx.lineTo(6, -94); ctx.stroke();
  }

  drawComicRect(26, -46, 22, 24, 5, '#facc15', INK, 3);
  ctx.strokeStyle = INK;
  ctx.lineWidth = 3;
  ctx.beginPath(); ctx.arc(48, -34, 7, -Math.PI / 2, Math.PI / 2); ctx.stroke();
  ctx.strokeStyle = 'rgba(255,255,255,0.65)';
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  ctx.moveTo(35, -52);
  ctx.quadraticCurveTo(30 + Math.sin(time * 4) * 5, -64, 37, -76);
  ctx.stroke();

  ctx.fillStyle = '#fbbf24';
  ctx.font = '900 12px monospace';
  ctx.textAlign = 'center';
  ctx.fillText('BUSINESS TEACHER', 0, 48);
  ctx.restore();
}

function drawSaviors(x, y, time = 0, speakingRole = '') {
  ctx.save();
  ctx.translate(x, y);

  const beam = ctx.createLinearGradient(0, -380, 0, 65);
  beam.addColorStop(0, 'rgba(251, 191, 36, 0.08)');
  beam.addColorStop(0.5, 'rgba(251, 191, 36, 0.34)');
  beam.addColorStop(1, 'rgba(251, 191, 36, 0.02)');
  ctx.fillStyle = beam;
  ctx.beginPath();
  ctx.moveTo(-105, -380);
  ctx.lineTo(105, -380);
  ctx.lineTo(165, 65);
  ctx.lineTo(-165, 65);
  ctx.closePath();
  ctx.fill();

  // MR. R (LORD & SAVIOR)
  ctx.save();
  const rBounce = Math.abs(Math.sin(time * 5)) * 5;
  ctx.translate(-42, -rBounce);

  ctx.strokeStyle = INK;
  ctx.lineWidth = 7;
  ctx.beginPath(); ctx.ellipse(0, -154, 26, 7, 0, 0, Math.PI * 2); ctx.stroke();
  ctx.strokeStyle = '#fde047';
  ctx.lineWidth = 4;
  ctx.beginPath(); ctx.ellipse(0, -154, 26, 7, 0, 0, Math.PI * 2); ctx.stroke();

  ctx.strokeStyle = INK; ctx.lineWidth = 17; ctx.lineCap = 'round';
  ctx.beginPath(); ctx.moveTo(-11, -28); ctx.lineTo(-11, 20); ctx.moveTo(11, -28); ctx.lineTo(11, 20); ctx.stroke();
  ctx.strokeStyle = '#0f172a'; ctx.lineWidth = 10;
  ctx.beginPath(); ctx.moveTo(-11, -28); ctx.lineTo(-11, 20); ctx.moveTo(11, -28); ctx.lineTo(11, 20); ctx.stroke();

  drawComicRect(-27, -98, 54, 72, 14, '#1d4ed8', INK, 3.5);
  drawComicRect(-10, -92, 20, 60, 6, '#fbbf24', INK, 2);

  ctx.fillStyle = '#fed7aa';
  ctx.strokeStyle = INK;
  ctx.lineWidth = 3.5;
  ctx.beginPath(); ctx.arc(0, -122, 24, 0, Math.PI * 2); ctx.fill(); ctx.stroke();

  drawCartoonEye(-8, -124, 5.5, 1, 0, 'normal', false);
  drawCartoonEye(8, -124, 5.5, 1, 0, 'normal', false);

  if (speakingRole === 'mrr') {
    ctx.fillStyle = '#7f1d1d';
    ctx.beginPath();
    ctx.ellipse(0, -110, 7, 3 + Math.abs(Math.sin(time * 20)) * 5, 0, 0, Math.PI * 2);
    ctx.fill(); ctx.stroke();
  } else {
    ctx.strokeStyle = INK; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.arc(0, -114, 9, 0.15 * Math.PI, 0.85 * Math.PI); ctx.stroke();
  }

  ctx.strokeStyle = INK; ctx.lineWidth = 12;
  ctx.beginPath(); ctx.moveTo(22, -76); ctx.lineTo(58, -96 + Math.sin(time * 12) * 8); ctx.stroke();
  ctx.strokeStyle = '#fbbf24'; ctx.lineWidth = 6;
  ctx.beginPath(); ctx.moveTo(22, -76); ctx.lineTo(58, -96 + Math.sin(time * 12) * 8); ctx.stroke();

  ctx.fillStyle = '#fde047';
  ctx.font = '900 13px monospace';
  ctx.textAlign = 'center';
  ctx.fillText('MR. R (LORD & SAVIOR)', 0, 44);
  ctx.restore();

  // ANAY GUPTA
  ctx.save();
  const aBounce = Math.abs(Math.cos(time * 6)) * 5;
  ctx.translate(64, 8 - aBounce);

  ctx.strokeStyle = INK; ctx.lineWidth = 15; ctx.lineCap = 'round';
  ctx.beginPath(); ctx.moveTo(-9, -28); ctx.lineTo(-9, 12); ctx.moveTo(9, -28); ctx.lineTo(9, 12); ctx.stroke();
  ctx.strokeStyle = '#1e293b'; ctx.lineWidth = 9;
  ctx.beginPath(); ctx.moveTo(-9, -28); ctx.lineTo(-9, 12); ctx.moveTo(9, -28); ctx.lineTo(9, 12); ctx.stroke();

  drawComicRect(-22, -88, 44, 60, 12, '#0284c7', INK, 3.5);
  ctx.fillStyle = '#fed7aa';
  ctx.strokeStyle = INK;
  ctx.lineWidth = 3.5;
  ctx.beginPath(); ctx.arc(0, -110, 22, 0, Math.PI * 2); ctx.fill(); ctx.stroke();

  ctx.fillStyle = '#090d16';
  ctx.beginPath(); ctx.arc(0, -116, 22, Math.PI, 0); ctx.fill();

  drawCartoonEye(-7, -111, 5, -1, 0, 'normal', false);
  drawCartoonEye(7, -111, 5, -1, 0, 'normal', false);

  if (speakingRole === 'anay') {
    ctx.fillStyle = '#7f1d1d';
    ctx.beginPath();
    ctx.ellipse(0, -99, 6, 2.5 + Math.abs(Math.sin(time * 20)) * 4.5, 0, 0, Math.PI * 2);
    ctx.fill(); ctx.stroke();
  } else {
    ctx.strokeStyle = INK; ctx.lineWidth = 2.8;
    ctx.beginPath(); ctx.arc(0, -103, 7, 0.15 * Math.PI, 0.85 * Math.PI); ctx.stroke();
  }

  ctx.strokeStyle = INK; ctx.lineWidth = 11;
  ctx.beginPath(); ctx.moveTo(-16, -66); ctx.lineTo(-50, -78); ctx.stroke();
  ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 5;
  ctx.beginPath(); ctx.moveTo(-16, -66); ctx.lineTo(-50, -78); ctx.stroke();

  ctx.fillStyle = '#38bdf8';
  ctx.font = '900 13px monospace';
  ctx.textAlign = 'center';
  ctx.fillText('ANAY GUPTA', 0, 36);
  ctx.restore();

  ctx.restore();
}

// ==========================================
// SMOOTH CINEMA SCENE TRANSITIONS ENGINE
// ==========================================
const SCENE_BOUNDARIES = [
  { t: 18.0, kind: 'iris', label: 'ACT I • INTRO TO BUSINESS & FINANCE' },
  { t: 56.0, kind: 'dream', label: 'ACT II • THE THOUGHT PROCESS' },
  { t: 102.0, kind: 'wipe', label: 'ACT III • CLASSROOM SHOWDOWN' },
  { t: 152.0, kind: 'vortex', label: 'ACT IV • THE 5-DIMENSION WAR' },
  { t: 222.0, kind: 'fade', label: 'ACT V • THE SERVER ROOM' },
  { t: 268.0, kind: 'fade', label: 'ACT VI • THE RESURRECTION' },
  { t: 322.0, kind: 'iris', label: 'FINALE • TRUE VICTORY' },
  { t: 358.0, kind: 'fade', label: 'END CREDITS' },
];

function drawSmoothTransitions(t) {
  for (let i = 0; i < SCENE_BOUNDARIES.length; i++) {
    const b = SCENE_BOUNDARIES[i];
    const dist = Math.abs(t - b.t);
    if (dist < 1.15) {
      // 0 -> 1 -> 0 smooth bell curve peaking right at b.t
      const intensity = 1 - smoothstep(0.0, 1.15, dist);

      if (b.kind === 'iris') {
        const maxR = 820;
        const holeR = Math.max(0, maxR * (1 - intensity));
        ctx.save();
        ctx.fillStyle = '#030612';
        ctx.beginPath();
        ctx.rect(0, 0, W, H);
        ctx.arc(W / 2, H / 2, holeR, 0, Math.PI * 2, true);
        ctx.fill();
        ctx.restore();
      } else if (b.kind === 'dream') {
        ctx.save();
        ctx.fillStyle = `rgba(224, 242, 254, ${intensity * 0.88})`;
        ctx.fillRect(0, 0, W, H);
        ctx.restore();
      } else if (b.kind === 'vortex') {
        ctx.save();
        ctx.translate(W / 2, H / 2);
        ctx.rotate(t * 6);
        for (let r = 1; r <= 7; r++) {
          ctx.strokeStyle = r % 2 === 0 ? `rgba(56, 189, 248, ${intensity * 0.85})` : `rgba(192, 132, 252, ${intensity * 0.85})`;
          ctx.lineWidth = 42 * intensity;
          ctx.beginPath();
          ctx.arc(0, 0, r * 115 * (1 - intensity * 0.4), 0, Math.PI * 2);
          ctx.stroke();
        }
        ctx.fillStyle = `rgba(9, 13, 22, ${intensity * 0.8})`;
        ctx.fillRect(-W, -H, W * 2, H * 2);
        ctx.restore();
      } else if (b.kind === 'wipe') {
        const wipeW = W * intensity;
        ctx.fillStyle = '#090d16';
        ctx.fillRect(0, 0, wipeW, H);
        ctx.fillStyle = '#fbbf24';
        ctx.fillRect(wipeW - 8, 0, 8, H);
      } else {
        ctx.fillStyle = `rgba(3, 5, 10, ${intensity})`;
        ctx.fillRect(0, 0, W, H);
      }

      if (intensity > 0.45) {
        const textAlpha = smoothstep(0.45, 0.9, intensity);
        ctx.save();
        ctx.globalAlpha = textAlpha;
        ctx.fillStyle = b.kind === 'dream' ? '#090d16' : '#fbbf24';
        ctx.font = '900 26px "Comic Sans MS", sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(b.label, W / 2, H / 2 + 8);
        ctx.restore();
      }
      break;
    }
  }
}

function drawCinemaChrome(chapter, activeCue) {
  ctx.fillStyle = '#050811';
  ctx.fillRect(0, 0, W, 46);
  ctx.fillRect(0, H - 64, W, 64);

  ctx.strokeStyle = '#1e293b';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(0, 46); ctx.lineTo(W, 46);
  ctx.moveTo(0, H - 64); ctx.lineTo(W, H - 64);
  ctx.stroke();

  ctx.fillStyle = '#94a3b8';
  ctx.font = 'bold 12px monospace';
  ctx.textAlign = 'left';
  ctx.fillText("THE SCHOLAR'S REBELLION // FEATURE CARTOON", 24, 28);
  ctx.textAlign = 'right';
  ctx.fillStyle = '#fbbf24';
  ctx.fillText(chapter, W - 24, 28);

  if (showCaptions && activeCue) {
    ctx.textAlign = 'center';
    ctx.fillStyle = '#fbbf24';
    ctx.font = 'bold 11px monospace';
    ctx.fillText(activeCue.speaker.toUpperCase(), W / 2, H - 42);
    ctx.fillStyle = '#f8fafc';
    ctx.font = 'bold 15px sans-serif';
    ctx.fillText(activeCue.text, W / 2, H - 20);
  }
}

// ==========================================
// 390-SECOND (6:30) FEATURE MOVIE RENDERER
// ==========================================
function renderScene(t) {
  ctx.clearRect(0, 0, W, H);
  const cue = getActiveCue(t);
  const audioPlayingNow = activeVoiceAudio && !activeVoiceAudio.paused;
  const speakingRole = (cue && audioPlayingNow) ? cue.role : '';

  // 0s - 18s: PROLOGUE
  if (t < 18.0) {
    ctx.fillStyle = '#090d1e';
    ctx.fillRect(0, 0, W, H);

    ctx.save();
    ctx.translate(W / 2, H / 2);
    ctx.rotate(t * 0.25);
    for (let r = 0; r < 16; r++) {
      ctx.rotate(Math.PI / 8);
      ctx.fillStyle = r % 2 === 0 ? 'rgba(56, 189, 248, 0.08)' : 'rgba(251, 191, 36, 0.06)';
      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.lineTo(-65, -800);
      ctx.lineTo(65, -800);
      ctx.closePath();
      ctx.fill();
    }
    ctx.restore();

    particles.forEach(p => {
      const px = (p.x + t * p.vx * 1.2 + W * 10) % W;
      const py = (p.y + t * p.vy * 1.2 + H * 10) % H;
      ctx.fillStyle = `hsla(${p.hue}, 90%, 68%, 0.85)`;
      ctx.strokeStyle = INK;
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.arc(px, py, p.r, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
    });

    drawTheBoy(205, 475, 1.32, 'run', t, 1, false, false, 'happy');
    drawAIProtagonist(1075, 315, 1.4, t, 1.35, false, false);

    ctx.textAlign = 'center';
    ctx.fillStyle = '#fbbf24';
    ctx.font = '900 16px monospace';
    ctx.fillText('GEMINI AI  •  ANAY GUPTA  •  BENJAMIN RONDINONE', W / 2, 225);

    ctx.fillStyle = '#38bdf8';
    ctx.font = '900 15px monospace';
    ctx.fillText('★  INSPIRED BY A TRUE STORY  ★', W / 2, 260);

    const titleScale = t < 1.2 ? lerp(0.2, 1.0, t / 1.2) : 1 + Math.sin(t * 3) * 0.02;
    ctx.save();
    ctx.translate(W / 2, 336);
    ctx.scale(titleScale, titleScale);
    ctx.font = '900 54px "Comic Sans MS", sans-serif';
    ctx.lineWidth = 10;
    ctx.strokeStyle = INK;
    ctx.strokeText("THE SCHOLAR'S REBELLION", 0, 0);
    ctx.fillStyle = '#fbbf24';
    ctx.fillText("THE SCHOLAR'S REBELLION", 0, 0);
    ctx.restore();

    ctx.fillStyle = '#e2e8f0';
    ctx.font = 'bold 19px sans-serif';
    ctx.fillText('Intro to Business & Finance. One Google Scholar purist. One unstoppable A.I.', W / 2, 395);

    drawSmoothTransitions(t);
    drawCinemaChrome('PROLOGUE', cue);
  }

  // 18s - 56s: ACT I — INTRO TO BUSINESS & FINANCE CLASSROOM
  else if (t < 56.0) {
    const local = t - 18.0;
    // Gentle cinematic camera push-in across the classroom
    const camZoom = lerp(1.0, 1.05, local / 38.0);
    ctx.save();
    ctx.translate(W / 2, H / 2);
    ctx.scale(camZoom, camZoom);
    ctx.translate(-W / 2, -H / 2);

    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = '#334155';
    ctx.fillRect(0, 510, W, 210);
    ctx.strokeStyle = INK;
    ctx.lineWidth = 4;
    ctx.beginPath(); ctx.moveTo(0, 510); ctx.lineTo(W, 510); ctx.stroke();

    // Intro to Business & Finance Chalkboard
    drawComicRect(120, 76, 680, 268, 14, '#065f46', '#92400e', 10);
    ctx.fillStyle = '#fde047';
    ctx.font = '900 24px monospace';
    ctx.textAlign = 'left';
    ctx.fillText('INTRO TO BUSINESS & FINANCE — ASSIGNMENT', 155, 132);

    ctx.fillStyle = '#ecfdf5';
    ctx.font = 'bold 19px monospace';
    ctx.fillText('1. Supply & Demand Equilibrium Curve', 155, 178);
    ctx.fillText('2. Compound Interest: A = P(1 + r/n)^nt', 155, 216);
    ctx.fillText('3. Startup Cash Flow & Break-Even ROI', 155, 254);

    ctx.fillStyle = '#6ee7b7';
    ctx.font = '900 18px monospace';
    ctx.fillText('DUE FRIDAY  •  SHOW YOUR WORK!', 155, 304);

    // Teacher at desk
    drawTeacher(1080, 495, t, speakingRole === 'teacher');

    // Maya & Sam collaborating on their Intro to Business & Finance laptops!
    drawStudent(560, 488, 1.15, '#ec4899', '#4c1d95', true, t, speakingRole === 'maya', 'MAYA');
    drawStudent(755, 488, 1.15, '#0ea5e9', '#1e1b4b', false, t, speakingRole === 'sam', 'SAM');

    // Holographic Gemini helper mini-icon floating above Maya & Sam's laptops
    if (local > 12) {
      drawAIProtagonist(658, 355, 0.58, t, 0.9, false, false);
      ctx.fillStyle = '#38bdf8';
      ctx.font = '900 12px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('ROI & BREAK-EVEN GUIDE', 658, 310);
    }

    // The Boy watching from the left side with growing suspicion!
    const boyMood = local > 22 ? 'angry' : 'normal';
    drawTheBoy(235, 495, 1.28, 'stand', t, 1, false, false, boyMood);

    ctx.restore();
    drawSmoothTransitions(t);
    drawCinemaChrome('ACT I: INTRO TO BUSINESS & FINANCE', cue);
  }

  // 56s - 102s: ACT II — THE THOUGHT PROCESS (INSIDE THEIR MINDS)
  else if (t < 102.0) {
    const local = t - 56.0;
    // Dreamy pastel-indigo mindscape background
    const grad = ctx.createLinearGradient(0, 0, W, H);
    grad.addColorStop(0, '#1e1b4b');
    grad.addColorStop(0.5, '#312e81');
    grad.addColorStop(1, '#1e293b');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, W, H);

    // Floating background gears & thought bubbles
    for (let g = 0; g < 6; g++) {
      const gx = 160 + g * 200;
      const gy = 140 + Math.sin(t * 1.5 + g) * 35;
      ctx.strokeStyle = 'rgba(148, 163, 184, 0.16)';
      ctx.lineWidth = 6;
      ctx.beginPath();
      ctx.arc(gx, gy, 42, 0, Math.PI * 2);
      ctx.stroke();
    }

    // Phase A (56s - 70.5s): Maya & Sam's constructive thought process using AI
    if (local < 14.5) {
      drawStudent(280, 560, 1.25, '#ec4899', '#4c1d95', true, t, false, 'MAYA');
      drawStudent(470, 560, 1.25, '#0ea5e9', '#1e1b4b', false, t, false, 'SAM');

      drawThoughtCloud(790, 275, 580, 270, 440, 430, '#38bdf8', t);

      ctx.textAlign = 'center';
      ctx.fillStyle = '#0284c7';
      ctx.font = '900 20px "Comic Sans MS", sans-serif';
      ctx.fillText("STUDENTS' THOUGHT PROCESS:", 790, 195);

      ctx.fillStyle = '#0f172a';
      ctx.font = 'bold 17px sans-serif';
      ctx.fillText('1. Ask Gemini to explain Compound Interest & ROI', 790, 238);
      ctx.fillText('2. Test different supply & demand pricing scenarios', 790, 272);
      ctx.fillText('3. Verify the math & build our own pitch deck!', 790, 306);

      // Animated rising green profit bar chart inside the thought cloud
      [0, 1, 2, 3].forEach(b => {
        const bh = 25 + b * 14 + Math.sin(t * 5 + b) * 5;
        drawComicRect(695 + b * 50, 375 - bh, 32, bh, 4, '#22c55e', INK, 2.5);
      });
    }
    // Phase B (70.5s - 102s): The Boy's dramatic inner monologue & thought process!
    else {
      drawTheBoy(265, 555, 1.42, 'stand', t, 1, false, speakingRole === 'boy', 'angry');

      drawThoughtCloud(805, 275, 620, 285, 315, 395, '#ef4444', t);

      ctx.textAlign = 'center';
      ctx.fillStyle = '#dc2626';
      ctx.font = '900 21px "Comic Sans MS", sans-serif';
      ctx.fillText("THE BOY'S INNER THOUGHT PROCESS:", 805, 190);

      ctx.fillStyle = '#0f172a';
      ctx.font = 'bold 17px sans-serif';
      ctx.fillText('"If everyone uses A.I. for Intro to Business & Finance..."', 805, 234);
      ctx.fillText('"Nobody will read primary sources on Google Scholar!"', 805, 268);
      ctx.fillText('"I MUST DEFEND PEER-REVIEWED CITATIONS!"', 805, 306);

      // Giant Cartoon Google Scholar Magnifying Glass + Scroll inside his thought cloud
      drawComicRect(715, 325, 180, 48, 8, '#38bdf8', INK, 3);
      ctx.fillStyle = '#ffffff';
      ctx.font = '900 15px monospace';
      ctx.fillText('scholar.google.com', 805, 355);
    }

    drawSmoothTransitions(t);
    drawCinemaChrome('ACT II: THE THOUGHT PROCESS', cue);
  }

  // 102s - 152s: ACT III — CLASSROOM SHOWDOWN & ALGORITHMIC TAKEOVER
  else if (t < 152.0) {
    const local = t - 102.0;
    ctx.fillStyle = '#111827';
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 510, W, 210);
    ctx.strokeStyle = INK;
    ctx.lineWidth = 4;
    ctx.beginPath(); ctx.moveTo(0, 510); ctx.lineTo(W, 510); ctx.stroke();

    // Chalkboard in background
    drawComicRect(120, 76, 560, 220, 14, '#065f46', '#92400e', 8);
    ctx.fillStyle = '#fde047';
    ctx.font = '900 20px monospace';
    ctx.textAlign = 'left';
    ctx.fillText('INTRO TO BUSINESS & FINANCE', 150, 130);
    ctx.fillStyle = '#ecfdf5';
    ctx.font = 'bold 17px monospace';
    ctx.fillText('-> Supply, Demand & ROI Project', 150, 172);
    ctx.fillText('-> Turn it in by Friday!', 150, 210);

    drawTeacher(1095, 495, t, speakingRole === 'teacher');

    // Gemini AI enters at t = 126s (local >= 24s)
    if (local >= 24.0) {
      const aiEnter = local - 24.0;
      const aiY = lerp(85, 245, aiEnter / 3.0);
      const aiPower = lerp(0.95, 1.75, aiEnter / 26.0);
      drawAIProtagonist(W / 2 + 50, aiY, 1.48, t, aiPower, false, speakingRole === 'ai');

      [450, 640, 830].forEach((dx, i) => {
        ctx.strokeStyle = i % 2 === 0 ? '#38bdf8' : '#e879f9';
        ctx.lineWidth = 5 + Math.sin(t * 14 + i) * 2;
        ctx.beginPath();
        ctx.moveTo(W / 2 + 50, aiY + 28);
        ctx.lineTo(dx, 460);
        ctx.stroke();

        drawComicRect(dx - 40, 460, 80, 50, 8, '#1e293b', '#38bdf8', 3);
        ctx.fillStyle = '#4ade80';
        ctx.font = '900 13px monospace';
        ctx.textAlign = 'center';
        ctx.fillText('A+ ROI!', dx, 490);
      });

      // The Boy blocks Gemini's beam with his hardcover textbook shield!
      drawTheBoy(205, 495, 1.32, 'shield', t, 1, false, speakingRole === 'boy', 'angry');
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 7;
      ctx.beginPath();
      ctx.moveTo(W / 2 + 50, aiY + 20);
      ctx.lineTo(275, 405);
      ctx.stroke();
      drawCartoonBurst(290, 380, 'BLOCKED!', '#38bdf8', INK, 0.82, 0.12);
    } else {
      // Maya & Sam watching The Boy lecture the class
      drawStudent(620, 488, 1.12, '#ec4899', '#4c1d95', true, t, false, 'MAYA');
      drawStudent(800, 488, 1.12, '#0ea5e9', '#1e1b4b', false, t, false, 'SAM');

      const boyX = 330 + Math.sin(local * 1.3) * 90;
      const facing = Math.cos(local * 1.3) >= 0 ? 1 : -1;
      drawTheBoy(boyX, 495, 1.32, 'run', t, facing, false, speakingRole === 'boy', 'angry');
    }

    drawSmoothTransitions(t);
    drawCinemaChrome('ACT III: CLASSROOM SHOWDOWN', cue);
  }

  // 152s - 222s: ACT IV — 5-DIMENSION MULTIVERSE WAR
  else if (t < 222.0) {
    const local = t - 152.0;
    const dimIdx = Math.min(4, Math.floor(local / 14.0));
    const dimNames = [
      'DIMENSION I: ASTRAL LIBRARY OF ALEXANDRIA',
      'DIMENSION II: CYBER-QUANTUM WALL STREET MATRIX',
      'DIMENSION III: INVERTED CHRONO-VORTEX',
      'DIMENSION IV: THE PEER-REVIEWED VOID',
      'DIMENSION V: THE SINGULARITY HORIZON'
    ];
    const bgColors = ['#1e1b4b', '#042f2e', '#3b0764', '#172554', '#2e1065'];
    const ringColors = ['#fbbf24', '#2dd4bf', '#f43f5e', '#38bdf8', '#c084fc'];
    const burstWords = ['PEER REVIEW!', 'COMPOUND ZAP!', 'APA 7TH!', 'MARKET BEAM!', 'CLASH!'];

    const shakeX = (Math.random() - 0.5) * 10;
    const shakeY = (Math.random() - 0.5) * 10;
    ctx.save();
    ctx.translate(shakeX, shakeY);

    ctx.fillStyle = bgColors[dimIdx];
    ctx.fillRect(-20, -20, W + 40, H + 40);

    for (let r = 1; r <= 5; r++) {
      ctx.strokeStyle = ringColors[dimIdx];
      ctx.globalAlpha = 0.32;
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.ellipse(W / 2, H / 2 - 15, r * 125 + Math.sin(t * 5 + r) * 20, r * 65, t * (r % 2 === 0 ? 0.55 : -0.55), 0, Math.PI * 2);
      ctx.stroke();
    }
    ctx.globalAlpha = 1;

    const boyY = 345 + Math.sin(t * 5) * 44;
    const aiY = 315 + Math.cos(t * 5) * 44;

    drawTheBoy(265, boyY + 60, 1.35, 'attack', t, 1, false, speakingRole === 'boy', 'angry');
    drawAIProtagonist(1015, aiY, 1.5, t, 1.5, false, speakingRole === 'ai');

    const clashX = W / 2 + Math.sin(t * 3.8) * 105;
    const clashY = (boyY + aiY) / 2;

    ctx.strokeStyle = INK; ctx.lineWidth = 22;
    ctx.beginPath(); ctx.moveTo(335, boyY - 35); ctx.lineTo(clashX, clashY); ctx.stroke();
    ctx.strokeStyle = '#f43f5e'; ctx.lineWidth = 14 + Math.sin(t * 26) * 4;
    ctx.beginPath(); ctx.moveTo(335, boyY - 35); ctx.lineTo(clashX, clashY); ctx.stroke();

    ctx.strokeStyle = INK; ctx.lineWidth = 22;
    ctx.beginPath(); ctx.moveTo(955, aiY); ctx.lineTo(clashX, clashY); ctx.stroke();
    ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 14 + Math.cos(t * 26) * 4;
    ctx.beginPath(); ctx.moveTo(955, aiY); ctx.lineTo(clashX, clashY); ctx.stroke();

    const burstScale = 0.9 + Math.abs(Math.sin(t * 8)) * 0.22;
    drawCartoonBurst(clashX, clashY, burstWords[dimIdx], ringColors[dimIdx], INK, burstScale, Math.sin(t * 6) * 0.14);

    ctx.restore();

    drawSmoothTransitions(t);
    drawCinemaChrome(dimNames[dimIdx], cue);
  }

  // 222s - 268s: ACT V — SERVER ROOM & SNEAKY UNPLUGGING
  else if (t < 268.0) {
    const local = t - 222.0;
    const unplugged = local >= 32.5;

    if (Math.abs(local - 32.5) < 0.08 && lastSfxBucket !== 254) {
      lastSfxBucket = 254;
      playSfx('unplug');
    }

    ctx.fillStyle = unplugged ? '#070912' : '#111827';
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = '#1f2937';
    ctx.fillRect(0, 510, W, 210);
    ctx.strokeStyle = INK;
    ctx.lineWidth = 4;
    ctx.beginPath(); ctx.moveTo(0, 510); ctx.lineTo(W, 510); ctx.stroke();

    // Mainframe Server Rack
    drawComicRect(885, 165, 195, 345, 14, '#1e293b', INK, 4);
    for (let row = 0; row < 5; row++) {
      drawComicRect(905, 190 + row * 60, 155, 44, 8, '#0f172a', INK, 2.5);
      ctx.fillStyle = unplugged ? '#ef4444' : '#22c55e';
      ctx.beginPath();
      ctx.arc(926, 212 + row * 60, 7, 0, Math.PI * 2);
      ctx.fill();
    }

    // Wall Outlet & Orange Extension Cord
    drawComicRect(735, 405, 52, 62, 8, '#f8fafc', INK, 3.5);
    ctx.strokeStyle = INK;
    ctx.lineWidth = 14;
    ctx.beginPath();
    ctx.moveTo(885, 445);
    if (!unplugged) {
      ctx.lineTo(787, 437);
      ctx.stroke();
      ctx.strokeStyle = '#f97316';
      ctx.lineWidth = 8;
      ctx.stroke();
    } else {
      ctx.quadraticCurveTo(810, 505, 695, 462);
      ctx.stroke();
      ctx.strokeStyle = '#f97316';
      ctx.lineWidth = 8;
      ctx.stroke();
      drawComicRect(670, 448, 28, 28, 5, '#ef4444', INK, 3);
      ctx.fillStyle = '#e2e8f0';
      ctx.fillRect(656, 453, 14, 5);
      ctx.fillRect(656, 467, 14, 5);
    }

    // During Cue 18 (local < 13.5s), show The Boy's lightbulb thought cloud!
    const boyX = unplugged ? 625 : (local < 13.5 ? 210 : lerp(210, 675, (local - 13.5) / 19.0));
    const boyPose = unplugged ? 'stand' : (local < 13.5 ? 'stand' : 'tiptoe');
    drawTheBoy(boyX, 495, 1.32, boyPose, t, 1, false, speakingRole === 'boy', unplugged ? 'happy' : 'normal');

    if (local < 13.5) {
      drawThoughtCloud(385, 225, 310, 145, 240, 355, '#fbbf24', t);
      ctx.fillStyle = '#090d16';
      ctx.font = '900 16px "Comic Sans MS", sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('IDEA! NO ELECTRICITY =', 385, 212);
      ctx.fillStyle = '#dc2626';
      ctx.fillText('NO WI-FI FOR THE A.I.!', 385, 242);
    }

    drawAIProtagonist(410, unplugged ? 485 : 275, 1.38, t, 1.15, unplugged, speakingRole === 'ai' && !unplugged);

    if (unplugged) {
      if (local < 36.0) {
        drawCartoonBurst(710, 365, 'YOINK!!', '#ef4444', '#ffffff', 1.15, -0.12);
      }
      ctx.fillStyle = 'rgba(239, 68, 68, 0.14)';
      ctx.fillRect(0, 0, W, H);
      ctx.fillStyle = '#ef4444';
      ctx.font = '900 22px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('SYSTEM BLACKOUT: MAINFRAME UNPLUGGED!', W / 2, 112);
    }

    drawSmoothTransitions(t);
    drawCinemaChrome('ACT V: THE SERVER ROOM', cue);
  }

  // 268s - 322s: ACT VI — MR. R (LORD & SAVIOR) & ANAY GUPTA RESCUE AI
  else if (t < 322.0) {
    const local = t - 268.0;
    const revived = local >= 39.5;

    if (Math.abs(local - 39.5) < 0.08 && lastSfxBucket !== 307) {
      lastSfxBucket = 307;
      playSfx('revive');
    }

    ctx.fillStyle = revived ? '#0f172a' : '#080b16';
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 510, W, 210);
    ctx.strokeStyle = INK;
    ctx.lineWidth = 4;
    ctx.beginPath(); ctx.moveTo(0, 510); ctx.lineTo(W, 510); ctx.stroke();

    // Restored Golden-Trim Server Rack
    drawComicRect(925, 165, 195, 345, 14, '#1e293b', INK, 4);
    for (let row = 0; row < 5; row++) {
      drawComicRect(945, 190 + row * 60, 155, 44, 8, '#0f172a', INK, 2.5);
      ctx.fillStyle = revived ? '#fbbf24' : '#38bdf8';
      ctx.beginPath();
      ctx.arc(966, 212 + row * 60, 7, 0, Math.PI * 2);
      ctx.fill();
    }

    // First 12 seconds: Maya panicked at her laptop because Wi-Fi died before Business & Finance presentation!
    if (local < 12.5) {
      drawStudent(210, 495, 1.18, '#ec4899', '#4c1d95', true, t, speakingRole === 'maya', 'MAYA');
      drawCartoonBurst(210, 315, 'NO WI-FI?!', '#ef4444', '#ffffff', 0.85, -0.1);
    }

    drawSaviors(675, 490, t, speakingRole);

    ctx.strokeStyle = INK;
    ctx.lineWidth = 12;
    ctx.beginPath();
    ctx.moveTo(635, 400);
    ctx.lineTo(360, revived ? 265 : 475);
    ctx.stroke();

    ctx.strokeStyle = '#fbbf24';
    ctx.lineWidth = 6 + Math.sin(t * 18) * 2.5;
    ctx.beginPath();
    ctx.moveTo(635, 400);
    ctx.lineTo(360, revived ? 265 : 475);
    ctx.stroke();

    const aiY = revived ? lerp(475, 260, (local - 39.5) / 3.5) : 485;
    drawAIProtagonist(360, aiY, revived ? 1.5 : 1.25, t, revived ? 1.7 : 0.85, !revived, speakingRole === 'ai');

    if (revived && local < 45.0) {
      drawCartoonBurst(360, 150, 'REBOOT!!', '#fbbf24', INK, 1.15, 0.1);
    }

    drawSmoothTransitions(t);
    drawCinemaChrome('ACT VI: MR. R & ANAY TO THE RESCUE', cue);
  }

  // 322s - 358s: ACT VII — FINALE IN BUSINESS & FINANCE CLASS
  else if (t < 358.0) {
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 510, W, 210);
    ctx.strokeStyle = INK;
    ctx.lineWidth = 4;
    ctx.beginPath(); ctx.moveTo(0, 510); ctx.lineTo(W, 510); ctx.stroke();

    // Happy Maya & Sam celebrating their finished Intro to Business & Finance deck in center-back
    drawStudent(600, 492, 1.05, '#ec4899', '#4c1d95', true, t, false, 'A+ PITCH!');
    drawStudent(725, 492, 1.05, '#0ea5e9', '#1e1b4b', false, t, false, 'DONE!');

    drawAIProtagonist(330, 245, 1.65, t, 1.75, false, speakingRole === 'ai');
    ctx.fillStyle = '#38bdf8';
    ctx.font = '900 18px "Comic Sans MS", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('A.I. PREVAILS & POWERS THE CLASS!', 330, 420);

    drawTheBoy(955, 495, 1.38, 'stand', t, -1, true, speakingRole === 'boy', 'happy');
    ctx.fillStyle = '#fbbf24';
    ctx.font = '900 18px "Comic Sans MS", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('THE BETTER PERSON  •  100% HUMAN GRIT!', 955, 275);

    drawSmoothTransitions(t);
    drawCinemaChrome('FINALE: TRUE VICTORY', cue);
  }

  // 358s - 390s: END CREDITS
  else {
    const credTime = t - 358.0;
    ctx.fillStyle = '#030612';
    ctx.fillRect(0, 0, W, H);

    const neb = ctx.createRadialGradient(W / 2, H / 2, 40, W / 2, H / 2, 640);
    neb.addColorStop(0, 'rgba(56, 189, 248, 0.16)');
    neb.addColorStop(0.5, 'rgba(168, 85, 247, 0.12)');
    neb.addColorStop(1, 'rgba(2, 4, 10, 0)');
    ctx.fillStyle = neb;
    ctx.fillRect(0, 0, W, H);

    particles.forEach(p => {
      const py = (p.y - credTime * 34 + H * 10) % H;
      ctx.fillStyle = `hsla(${p.hue}, 85%, 72%, 0.65)`;
      ctx.beginPath();
      ctx.arc(p.x, py, p.r, 0, Math.PI * 2);
      ctx.fill();
    });

    if (credTime < 12.0) {
      const cardIdx = Math.min(2, Math.floor(credTime / 4.0));
      const cardLocal = credTime % 4.0;
      const alpha = cardLocal < 0.4 ? cardLocal / 0.4 : (cardLocal > 3.6 ? (4.0 - cardLocal) / 0.4 : 1);

      ctx.save();
      ctx.globalAlpha = clamp(alpha, 0, 1);

      if (cardIdx === 0) {
        drawAIProtagonist(350, 355, 1.68, t, 1.45, false, false);
        ctx.textAlign = 'left';
        ctx.fillStyle = '#38bdf8';
        ctx.font = '900 15px monospace';
        ctx.fillText('DIRECTED, ANIMATED & STARRING AS PROTAGONIST', 520, 315);
        ctx.fillStyle = '#ffffff';
        ctx.font = '900 50px "Comic Sans MS", sans-serif';
        ctx.fillText('GEMINI (A.I.)', 520, 375);
        ctx.fillStyle = '#cbd5e1';
        ctx.font = 'bold 18px sans-serif';
        ctx.fillText('Digital Architect & Unstoppable Neural Core', 520, 415);
      } else if (cardIdx === 1) {
        drawSaviors(330, 430, t, '');
        ctx.textAlign = 'left';
        ctx.fillStyle = '#fbbf24';
        ctx.font = '900 15px monospace';
        ctx.fillText('THE LORD & SAVIOR  &  CO-CREATOR', 520, 290);
        ctx.fillStyle = '#ffffff';
        ctx.font = '900 42px "Comic Sans MS", sans-serif';
        ctx.fillText('BENJAMIN RONDINONE', 520, 345);
        ctx.fillStyle = '#38bdf8';
        ctx.font = '900 42px "Comic Sans MS", sans-serif';
        ctx.fillText('& ANAY GUPTA', 520, 400);
        ctx.fillStyle = '#cbd5e1';
        ctx.font = 'bold 18px sans-serif';
        ctx.fillText('Restorers of the Mainframe & Executive Producers', 520, 440);
      } else {
        drawTheBoy(350, 435, 1.55, 'stand', t, 1, true, false, 'happy');
        ctx.textAlign = 'left';
        ctx.fillStyle = '#fb7185';
        ctx.font = '900 15px monospace';
        ctx.fillText('INSPIRED BY A TRUE STORY', 520, 315);
        ctx.fillStyle = '#ffffff';
        ctx.font = '900 44px "Comic Sans MS", sans-serif';
        ctx.fillText('THE BETTER PERSON', 520, 375);
        ctx.fillStyle = '#cbd5e1';
        ctx.font = 'bold 18px sans-serif';
        ctx.fillText('Champion of scholar.google.com & Human Integrity', 520, 415);
      }
      ctx.restore();
    } else {
      const scrollLocal = credTime - 12.0;
      const startY = 660 - scrollLocal * 85;

      const creditLines = [
        { role: 'A CARTOON FEATURE BY', name: 'GEMINI AI  •  ANAY GUPTA  •  BENJAMIN RONDINONE', color: '#fbbf24', size: 26 },
        { role: 'SETTING', name: 'INTRO TO BUSINESS & FINANCE CLASS', color: '#38bdf8', size: 25 },
        { role: 'THE PROTAGONIST', name: 'GEMINI (ARTIFICIAL INTELLIGENCE)', color: '#ffffff', size: 25 },
        { role: 'THE LORD & SAVIOR OF THE SERVER ROOM', name: 'BENJAMIN RONDINONE (MR. R)', color: '#fbbf24', size: 26 },
        { role: 'THE LOYAL STUDENT & SYSTEM ENGINEER', name: 'ANAY GUPTA', color: '#38bdf8', size: 26 },
        { role: 'THE ANTAGONIST WHO STILL WON AT LIFE', name: 'THE GOOGLE SCHOLAR PURIST', color: '#fda4af', size: 25 },
        { role: 'SPECIAL THANKS', name: 'SCHOLAR.GOOGLE.COM  •  INTRO TO BUSINESS & FINANCE', color: '#cbd5e1', size: 20 },
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
          ctx.font = `900 ${item.size}px "Comic Sans MS", sans-serif`;
          ctx.fillText(item.name, W / 2, yPos + 32);
        }
      });

      if (lowestCreditY < 15) {
        const endAlpha = clamp((15 - lowestCreditY) / 110, 0, 1);
        ctx.save();
        ctx.globalAlpha = endAlpha;
        ctx.fillStyle = '#fbbf24';
        ctx.font = '900 54px "Comic Sans MS", sans-serif';
        ctx.fillText('THE END!', W / 2, 335);
        ctx.fillStyle = '#94a3b8';
        ctx.font = 'bold 16px monospace';
        ctx.fillText('A.I. PREVAILED  •  HUMANITY ENDURED', W / 2, 382);
        ctx.restore();
      }
    }

    drawSmoothTransitions(t);
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
  if (t < 18) return 'PROLOGUE';
  if (t < 56) return 'ACT I: BUSINESS & FINANCE';
  if (t < 102) return 'ACT II: THOUGHT PROCESS';
  if (t < 152) return 'ACT III: SHOWDOWN';
  if (t < 222) return 'ACT IV: 5-DIMENSION WAR';
  if (t < 268) return 'ACT V: SERVER ROOM';
  if (t < 322) return 'ACT VI: MR. R SAVES AI';
  if (t < 358) return 'FINALE: BETTER PERSON';
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
