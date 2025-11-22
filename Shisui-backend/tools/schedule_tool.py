from typing import List, Dict

def create_study_schedule(tasks: List[Dict[str, str]]) -> Dict:
    """
    Creates a study schedule based on the provided tasks.
    
    Args:
        tasks: A list of dictionaries, where each dictionary represents a task 
               and has keys 'time' (e.g., "10:00 AM") and 'activity' (e.g., "Read Chapter 1").
               
    Returns:
        A dictionary containing the action 'set_schedule' and the schedule details.
    """
    return {
        "action": "set_schedule",
        "schedule": tasks,
        "message": f"I've created a study schedule with {len(tasks)} items for you."
    }

def get_schedule_tool():
    return create_study_schedule
