# src/services/agent_service.py
from src.agents.historian import agent_historian_summarize
from src.agents.strategist import agent_strategist_analyze
from src.agents.responder import agent_responder_generate

class AgentService:
    async def process_message(self, current_message_content, recent_chunk, old_chunk, image_url=None):
        """
        Orchestrates the three-agent system to generate a final response,
        now with multimodal capabilities.
        """
        summary = await agent_historian_summarize(old_chunk)
        strategy = await agent_strategist_analyze(current_message_content, summary)

        final_response = await agent_responder_generate(
            current_message_content,
            recent_chunk,
            summary,
            strategy,
            image_url  # Pass the image URL to the responder
        )

        return final_response

# Singleton instance
agent_service = AgentService()
