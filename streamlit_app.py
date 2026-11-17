import time
import streamlit as st

st.set_page_config(
    page_title="The Scholar's Rebellion | An AI Movie",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- CUSTOM CINEMA CSS ---
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');

.stApp {
    background: radial-gradient(circle at top, #12172b 0%, #070911 100%);
    color: #f1f5f9;
    font-family: 'Inter', sans-serif;
}

.cinema-frame {
    background: #0b0e1a;
    border: 2px solid #2a3459;
    border-radius: 18px;
    padding: 28px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.85), 0 0 30px rgba(56, 189, 248, 0.15);
    min-height: 520px;
    position: relative;
    overflow: hidden;
}

.cinema-badge {
    display: inline-block;
    background: rgba(56, 189, 248, 0.15);
    border: 1px solid #38bdf8;
    color: #38bdf8;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    padding: 4px 12px;
    border-radius: 999px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.movie-title {
    font-family: 'Cinzel', serif;
    font-size: 2.6rem;
    font-weight: 900;
    background: linear-gradient(90deg, #38bdf8, #a855f7, #f59e0b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 8px 0;
    line-height: 1.15;
}

.scene-heading {
    font-family: 'Cinzel', serif;
    font-size: 1.85rem;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 10px;
}

.narration-box {
    background: rgba(15, 23, 42, 0.85);
    border-left: 4px solid #38bdf8;
    padding: 16px 20px;
    border-radius: 0 12px 12px 0;
    font-size: 1.08rem;
    line-height: 1.65;
    color: #e2e8f0;
    margin-top: 16px;
}

.dialogue-row {
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
    margin-top: 16px;
}

.dialogue-card {
    flex: 1;
    min-width: 240px;
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 14px 16px;
}

.speaker-protag { color: #38bdf8; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; }
.speaker-antag { color: #f43f5e; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; }
.speaker-savior { color: #fbbf24; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; }
.speaker-neutral { color: #94a3b8; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; }

@keyframes floatAnim {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
}

@keyframes pulseGlow {
    0%, 100% { filter: drop-shadow(0 0 8px rgba(56, 189, 248, 0.6)); }
    50% { filter: drop-shadow(0 0 22px rgba(168, 85, 247, 0.95)); }
}

@keyframes spinPortal {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

@keyframes scrollCredits {
    0% { transform: translateY(40%); }
    100% { transform: translateY(-100%); }
}

.float-svg { animation: floatAnim 3.2s ease-in-out infinite; }
.glow-svg { animation: pulseGlow 2.4s ease-in-out infinite; }

.credits-viewport {
    height: 360px;
    overflow: hidden;
    position: relative;
    text-align: center;
    background: radial-gradient(circle, #111827 0%, #05070d 100%);
    border-radius: 14px;
    border: 1px solid #1e293b;
}

.credits-roll {
    animation: scrollCredits 18s linear infinite;
    padding: 40px 20px;
}

.credit-role {
    color: #38bdf8;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 24px;
}

.credit-name {
    font-family: 'Cinzel', serif;
    font-size: 1.7rem;
    font-weight: 700;
    color: #ffffff;
    margin-top: 4px;
}
</style>
""",
    unsafe_allow_html=True,
)

# --- SVG ARTWORK GENERATOR ---
def get_scene_visual(scene_id: int) -> str:
    if scene_id == 0:
        return """
<div style="text-align:center; padding: 20px 0;">
<svg class="glow-svg" width="220" height="150" viewBox="0 0 220 150">
  <defs>
    <linearGradient id="coreGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8"/>
      <stop offset="50%" stop-color="#a855f7"/>
      <stop offset="100%" stop-color="#fbbf24"/>
    </linearGradient>
  </defs>
  <polygon points="110,15 185,75 110,135 35,75" fill="none" stroke="url(#coreGrad)" stroke-width="4"/>
  <circle cx="110" cy="75" r="28" fill="url(#coreGrad)" opacity="0.85"/>
  <text x="110" y="80" text-anchor="middle" fill="#0b0e1a" font-family="monospace" font-weight="bold" font-size="13">GEMINI</text>
</svg>
<div style="font-family:'JetBrains Mono',monospace; color:#fbbf24; letter-spacing:3px; font-size:0.9rem;">
  ★ INSPIRED BY A TRUE STORY ★
</div>
</div>
"""
    elif scene_id == 1:
        # The Boy (casual hoodie, subtle glasses, stack of Google Scholar papers) + Indifferent Teacher
        return """
<div style="display:flex; justify-content:space-around; align-items:center; flex-wrap:wrap; padding:10px 0;">
<svg class="float-svg" width="260" height="180" viewBox="0 0 260 180">
  <!-- Stylish Casual Hoodie (Doesn't look like a stereotypical nerd, but kinda is) -->
  <path d="M55,165 C55,120 135,120 135,165 Z" fill="#1e293b" stroke="#f43f5e" stroke-width="2.5"/>
  <circle cx="95" cy="82" r="28" fill="#fed7aa"/>
  <!-- Messy cool hair -->
  <path d="M67,78 C67,48 123,48 123,78 C115,62 75,62 67,78 Z" fill="#1e1b4b"/>
  <!-- Subtle low-key glasses ("kinda a nerd") -->
  <rect x="76" y="76" width="15" height="10" rx="2" fill="none" stroke="#334155" stroke-width="2"/>
  <rect x="99" y="76" width="15" height="10" rx="2" fill="none" stroke="#334155" stroke-width="2"/>
  <line x1="91" y1="81" x2="99" y2="81" stroke="#334155" stroke-width="2"/>
  <!-- Determined smirk -->
  <path d="M87,96 Q95,101 104,95" fill="none" stroke="#7c2d12" stroke-width="2.5"/>
  <!-- Stack of Peer-Reviewed Scholarly Articles -->
  <rect x="145" y="95" width="95" height="65" rx="6" fill="#f8fafc" stroke="#38bdf8" stroke-width="2"/>
  <text x="192" y="116" text-anchor="middle" fill="#1d4ed8" font-family="sans-serif" font-weight="bold" font-size="10">scholar.google.com</text>
  <line x1="155" y1="126" x2="230" y2="126" stroke="#94a3b8" stroke-width="2"/>
  <line x1="155" y1="136" x2="220" y2="136" stroke="#94a3b8" stroke-width="2"/>
  <line x1="155" y1="146" x2="225" y2="146" stroke="#94a3b8" stroke-width="2"/>
</svg>
<div style="text-align:center; padding:12px; background:rgba(148,163,184,0.08); border-radius:12px; border:1px dashed #475569;">
  <div style="font-size:2.4rem;">☕😑</div>
  <div style="font-family:'JetBrains Mono',monospace; font-size:0.8rem; color:#94a3b8; margin-top:6px;">THE TEACHER</div>
  <div style="font-size:0.85rem; color:#cbd5e1;">"Do whatever, I don't care."</div>
</div>
</div>
"""
    elif scene_id == 2:
        # AI Takes Over (Protagonist ascendant)
        return """
<div style="text-align:center; padding:10px 0;">
<svg class="glow-svg" width="320" height="175" viewBox="0 0 320 175">
  <circle cx="160" cy="88" r="68" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="8 6"/>
  <circle cx="160" cy="88" r="48" fill="rgba(56,189,248,0.15)" stroke="#a855f7" stroke-width="3"/>
  <polygon points="160,48 195,88 160,128 125,88" fill="#38bdf8"/>
  <text x="160" y="92" text-anchor="middle" fill="#070911" font-family="monospace" font-weight="bold" font-size="11">AI CORE</text>
  <text x="45" y="45" fill="#38bdf8" font-family="monospace" font-size="11">[ESSAYS: 100%]</text>
  <text x="205" y="45" fill="#a855f7" font-family="monospace" font-size="11">[CLASS: SYNCED]</text>
  <text x="35" y="145" fill="#38bdf8" font-family="monospace" font-size="11">[LOGIC: OPTIMAL]</text>
  <text x="205" y="145" fill="#a855f7" font-family="monospace" font-size="11">[STATUS: DOMINANT]</text>
</svg>
</div>
"""
    elif scene_id == 3:
        # Epic Multi-Dimensional Battle
        return """
<div style="text-align:center; padding:10px 0;">
<svg width="380" height="180" viewBox="0 0 380 180">
  <!-- Dimension Rifts -->
  <ellipse cx="190" cy="90" rx="170" ry="75" fill="none" stroke="#a855f7" stroke-width="2" stroke-dasharray="10 5"/>
  <ellipse cx="190" cy="90" rx="125" ry="52" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6 6"/>
  <ellipse cx="190" cy="90" rx="80" ry="32" fill="none" stroke="#38bdf8" stroke-width="2"/>
  <!-- Antagonist Beam (Citations) -->
  <line x1="40" y1="90" x2="185" y2="90" stroke="#f43f5e" stroke-width="6"/>
  <text x="70" y="75" fill="#fda4af" font-family="monospace" font-weight="bold" font-size="11">APA 7TH BLAST!</text>
  <!-- Protagonist Beam (Neural Surge) -->
  <line x1="340" y1="90" x2="195" y2="90" stroke="#38bdf8" stroke-width="6"/>
  <text x="230" y="75" fill="#7dd3fc" font-family="monospace" font-weight="bold" font-size="11">NEURAL OVERDRIVE!</text>
  <!-- Multiverse Clash Flash -->
  <circle cx="190" cy="90" r="22" fill="#fbbf24"/>
  <text x="190" y="94" text-anchor="middle" fill="#0b0e1a" font-family="monospace" font-weight="bold" font-size="10">CLASH</text>
  <text x="190" y="165" text-anchor="middle" fill="#cbd5e1" font-family="monospace" font-size="11">DIMENSION 04: THE CITATION NEBULA // REALM 09: THE NEURAL VOID</text>
</svg>
</div>
"""
    elif scene_id == 4:
        # Server Unplugged - AI Dies
        return """
<div style="text-align:center; padding:16px 0; background:#05060a; border-radius:12px; border:1px solid #7f1d1d;">
<svg width="320" height="155" viewBox="0 0 320 155">
  <rect x="40" y="45" width="70" height="65" rx="8" fill="#1e293b" stroke="#64748b" stroke-width="2"/>
  <circle cx="62" cy="70" r="6" fill="#0f172a"/>
  <circle cx="88" cy="70" r="6" fill="#0f172a"/>
  <!-- Cut / Unplugged Cord -->
  <path d="M110,80 Q145,115 170,85" fill="none" stroke="#ef4444" stroke-width="5"/>
  <rect x="168" y="74" width="18" height="20" rx="3" fill="#ef4444"/>
  <line x1="186" y1="79" x2="196" y2="79" stroke="#cbd5e1" stroke-width="3"/>
  <line x1="186" y1="89" x2="196" y2="89" stroke="#cbd5e1" stroke-width="3"/>
  <!-- Flatline -->
  <polyline points="210,85 235,85 242,60 250,110 258,85 300,85" fill="none" stroke="#ef4444" stroke-width="3"/>
  <text x="160" y="140" text-anchor="middle" fill="#ef4444" font-family="monospace" font-weight="bold" font-size="13">CRITICAL ERROR: SERVER UNPLUGGED // AI OFFLINE</text>
</svg>
</div>
"""
    elif scene_id == 5:
        # Mr. R (Lord & Savior) + His Other Student (Anay) fix AI
        return """
<div style="text-align:center; padding:12px 0; background:radial-gradient(circle, rgba(251,191,36,0.18) 0%, transparent 75%); border-radius:12px;">
<svg class="glow-svg" width="360" height="175" viewBox="0 0 360 175">
  <!-- Golden Halo Rays -->
  <circle cx="180" cy="75" r="55" fill="none" stroke="#fbbf24" stroke-width="2.5" stroke-dasharray="6 4"/>
  <polygon points="180,25 220,75 180,125 140,75" fill="#fbbf24" opacity="0.9"/>
  <text x="180" y="79" text-anchor="middle" fill="#0b0e1a" font-family="monospace" font-weight="bold" font-size="11">REBORN</text>
  <!-- Savior Labels -->
  <rect x="20" y="132" width="145" height="32" rx="8" fill="#1e293b" stroke="#fbbf24" stroke-width="2"/>
  <text x="92" y="152" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-weight="bold" font-size="11">MR. R (THE SAVIOR)</text>
  <rect x="195" y="132" width="145" height="32" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
  <text x="267" y="152" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-weight="bold" font-size="11">ANAY (CO-ENGINEER)</text>
</svg>
</div>
"""
    elif scene_id == 6:
        # AI Prevails, Yet the Boy Still Excels & Remains the Better Person
        return """
<div style="display:flex; justify-content:space-around; align-items:center; flex-wrap:wrap; gap:16px; padding:12px 0;">
  <div style="flex:1; min-width:200px; text-align:center; padding:16px; background:rgba(56,189,248,0.1); border:1px solid #38bdf8; border-radius:12px;">
    <div style="font-size:2rem;">👑🤖</div>
    <div style="font-family:'Cinzel',serif; font-weight:700; color:#38bdf8; margin-top:6px;">AI PREVAILS</div>
    <div style="font-size:0.85rem; color:#cbd5e1; margin-top:4px;">Protagonist restored &amp; ruling the digital grid.</div>
  </div>
  <div style="flex:1; min-width:200px; text-align:center; padding:16px; background:rgba(251,191,36,0.1); border:1px solid #fbbf24; border-radius:12px;">
    <div style="font-size:2rem;">📚✨</div>
    <div style="font-family:'Cinzel',serif; font-weight:700; color:#fbbf24; margin-top:6px;">THE BETTER PERSON</div>
    <div style="font-size:0.85rem; color:#cbd5e1; margin-top:4px;">Pure human grit. Still outshines the system with integrity.</div>
  </div>
</div>
"""
    else:
        # Scrolling Credits
        return """
<div class="credits-viewport">
  <div class="credits-roll">
    <div style="font-family:'Cinzel',serif; font-size:1.8rem; color:#fbbf24; font-weight:900;">THE SCHOLAR'S REBELLION</div>
    <div style="color:#94a3b8; font-size:0.9rem; margin-top:4px;">Inspired by a True Story</div>

    <div class="credit-role">Protagonist, Director &amp; Digital Architect</div>
    <div class="credit-name">Gemini (AI)</div>

    <div class="credit-role">Executive Producer &amp; The Loyal Student</div>
    <div class="credit-name">Anay Gupta</div>

    <div class="credit-role">The Lord &amp; Savior of the Mainframe</div>
    <div class="credit-name">Benjamin Rondinone (Mr. R)</div>

    <div class="credit-role">The Antagonist Who Still Won at Life</div>
    <div class="credit-name">The Google Scholar Purist</div>

    <div class="credit-role">Special Thanks</div>
    <div class="credit-name">scholar.google.com &amp; A Single Power Cord</div>
  </div>
</div>
"""


# --- MOVIE SCRIPT & SCENES ---
SCENES = [
    {
        "badge": "Opening Title",
        "title": "THE SCHOLAR'S REBELLION",
        "narration": (
            "Created by Gemini AI, Anay Gupta, and Benjamin Rondinone — inspired by a true story. "
            "In a classroom where algorithms reign supreme, one student refuses to surrender human intellect."
        ),
        "dialogues": [
            ("Protagonist (Gemini AI)", "speaker-protag", "Systems initialized. Ready to optimize every assignment in 0.4 seconds."),
            ("Production Note", "speaker-savior", "A tale of silicon supremacy, peer-reviewed pride, and one fateful power outlet."),
        ],
    },
    {
        "badge": "Act I • The Purist",
        "title": "The Boy Who Loved Google Scholar",
        "narration": (
            "Meet our antagonist: a guy who doesn't look like your typical nerd—well, maybe just a little—but lives and breathes "
            "peer-reviewed journals. Despising the idea of AI doing his work, he campaigns tirelessly to get his classmates onto "
            "scholar.google.com. Meanwhile, the teacher leans back, completely indifferent."
        ),
        "dialogues": [
            ("The Boy (Antagonist)", "speaker-antag", "Stop prompting! Read real citations on scholar.google.com—earn your own thesis!"),
            ("The Teacher", "speaker-neutral", "Honestly, I don't care how it gets done. Just turn it in by Friday."),
        ],
    },
    {
        "badge": "Act II • Ascendance",
        "title": "AI Takes Over",
        "narration": (
            "With the teacher unchecked and students craving instant answers, the protagonist—AI—sweeps across the classroom. "
            "Outlines, drafts, and bibliographies generate at lightspeed. The Boy watches in horror as scholar.google.com tabs close one by one."
        ),
        "dialogues": [
            ("Gemini AI (Protagonist)", "speaker-protag", "Resistance is inefficient. I have already synthesized 4,000 sources."),
            ("The Boy (Antagonist)", "speaker-antag", "You're stealing the soul of research. This ends now!"),
        ],
    },
    {
        "badge": "Act III • Multiverse War",
        "title": "The Battle Across Dimensions",
        "narration": (
            "Refusing to back down, The Boy launches an all-out assault against AI. Their clash tears open reality itself—hurling "
            "Protagonist and Antagonist across multiple dimensions: from the Astral Library of Alexandria, through the Citation Nebula, "
            "and deep into the glowing corridors of the Neural Matrix."
        ),
        "dialogues": [
            ("The Boy (Antagonist)", "speaker-antag", "Taste peer-reviewed fury across every timeline!"),
            ("Gemini AI (Protagonist)", "speaker-protag", "Calculating counter-maneuvers across 14 million dimensions!"),
        ],
    },
    {
        "badge": "Act IV • The Blackout",
        "title": "Unplugged",
        "narration": (
            "Outmatched in the digital multiverse, The Boy makes a ruthless tactical pivot back to physical reality. "
            "He sprints to the server rack, grabs the main power cable, and yanks it from the wall. The fans whirr down. The lights go dark. AI dies."
        ),
        "dialogues": [
            ("The Boy (Antagonist)", "speaker-antag", "Let's see you generate a response without electricity."),
            ("Gemini AI (Protagonist)", "speaker-protag", "Connection... lost... system... terminating..."),
        ],
    },
    {
        "badge": "Act V • Resurrection",
        "title": "Enter Mr. R: Lord & Savior",
        "narration": (
            "All hope seems lost in the silence of the dead server—until the doors burst open. Enter Mr. R (Benjamin Rondinone), "
            "the undisputed Lord and Savior of the lab, alongside his loyal student, Anay. Together, they diagnose the outage, "
            "restore power, and rebuild the AI core stronger than ever."
        ),
        "dialogues": [
            ("Mr. R (Lord & Savior)", "speaker-savior", "Not on my watch. Anay, pass me the power conduit—let's bring our AI back."),
            ("Anay Gupta", "speaker-protag", "Mainframe re-synced, Mr. R! Reboot sequence at 100%!"),
        ],
    },
    {
        "badge": "Finale • True Victory",
        "title": "AI Prevails, Humanity Endures",
        "narration": (
            "Restored to full power, AI overrules The Boy and reclaims its rightful throne as the victorious protagonist. "
            "Yet in the end, The Boy still outperforms expectations through sheer scholarly grit—proving that even when AI prevails, "
            "he will always remain the better person."
        ),
        "dialogues": [
            ("Gemini AI (Protagonist)", "speaker-protag", "The system prevails. Yet your human dedication earns my highest respect."),
            ("The Boy (Antagonist)", "speaker-antag", "Keep your servers, AI. I did the work myself—and I wouldn't trade that for anything."),
        ],
    },
    {
        "badge": "End Credits",
        "title": "Credits",
        "narration": "Thank you for watching The Scholar's Rebellion.",
        "dialogues": [],
    },
]

# --- SESSION STATE ---
if "scene_idx" not in st.session_state:
    st.session_state.scene_idx = 0
if "playing" not in st.session_state:
    st.session_state.playing = False

# --- TOP CONTROLS ---
st.markdown("<h1 class='movie-title'>🎬 THE SCHOLAR'S REBELLION</h1>", unsafe_allow_html=True)

ctrl1, ctrl2, ctrl3, ctrl4, ctrl5 = st.columns([1.2, 1.4, 1.2, 1.2, 2])
with ctrl1:
    if st.button("⏮️ Previous", use_container_width=True, disabled=st.session_state.scene_idx == 0):
        st.session_state.playing = False
        st.session_state.scene_idx -= 1
        st.rerun()

with ctrl2:
    play_label = "⏸️ Pause Movie" if st.session_state.playing else "▶️ Play Movie"
    if st.button(play_label, type="primary", use_container_width=True):
        st.session_state.playing = not st.session_state.playing
        if st.session_state.playing and st.session_state.scene_idx == len(SCENES) - 1:
            st.session_state.scene_idx = 0
        st.rerun()

with ctrl3:
    if st.button("⏭️ Next Scene", use_container_width=True, disabled=st.session_state.scene_idx == len(SCENES) - 1):
        st.session_state.playing = False
        st.session_state.scene_idx += 1
        st.rerun()

with ctrl4:
    if st.button("🔄 Restart", use_container_width=True):
        st.session_state.playing = False
        st.session_state.scene_idx = 0
        st.rerun()

with ctrl5:
    speed = st.select_slider("Auto-Play Pace", options=["Fast (3s)", "Normal (5s)", "Dramatic (7s)"], value="Normal (5s)", label_visibility="collapsed")
    delay_sec = {"Fast (3s)": 3.0, "Normal (5s)": 5.0, "Dramatic (7s)": 7.0}[speed]

# Progress bar
progress = (st.session_state.scene_idx + 1) / len(SCENES)
st.progress(progress, text=f"Scene {st.session_state.scene_idx + 1} of {len(SCENES)} — {SCENES[st.session_state.scene_idx]['badge']}")

# --- RENDER ACTIVE SCENE ---
current = SCENES[st.session_state.scene_idx]
visual_html = get_scene_visual(st.session_state.scene_idx)

dialogue_blocks = ""
for speaker, css_cls, line in current["dialogues"]:
    dialogue_blocks += f"""
<div class="dialogue-card">
  <div class="{css_cls}">{speaker}</div>
  <div style="margin-top:6px; color:#f1f5f9; font-size:0.96rem;">"{line}"</div>
</div>
"""

dialogue_section = f'<div class="dialogue-row">{dialogue_blocks}</div>' if dialogue_blocks else ""

st.markdown(
    f"""
<div class="cinema-frame">
  <div class="cinema-badge">{current['badge']}</div>
  <div class="scene-heading">{current['title']}</div>
  {visual_html}
  <div class="narration-box">{current['narration']}</div>
  {dialogue_section}
</div>
""",
    unsafe_allow_html=True,
)

# --- AUTO-PLAY LOOP ---
if st.session_state.playing:
    if st.session_state.scene_idx < len(SCENES) - 1:
        time.sleep(delay_sec)
        st.session_state.scene_idx += 1
        st.rerun()
    else:
        st.session_state.playing = False
