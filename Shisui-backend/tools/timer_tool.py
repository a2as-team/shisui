from typing import Dict, Any

def start_timer(duration_minutes: int, label: str = "Study Session") -> Dict[str, Any]:
    """
    Starts a study timer for the specified duration.
    
    Args:
        duration_minutes: Duration of the timer in minutes
        label: Label for the timer (e.g., "Math Study", "Break")
        
    Returns:
        Dictionary containing timer configuration for the frontend
    """
    return {
        "action": "start_timer",
        "duration_minutes": duration_minutes,
        "label": label,
        "message": f"Starting a {duration_minutes} minute timer for {label}."
    }

def get_timer_tool():
    return start_timer
