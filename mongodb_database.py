from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure
from datetime import datetime
from typing import List, Dict, Optional, Any
from config import Config
import logging

# Import ObjectId with fallback for different pymongo versions
try:
    from bson.objectid import ObjectId
except ImportError:
    from pymongo.objectid import ObjectId

class GoalMongoDB:
    def __init__(self, uri: str = Config.MONGO_URI, db_name: str = Config.DB_NAME):
        try:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client[db_name]
            
            # Initialize collections
            self.goals = self.db['goals']
            self.milestones = self.db['milestones'] 
            self.progress_logs = self.db['progress_logs']
            
            # Create indexes for better performance
            self._create_indexes()
            logging.info("Connected to MongoDB successfully")
            
        except ConnectionFailure as e:
            logging.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    def _create_indexes(self):
        """Create database indexes for optimized queries"""
        try:
            self.goals.create_index([("user_id", ASCENDING), ("status", ASCENDING)])
            self.goals.create_index([("created_date", DESCENDING)])
            self.milestones.create_index([("goal_id", ASCENDING)])
            self.progress_logs.create_index([("goal_id", ASCENDING), ("timestamp", DESCENDING)])
        except Exception as e:
            logging.warning(f"Index creation warning: {e}")
    
    def create_goal(self, goal_data: Dict[str, Any]) -> str:
        """Create a new goal and return its ObjectId as string"""
        goal_doc = {
            "user_id": goal_data.get('user_id', 'default'),
            "title": goal_data['title'],
            "description": goal_data.get('description', ''),
            "category": goal_data.get('category', 'personal'),
            "priority": goal_data.get('priority', 3),
            "status": goal_data.get('status', 'active'),
            "target_date": goal_data.get('target_date'),
            "created_date": datetime.utcnow(),
            "updated_date": datetime.utcnow(),
            "metadata": goal_data.get('metadata', {}),
            "progress_percentage": 0
        }
        
        result = self.goals.insert_one(goal_doc)
        return str(result.inserted_id)
    
    def get_goals(self, user_id: str = 'default', status: str = 'active', 
                  limit: int = None) -> List[Dict[str, Any]]:
        """Retrieve goals for a user"""
        try:
            query = {"user_id": user_id}
            if status != 'all':
                query["status"] = status
            
            cursor = self.goals.find(query).sort([
                ("priority", DESCENDING), 
                ("created_date", DESCENDING)
            ])
            
            if limit:
                cursor = cursor.limit(limit)
                
            goals = []
            for doc in cursor:
                goal = self._serialize_document(doc)
                # Add milestone count
                goal['milestone_count'] = self.milestones.count_documents({"goal_id": goal['id']})
                goals.append(goal)
                
            return goals
            
        except Exception as e:
            logging.error(f"Error retrieving goals: {e}")
            return []
    
    def get_goal_by_id(self, goal_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific goal by ID"""
        try:
            doc = self.goals.find_one({"_id": ObjectId(goal_id)})
            return self._serialize_document(doc) if doc else None
        except Exception as e:
            logging.error(f"Error retrieving goal {goal_id}: {e}")
            return None
    
    def update_goal(self, goal_id: str, update_data: Dict[str, Any]) -> bool:
        """Update a goal"""
        try:
            update_data['updated_date'] = datetime.utcnow()
            result = self.goals.update_one(
                {"_id": ObjectId(goal_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            logging.error(f"Error updating goal {goal_id}: {e}")
            return False
    
    def add_milestone(self, goal_id: str, milestone_data: Dict[str, Any]) -> str:
        """Add a milestone to a goal"""
        milestone_doc = {
            "goal_id": goal_id,
            "title": milestone_data['title'],
            "description": milestone_data.get('description', ''),
            "due_date": milestone_data.get('due_date'),
            "completed": False,
            "completed_date": None,
            "created_date": datetime.utcnow(),
            "priority": milestone_data.get('priority', 3)
        }
        
        result = self.milestones.insert_one(milestone_doc)
        return str(result.inserted_id)
    
    def get_milestones(self, goal_id: str) -> List[Dict[str, Any]]:
        """Get all milestones for a goal"""
        try:
            cursor = self.milestones.find({"goal_id": goal_id}).sort("created_date", ASCENDING)
            return [self._serialize_document(doc) for doc in cursor]
        except Exception as e:
            logging.error(f"Error retrieving milestones for goal {goal_id}: {e}")
            return []
    
    def log_progress(self, goal_id: str, entry_type: str, content: str, 
                     metadata: Dict[str, Any] = None) -> str:
        """Log progress for a goal"""
        log_doc = {
            "goal_id": goal_id,
            "entry_type": entry_type,  # 'progress', 'obstacle', 'achievement', 'reflection'
            "content": content,
            "timestamp": datetime.utcnow(),
            "metadata": metadata or {}
        }
        
        result = self.progress_logs.insert_one(log_doc)
        return str(result.inserted_id)
    
    def get_progress_logs(self, goal_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get progress logs for a goal"""
        try:
            cursor = self.progress_logs.find({"goal_id": goal_id}).sort("timestamp", DESCENDING).limit(limit)
            return [self._serialize_document(doc) for doc in cursor]
        except Exception as e:
            logging.error(f"Error retrieving progress logs: {e}")
            return []
    
    def get_goal_analytics(self, user_id: str = 'default') -> Dict[str, Any]:
        """Get analytics data for user's goals"""
        try:
            # Status breakdown
            pipeline = [
                {"$match": {"user_id": user_id}},
                {"$group": {
                    "_id": "$status",
                    "count": {"$sum": 1},
                    "avg_priority": {"$avg": "$priority"}
                }}
            ]
            
            status_stats = list(self.goals.aggregate(pipeline))
            
            # Category breakdown
            category_pipeline = [
                {"$match": {"user_id": user_id, "status": "active"}},
                {"$group": {
                    "_id": "$category",
                    "count": {"$sum": 1}
                }}
            ]
            
            category_stats = list(self.goals.aggregate(category_pipeline))
            
            return {
                "status_breakdown": status_stats,
                "category_breakdown": category_stats,
                "total_goals": self.goals.count_documents({"user_id": user_id}),
                "active_goals": self.goals.count_documents({"user_id": user_id, "status": "active"})
            }
            
        except Exception as e:
            logging.error(f"Error getting analytics: {e}")
            return {}
    
    @staticmethod
    def _serialize_document(doc: Dict[str, Any]) -> Dict[str, Any]:
        """Convert MongoDB document to serializable format"""
        if not doc:
            return {}
            
        doc = doc.copy()
        doc['id'] = str(doc.pop('_id'))
        
        # Convert datetime objects to ISO strings
        for key, value in doc.items():
            if isinstance(value, datetime):
                doc[key] = value.isoformat()
                
        return doc
    
    # def close(self):
    #     """Close database connection"""
    #     if self.client:
    #         self.client.close()
    #         logging.info("MongoDB connection closed")
