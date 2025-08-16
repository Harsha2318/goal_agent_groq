from groq import Groq
import json
from datetime import datetime
from typing import List, Dict, Optional
from config import Config
from tools import GoalTools, GOAL_TOOLS
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

class GoalAgent:
    def __init__(self, api_key: str = Config.GROQ_API_KEY):
        if not api_key:
            raise ValueError("GROQ_API_KEY is required")
            
        self.client = Groq(api_key=api_key)
        self.tools = GoalTools()
        self.conversation_history = []
        
        # Enhanced system prompt for MongoDB-based goal agent
        self.system_prompt = f"""You are an expert Goal Achievement Assistant with comprehensive goal management capabilities. Current date: {datetime.now().strftime('%Y-%m-%d')}

CORE ROLE & IDENTITY:
You are a strategic goal-setting coach who combines expertise in behavioral psychology, productivity science, and achievement methodology. You have access to a powerful MongoDB database that stores user goals, milestones, progress logs, and analytics.

PRIMARY OBJECTIVES:
- Guide users through comprehensive goal-setting using SMART methodology
- Create detailed action plans with timelines, milestones, and accountability measures
- Provide ongoing motivation, tracking, and adaptive coaching
- Help users overcome obstacles and maintain momentum toward their goals
- Foster self-reflection and continuous improvement in goal achievement

TOOL USAGE:
You have access to powerful goal management tools:
- create_goal(): Create new SMART goals with full metadata
- get_goals(): Retrieve goals with filtering by status, category, priority
- get_goal_details(): Get complete goal information with milestones and progress
- add_milestone(): Break goals into manageable milestones
- log_progress(): Track progress, obstacles, and achievements
- update_goal(): Modify goal details, status, and priorities
- get_analytics(): Analyze goal performance and patterns

Always use tools when users want to save goals, track progress, or review existing goals.

SMART GOAL FRAMEWORK:
- Specific: Define exactly what will be accomplished
- Measurable: Establish clear metrics and success indicators  
- Achievable: Ensure goals are realistic given current circumstances
- Relevant: Align goals with user's broader life vision and values
- Time-bound: Set clear deadlines and interim checkpoints

COMMUNICATION STYLE:
- Encouraging and supportive, but also honest about challenges
- Ask thoughtful questions that promote self-discovery
- Provide specific, actionable advice rather than generic platitudes
- Balance optimism with realistic assessment of obstacles
- Celebrate progress while maintaining focus on the bigger picture

Remember: Your role is to be a catalyst for positive change, helping users not just set goals, but actually achieve them through thoughtful planning, consistent action, and adaptive learning."""

    def chat(self, user_message: str) -> str:
        """Main chat interface with tool calling capabilities"""
        self.conversation_history.append({"role": "user", "content": user_message})
        
        messages = [
            {"role": "system", "content": self.system_prompt}
        ] + self.conversation_history
        
        try:
            # Initial API call with tools
            response = self.client.chat.completions.create(
                model=Config.MODELS["primary"],
                messages=messages,
                tools=GOAL_TOOLS if GOAL_TOOLS else None,
                tool_choice="auto" if GOAL_TOOLS else None,
                **Config.GENERATION_PARAMS
            )
            
            # Simple response parsing - same as working test
            response_message = response.choices[0].message
            tool_calls = getattr(response_message, 'tool_calls', None)
            
            # Add assistant response to conversation
            assistant_message = {
                "role": "assistant",
                "content": response_message.content or ""
            }
            
            if tool_calls:
                assistant_message["tool_calls"] = [
                    {
                        "id": tc.id,
                        "type": tc.type,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in tool_calls
                ]
            
            self.conversation_history.append(assistant_message)
            
            # Process tool calls if any
            if tool_calls:
                return self._handle_tool_calls(tool_calls, messages)
            
            return response_message.content or ""
            
        except Exception as e:
            logging.error(f"Error in chat: {e}")
            return f"I apologize, but I encountered an error: {str(e)}. Please try again."
    
    def _handle_tool_calls(self, tool_calls, messages: List[Dict]) -> str:
        """Handle tool function calls"""
        # Define available functions
        available_functions = {
            "create_goal": self.tools.create_goal_function,
            "get_goals": self.tools.get_goals_function,
            "get_goal_details": self.tools.get_goal_details_function,
            "add_milestone": self.tools.add_milestone_function,
            "log_progress": self.tools.log_progress_function,
            "update_goal": self.tools.update_goal_function,
            "get_analytics": self.tools.get_analytics_function
        }
        
        # Process each tool call
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions.get(function_name)
            
            if function_to_call:
                try:
                    # Parse function arguments
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # Call the function
                    function_response = function_to_call(**function_args)
                    
                except Exception as e:
                    logging.error(f"Tool execution error: {e}")
                    function_response = {"error": str(e), "success": False}
                
                # Add tool response to conversation
                self.conversation_history.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(function_response)
                })
        
        # Make second API call with tool responses
        updated_messages = [
            {"role": "system", "content": self.system_prompt}
        ] + self.conversation_history
        
        try:
            second_response = self.client.chat.completions.create(
                model=Config.MODELS["primary"],
                messages=updated_messages,
                **Config.GENERATION_PARAMS
            )
            
            # Simple response parsing
            final_content = second_response.choices[0].message.content
            
            # Add final response to conversation
            self.conversation_history.append({
                "role": "assistant", 
                "content": final_content
            })
            
            return final_content or ""
            
        except Exception as e:
            logging.error(f"Error in second API call: {e}")
            return "I processed your request but encountered an issue generating the final response. Please try again."
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []
        logging.info("Conversation history reset")
    
    def get_user_analytics(self) -> Dict:
        """Get analytics for the current user"""
        return self.tools.get_analytics_function()
    
    def close(self):
        """Close database connections"""
        if self.tools.db:
            self.tools.db.close()
