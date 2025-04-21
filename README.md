# AI-Based Geography Quiz Bot

An interactive geography quiz application that tests users' knowledge of world geography using AI-generated questions and interactive maps.

## Features

- Interactive geography quizzes using Google Gemini AI
- Real-world location data integration with Foursquare Places API
- Interactive map interface using Leaflet.js
- User authentication and progress tracking
- Dark theme UI with responsive design

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Node.js (for development)
- Google Gemini API key
- Foursquare Places API key

### Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-geography-quiz
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your API keys:
```
GEMINI_API_KEY=your_gemini_api_key
FOURSQUARE_API_KEY=your_foursquare_api_key
JWT_SECRET_KEY=your_jwt_secret_key
```

4. Run the development server:
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

### Deployment to Vercel

1. Push your code to GitHub
2. Connect your GitHub repository to Vercel
3. Configure environment variables in Vercel dashboard
4. Deploy!

## Project Structure

```
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
├── app.py
├── requirements.txt
├── vercel.json
└── README.md
```

## API Documentation

### Authentication
- POST /api/auth/register - Register new user
- POST /api/auth/login - User login
- GET /api/auth/me - Get current user info

### Quiz Endpoints
- GET /api/quiz/generate - Generate new quiz
- POST /api/quiz/submit - Submit quiz answers
- GET /api/quiz/progress - Get user progress

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License 