# src/services/agent_service.py
from src.agents.historian import agent_historian_summarize
from src.agents.strategist import agent_strategist_analyze
from src.agents.responder import agent_responder_generate

class AgentService:
    async def process_message(self, current_message_content, recent_chunk, old_chunk):
        """
        Orchestrates the three-agent system to generate a final response.
        """
        # 1. Agent 1 summarizes the old part of the history
        summary = await agent_historian_summarize(old_chunk)

        # 2. Agent 2 analyzes the situation and defines a strategy
        strategy = await agent_strategist_analyze(current_message_content, summary)

        # 3. Agent 3 generates the final response based on all available data
        final_response = await agent_responder_generate(
            current_message_content,
            recent_chunk,
            summary,
            strategy
        )

        return final_response

# Singleton instance
agent_service = AgentService()
