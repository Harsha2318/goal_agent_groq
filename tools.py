import json
from typing import Dict, List, Any
from mongodb_database import GoalMongoDB
from datetime import datetime, timedelta
import logging

class GoalTools:
    def __init__(self):
        self.db = GoalMongoDB()
    
    def create_goal_function(self, title: str, description: str = "", category: str = "personal", 
                           priority: int = 3, target_date: str = "", user_id: str = "default") -> Dict:
        """Create a new goal with SMART criteria validation"""
        try:
            goal_data = {
                'user_id': user_id,
                'title': title,
                'description': description,
                'category': category,
                'priority': min(max(priority, 1), 5),  # Ensure priority is 1-5
                'target_date': target_date,
                'metadata': {
                    'created_by': 'goal_agent',
                    'smart_validated': True,
                    'version': '1.0'
                }
            }
            
            goal_id = self.db.create_goal(goal_data)
            return {
                "success": True, 
                "goal_id": goal_id, 
                "message": f"Goal '{title}' created successfully with ID: {goal_id}"
            }
            
        except Exception as e:
            logging.error(f"Error creating goal: {e}")
            return {"success": False, "error": str(e)}
    
    def get_goals_function(self, user_id: str = "default", status: str = "active", 
                          limit: int = None) -> Dict:
        """Retrieve user's goals"""
        try:
            goals = self.db.get_goals(user_id, status, limit)
            return {
                "success": True,
                "goals": goals,
                "count": len(goals)
            }
        except Exception as e:
            logging.error(f"Error retrieving goals: {e}")
            return {"success": False, "error": str(e)}
    
    def get_goal_details_function(self, goal_id: str) -> Dict:
        """Get detailed information about a specific goal"""
        try:
            goal = self.db.get_goal_by_id(goal_id)
            if not goal:
                return {"success": False, "message": "Goal not found"}
            
            milestones = self.db.get_milestones(goal_id)
            progress_logs = self.db.get_progress_logs(goal_id, limit=10)
            
            return {
                "success": True,
                "goal": goal,
                "milestones": milestones,
                "recent_progress": progress_logs
            }
        except Exception as e:
            logging.error(f"Error getting goal details: {e}")
            return {"success": False, "error": str(e)}
    
    def add_milestone_function(self, goal_id: str, milestone_title: str, 
                             milestone_description: str = "", due_date: str = "", 
                             priority: int = 3) -> Dict:
        """Add a milestone to a goal"""
        try:
            milestone_data = {
                'title': milestone_title,
                'description': milestone_description,
                'due_date': due_date,
                'priority': priority
            }
            
            milestone_id = self.db.add_milestone(goal_id, milestone_data)
            return {
                "success": True, 
                "milestone_id": milestone_id,
                "message": f"Milestone '{milestone_title}' added to goal successfully"
            }
            
        except Exception as e:
            logging.error(f"Error adding milestone: {e}")
            return {"success": False, "error": str(e)}
    
    def log_progress_function(self, goal_id: str, progress_type: str, content: str, 
                            metadata: Dict = None) -> Dict:
        """Log progress for a goal"""
        try:
            log_id = self.db.log_progress(goal_id, progress_type, content, metadata or {})
            return {
                "success": True, 
                "log_id": log_id,
                "message": "Progress logged successfully"
            }
        except Exception as e:
            logging.error(f"Error logging progress: {e}")
            return {"success": False, "error": str(e)}
    
    def update_goal_function(self, goal_id: str, **update_fields) -> Dict:
        """Update goal fields"""
        try:
            # Filter out None values and empty strings
            update_data = {k: v for k, v in update_fields.items() if v is not None and v != ""}
            
            success = self.db.update_goal(goal_id, update_data)
            if success:
                return {"success": True, "message": "Goal updated successfully"}
            else:
                return {"success": False, "message": "Goal not found or no changes made"}
                
        except Exception as e:
            logging.error(f"Error updating goal: {e}")
            return {"success": False, "error": str(e)}
    
    def get_analytics_function(self, user_id: str = "default") -> Dict:
        """Get goal analytics for user"""
        try:
            analytics = self.db.get_goal_analytics(user_id)
            return {"success": True, "analytics": analytics}
        except Exception as e:
            logging.error(f"Error getting analytics: {e}")
            return {"success": False, "error": str(e)}

# Tool definitions for Groq API
GOAL_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "create_goal",
            "description": "Create a new SMART goal with title, description, and target date",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "The goal title"},
                    "description": {"type": "string", "description": "Detailed goal description"},
                    "category": {"type": "string", "description": "Goal category (personal, professional, health, etc.)"},
                    "priority": {"type": "integer", "description": "Priority level 1-5 (5 = highest)", "minimum": 1, "maximum": 5},
                    "target_date": {"type": "string", "description": "Target completion date (YYYY-MM-DD)"}
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function", 
        "function": {
            "name": "get_goals",
            "description": "Retrieve user's goals with optional filtering",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {"type": "string", "description": "Goal status filter (active, completed, paused, all)"},
                    "limit": {"type": "integer", "description": "Maximum number of goals to return"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_goal_details",
            "description": "Get detailed information about a specific goal including milestones and progress",
            "parameters": {
                "type": "object",
                "properties": {
                    "goal_id": {"type": "string", "description": "The goal ID"}
                },
                "required": ["goal_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_milestone",
            "description": "Add a milestone to an existing goal",
            "parameters": {
                "type": "object",
                "properties": {
                    "goal_id": {"type": "string", "description": "The goal ID"},
                    "milestone_title": {"type": "string", "description": "Milestone title"},
                    "milestone_description": {"type": "string", "description": "Milestone description"},
                    "due_date": {"type": "string", "description": "Milestone due date (YYYY-MM-DD)"},
                    "priority": {"type": "integer", "description": "Milestone priority 1-5"}
                },
                "required": ["goal_id", "milestone_title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "log_progress",
            "description": "Log progress, obstacles, or achievements for a goal",
            "parameters": {
                "type": "object",
                "properties": {
                    "goal_id": {"type": "string", "description": "The goal ID"},
                    "progress_type": {"type": "string", "description": "Type: 'progress', 'obstacle', 'achievement', 'reflection'"},
                    "content": {"type": "string", "description": "Progress description"}
                },
                "required": ["goal_id", "progress_type", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_goal",
            "description": "Update goal information",
            "parameters": {
                "type": "object",
                "properties": {
                    "goal_id": {"type": "string", "description": "The goal ID"},
                    "title": {"type": "string", "description": "Updated goal title"},
                    "description": {"type": "string", "description": "Updated description"},
                    "status": {"type": "string", "description": "Updated status"},
                    "priority": {"type": "integer", "description": "Updated priority 1-5"}
                },
                "required": ["goal_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_analytics",
            "description": "Get goal analytics and statistics for the user",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]
