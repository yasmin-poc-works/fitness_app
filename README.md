# fitness_app

Personalized workout plan generator built with Streamlit and Groq.

## Features

- Collects height, weight, fitness goal, experience level, training days, equipment access, goal weight, and limitations
- Sends the inputs to Groq to generate a realistic weekly workout plan
- Handles missing API keys, invalid input ranges, and empty responses with user-friendly messages
- Lets you download the generated plan as a Word document

## Setup

### Option 1: Install with pip

1. Create and activate a virtual environment.

2. Install the dependencies:

```powershell
pip install -r requirements.txt
```

3. Add your Groq API key to a `.env` file:

```powershell
GROQ_API_KEY=your_key_here
```

4. Run the app:

```powershell
streamlit run app.py
```

### Option 2: Install with UV

```powershell
uv venv .venv
uv sync
uv run streamlit run app.py
```

## Environment Variables

- `GROQ_API_KEY` is required
- `GROQ_MODEL` is optional and defaults to `openai/gpt-oss-120b`

## Project Structure

- `app.py` - Streamlit UI and app flow
- `src/workout_planner.py` - Groq prompt building, validation, and plan generation
- `src/utils.py` - Word document export helper
