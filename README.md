# German ChatBot with Flask, SocketIO, and LangGraph

## Overview
This project is a real-time chatbot application that leverages Flask, SocketIO, and LangGraph with the Llama3 model from Groq. The chatbot processes user messages and responds in German while maintaining conversation state.

## Features
- Real-time chat communication using Flask-SocketIO.
- AI-powered chatbot using LangChain and LangGraph.
- Messages formatted in German with bullet points for clarity.
- Persistent session management for user conversations.

## Technologies Used
- **Python**: Backend development.
- **Flask**: Web framework for handling HTTP requests.
- **Flask-SocketIO**: Enables real-time, bidirectional communication.
- **LangChain & LangGraph**: AI workflow processing.
- **Groq (Llama3-8B-8192)**: AI model provider.

## Installation and Setup
### Prerequisites
Ensure you have Python installed (recommended version: 3.8+). Install the required dependencies using:
```bash
pip install flask flask-socketio langchain-core langgraph typing-extensions
```

### Set Environment Variables
Set up the Groq API key before running the application:
```bash
export GROQ_API_KEY='your_groq_api_key'
```
(Replace `your_groq_api_key` with your actual API key.)

### Running the Application
1. Clone the repository:
```bash
git clone <repository_url>
cd <project_directory>
```
2. Start the Flask server:
```bash
python app.py
```
3. Open your browser and go to:
```
http://127.0.0.1:5000/
```

## Project Structure
```
|-- app.py               # Main Flask application with SocketIO
|-- templates/
    |-- index.html       # Frontend for the chatbot
```

## How It Works
1. **User sends a message** via the web interface.
2. **Flask-SocketIO handles the message** and assigns a session ID.
3. **LangGraph processes the message** using Llama3 to generate a response in German.
4. **Response is formatted and sent back** to the frontend in real-time.

## Future Enhancements
- Add a ReactJS frontend for an improved user experience.
- Store chat history using MongoDB.
- Enhance response formatting for better readability.
