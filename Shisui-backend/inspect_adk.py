import sys
import os

# Add the current directory to sys.path
sys.path.append(os.getcwd())

try:
    from google.adk.agents import Agent
    print("Successfully imported Agent")
    print("Attributes of Agent class:")
    print(dir(Agent))
    
    print("\nHelp on Agent class:")
    help(Agent)
except ImportError as e:
    print(f"Error importing Agent: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
