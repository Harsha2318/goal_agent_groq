#!/usr/bin/env python3
"""
Goal Agent with MongoDB - AI-powered goal setting and tracking assistant
Built with Groq LLM and MongoDB for fast, intelligent responses and robust data storage
"""

import sys
import logging
from goal_agent import GoalAgent
from config import Config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """Main application entry point"""
    if not Config.GROQ_API_KEY:
        print("❌ Error: GROQ_API_KEY not found in environment variables")
        print("Please set your Groq API key in .env file or environment")
        sys.exit(1)
    
    # Initialize the goal agent
    print("🎯 Goal Agent with MongoDB starting up...")
    print("Powered by Groq LLM for lightning-fast responses")
    print("Using MongoDB for robust goal tracking and analytics\n")
    
    try:
        agent = GoalAgent()
        print("✅ Successfully connected to MongoDB and Groq API")
    except Exception as e:
        print(f"❌ Failed to initialize Goal Agent: {e}")
        print("Please check your MongoDB connection and Groq API key")
        sys.exit(1)
    
    print("\n👋 Hello! I'm your Goal Achievement Assistant.")
    print("I can help you:")
    print("  🎯 Set SMART goals with detailed tracking")
    print("  📊 Create actionable milestones and deadlines")  
    print("  📈 Track progress and analyze patterns")
    print("  🚀 Provide motivation and overcome obstacles")
    print("  🔍 Search and manage all your goals")
    print("\nType 'help' for commands, or 'quit' to exit.\n")
    
    # Main conversation loop
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                print("\n🎯 Keep working towards your goals! Good luck!")
                break
            
            # Handle help command
            if user_input.lower() == 'help':
                show_help()
                continue
                
            # Handle analytics command
            if user_input.lower() == 'analytics':
                show_analytics(agent)
                continue
                
            # Handle reset command
            if user_input.lower() == 'reset':
                agent.reset_conversation()
                print("🔄 Conversation history cleared!\n")
                continue
            
            if not user_input:
                continue
            
            # Process user input and get response
            print("\n🤔 Analyzing your request...")
            response = agent.chat(user_input)
            print(f"\n🎯 Goal Agent: {response}\n")
            print("-" * 50 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Conversation interrupted. Keep achieving your goals!")
            break
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            print(f"\n❌ Unexpected error: {e}")
            print("Let's try that again...\n")
        finally:
            # Clean up resources
            if 'agent' in locals():
                agent.close()

def show_help():
    """Display help information"""
    print("""
🎯 Goal Agent Commands:

Basic Commands:
  help        - Show this help message
  analytics   - View your goal statistics
  reset       - Clear conversation history  
  quit/exit   - End the session

Example Conversations:
  "I want to learn Python programming this year"
  "Show me all my current goals"
  "Help me break down my fitness goal into milestones"
  "I'm struggling with motivation on my career goals"
  "Update my writing goal to have a higher priority"
  "What progress have I made on my health goals?"

Tips:
  • Be specific about what you want to achieve
  • Mention timeframes when setting goals
  • Ask for help breaking down large goals
  • Regular check-ins help maintain momentum
""")

def show_analytics(agent):
    """Display user analytics"""
    try:
        print("\n📊 Analyzing your goals...")
        analytics = agent.get_user_analytics()
        
        if analytics.get('success'):
            data = analytics['analytics']
            print(f"\n🎯 Your Goal Analytics:")
            print(f"  Total Goals: {data.get('total_goals', 0)}")
            print(f"  Active Goals: {data.get('active_goals', 0)}")
            
            if data.get('status_breakdown'):
                print("\n📈 Status Breakdown:")
                for item in data['status_breakdown']:
                    print(f"  {item['_id'].title()}: {item['count']} goals")
                    
            if data.get('category_breakdown'):
                print("\n🏷️ Category Breakdown:")
                for item in data['category_breakdown']:
                    print(f"  {item['_id'].title()}: {item['count']} goals")
        else:
            print("❌ Unable to retrieve analytics at this time")
            
    except Exception as e:
        print(f"❌ Error retrieving analytics: {e}")
    
    print()

def run_demo():
    """Run a demonstration of the goal agent capabilities"""
    try:
        agent = GoalAgent()
        
        demo_interactions = [
            "I want to learn machine learning and get a job in AI by the end of next year",
            "Show me my goals",
            "Help me create milestones for my machine learning goal",
            "I completed an online course on Python. Log this as progress.",
            "What are my goal analytics?"
        ]
        
        print("🎯 Running Goal Agent Demo\n")
        
        for i, interaction in enumerate(demo_interactions, 1):
            print(f"Demo {i}: {interaction}")
            response = agent.chat(interaction)
            print(f"Response: {response}\n")
            print("-" * 60 + "\n")
            
    except Exception as e:
        print(f"❌ Demo failed: {e}")
    finally:
        if 'agent' in locals():
            agent.close()

if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        run_demo()
    else:
        main()
