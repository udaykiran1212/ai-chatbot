from app import app

# This is the entry point for Vercel serverless functions
def handler(event, context):
    return app(event, context) 