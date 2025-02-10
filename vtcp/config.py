from dotenv import load_dotenv
import os

def load_config():
    load_dotenv()
    
    required_vars = ['AZURE_SPEECH_KEY', 'AZURE_SPEECH_REGION']
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
    
    return {
        'speech_key': os.getenv('AZURE_SPEECH_KEY'),
        'speech_region': os.getenv('AZURE_SPEECH_REGION')
    }