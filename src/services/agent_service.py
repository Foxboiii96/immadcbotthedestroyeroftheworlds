# src/services/agent_service.py
from src.services.memory_service import memory_service
from src.agents.historian import agent_historian_summarize
from src.agents.strategist import agent_strategist_analyze
from src.agents.responder import agent_responder_generate
from src.agents.archivist import agent_archivist_filter_and_summarize

class AgentService:
    async def process_message(self, current_message_content, recent_chunk, old_chunk, image_url=None):
        """
        Orchestrates the full agent system, including long-term memory,
        to generate a final response.
        """
        # 1. Retrieve relevant long-term memories
        long_term_memories = memory_service.retrieve_relevant_memories(current_message_content)

        # 2. Generate short-term summary and strategy
        summary = await agent_historian_summarize(old_chunk)
        strategy = await agent_strategist_analyze(current_message_content, summary)

        # 3. Generate the final response using all available context
        final_response = await agent_responder_generate(
            current_message_content,
            recent_chunk,
            summary,
            strategy,
            long_term_memories,  # Pass memories to the responder
            image_url
        )

        # 4. Post-response: attempt to archive a new memory
        # We include the bot's own response for full context.
        full_conversation_log = "\n".join(recent_chunk + [f"Bot: {final_response}"])
        new_memory = await agent_archivist_filter_and_summarize(full_conversation_log)

        if new_memory:
            memory_service.add_memory(new_memory)
            print(f"New memory archived: {new_memory}")

        return final_response

# Singleton instance
agent_service = AgentService()
