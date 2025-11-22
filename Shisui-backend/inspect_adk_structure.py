import sys
import os
import pkgutil
import google.adk

print(f"google.adk path: {google.adk.__path__}")

def list_modules(package):
    for importer, modname, ispkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        print(modname)

list_modules(google.adk)

# Try to find InvocationContext
try:
    from google.adk.agents.invocation_context import InvocationContext
    print("\nFound InvocationContext in google.adk.agents.invocation_context")
    print(help(InvocationContext))
except ImportError:
    print("\nInvocationContext not found in google.adk.agents.invocation_context")

try:
    from google.adk.types import InvocationContext
    print("\nFound InvocationContext in google.adk.types")
except ImportError:
    pass
