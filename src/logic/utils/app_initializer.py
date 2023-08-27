from dotenv import load_dotenv
import logic.audio_systems.precise_access as precise

def initialize_app():
    # Load .env file
    load_dotenv()
    
    # Initialize precise
    precise.initialize()
    