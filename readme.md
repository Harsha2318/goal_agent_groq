Goal Agent - AI-Powered Goal Setting & Tracking System
Transform your aspirations into achievements with intelligent goal management powered by Groq LLM and MongoDB

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/release/python-380/)

Goal Agent is an intelligent AI assistant that helps you set, track, and achieve your personal and professional goals using the proven SMART methodology. Built with cutting-edge technology including Groq's lightning-fast LLM inference and MongoDB's robust data storage, this system provides personalized coaching, milestone tracking, and progress analytics.

🎯 What Makes It Special
SMART Goal Framework: Automatically structures goals to be Specific, Measurable, Achievable, Relevant, and Time-bound
AI-Powered Coaching: Behavioral psychology insights and personalized motivation strategies
Real-time Progress Tracking: Comprehensive milestone management and achievement logging
Advanced Analytics: Goal performance insights and completion rate analysis
Natural Language Interface: Conversational goal setting and progress updates
Persistent Memory: MongoDB storage ensures your goals and progress are never lost
🚀 Key Features
🧠 Intelligent Goal Management
Dynamic Goal Creation: Convert vague aspirations into concrete action plans
Milestone Breakdown: Automatically decompose large goals into manageable steps
Progress Logging: Track achievements, obstacles, and reflections
Smart Reminders: AI-driven check-ins and motivation
📊 Comprehensive Analytics
Goal Statistics: Completion rates, category breakdowns, and priority analysis
Progress Visualization: Track momentum and identify patterns
Performance Insights: Understand what works best for your goal achievement
🤖 Advanced AI Capabilities
Natural Language Processing: Chat naturally about your goals and progress
Behavioral Psychology Integration: Evidence-based motivation strategies
Adaptive Coaching: Personalized advice based on your unique patterns
Tool-Calling Architecture: Seamless database operations through conversation
⚡ High Performance
Groq LLM: Lightning-fast response times (up to 500 tokens/second)
MongoDB Storage: Scalable, flexible document database
Real-time Analytics: Instant insights and progress updates
Robust Error Handling: Graceful failure recovery and user feedback
🛠️ Technology Stack
ComponentTechnologyPurposeAI EngineGroq LLM (Llama 3.3 70B)Natural language understanding and generationDatabaseMongoDBGoal, milestone, and progress storageBackendPython 3.8+Core application logic and APIAI FrameworkCustom goal-setting methodologySMART goal structuring and coachingEnvironmentpython-dotenvSecure configuration management


📋 Prerequisites
Before installation, ensure you have:

Python 3.8 or higher installed
MongoDB running (local installation or MongoDB Atlas)
Groq API key (get one from Groq Console)
Git for cloning the repository
⚙️ Installation
1. Clone the Repository

bash
git clone https://github.com/yourusername/goal-agent-groq.gitcd goal-agent-groq
2. Set Up Virtual Environment

bash
# Create virtual environment
python -m venv goal_env
# Activate virtual environment
# On Windows:
goal_env\Scripts\activate
# On macOS/Linux:
source goal_env/bin/activate
3. Install Dependencies

bash
pip install -r requirements.txt
4. Environment Configuration
Create a .env file in the project root:


text
### Groq API Configuration
```bash
GROQ_API_KEY=your_groq_api_key_here
```
### MongoDB Configuration
```bash
MONGO_URI=mongodb://localhost:27017/
```

### For MongoDB Atlas:
```bash
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/DB_NAME=goal_agent
```
5. Database Setup

Option A: Local MongoDB


```bash
# Install MongoDB Community Edition
Visit: https://www.mongodb.com/try/download/community
# Start MongoDB service
mongod
```
Option B: MongoDB Atlas (Cloud)

1. Create account at MongoDB Atlas
2. Create a new cluster
3. Get connection string and update 
```
MONGO_URI in .env
```
Option C: Docker

```bash
docker run --name mongodb -p 27017:27017 -d mongo:latest
```

🚀 Quick Start
1. Test Your Setup

```bash
# Test Groq API connection
python test_simple_groq.py
# Test MongoDB connection
python -c "from mongodb_database import GoalMongoDB; db = GoalMongoDB(); print('✅ MongoDB connected!')"
2. Launch Goal Agent

```bash
python main.py
```
3. Start Your First Conversation
```
text
You: I want to learn Python programming this year🎯 Goal Agent: That's a great aspiration! Let me help you create a SMART goal...[Agent will guide you through goal creation with milestones and tracking.
```
4. Example Interactions
Create Goals:


```text
"Help me set a fitness goal to run a 5K by March""I want to improve my career prospects this year""Create a goal for learning Spanish in 6 months"
Track Progress:
```
```text
"I completed my first Python course today""Log that I've been struggling with motivation lately""I achieved my weekly running milestone"
Get Insights:


