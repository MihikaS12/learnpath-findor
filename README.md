# LearnPath (Findor) - AI Learning Assistant

An AI-powered learning assistant that creates personalized educational experiences. The system processes various types of prompts (courses, examinations, JDs, business plans, queries) and generates structured learning paths with resources and interactive elements.

## Features

- **Personalized Learning Paths**: Generate detailed course plans based on learning goals
- **Concept Explainer**: Transform complex concepts into engaging visual explanations
- **1:1 Mentorship**: Get personalized guidance and answers to specific questions
- **Test Simulator**: Create custom tests with explanations and performance reports
- **Learning Schedule**: Integrate learning plans into daily life with accountability features

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Node.js, Express
- **AI**: OpenAI API
- **Deployment**: Vercel

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/learnpath-findor.git
   cd learnpath-findor
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key
   PORT=3000
   ```

4. Start the development server:
   ```
   npm run dev
   ```

5. Open your browser and navigate to `http://localhost:3000`

## Deployment to Vercel

1. Install Vercel CLI:
   ```
   npm install -g vercel
   ```

2. Login to Vercel:
   ```
   vercel login
   ```

3. Add your OpenAI API key as a secret:
   ```
   vercel secrets add openai_api_key "your_openai_api_key"
   ```

4. Deploy to Vercel:
   ```
   vercel --prod
   ```

## API Endpoints

- **POST /api/chat**: Process general chat messages
- **POST /api/explainer**: Generate concept explainers
- **POST /api/mentor**: Get mentorship responses
- **POST /api/evaluation**: Create custom tests
- **POST /api/schedule**: Generate personalized learning schedules

## Project Structure

- `index.html`: Main HTML file
- `styles.css`: CSS styles
- `script.js`: Frontend JavaScript
- `server.js`: Node.js server
- `package.json`: Project dependencies
- `.env`: Environment variables
- `vercel.json`: Vercel deployment configuration

## Credits

Based on the LearnPath (Findor) workflow document.
