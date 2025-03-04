import os
from crewai import Agent
from dotenv import load_dotenv

load_dotenv()

def get_agent_config():
    """Get the configuration for the AI provider"""
    ai_provider = os.getenv('AI_PROVIDER', 'openai').lower()
    
    if ai_provider == 'anthropic':
        return {
            'model': 'claude-3-opus-20240229',
            'provider': 'anthropic'
        }
    else:  # default to OpenAI
        return {
            'model': 'gpt-4o-mini',
            'provider': 'openai'
        }

def create_agent(role, goal, backstory, verbose=True):
    """Create an agent with the configured AI provider"""
    config = get_agent_config()
    
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        verbose=verbose,
        **config
    ) 