text
"Show me my current goals""What's my goal completion rate?""analytics" (special command for detailed statistics)
```
```
📁 Project Structure
goal-agent-groq/
├── main.py                    # Main application entry point
├── goal_agent.py              # Core AI agent implementation
├── mongodb_database.py        # MongoDB database layer
├── tools.py                   # Goal management tools and functions
├── config.py                  # Configuration management
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create this)
├── .gitignore                 # Git ignore rules
├── test_simple_groq.py        # Connection testing
└── README.md                  # This 
```

file
🎮 Usage Examples
Setting SMART Goals

python
# The agent automatically structures goals using SMART criteria:
User: "I want to get better at programming"
Agent Response:
- Specific: Learn Python web development
- Measurable: Complete 3 projects and 1 certification
- Achievable: Based on your 1-2 hours daily availability
- Relevant: Aligns with your career advancement goals
- Time-bound: 6-month timeline with monthly milestones
Milestone Tracking

python
# Automatic milestone creation and tracking:
```
Goal: "Learn Python Programming"
├── Month 1: Complete Python basics course
├── Month 2: Build first web application
├── Month 3: Learn Django framework
├── Month 4: Create portfolio project
├── Month 5: Apply to 5 Python developer positions
└── Month 6: Land first Python role
```
Progress Analytics
```bash
# View comprehensive goal analytics
You: analytics
📊 Your Goal Analytics:
  Total Goals: 12
  Active Goals: 8
  Completed Goals: 4
  📈 Status Breakdown:
    Active: 8 goals
    Completed: 4 goals
  🏷️ Category Breakdown:
    Career: 5 goals
    Health: 3 goals
    Learning: 4 goals
