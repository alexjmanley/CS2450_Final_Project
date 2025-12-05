# CS2450_Final_Project

A small Python calendar application with a built-in rule-based chatbot interface.

## Team Members
- **Alex Manley** (alexjmanley)
- **Jonah Hoff** (JonahHoff78)

## Features
- SQLite-backed calendar storage
- Simple rule-based chatbot for adding/listing/removing events
- CLI interactive chat loop
- Tkinter-based GUI

## Quick start

1. Install Python dependencies:

```powershell
pip install -r requirements.txt
```

Or with a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Download Ollama with llama3.2:1b 

linux / macOS install
```powershell
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:1b
```

Windows install
Download the Windows installer from the official website:
https://ollama.com/download
then run 
```powershell
ollama pull llama3.2:1b
```

3. Run the GUI application:

```powershell
python main_gui.py
```

Or run the chat CLI:

```powershell
python main.py
```

Example commands to type to the chatbot:
- add Meeting with Bob on 2025-11-20 at 14:00
- list
- list on 2025-11-20
- remove 1
- help

## Project structure
- `calendar_app/` — package with DB, calendar logic and chatbot
- `main.py` — interactive chat CLI
- `main_gui.py` — Tkinter GUI interface
- `tests/` — unit tests
