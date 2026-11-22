
import logging

from tavily import AsyncTavilyClient

from app.core.config import settings


logger = logging.getLogger(__name__)


class SearchService:

    def __init__(self):
        self.client = AsyncTavilyClient( api_key=settings.tavily_api_key )

    async def search(self, question: str) -> str:

        if not question.strip():
            raise ValueError("Search question cannot be empty")

        logger.info("Searching the web using Tavily")

        response = await self.client.search(
            query=question,
            search_depth="basic",
            max_results=3
        )

        results = response.get("results", [])

        if not results:
            return ""

        context = "\n\n".join(
            f"Title: {item.get('title', '')}\n"
            f"Source: {item.get('url', '')}\n"
            f"Content: {item.get('content', '')}"
            for item in results
        )

        logger.info("Retrieved %d search results", len(results))

        return context


search_service = SearchService()
