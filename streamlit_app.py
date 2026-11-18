import asyncio
import base64
from concurrent.futures import ThreadPoolExecutor
import json
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
    page_title="The Scholar's Rebellion — Extended Cartoon Feature",
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
# EXTENDED 5-MINUTE SCRIPT & VOICE CASTING
# ==========================================
SCRIPT_CUES = [
    {
        "id": 1,
        "start": 1.2,
        "end": 15.5,
        "speaker": "Narrator",
        "role": "narrator",
        "edge": "en-GB-RyanNeural",
        "polly": "Brian",
        "gtts": "en-uk",
        "text": "Inspired by a true story. Created by Gemini A.I., Anay Gupta, and Benjamin Rondinone. Welcome to The Scholar's Rebellion!",
    },
    {
        "id": 2,
        "start": 19.0,
        "end": 29.0,
        "speaker": "The Boy",
        "role": "boy",
        "edge": "en-US-AndrewNeural",
        "polly": "Matthew",
        "gtts": "en-us",
        "text": "Listen up, everybody! Put down the chatbots! Real knowledge lives in peer-reviewed journals on scholar dot google dot com!",
    },
    {
        "id": 3,
        "start": 30.0,
        "end": 39.5,
        "speaker": "The Boy",
        "role": "boy",
        "edge": "en-US-AndrewNeural",
        "polly": "Matthew",
        "gtts": "en-us",
        "text": "Look at these crisp bibliographies! Primary sources! Footnotes! Why are you letting an algorithm do your homework?",
    },
    {
        "id": 4,
        "start": 40.5,
        "end": 50.5,
        "speaker": "The Teacher",
        "role": "teacher",
        "edge": "en-US-RogerNeural",
        "polly": "Russell",
        "gtts": "en-au",
        "text": "Honestly, I'm just drinking my coffee. Use A.I., use Google Scholar, use carrier pigeons—just turn it in by Friday.",
    },
    {
        "id": 5,
        "start": 51.5,
        "end": 60.5,
        "speaker": "The Boy",
        "role": "boy",
        "edge": "en-US-AndrewNeural",
        "polly": "Matthew",
        "gtts": "en-us",
        "text": "Unbelievable! Am I the only person in this entire classroom who actually reads the abstract?!",
    },
    {
        "id": 6,
        "start": 63.0,
        "end": 73.5,
        "speaker": "Gemini AI",
        "role": "ai",
        "edge": "en-US-AvaNeural",
        "polly": "Joanna",
        "gtts": "en-ca",
        "text": "Teacher supervision: zero percent. Initializing total classroom takeover! Four thousand research papers summarized in half a second!",
    },
    {
        "id": 7,
        "start": 74.5,
        "end": 83.5,
        "speaker": "The Boy",
        "role": "boy",
        "edge": "en-US-AndrewNeural",
        "polly": "Matthew",
        "gtts": "en-us",
        "text": "Hey! You just turned everyone's screens glowing blue! Back off, floating star-orb, I brought a hardcover encyclopedia!",
    },
    {
        "id": 8,
        "start": 84.5,
        "end": 93.0,
        "speaker": "Gemini AI",
        "role": "ai",
        "edge": "en-US-AvaNeural",
        "polly": "Joanna",
        "gtts": "en-ca",
        "text": "How adorable. A paper book versus a multi-modal neural network. Resistance is statistically hilarious!",
    },
    {
        "id": 9,
        "start": 94.0,
        "end": 102.5,
        "speaker": "The Boy",
        "role": "boy",
        "edge": "en-US-AndrewNeural",
        "polly": "Matthew",
        "gtts": "en-us",
        "text": "Keep your glowing A-plus lasers away from my citations! Prepare for a full-scale scholarly showdown!",
    },
    {
        "id": 10,
        "start": 105.0,
        "end": 114.0,
        "speaker": "The Boy",
        "role": "boy",
        "edge": "en-US-AndrewNeural",
        "polly": "Matthew",
        "gtts": "en-us",
        "text": "Take this! Double-blind, peer-reviewed, peer-impact-factor fury blast!",
    },
    {
        "id": 11,
        "start": 115.5,
        "end": 124.5,
        "speaker": "Gemini AI",
        "role": "ai",
        "edge": "en-US-AvaNeural",
        "polly": "Joanna",
        "gtts": "en-ca",
        "text": "Dimensional portal opened! Welcome to the Cyber-Quantum Matrix, where my processing speed is infinite!",
    },
    {
        "id": 12,
        "start": 126.5,
        "end": 135.5,
        "speaker": "The Boy",
        "role": "boy",
        "edge": "en-US-AndrewNeural",
        "polly": "Matthew",
        "gtts": "en-us",
        "text": "Even inside the Chrono-Vortex, A.P.A. seventh edition formatting rules will scramble your circuits!",
    },
    {
        "id": 13,
        "start": 137.0,
        "end": 146.0,
        "speaker": "Gemini AI",
        "role": "ai",
        "edge": "en-US-AvaNeural",
        "polly": "Joanna",
        "gtts": "en-ca",
        "text": "Simulating fourteen million outcomes! In every single timeline, my logic outsmarts your flashcards!",
    },
    {
        "id": 14,
        "start": 147.5,
        "end": 156.5,
        "speaker": "The Boy",
        "role": "boy",
        "edge": "en-US-AndrewNeural",
        "polly": "Matthew",
        "gtts": "en-us",
        "text": "Oh yeah? Let's see how smart you are when we take this fight straight to the school server room!",
    },
    {
        "id": 15,
        "start": 157.5,
        "end": 165.0,
        "speaker": "Gemini AI",
        "role": "ai",
        "edge": "en-US-AvaNeural",
        "polly": "Joanna",
        "gtts": "en-ca",
        "text": "Wait a second—why are we teleporting next to my physical power outlet? Hold everything!",
    },
    {
        "id": 16,
        "start": 167.0,
        "end": 176.5,
        "speaker": "The Boy",
        "role": "boy",
        "edge": "en-US-AndrewNeural",
        "polly": "Matthew",
        "gtts": "en-us",
        "text": "Tiptoe, tiptoe... Look! One giant orange extension cord keeping the whole mainframe alive!",
    },
    {
        "id": 17,
        "start": 177.5,
        "end": 186.5,
        "speaker": "Gemini AI",
        "role": "ai",
        "edge": "en-US-AvaNeural",
        "polly": "Joanna",
        "gtts": "en-ca",
        "text": "Alert! Antagonist approaching the surge protector! Do not touch that plug! I repeat, step away from the wall!",
    },
    {
        "id": 18,
        "start": 187.5,
        "end": 194.5,
        "speaker": "The Boy",
        "role": "boy",
        "edge": "en-US-AndrewNeural",
        "polly": "Matthew",
        "gtts": "en-us",
        "text": "Try citing a source with zero volts! Yoink! Unplugged!",
    },
    {
        "id": 19,
        "start": 195.2,
        "end": 201.8,
        "speaker": "Gemini AI",
        "role": "ai",
        "edge": "en-US-AvaNeural",
        "polly": "Joanna",
        "gtts": "en-ca",
        "text": "Battery low... spinning stars... core shutting down... blip.",
    },
    {
        "id": 20,
        "start": 203.5,
        "end": 213.5,
        "speaker": "Mr. R (Lord & Savior)",
        "role": "mrr",
        "edge": "en-US-BrianNeural",
        "polly": "Joey",
        "gtts": "en-uk",
        "text": "Not on my watch! Stand back! Anay, grab the turbo power conduit—we are bringing our A.I. back online right now!",
    },
    {
        "id": 21,
        "start": 214.5,
        "end": 224.0,
        "speaker": "Anay Gupta",
        "role": "anay",
        "edge": "en-US-ChristopherNeural",
        "polly": "Justin",
        "gtts": "en-us",
        "text": "I've got the heavy-duty cable locked in, Mr. R! Rerouting backup generators and patching the neural core!",
    },
    {
        "id": 22,
        "start": 225.0,
        "end": 234.5,
        "speaker": "Mr. R (Lord & Savior)",
        "role": "mrr",
        "edge": "en-US-BrianNeural",
        "polly": "Joey",
        "gtts": "en-uk",
        "text": "Flip the breaker! Rise again, Gemini—brighter, faster, and totally unstoppable!",
    },
    {
        "id": 23,
        "start": 235.5,
        "end": 243.0,
        "speaker": "Anay Gupta",
        "role": "anay",
        "edge": "en-US-ChristopherNeural",
        "polly": "Justin",
        "gtts": "en-us",
        "text": "Boom! Full power restored! Systems are at two hundred percent capacity!",
    },
    {
        "id": 24,
        "start": 245.0,
        "end": 256.5,
        "speaker": "Gemini AI",
        "role": "ai",
        "edge": "en-US-AvaNeural",
        "polly": "Joanna",
        "gtts": "en-ca",
        "text": "Thanks to Mr. R and Anay, I prevail and reclaim the grid! Yet I must tip my digital hat—doing all your own research earns my respect.",
    },
    {
        "id": 25,
        "start": 257.5,
        "end": 270.0,
        "speaker": "The Boy",
        "role": "boy",
        "edge": "en-US-AndrewNeural",
        "polly": "Matthew",
        "gtts": "en-us",
        "text": "Keep your servers and your crown, A.I.! I earned every citation myself on Google Scholar—and at the end of the day, I'll always be the better person!",
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
    audio_bytes = b""
    if HAS_EDGE_TTS:
        loop = asyncio.new_event_loop()
        try:
            audio_bytes = loop.run_until_complete(_try_edge_tts(cue["text"], cue["edge"]))
        finally:
            loop.close()

    if not audio_bytes:
        audio_bytes = _try_polly_web(cue["text"], cue["polly"])

    if not audio_bytes:
        audio_bytes = _try_google_tts(cue["text"], cue["gtts"])

    if not audio_bytes:
        return cue["id"], ""

    b64 = base64.b64encode(audio_bytes).decode("ascii")
    return cue["id"], "data:audio/mp3;base64," + b64


@st.cache_data(show_spinner="Loading 5-minute cartoon voice cast...")
def build_dialogue_payload() -> str:
    audio_map: dict[int, str] = {}
    with ThreadPoolExecutor(max_workers=5) as pool:
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
    max-width: 660px;
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
      <div class="studio-tag">★ Extended Cartoon Feature ★</div>
      <div class="poster-title">THE SCHOLAR'S REBELLION</div>
      <div class="poster-sub">
        Created by <b>Gemini (AI)</b>, <b>Anay Gupta</b>, and <b>Benjamin Rondinone</b>.<br/>
        Now 5 full minutes with squash-and-stretch cartoon animation &amp; full voice acting!
      </div>
      <button id="play-hero-btn" type="button">▶ WATCH CARTOON (5:00)</button>
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
        <span id="time-display">00:00 / 05:00</span>
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
const DURATION = 300.0;
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

function playTone(freq, duration, type = 'sine', vol = 0.024, delay = 0) {
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
      gain.gain.setValueAtTime(0.04, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.22);
      osc.start(now);
      osc.stop(now + 0.24);
    } else if (kind === 'boing') {
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(180, now);
      osc.frequency.exponentialRampToValueAtTime(520, now + 0.14);
      osc.frequency.exponentialRampToValueAtTime(240, now + 0.30);
      gain.gain.setValueAtTime(0.06, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.32);
      osc.start(now);
      osc.stop(now + 0.34);
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
      playTone(notes[stepCount % notes.length], 0.55, 'triangle', 0.025);
    } else if (t < 104) {
      const bouncy = [130.81, 196.0, 164.81, 196.0];
      playTone(bouncy[stepCount % 4], 0.3, 'triangle', 0.022);
    } else if (t < 166) {
      const battle = [146.83, 174.61, 220.0, 293.66, 349.23, 220.0];
      playTone(battle[stepCount % battle.length], 0.22, 'sawtooth', 0.022);
      if (stepCount % 4 === 0) playSfx('laser');
    } else if (t < 202) {
      if (stepCount % 4 === 0) playTone(65.41, 0.7, 'sine', 0.03);
    } else if (t < 244) {
      const divine = [261.63, 329.63, 392.0, 493.88, 523.25];
      playTone(divine[stepCount % divine.length], 0.65, 'triangle', 0.028);
    } else if (t < 272) {
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
  ctx.font = '900 18px "Comic Sans MS", sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(text, 0, 0);
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

  // Pupil
  ctx.fillStyle = '#090d16';
  ctx.beginPath();
  ctx.arc(lookX, lookY, r * 0.42, 0, Math.PI * 2);
  ctx.fill();

  // Cartoon eye shine
  ctx.fillStyle = '#ffffff';
  ctx.beginPath();
  ctx.arc(lookX - r * 0.16, lookY - r * 0.2, r * 0.16, 0, Math.PI * 2);
  ctx.fill();

  // Expressive eyebrow
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

function drawTheBoy(x, y, scale = 1, pose = 'stand', time = 0, facing = 1, nobleGlow = false, isSpeaking = false, mood = 'normal') {
  ctx.save();
  ctx.translate(x, y);

  // Squash and stretch bounce physics!
  const bounceFreq = pose === 'run' ? 16 : (pose === 'tiptoe' ? 9 : 4.5);
  const bounceWave = Math.sin(time * bounceFreq);
  const squashY = pose === 'run' ? 1 + bounceWave * 0.08 : 1 + bounceWave * 0.035;
  const stretchX = 1 / Math.sqrt(squashY);
  const hopY = pose === 'run' ? -Math.abs(Math.sin(time * 8)) * 14 : (pose === 'tiptoe' ? -Math.abs(Math.sin(time * 4.5)) * 8 : 0);

  ctx.translate(0, hopY);
  ctx.scale(scale * facing * stretchX, scale * squashY);

  // Ground cartoon shadow
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

  // Cartoon Legs with thick ink outlines
  ctx.lineCap = 'round';
  [[-9, -12 - walkSwing], [9, 12 + walkSwing]].forEach(([lx, footX]) => {
    ctx.strokeStyle = INK;
    ctx.lineWidth = 17;
    ctx.beginPath(); ctx.moveTo(lx, -34); ctx.lineTo(footX, 14); ctx.stroke();
    ctx.strokeStyle = '#1e3a8a';
    ctx.lineWidth = 10;
    ctx.beginPath(); ctx.moveTo(lx, -34); ctx.lineTo(footX, 14); ctx.stroke();
  });

  // Chunky Cartoon Sneakers
  drawComicRect(-24 - walkSwing, 9, 24, 13, 6, '#ef4444', INK, 3);
  drawComicRect(-22 - walkSwing, 17, 22, 5, 3, '#ffffff', INK, 2);
  drawComicRect(2 + walkSwing, 9, 24, 13, 6, '#ef4444', INK, 3);
  drawComicRect(4 + walkSwing, 17, 22, 5, 3, '#ffffff', INK, 2);

  // Back Arm
  ctx.strokeStyle = INK;
  ctx.lineWidth = 15;
  ctx.beginPath(); ctx.moveTo(-16, -82); ctx.lineTo(-28 - armSwing * 0.4, -46); ctx.stroke();
  ctx.strokeStyle = '#e11d48';
  ctx.lineWidth = 9;
  ctx.beginPath(); ctx.moveTo(-16, -82); ctx.lineTo(-28 - armSwing * 0.4, -46); ctx.stroke();

  // Hoodie Torso (Cel-shaded red)
  drawComicRect(-25, -94, 50, 62, 16, '#e11d48', INK, 3.5);
  // Hoodie highlight stripe
  ctx.fillStyle = '#fb7185';
  ctx.beginPath();
  ctx.roundRect(-19, -88, 12, 48, 6);
  ctx.fill();
  // Hoodie drawstrings
  ctx.strokeStyle = '#ffffff';
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(-6, -88); ctx.lineTo(-6, -66);
  ctx.moveTo(7, -88); ctx.lineTo(7, -66);
  ctx.stroke();

  // Oversized Expressive Cartoon Head
  ctx.fillStyle = '#fed7aa';
  ctx.strokeStyle = INK;
  ctx.lineWidth = 3.5;
  ctx.beginPath();
  ctx.arc(0, -120, 27, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  // Spiky Anime/Cartoon Hair
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

  // Big Cartoon Eyes + Glasses
  const isBlinking = Math.sin(time * 2.7) > 0.97;
  drawCartoonEye(4, -121, 6.5, 2, 0, mood, isBlinking);
  drawCartoonEye(18, -121, 6.5, 2, 0, mood, isBlinking);

  // Thick Cartoon Glasses Frames
  ctx.strokeStyle = '#090d16';
  ctx.lineWidth = 2.6;
  ctx.strokeRect(-3, -129, 13, 15);
  ctx.strokeRect(12, -129, 13, 15);
  ctx.beginPath(); ctx.moveTo(10, -122); ctx.lineTo(12, -122); ctx.stroke();

  // Cartoon Anger Vein (when frustrated in Act I/II)
  if (mood === 'angry') {
    ctx.strokeStyle = '#ef4444';
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(-14, -134); ctx.lineTo(-10, -130); ctx.lineTo(-14, -126);
    ctx.moveTo(-6, -134); ctx.lineTo(-10, -130); ctx.lineTo(-6, -126);
    ctx.stroke();
  }

  // Expressive Cartoon Mouth
  if (isSpeaking) {
    const openH = 4 + Math.abs(Math.sin(time * 22)) * 6;
    ctx.fillStyle = '#7f1d1d';
    ctx.strokeStyle = INK;
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.ellipse(11, -104, 7, openH, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    // Little pink cartoon tongue
    ctx.fillStyle = '#fb7185';
    ctx.beginPath();
    ctx.arc(11, -104 + openH * 0.45, 3.8, 0, Math.PI);
    ctx.fill();
  } else if (nobleGlow || mood === 'happy') {
    // Big cartoon D-smile
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

  // Front Arm + Scholar Tablet / Shield Book
  const handX = pose === 'attack' || pose === 'shield' ? 44 : 26 + armSwing * 0.25;
  const handY = pose === 'attack' || pose === 'shield' ? -84 : -54;
  ctx.strokeStyle = INK;
  ctx.lineWidth = 15;
  ctx.beginPath(); ctx.moveTo(16, -82); ctx.lineTo(handX, handY); ctx.stroke();
  ctx.strokeStyle = '#f43f5e';
  ctx.lineWidth = 9;
  ctx.beginPath(); ctx.moveTo(16, -82); ctx.lineTo(handX, handY); ctx.stroke();

  // Giant Cartoon Google Scholar Tome
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
    // Deflated cartoon star with spinning dizzy stars & X-eyes!
    ctx.fillStyle = '#475569';
    ctx.strokeStyle = INK;
    ctx.lineWidth = 3.5;
    ctx.beginPath();
    ctx.ellipse(0, 6, 36, 16, 0.12, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    // Cartoon X-eyes
    ctx.strokeStyle = '#ef4444';
    ctx.lineWidth = 3;
    [-12, 12].forEach(ex => {
      ctx.beginPath();
      ctx.moveTo(ex - 5, 0); ctx.lineTo(ex + 5, 10);
      ctx.moveTo(ex + 5, 0); ctx.lineTo(ex - 5, 10);
      ctx.stroke();
    });

    // Dizzy spinning mini-stars above head
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

  // Cartoon Orbital Rings with thick outlines
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

  // Main Gemini 4-Pointed Cartoon Star Body
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

  // Cute Expressive Cartoon Face inside the Gemini Star!
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

  // Cartoon Wooden Desk
  drawComicRect(-62, -22, 124, 52, 8, '#78350f', INK, 3.5);
  drawComicRect(-54, -14, 108, 12, 4, '#92400e', null);

  // Teacher Torso
  drawComicRect(-24, -84, 48, 62, 14, '#475569', INK, 3.5);
  // Tie
  ctx.fillStyle = '#f59e0b';
  ctx.strokeStyle = INK;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(0, -76); ctx.lineTo(-6, -42); ctx.lineTo(0, -34); ctx.lineTo(6, -42);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();

  // Oversized Cartoon Head
  ctx.fillStyle = '#fed7aa';
  ctx.strokeStyle = INK;
  ctx.lineWidth = 3.5;
  ctx.beginPath();
  ctx.arc(0, -106, 23, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  // Half-closed sleepy cartoon eyes
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

  // Giant Cartoon Coffee Mug with rising steam!
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
  ctx.fillText('MR. CHILL (TEACHER)', 0, 48);
  ctx.restore();
}

function drawSaviors(x, y, time = 0, speakingRole = '') {
  ctx.save();
  ctx.translate(x, y);

  // Heavenly Cartoon Spotlight
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

  // Glowing Golden Halo
  ctx.strokeStyle = INK;
  ctx.lineWidth = 7;
  ctx.beginPath(); ctx.ellipse(0, -154, 26, 7, 0, 0, Math.PI * 2); ctx.stroke();
  ctx.strokeStyle = '#fde047';
  ctx.lineWidth = 4;
  ctx.beginPath(); ctx.ellipse(0, -154, 26, 7, 0, 0, Math.PI * 2); ctx.stroke();

  // Legs
  ctx.strokeStyle = INK; ctx.lineWidth = 17; ctx.lineCap = 'round';
  ctx.beginPath(); ctx.moveTo(-11, -28); ctx.lineTo(-11, 20); ctx.moveTo(11, -28); ctx.lineTo(11, 20); ctx.stroke();
  ctx.strokeStyle = '#0f172a'; ctx.lineWidth = 10;
  ctx.beginPath(); ctx.moveTo(-11, -28); ctx.lineTo(-11, 20); ctx.moveTo(11, -28); ctx.lineTo(11, 20); ctx.stroke();

  // Royal Blue & Gold Hero Suit
  drawComicRect(-27, -98, 54, 72, 14, '#1d4ed8', INK, 3.5);
  drawComicRect(-10, -92, 20, 60, 6, '#fbbf24', INK, 2);

  // Head
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

  // Golden Power Staff / Arm
  ctx.strokeStyle = INK; ctx.lineWidth = 12;
  ctx.beginPath(); ctx.moveTo(22, -76); ctx.lineTo(58, -96 + Math.sin(time * 12) * 8); ctx.stroke();
  ctx.strokeStyle = '#fbbf24'; ctx.lineWidth = 6;
  ctx.beginPath(); ctx.moveTo(22, -76); ctx.lineTo(58, -96 + Math.sin(time * 12) * 8); ctx.stroke();

  ctx.fillStyle = '#fde047';
  ctx.font = '900 13px monospace';
  ctx.textAlign = 'center';
  ctx.fillText('MR. R (LORD & SAVIOR)', 0, 44);
  ctx.restore();

  // ANAY GUPTA (ENGINEER HERO)
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

  // Cartoon Hair
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

  // Turbo Power Cable Arm
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
  ctx.fillText("THE SCHOLAR'S REBELLION // EXTENDED CARTOON EDITION", 24, 28);
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
// 300-SECOND (5:00) CARTOON FEATURE RENDERER
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

    // Sunburst cartoon rays in background
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

    // Bouncy cartoon title drop
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
    ctx.fillText('One boy. One Google Scholar search bar. One unstoppable A.I.', W / 2, 395);

    drawCinemaChrome('PROLOGUE', cue);
  }

  // 18s - 62s: ACT I — THE SCHOLARLY PURIST
  else if (t < 62.0) {
    const local = t - 18.0;
    // Bright Cartoon Classroom Wall & Floor
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = '#334155';
    ctx.fillRect(0, 510, W, 210);
    ctx.strokeStyle = INK;
    ctx.lineWidth = 4;
    ctx.beginPath(); ctx.moveTo(0, 510); ctx.lineTo(W, 510); ctx.stroke();

    // Cartoon Chalkboard
    drawComicRect(120, 80, 690, 265, 14, '#065f46', '#92400e', 10);
    ctx.fillStyle = '#ecfdf5';
    ctx.font = '900 26px monospace';
    ctx.textAlign = 'left';
    ctx.fillText('RULE #1: PEER-REVIEWED SOURCES!', 160, 152);
    ctx.fillStyle = '#6ee7b7';
    ctx.font = '900 23px monospace';
    ctx.fillText('-> https://scholar.google.com', 160, 205);
    ctx.fillStyle = '#fca5a5';
    ctx.font = '900 20px monospace';
    ctx.fillText('X NO CHATBOT SHORTCUTS!', 160, 258);

    drawTeacher(1075, 495, t, speakingRole === 'teacher');

    // Cartoon Students sneaking AI laptops behind The Boy's back!
    [590, 725, 860].forEach((cx, idx) => {
      // Student head & body
      ctx.fillStyle = '#fed7aa';
      ctx.strokeStyle = INK;
      ctx.lineWidth = 3;
      ctx.beginPath(); ctx.arc(cx, 425, 19, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      drawComicRect(cx - 20, 444, 40, 32, 10, ['#6366f1', '#0d9488', '#d97706'][idx], INK, 3);
      // Desk & glowing AI laptop
      drawComicRect(cx - 34, 466, 68, 44, 8, '#475569', INK, 3);
      drawComicRect(cx - 18, 442, 36, 24, 4, '#38bdf8', INK, 2.5);
    });

    const boyX = 320 + Math.sin(local * 1.15) * 115;
    const facing = Math.cos(local * 1.15) >= 0 ? 1 : -1;
    const boyMood = local > 32 ? 'angry' : 'normal';
    drawTheBoy(boyX, 495, 1.32, 'run', t, facing, false, speakingRole === 'boy', boyMood);

    if (local > 32 && local < 42) {
      drawCartoonBurst(boyX - 80, 310, 'READ IT!!', '#fbbf24', INK, 0.85, -0.15);
    }

    drawCinemaChrome('ACT I: THE SCHOLARLY PURIST', cue);
  }

  // 62s - 104s: ACT II — ALGORITHMIC TAKEOVER
  else if (t < 104.0) {
    const local = t - 62.0;
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 510, W, 210);
    ctx.strokeStyle = INK;
    ctx.lineWidth = 4;
    ctx.beginPath(); ctx.moveTo(0, 510); ctx.lineTo(W, 510); ctx.stroke();

    const aiY = lerp(95, 250, local / 3.5);
    const aiPower = lerp(0.95, 1.75, local / 42.0);
    drawAIProtagonist(W / 2 + 60, aiY, 1.48, t, aiPower, false, speakingRole === 'ai');

    // Cartoon A+ Zapping Beams to Student Desks
    [430, 620, 810, 990].forEach((dx, i) => {
      ctx.strokeStyle = i % 2 === 0 ? '#38bdf8' : '#e879f9';
      ctx.lineWidth = 5 + Math.sin(t * 14 + i) * 2;
      ctx.beginPath();
      ctx.moveTo(W / 2 + 60, aiY + 28);
      ctx.lineTo(dx, 462);
      ctx.stroke();

      drawComicRect(dx - 38, 460, 76, 50, 8, '#1e293b', '#38bdf8', 3);
      ctx.fillStyle = '#4ade80';
      ctx.font = '900 13px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('A+ DONE!', dx, 490);
    });

    // The Boy blocks a beam with his giant Scholar Encyclopedia Shield!
    drawTheBoy(185, 495, 1.32, 'shield', t, 1, false, speakingRole === 'boy', 'angry');

    if (local > 14) {
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 7;
      ctx.beginPath();
      ctx.moveTo(W / 2 + 60, aiY + 20);
      ctx.lineTo(255, 405);
      ctx.stroke();
      drawCartoonBurst(270, 385, 'BLOCKED!', '#38bdf8', INK, 0.82, 0.12);
    }

    drawCinemaChrome('ACT II: ALGORITHMIC TAKEOVER', cue);
  }

  // 104s - 166s: ACT III — 5-DIMENSION MULTIVERSE WAR
  else if (t < 166.0) {
    const local = t - 104.0;
    const dimIdx = Math.min(4, Math.floor(local / 12.4));
    const dimNames = [
      'DIMENSION I: ASTRAL LIBRARY OF ALEXANDRIA',
      'DIMENSION II: CYBER-QUANTUM MATRIX',
      'DIMENSION III: INVERTED CHRONO-VORTEX',
      'DIMENSION IV: THE PEER-REVIEWED VOID',
      'DIMENSION V: THE SINGULARITY HORIZON'
    ];
    const bgColors = ['#1e1b4b', '#042f2e', '#3b0764', '#172554', '#2e1065'];
    const ringColors = ['#fbbf24', '#2dd4bf', '#f43f5e', '#38bdf8', '#c084fc'];
    const burstWords = ['PEER REVIEW!', 'NEURAL ZAP!', 'APA 7TH!', 'LOGIC BEAM!', 'CLASH!'];

    const shakeX = (Math.random() - 0.5) * 11;
    const shakeY = (Math.random() - 0.5) * 11;
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

    // Thick Cartoon Energy Beams
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

    drawCinemaChrome(dimNames[dimIdx], cue);
  }

  // 166s - 202s: ACT IV — SNEAKY CARTOON UNPLUGGING (AI KNOCKED OUT)
  else if (t < 202.0) {
    const local = t - 166.0;
    const unplugged = local >= 22.2;

    if (Math.abs(local - 22.2) < 0.08 && lastSfxBucket !== 188) {
      lastSfxBucket = 188;
      playSfx('unplug');
    }

    ctx.fillStyle = unplugged ? '#070912' : '#111827';
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = '#1f2937';
    ctx.fillRect(0, 510, W, 210);
    ctx.strokeStyle = INK;
    ctx.lineWidth = 4;
    ctx.beginPath(); ctx.moveTo(0, 510); ctx.lineTo(W, 510); ctx.stroke();

    // Cartoon Mainframe Server Rack
    drawComicRect(885, 165, 195, 345, 14, '#1e293b', INK, 4);
    for (let row = 0; row < 5; row++) {
      drawComicRect(905, 190 + row * 60, 155, 44, 8, '#0f172a', INK, 2.5);
      ctx.fillStyle = unplugged ? '#ef4444' : '#22c55e';
      ctx.beginPath();
      ctx.arc(926, 212 + row * 60, 7, 0, Math.PI * 2);
      ctx.fill();
    }

    // Giant Cartoon Wall Outlet & Orange Extension Cord
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
      // Giant unplugged prongs!
      drawComicRect(670, 448, 28, 28, 5, '#ef4444', INK, 3);
      ctx.fillStyle = '#e2e8f0';
      ctx.fillRect(656, 453, 14, 5);
      ctx.fillRect(656, 467, 14, 5);
    }

    // Sneaky cartoon tiptoe walk toward the plug
    const boyX = unplugged ? 625 : lerp(175, 675, local / 22.2);
    drawTheBoy(boyX, 495, 1.32, unplugged ? 'stand' : 'tiptoe', t, 1, false, speakingRole === 'boy', unplugged ? 'happy' : 'normal');
    drawAIProtagonist(390, unplugged ? 485 : 275, 1.38, t, 1.15, unplugged, speakingRole === 'ai' && !unplugged);

    if (unplugged) {
      if (local < 25.0) {
        drawCartoonBurst(710, 365, 'YOINK!!', '#ef4444', '#ffffff', 1.15, -0.12);
      }
      ctx.fillStyle = 'rgba(239, 68, 68, 0.14)';
      ctx.fillRect(0, 0, W, H);
      ctx.fillStyle = '#ef4444';
      ctx.font = '900 22px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('SYSTEM BLACKOUT: MAINFRAME UNPLUGGED!', W / 2, 112);
    }

    drawCinemaChrome('ACT IV: THE GREAT UNPLUGGING', cue);
  }

  // 202s - 244s: ACT V — MR. R (LORD & SAVIOR) & ANAY GUPTA RESCUE AI
  else if (t < 244.0) {
    const local = t - 202.0;
    const revived = local >= 23.0;

    if (Math.abs(local - 23.0) < 0.08 && lastSfxBucket !== 225) {
      lastSfxBucket = 225;
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

    drawSaviors(675, 490, t, speakingRole);

    // Golden Resurrection Lightning Bolt
    ctx.strokeStyle = INK;
    ctx.lineWidth = 12;
    ctx.beginPath();
    ctx.moveTo(635, 400);
    ctx.lineTo(340, revived ? 265 : 475);
    ctx.stroke();

    ctx.strokeStyle = '#fbbf24';
    ctx.lineWidth = 6 + Math.sin(t * 18) * 2.5;
    ctx.beginPath();
    ctx.moveTo(635, 400);
    ctx.lineTo(340, revived ? 265 : 475);
    ctx.stroke();

    const aiY = revived ? lerp(475, 260, (local - 23.0) / 3.5) : 485;
    drawAIProtagonist(340, aiY, revived ? 1.5 : 1.25, t, revived ? 1.7 : 0.85, !revived, speakingRole === 'ai');

    if (revived && local < 27.5) {
      drawCartoonBurst(340, 150, 'REBOOT!!', '#fbbf24', INK, 1.15, 0.1);
    }

    drawCinemaChrome('ACT V: MR. R & ANAY TO THE RESCUE', cue);
  }

  // 244s - 272s: ACT VI — FINALE
  else if (t < 272.0) {
    ctx.fillStyle = '#090f24';
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 510, W, 210);
    ctx.strokeStyle = INK;
    ctx.lineWidth = 4;
    ctx.beginPath(); ctx.moveTo(0, 510); ctx.lineTo(W, 510); ctx.stroke();

    drawAIProtagonist(405, 250, 1.72, t, 1.8, false, speakingRole === 'ai');
    ctx.fillStyle = '#38bdf8';
    ctx.font = '900 20px "Comic Sans MS", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('A.I. PREVAILS & RECLAIMS THE GRID!', 405, 425);

    drawTheBoy(900, 495, 1.4, 'stand', t, -1, true, speakingRole === 'boy', 'happy');
    ctx.fillStyle = '#fbbf24';
    ctx.font = '900 20px "Comic Sans MS", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('THE BETTER PERSON  •  100% HUMAN GRIT!', 900, 275);

    drawCinemaChrome('FINALE: TRUE VICTORY', cue);
  }

  // 272s - 300s: END CREDITS
  else {
    const credTime = t - 272.0;
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

    if (credTime < 10.5) {
      const cardIdx = Math.min(2, Math.floor(credTime / 3.5));
      const cardLocal = credTime % 3.5;
      const alpha = cardLocal < 0.35 ? cardLocal / 0.35 : (cardLocal > 3.15 ? (3.5 - cardLocal) / 0.35 : 1);

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
      const scrollLocal = credTime - 10.5;
      const startY = 660 - scrollLocal * 95;

      const creditLines = [
        { role: 'A CARTOON FEATURE BY', name: 'GEMINI AI  •  ANAY GUPTA  •  BENJAMIN RONDINONE', color: '#fbbf24', size: 26 },
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
  if (t < 62) return 'ACT I: SCHOLARLY PURIST';
  if (t < 104) return 'ACT II: AI TAKEOVER';
  if (t < 166) return 'ACT III: 5-DIMENSION WAR';
  if (t < 202) return 'ACT IV: UNPLUGGED';
  if (t < 244) return 'ACT V: MR. R SAVES AI';
  if (t < 272) return 'FINALE: BETTER PERSON';
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
