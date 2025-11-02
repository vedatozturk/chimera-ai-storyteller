Chimera - AI Storyteller

A web-based, interactive text-adventure game powered by Google Gemini and a FastAPI backend. This project utilizes a "Model Context Protocol" (MCP) concept to generate dynamic, adaptive narratives based on player choice and a persistent game state.

Core Features

Dynamic Story Generation: The narrative is generated in real-time by the Google Gemini AI, ensuring no two playthroughs are the same.

Persistent Memory: The AI tracks the player's state, NPC moods, and world events, leading to a coherent and adaptive experience.

Web-Based Interface: A clean, modern chat interface built with plain HTML, CSS, and JavaScript.

Async Backend: Powered by a high-performance FastAPI server to handle all game logic and AI communication.

Tech Stack

Backend: Python 3, FastAPI, Uvicorn

AI: Google Gemini API (google-generativeai)

Data Validation: Pydantic

Frontend: HTML, CSS, JavaScript (Fetch API)

Utilities: python-dotenv, fastapi-cors

How to Run Locally

Follow these steps to run the project on your local machine.

1. Clone the Repository

git clone [https://github.com/vedatozturk/chimera-ai-storyteller.git](https://github.com/vedatozturk/chimera-ai-storyteller.git)
cd chimera-ai-storyteller



2. Set Up a Virtual Environment

python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Mac/Linux



3. Install Dependencies

pip install fastapi "uvicorn[standard]" pydantic google-generativeai python-dotenv fastapi-cors



(Note: A requirements.txt file can be generated with pip freeze > requirements.txt)

4. Set Up Your API Key
Create a .env file in the root directory and add your Google AI Studio API key:

API_KEY="YOUR_GOOGLE_API_KEY_HERE"



5. Run the Backend Server
Start the FastAPI server in your terminal:

uvicorn main:app --reload



6. Play the Game
Open the index.html file in your web browser to start playing.
