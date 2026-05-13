import streamlit as st
import os
import shutil
import re
import io
from contextlib import redirect_stdout
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Chain-Vision",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: #080810;
    color: #dddaf0;
}
.stApp { background: #080810; }

[data-testid="stSidebar"] {
    background: #0d0d1a !important;
    border-right: 1px solid #1c1c30 !important;
}
[data-testid="stSidebar"] * { color: #dddaf0 !important; }

.brand-name {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.65rem;
    font-weight: 700;
    background: linear-gradient(120deg, #c084fc 0%, #818cf8 55%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.03em;
    line-height: 1;
}
.brand-sub {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #3a3a5a;
    margin-top: 4px;
}

.pipe-step {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 6px 0 6px 12px;
    font-size: 0.78rem;
    color: #44446a;
    font-family: 'IBM Plex Mono', monospace;
    border-left: 2px solid #1c1c30;
    margin-left: 4px;
}
.pipe-step.done  { color: #a78bfa; border-left-color: #7c3aed; }
.pipe-step.running { color: #fbbf24; border-left-color: #f59e0b; }
.pipe-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #1c1c30;
    flex-shrink: 0;
}
.pipe-step.done .pipe-dot    { background: #7c3aed; }
.pipe-step.running .pipe-dot { background: #f59e0b; box-shadow: 0 0 6px #f59e0b; }

.stTextInput > div > div > input,
.stTextArea > div > textarea {
    background: #0e0e1c !important;
    border: 1px solid #252540 !important;
    border-radius: 8px !important;
    color: #dddaf0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    caret-color: #a78bfa;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > textarea:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.18) !important;
    outline: none !important;
}

.stButton > button {
    background: linear-gradient(135deg, #6d28d9 0%, #2563eb 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.04em !important;
    padding: 0.5rem 1.3rem !important;
    box-shadow: 0 2px 16px rgba(124,58,237,0.25) !important;
    transition: opacity 0.2s, transform 0.15s !important;
}
.stButton > button:hover   { opacity: 0.85 !important; transform: translateY(-1px) !important; }
.stButton > button:active  { transform: translateY(0) !important; }

.stSelectbox > div > div {
    background: #0e0e1c !important;
    border-color: #252540 !important;
    color: #dddaf0 !important;
    border-radius: 8px !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 1px solid #1c1c30;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #44446a;
    padding: 0.65rem 1.1rem;
    background: transparent;
    border-bottom: 2px solid transparent;
}
.stTabs [aria-selected="true"] {
    color: #a78bfa !important;
    border-bottom-color: #7c3aed !important;
    background: transparent !important;
}

.cv-card {
    background: #0e0e1c;
    border: 1px solid #1c1c30;
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 0.9rem;
}
.cv-card-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #44446a;
    margin-bottom: 0.6rem;
}
.cv-card-body {
    font-size: 0.88rem;
    line-height: 1.75;
    color: #b8b5cc;
}

.cv-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.15rem;
    font-weight: 700;
    color: #c084fc;
    line-height: 1.3;
}
.cv-title-bar {
    background: #0e0e1c;
    border: 1px solid #1c1c30;
    border-radius: 10px;
    padding: 0.9rem 1.25rem;
    margin-bottom: 1.1rem;
    display: flex;
    align-items: center;
    gap: 10px;
}

.cv-bullet {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 0.45rem 0;
    border-bottom: 1px solid #131320;
    font-size: 0.87rem;
    color: #b8b5cc;
    line-height: 1.65;
}
.cv-dot {
    width: 5px; height: 5px;
    border-radius: 50%;
    background: #7c3aed;
    margin-top: 7px;
    flex-shrink: 0;
}

.chat-wrap {
    background: #0a0a14;
    border: 1px solid #1c1c30;
    border-radius: 12px;
    padding: 1rem;
    max-height: 52vh;
    overflow-y: auto;
    margin-bottom: 0.9rem;
}
.msg-row { margin-bottom: 0.75rem; }
.msg-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #3a3a5a;
    margin-bottom: 3px;
}
.msg-label.right { text-align: right; }
.msg-bubble-user {
    background: #1a1530;
    border: 1px solid #2a2050;
    border-radius: 10px 10px 3px 10px;
    padding: 0.65rem 0.9rem;
    font-size: 0.87rem;
    color: #c8c5e0;
    text-align: right;
    margin-left: 20%;
}
.msg-bubble-ai {
    background: #0e0e1c;
    border: 1px solid #1e1e34;
    border-radius: 10px 10px 10px 3px;
    padding: 0.65rem 0.9rem;
    font-size: 0.87rem;
    color: #dddaf0;
    line-height: 1.7;
    margin-right: 20%;
    white-space: pre-wrap;
}

.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #0a1a10;
    border: 1px solid #1a4a20;
    border-radius: 999px;
    padding: 4px 14px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: #4ade80;
    margin-bottom: 1.25rem;
}

.yt-wrap {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #1c1c30;
    box-shadow: 0 4px 40px rgba(124,58,237,0.15);
    background: #000;
    margin-bottom: 1rem;
}

.section-heading {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #44446a;
    margin-bottom: 0.75rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #131320;
}

.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #7c3aed, #2563eb) !important;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #252540; border-radius: 2px; }

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
_defaults = {
    "result": None,
    "rag_chain": None,
    "chat_history": [],
    "source_url": "",
    "pipeline_step": 0,
}
for _k, _v in _defaults.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def extract_yt_id(url: str) -> str:
    for pat in [
        r"youtu\.be/([A-Za-z0-9_-]{11})",
        r"youtube\.com/watch\?.*v=([A-Za-z0-9_-]{11})",
        r"youtube\.com/shorts/([A-Za-z0-9_-]{11})",
        r"youtube\.com/embed/([A-Za-z0-9_-]{11})",
    ]:
        m = re.search(pat, url)
        if m:
            return m.group(1)
    return ""

def is_youtube_url(url: str) -> bool:
    return any(x in url for x in ["youtube.com/watch", "youtu.be/", "youtube.com/shorts"])

def render_chat(key_suffix: str = ""):
    """Reusable Q&A chat panel — mirrors main.py while loop."""
    if st.session_state.rag_chain is None:
        st.warning("No RAG chain available. Process a video or load a vector DB first.")
        return

    from core.rag import user_query

    # Message history display
    chat_html = '<div class="chat-wrap">'
    if not st.session_state.chat_history:
        chat_html += (
            '<div style="text-align:center;padding:2.5rem 0;color:#2e2e50;'
            'font-family:IBM Plex Mono,monospace;font-size:0.72rem;">'
            "Ask anything about the video…"
            "</div>"
        )
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            chat_html += (
                '<div class="msg-row">'
                '<div class="msg-label right">You</div>'
                f'<div class="msg-bubble-user">{msg["content"]}</div>'
                "</div>"
            )
        else:
            chat_html += (
                '<div class="msg-row">'
                '<div class="msg-label">Chain-Vision</div>'
                f'<div class="msg-bubble-ai">{msg["content"]}</div>'
                "</div>"
            )
    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)

    # Input
    c1, c2 = st.columns([5, 1])
    with c1:
        question = st.text_input(
            "",
            placeholder="Ask a question (type 'exit' to reset)…",
            key=f"q_{key_suffix}",
            label_visibility="collapsed",
        )
    with c2:
        ask = st.button("Send", key=f"send_{key_suffix}", use_container_width=True)

    if ask and question.strip():
        # Mirror main.py: user_query(rag_chain=rag_chain, question=question)
        if question.lower() == "exit":
            for k in _defaults:
                st.session_state[k] = _defaults[k]
            st.rerun()

        with st.spinner("Thinking…"):
            buf = io.StringIO()
            with redirect_stdout(buf):
                user_query(rag_chain=st.session_state.rag_chain, question=question)
            answer = buf.getvalue().strip() or "_(No response returned)_"

        st.session_state.chat_history.append({"role": "user", "content": question})
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

    if st.session_state.chat_history:
        if st.button("🗑  Clear chat", key=f"clr_{key_suffix}"):
            st.session_state.chat_history = []
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="brand-name">Chain-Vision</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">AI Video Intelligence</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    mode = st.radio(
        "Mode",
        ["🎬  Process New Video", "🗄️  Load Existing Vector DB"],
    )

    st.markdown("---")

    STEPS = [
        "Audio Processing",
        "Transcription",
        "Summary Generation",
        "Transcript Analysis",
        "Vector Store Build",
    ]
    st.markdown('<div class="brand-sub" style="margin-bottom:10px;">Pipeline</div>', unsafe_allow_html=True)
    s = st.session_state.pipeline_step
    for i, label in enumerate(STEPS, start=1):
        cls = "done" if (s == 6 or i < s) else ("running" if i == s else "")
        st.markdown(
            f'<div class="pipe-step {cls}"><div class="pipe-dot"></div>{label}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    if st.session_state.result is not None:
        if st.button("🔄  Reset Session", use_container_width=True):
            for k in _defaults:
                st.session_state[k] = _defaults[k]
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# INPUT SCREEN
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.result is None:
    _, col, _ = st.columns([0.6, 2.8, 0.6])
    with col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(
            '<div style="text-align:center;margin-bottom:2.5rem;">'
            '<div class="brand-name" style="font-size:2.8rem;">Chain-Vision</div>'
            '<div class="brand-sub" style="font-size:0.72rem;margin-top:8px;">'
            "Transcribe &nbsp;&middot;&nbsp; Summarise &nbsp;&middot;&nbsp; Analyse &nbsp;&middot;&nbsp; Query"
            "</div></div>",
            unsafe_allow_html=True,
        )

        # ── Process new video ──────────────────────────────────────────────
        if "Process" in mode:
            st.markdown('<div class="cv-card">', unsafe_allow_html=True)
            st.markdown('<div class="cv-card-label">Video Source</div>', unsafe_allow_html=True)
            source = st.text_input(
                "source",
                placeholder="YouTube URL  or  /path/to/local/video.mp4",
                label_visibility="collapsed",
            )
            st.markdown("</div>", unsafe_allow_html=True)

            if st.button("▶  Run Pipeline", use_container_width=True):
                if not source.strip():
                    st.error("Please enter a YouTube URL or local file path.")
                else:
                    try:
                        from utils.audip_processor import process_data
                        from core.Summary import summarize_data
                        from core.transcipt import transcribe_all_chunk
                        from core.extractor import analyze_transcript
                        from core.rag import build_rag_chain

                        prog = st.progress(0, text="Starting pipeline…")

                        # Step 1
                        st.session_state.pipeline_step = 1
                        prog.progress(5, text="Processing audio…")
                        chunks = process_data(source=source)

                        # Step 2
                        st.session_state.pipeline_step = 2
                        prog.progress(22, text="Transcribing audio chunks…")
                        transcript = transcribe_all_chunk(chunks=chunks)

                        # Step 3
                        st.session_state.pipeline_step = 3
                        prog.progress(45, text="Generating summary…")
                        summary_result = summarize_data(transcript=transcript)
                        title = summary_result["title"]
                        summary_points = summary_result["summary"]

                        # Step 4  — analysis_type hardcoded as 'summary' (matches main.py)
                        st.session_state.pipeline_step = 4
                        prog.progress(65, text="Analysing transcript…")
                        decision = analyze_transcript(
                            transcript=transcript,
                            analysis_type="summary",
                        )

                        # Step 5
                        st.session_state.pipeline_step = 5
                        prog.progress(82, text="Building vector store…")
                        rag_chain = build_rag_chain(transcipt=transcript)

                        # Cleanup — mirrors main.py shutil block
                        prog.progress(95, text="Cleaning temporary files…")
                        try:
                            if chunks:
                                for f in chunks:
                                    if os.path.exists(f):
                                        os.remove(f)
                            if os.path.exists("downloads"):
                                shutil.rmtree("downloads")
                        except Exception:
                            pass

                        prog.progress(100, text="Done!")
                        st.session_state.pipeline_step = 6
                        st.session_state.result = {
                            "title": title,
                            "transcript": transcript,
                            "summary": summary_points,
                            "actions and decision": decision,
                        }
                        st.session_state.rag_chain = rag_chain
                        st.session_state.source_url = source.strip()
                        st.rerun()

                    except Exception as e:
                        st.error(f"Pipeline error: {e}")
                        st.session_state.pipeline_step = 0

        # ── Load existing vector DB ────────────────────────────────────────
        else:
            st.markdown('<div class="cv-card">', unsafe_allow_html=True)
            st.markdown('<div class="cv-card-label">Load Vector Database</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="cv-card-body">Resume from a previously built vector store '
                "without reprocessing the video.</div>",
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

            if st.button("🗄️  Load Vector DB", use_container_width=True):
                try:
                    from core.rag import load_rag_chain
                    with st.spinner("Loading vector database…"):
                        rag_chain = load_rag_chain()
                    st.session_state.rag_chain = rag_chain
                    st.session_state.source_url = ""
                    st.session_state.pipeline_step = 6
                    st.session_state.result = {
                        "title": "Loaded from existing vector DB",
                        "transcript": "",
                        "summary": [],
                        "actions and decision": "",
                    }
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to load vector DB: {e}")

# ─────────────────────────────────────────────────────────────────────────────
# RESULTS SCREEN
# ─────────────────────────────────────────────────────────────────────────────
else:
    result     = st.session_state.result
    source_url = st.session_state.source_url
    _is_yt     = is_youtube_url(source_url)
    _db_only   = not result.get("transcript", "").strip()

    icon = "🗄️" if _db_only else "📽"
    st.markdown(
        f'<div class="cv-title-bar"><span style="font-size:1.4rem;">{icon}</span>'
        f'<div class="cv-title">{result["title"]}</div></div>',
        unsafe_allow_html=True,
    )

    # ══════════════════════════════════════════════════════════════════════
    # LAYOUT A — YouTube URL → video (left) + chat (right)
    # ══════════════════════════════════════════════════════════════════════
    if _is_yt and not _db_only:
        yt_id = extract_yt_id(source_url)
        col_l, col_r = st.columns([1, 1], gap="large")

        with col_l:
            if yt_id:
                st.markdown(
                    f'<div class="yt-wrap"><iframe '
                    f'src="https://www.youtube.com/embed/{yt_id}?rel=0&modestbranding=1" '
                    f'width="100%" height="315" frameborder="0" '
                    f'allow="accelerometer;autoplay;clipboard-write;encrypted-media;'
                    f'gyroscope;picture-in-picture" allowfullscreen '
                    f'style="display:block;"></iframe></div>',
                    unsafe_allow_html=True,
                )
            else:
                st.warning("Could not extract a video ID from the URL.")

            t_s, t_a, t_t = st.tabs(["  Summary  ", "  Analysis  ", "  Transcript  "])

            with t_s:
                items = result.get("summary", [])
                if isinstance(items, str):
                    items = [items]
                for pt in items:
                    st.markdown(
                        f'<div class="cv-bullet"><div class="cv-dot"></div><div>{pt}</div></div>',
                        unsafe_allow_html=True,
                    )

            with t_a:
                st.markdown(
                    f'<div class="cv-card"><div class="cv-card-label">Actions & Decisions</div>'
                    f'<div class="cv-card-body">{result.get("actions and decision","—")}</div></div>',
                    unsafe_allow_html=True,
                )

            with t_t:
                tx = result.get("transcript", "")
                if tx:
                    st.text_area("", value=tx, height=280, label_visibility="collapsed")
                else:
                    st.info("Transcript not available.")

        with col_r:
            st.markdown('<div class="section-heading">Ask the Video</div>', unsafe_allow_html=True)
            render_chat(key_suffix="yt")

    # ══════════════════════════════════════════════════════════════════════
    # LAYOUT B — Load existing DB → full-width Q&A immediately
    # ══════════════════════════════════════════════════════════════════════
    elif _db_only:
        st.markdown(
            '<div class="status-badge">'
            '<span style="width:6px;height:6px;border-radius:50%;background:#4ade80;'
            'display:inline-block;flex-shrink:0;"></span>'
            "Vector database loaded — ready to answer questions"
            "</div>",
            unsafe_allow_html=True,
        )
        render_chat(key_suffix="db")

    # ══════════════════════════════════════════════════════════════════════
    # LAYOUT C — Local file → tabbed (Summary / Analysis / Transcript / Q&A)
    # ══════════════════════════════════════════════════════════════════════
    else:
        t_s, t_a, t_t, t_q = st.tabs(
            ["  Summary  ", "  Analysis  ", "  Transcript  ", "  Q & A  "]
        )

        with t_s:
            st.markdown("<br>", unsafe_allow_html=True)
            items = result.get("summary", [])
            if isinstance(items, str):
                items = [items]
            for pt in items:
                st.markdown(
                    f'<div class="cv-bullet"><div class="cv-dot"></div><div>{pt}</div></div>',
                    unsafe_allow_html=True,
                )

        with t_a:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                f'<div class="cv-card"><div class="cv-card-label">Actions & Decisions</div>'
                f'<div class="cv-card-body">{result.get("actions and decision","—")}</div></div>',
                unsafe_allow_html=True,
            )

        with t_t:
            st.markdown("<br>", unsafe_allow_html=True)
            tx = result.get("transcript", "")
            if tx:
                st.text_area("", value=tx, height=440, label_visibility="collapsed")
            else:
                st.info("No transcript available.")

        with t_q:
            st.markdown("<br>", unsafe_allow_html=True)
            render_chat(key_suffix="local")