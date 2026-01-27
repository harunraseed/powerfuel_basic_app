import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel requires the app to be exported
application = app

# For Vercel serverless function
def handler(event, context):
    return application(event, context)