```

🧠 AI Agent Capabilities


Intelligent Coaching Features
1. Discovery Phase: Deep exploration of values and motivations
2. SMART Structuring: Automatic goal optimization
3. Action Planning: Detailed roadmaps with timelines
4. Obstacle Management: Proactive problem-solving strategies
5. Behavioral Psychology: Evidence-based motivation techniques
Advanced Conversation Features
Context Awareness: Remembers your goals and progress across sessions
Natural Language: Chat naturally about your aspirations and challenges
Adaptive Responses: Personalized advice based on your patterns
Multi-turn Reasoning: Complex goal planning across multiple interactions
Database Operations
The agent seamlessly performs database operations through natural conversation:

# Creates goals with rich metadata
Tracks milestones and deadlines
Logs progress, obstacles, and achievements
Provides analytics and insights
Updates goal status and priorities

📊 MongoDB Schema

1. Goals Collection:

```javascript
{  "_id": ObjectId,  "user_id": "string",  "title": "string",  "description": "string",  "category": "string",      // personal, professional, health, etc.  "priority": "number",      // 1-5 scale  "status": "string",        // active, completed, paused  "target_date": "string",  "created_date": "datetime",  "updated_date": "datetime",  "progress_percentage": "number",  "metadata": {}             // Additional goal information}
```

2. Milestones Collection:

```javascript
{  "_id": ObjectId,  "goal_id": "string",  "title": "string",  "description": "string",  "due_date": "string",  "completed": "boolean",  "completed_date": "datetime",  "created_date": "datetime",  "priority": "number"}
```

3. Progress Logs Collection

```javascript
{  "_id": ObjectId,  "goal_id": "string",  "entry_type": "string",    // progress, obstacle, achievement, reflection  "content": "string",  "timestamp": "datetime",  "metadata": {}}
```

🔧 Configuration Options
Groq Model Selection

```python
# Available models in config.py
MODELS = {
    "primary": "llama-3.3-70b-versatile",    # Default - balanced performance
    "fast": "llama-3.1-8b-instant",          # Faster responses
    "creative": "mixtral-8x7b-32768"         # More creative responses
}
```

Generation Parameters

```python
GENERATION_PARAMS = {
    "temperature": 0.7,       # Creativity level (0.0-1.0)
    "max_tokens": 4096,       # Maximum response length
    "top_p": 0.9              # Nucleus sampling parameter
}
```

🎯 Commands Reference

```Interactive Commands
CommandDescriptionhelpShow available commands and examplesanalyticsDisplay detailed goal statisticsresetClear conversation historyquit / exitExit the application
```

# Natural Language Commands

IntentExampleCreate Goal
```
"I want to learn guitar this year"
Add Milestone
```
"Add a milestone to practice 30 minutes daily"

Log Progress
```
"I completed my first lesson today"
View Goals
```
"Show me my current goals"
Update Goal
```
"Change my fitness goal priority to high"
Get Analytics
```
"What's my goal completion rate?"

🔍 Troubleshooting
```bash
Common Issues
Groq API Key Error

```

❌ Error: GROQ_API_KEY not found
```bash
Solution: Ensure your .env file contains the correct API key
MongoDB Connection Failed

```

❌ Failed to connect to MongoDB
```bash
Solution:

Check MongoDB is running: mongod
Verify connection string in .env
For Atlas: Check network access and credentials
Import Errors
```


❌ Failed to connect to MongoDB
```bash
Solution:

Check MongoDB is running: mongod
Verify connection string in .env
For Atlas: Check network access and credentials
Import Errors
```


❌ ModuleNotFoundError: No module 

named 'groq'

Solution:
```bash
pip install -r requirements.txt
Empty Collections
```

This is normal! Collections populate when you create goals

Test with: "I want to learn Python programming"

Performance Optimization
Faster Responses

# Use the fast model for quicker interactions

1. Config.MODELS["primary"] = "llama-3.1-8b-instant"
MongoDB Indexing

2. The system automatically creates indexes for optimal query performance:
Goals: user_id + status, priority, created_date

3. Milestones: goal_id, due_date
Progress: goal_id + timestamp, entry_type


🚀 Advanced Usage
Running Demo Mode

```bash
# Experience pre-built goal creation scenarios
python main.py demo
Custom Goal Categories
The system supports any goal category:

personal - Personal development, hobbies
professional - Career, skills, networking
health - Fitness, nutrition, mental health
financial - Savings, investments, budgeting
relationships - Family, friends, social goals
learning - Education, certifications, new skills
Batch Operations
```

```python
# Programmatic goal creation
from goal_agent import GoalAgent

agent = GoalAgent()
goals = [
    "Learn Python programming in 6 months",
    "Run a 10K by summer",
    "Save $10,000 this year"
]
for goal in goals:
    response = agent.chat(f"Create goal: {goal}")
    print(response)

```

🤝 Contributing
We welcome contributions to improve Goal Agent! Here's how you can help:

## Getting Started
Fork the repository

Create a feature branch:
```bash
git checkout -b feature/amazing-feature

```
Make your changes
```bash
Add tests for new functionality
Commit changes: git commit -m 'Add amazing feature'
```
Push to branch:
```bash
git push origin feature/amazing-feature
```
# Open a Pull Request
Development Setup:

```bash
# Install development dependencies
pip install -r requirements-dev.txt
# Run tests
python -m pytest
# Format code
black .
isort .
# Type checking
mypy .
```bash
# Install development dependencies
pip install -r requirements-dev.txt
# Run tests
python -m pytest
# Format code
black .
isort .
# Type checking
mypy .
```
```bash
# Install development dependencies
pip install -r requirements-dev.txt
# Run tests
python -m pytest
# Format code
black .
isort .
# Type checking
mypy .

```

Areas for Contribution
🎨 UI Development: Web interface for goal management
📱 Mobile App: React Native or Flutter integration
📊 Visualization: Advanced analytics and progress charts
🔌 Integrations: Calendar sync, Slack notifications, etc.
🌐 Internationalization: Multi-language support
🧪 Testing: Expand test coverage
📚 Documentation: Improve guides and examples

📜 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
Groq for providing ultra-fast LLM inference
MongoDB for robust document storage
OpenAI for inspiration from GPT function calling patterns
SMART Goals Framework by George T. Doran
The open-source community for valuable feedback and contributions

🔗 Links
Documentation: Full API Documentation
Groq Console: Get your API key
MongoDB Atlas: Free cloud database
Issue Tracker: Report bugs or request features
Discussions: Community support

📈 Roadmap

Version 2.0 (Coming Soon)
 Web-based dashboard
 Calendar integration
 Team goal collaboration
 Advanced analytics with charts
 Mobile notifications
 Goal templates library
Version 3.0 (Future)
 Multi-user support with authentication
 Goal sharing and social features
 Integration with productivity apps
 Voice interface support
 Machine learning-based success prediction
 Gamification elements
 
Built with ❤️ by developers who believe in the power of structured goal achievement

Start your journey to achieving your dreams today with Goal Agent! 🎯