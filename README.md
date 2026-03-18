<div align="center">

# 🎙️ Pocket TTS Demo

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Gradio](https://img.shields.io/badge/Gradio-6.9.0-orange?logo=gradio&logoColor=white)](https://gradio.app/)
[![Pocket TTS](https://img.shields.io/badge/Pocket_TTS-1.1.1-purple)](https://pypi.org/project/pocket-tts/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.10.0-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Hugging Face Spaces](https://img.shields.io/badge/HuggingFace-Spaces-yellow?logo=huggingface&logoColor=white)](https://huggingface.co/spaces)

**A local text-to-speech demo powered by Kyutai's Pocket TTS — supports 8 pre-built voices and custom voice cloning, no GPU or API key required.**

[Report Bug](../../issues) · [Request Feature](../../issues)

</div>

---

## Screenshot

<!-- Add a screenshot of your app here -->
<!-- ![Screenshot](screenshot.png) -->

---

## About

**Pocket TTS Demo** is a lightweight, CPU-friendly text-to-speech application built with [Pocket TTS](https://pypi.org/project/pocket-tts/) (Kyutai's 100M-parameter TTS model) and a [Gradio](https://gradio.app/) web interface. It runs entirely locally — no API keys, no GPU, no cloud fees.

### ✨ Key Features

- 🗣️ **8 Pre-built Voices** — Choose from alba, marius, javert, jean, fantine, cosette, eponine, and azelma
- 🎤 **Voice Cloning** — Upload any audio file to clone a custom voice on-the-fly
- ⚡ **Voice State Caching** — All voices pre-loaded at startup for near-instant switching
- 💾 **WAV Output** — Generated speech saved as a `.wav` file and played directly in the browser
- 🖥️ **CPU-Only** — Runs on any machine without a GPU
- 🌐 **Gradio Interface** — Clean two-column UI, deployable to Hugging Face Spaces in minutes

---

## Tech Stack

| Category | Technology |
|---|---|
| **Frontend / UI** | [Gradio](https://gradio.app/) 6.9.0 |
| **TTS Model** | [Pocket TTS](https://pypi.org/project/pocket-tts/) 1.1.1 (Kyutai) |
| **Deep Learning** | [PyTorch](https://pytorch.org/) 2.10.0 |
| **Audio Processing** | [SciPy](https://scipy.org/) 1.17.1 |
| **Numerical Computing** | [NumPy](https://numpy.org/) 2.4.2 |
| **Deployment** | [Hugging Face Spaces](https://huggingface.co/spaces) |
| **Package Manager** | [uv](https://github.com/astral-sh/uv) |

---

## Architecture

```
┌─────────────────────────────────────────┐
│              Gradio Web UI              │
│   ┌──────────────────┐  ┌────────────┐  │
│   │   Input Panel    │  │  Output    │  │
│   │  - Text Input    │  │  Panel     │  │
│   │  - Voice Select  │  │  - Audio   │  │
│   │  - Audio Upload  │  │  Player    │  │
│   │  - Generate Btn  │  │            │  │
│   └────────┬─────────┘  └────────────┘  │
└────────────│────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│           generate_speech()             │
│  - Select voice state (pre-built /      │
│    cloned from upload)                  │
│  - Call tts_model.generate_audio()      │
│  - Write .wav via scipy.io.wavfile      │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│         Pocket TTS Model                │
│  TTSModel.load_model()                  │
│  get_state_for_audio_prompt()           │
│  generate_audio()   [CPU inference]     │
└─────────────────────────────────────────┘
```

---

## Project Structure

```
gradio-bonus/
├── pocket_tts_demo.py      # Main application (Gradio + Pocket TTS)
├── main.py                 # Entry point
├── pyproject.toml          # Project metadata and dependencies (uv)
├── requirements.txt        # Pip-compatible requirements
├── uv.lock                 # Locked dependency versions
├── POCKET-TTS-GUIDE.md     # Vibe coding guide for this project
├── prompt.md               # Original AI prompt used to generate the app
├── .python-version         # Python version pin (3.12+)
└── .agent/
    └── skills/
        └── readme/         # README generation skill
```

---

## Getting Started

### Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd gradio-bonus

# Install dependencies with uv
uv sync

# Or with pip
pip install -r requirements.txt
```

### Run the App

```bash
# With uv
uv run pocket_tts_demo.py

# Or with Python directly (after activating the venv)
.venv\Scripts\activate   # Windows
python pocket_tts_demo.py
```

Then open [http://127.0.0.1:7860](http://127.0.0.1:7860) in your browser.

> **Note:** The model (~100MB) is downloaded automatically on first run. All 8 voice states are cached at startup.

---

## Usage

1. **Enter text** in the text box (defaults to a sample sentence)
2. **Select a pre-built voice** from the dropdown (alba, marius, javert, jean, fantine, cosette, eponine, azelma)
3. *(Optional)* **Upload a custom audio file** to clone a voice instead
4. Click **Generate Speech** — the audio plays in the output panel on the right

---

## Deployment

### Hugging Face Spaces

```python
from huggingface_hub import HfApi
import io

api = HfApi(token="hf_YOUR_TOKEN_HERE")

# Create the Space
api.create_repo(
    repo_id="YOUR_USERNAME/pocket-tts-demo",
    repo_type="space",
    space_sdk="gradio",
    exist_ok=True,
)

# Upload app file
api.upload_file(
    path_or_fileobj="pocket_tts_demo.py",
    path_in_repo="app.py",
    repo_id="YOUR_USERNAME/pocket-tts-demo",
    repo_type="space",
)

# Upload requirements.txt
requirements = b"pocket-tts\nscipy\ngradio\nnumpy\n"
api.upload_file(
    path_or_fileobj=io.BytesIO(requirements),
    path_in_repo="requirements.txt",
    repo_id="YOUR_USERNAME/pocket-tts-demo",
    repo_type="space",
)

print("Deployed! Visit: https://huggingface.co/spaces/YOUR_USERNAME/pocket-tts-demo")
```

> Hugging Face will install dependencies, download the model, and serve the app within 3–5 minutes.

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'feat: add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

Ideas for extensions:
- Real-time audio streaming
- Speech rate / pitch control
- Batch text-to-speech generation
- Waveform visualization
- Multi-language warning for non-English input

---

## Developed By

<div align="center">

**Tertiary Infotech Academy Pte. Ltd.**

*Empowering the next generation of AI developers through vibe coding.*

</div>

---

## Acknowledgements

- [Kyutai](https://kyutai.org/) for the open-source [Pocket TTS](https://github.com/kyutai-labs/pocket-tts) model
- [Gradio](https://gradio.app/) for making AI demos simple to build and deploy
- [Hugging Face](https://huggingface.co/) for free model and app hosting

---

<div align="center">

⭐ **Star this repo if you found it useful!** ⭐

</div>
