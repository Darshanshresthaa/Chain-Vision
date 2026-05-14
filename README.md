----
# 🎬 Chain-Vision
-----

> **AI-powered video & audio intelligence platform** — transcribe, summarize, analyze, and chat with any video or audio content.

---

## What is Chain-Vision?

Chain-Vision is a **Streamlit-based AI application** that takes any YouTube video or local audio/video file and runs it through a full intelligence pipeline:

1. **Downloads & processes** the audio
2. **Transcribes** it using Faster Whisper (speech-to-text)
3. **Summarizes** the content with a generated title
4. **Extracts** action items, decisions, deadlines, risks, and questions
5. **Embeds** the transcript into a **ChromaDB vector store**
6. **Enables Q&A** over the content via a RAG (Retrieval-Augmented Generation) chat interface

---

## ✨ Features

- 🔗 **YouTube URL support** — paste a link, get full analysis + embedded video player
- 📁 **Local file support** — MP3, MP4, WAV, and more
- 🌐 **Translation mode** — transcribe non-English audio into English
- 📝 **Smart summarization** — chunked map-reduce summarization with a generated title
- 🔍 **Meeting analysis** — extracts action items, decisions, deadlines, risks, and questions
- 💬 **RAG chat** — ask anything about the content with conversation history
- 🗄️ **Persistent vector DB** — load a previously built ChromaDB store without reprocessing
- 🎨 **Dark UI** — custom-designed Streamlit interface with IBM Plex Mono + Inter fonts

---

## 🏗️ Architecture

```
chain-vision/
│
├── app/main.py                  # Streamlit UI entry point (Chain-Vision)
│
├── core/
│   ├── model.py                 # LLM loaders (Mistral via LangChain)
│   ├── transcipt.py             # Faster Whisper transcription engine
│   ├── Summary.py               # Chunked map-reduce summarization chain
│   ├── extractor.py             # Meeting analysis (action items, decisions, etc.)
│   ├── rag.py                   # RAG chain builder + chat history management
│   └── vectorstore.py           # ChromaDB vector store (build / load / retrieve)
│
└── utils/
    └── audio_processor.py       # YouTube download, WAV conversion, audio chunking
```

---

## 🧠 AI Pipeline

```
Input (YouTube URL / Local File)
        │
        ▼
  [ Audio Processor ]       yt-dlp download → FFmpeg WAV conversion → 10-min chunks
        │
        ▼
  [ Faster Whisper ]        Speech-to-text per chunk → full transcript string
        │
        ▼
  [ Summarizer ]            Chunk → chunk summary → combined → final summary + title
        │
        ▼
  [ Extractor ]             Transcript → action items / decisions / risks / deadlines
        │
        ▼
  [ Vector Store ]          Transcript → ChromaDB (sentence-transformers embeddings)
        │
        ▼
  [ RAG Chain ]             User question + history → retriever → Mistral → answer
```

---

## 🗄️ Vector Database

Chain-Vision uses **[ChromaDB](https://www.trychroma.com/)** as its local persistent vector store.

| Setting | Value |
|---|---|
| Storage directory | `Vector_db/` (local) |
| Collection name | `meeting_transcript` |
| Embedding model | `sentence-transformers/all-mpnet-base-v2` |
| Chunk size | 3000 tokens, 500 overlap |
| Retrieval type | Similarity search, top-4 chunks |
| Device | CUDA if available, else CPU |

The vector store is **persisted to disk** after every pipeline run. On subsequent sessions you can click **"Load Vector DB"** in the sidebar to skip reprocessing and jump straight to chat.

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| Speech-to-text | Faster Whisper (`medium` model by default) |
| LLM | Mistral AI (`mistral-small-latest`) via LangChain |
| Embeddings | HuggingFace `sentence-transformers/all-mpnet-base-v2` |
| Vector DB | ChromaDB |
| Audio processing | yt-dlp, pydub, FFmpeg |
| Orchestration | LangChain (LCEL chains, RunnableParallel, RAG) |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/chain-vision.git
cd chain-vision
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

**Key packages:**
```
streamlit
faster-whisper
langchain langchain-mistralai langchain-huggingface langchain-chroma
langchain-text-splitters
chromadb
sentence-transformers
yt-dlp
pydub
torch
python-dotenv
```

> FFmpeg must be installed and available in your system PATH for audio conversion.

### 3. Set up environment variables

Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
WHISPER_MODEL=medium        # Options: tiny, base, small, medium, large-v2
```

Get a free Mistral API key at [console.mistral.ai](https://console.mistral.ai).

### 4. Run the app

```bash
streamlit run app/main.py
```

---

## 📖 Usage

### New video / file

1. Open the app in your browser
2. In the sidebar, choose **"New Source"**
3. Paste a **YouTube URL** or enter a **local file path**
4. Click **▶ Run Pipeline**
5. Wait for the pipeline to complete (progress bar shows each step)
6. View the **Summary**, **Analysis**, and **Transcript** tabs
7. Use the **chat panel** to ask questions about the content

### Load existing vector DB

1. In the sidebar, choose **"Existing Vector DB"**
2. Click **🗄️ Load Vector DB**
3. Start chatting immediately — no reprocessing needed

---

## 🔍 Analysis Types

The extractor supports the following analysis modes (selectable programmatically via `analyze_transcript(transcript, analysis_type)`):

| Type | Description |
|---|---|
| `summary` | Full structured meeting summary with decisions, actions, risks |
| `action_items` | Tasks with assigned person, deadline, and priority |
| `decisions` | Final confirmed decisions and agreements |
| `questions` | Direct and indirect questions raised |
| `deadlines` | All mentioned deadlines linked to tasks |
| `risks` | Blockers, delays, and issues flagged |

---

## 📁 Generated Files

| Path | Contents |
|---|---|
| `Vector_db/` | Persisted ChromaDB vector store |
| `downloads/` | Temporary audio downloads (auto-deleted after pipeline) |

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

