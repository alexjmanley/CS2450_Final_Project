# DESIGN.md

## System Architecture

The Calendar Assistant uses a **layered architecture** with three main layers:

1. **Presentation Layer** - CLI (main.py) and GUI (gui.py) interfaces
2. **Application Layer** - ChatBot and Calendar business logic
3. **Data Layer** - Database abstraction and SQLite storage

Each layer depends only on the layer below it, ensuring clean separation of concerns and testability.

## Major Classes

### Calendar (calendar.py)
Core business logic for event management. Handles CRUD operations (add, list, remove events) and date validation. Uses ISO 8601 format (YYYY-MM-DD HH:MM) for consistency.

### ChatBot (chatbot.py)
Manages user interaction through natural language and structured commands. Uses regex for parsing structured commands (add/list/remove) and integrates with Ollama LLM for conversational responses. Hybrid approach ensures reliability for critical operations while providing natural UX.

### GUI (gui.py)
Provides visual interface with side-by-side chat and calendar layout. Implements three calendar views:
- **Day View**: Hourly schedule (6 AM - 11 PM)
- **Month View**: Traditional calendar grid
- **Year View**: 12-month overview

Uses tkinter for zero external dependencies. Calendar panel can be toggled visible/hidden.

### Database (db.py)
Abstracts SQLite operations using repository pattern. Auto-creates schema on first run. All SQL is hidden from Calendar class, making it easy to swap databases later.

## Design Patterns

- **Layered Architecture**: Clear separation between UI, logic, and data
- **Repository Pattern**: Database class abstracts all SQL operations
- **Singleton Pattern**: CalendarView prevents duplicate calendar windows
- **Facade Pattern**: ChatBot provides simple API hiding complex parsing logic

## Key Design Decisions

### 1. Hybrid Chatbot (Regex + LLM)
Structured commands for critical operations (deterministic, testable) with LLM fallback for conversational queries. Best of both worlds: reliability and natural interaction.

### 2. Local LLM (Ollama)
Using Ollama instead of cloud API for privacy, zero cost, and offline capability. Trade-off: requires installation and local resources.

### 3. Side-by-Side Layout
Calendar embedded next to chat (vs popup) for better workflow and reduced context switching. Modern productivity app pattern.

### 4. SQLite Storage
Persistent file-based storage for simplicity and zero configuration. Events survive app restarts without external database server.

## Reflections

**What went well**: Modular design allowed parallel development (one member on UI, one on LLM). Layered architecture made it easy to add features without rewriting existing code.

**What could improve**: Earlier integration testing, more comprehensive test coverage, externalize configuration (colors, DB path), add graceful fallback if Ollama unavailable.

**Key takeaway**: Good architecture pays off. Clean separation of concerns made it easy to add the LLM and GUI features without modifying core calendar logic.

## Future Improvements

- Async LLM calls (threading) to prevent UI blocking
- Recurring events (daily/weekly/monthly)
- Event editing and categories
- iCal export/import
- Desktop notifications before events
