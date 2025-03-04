"""Service for handling RAG (Retrieval-Augmented Generation) operations."""

import json
from collections.abc import AsyncGenerator, Sequence
from typing import Any

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline  # type: ignore

from app.core.config import settings
from app.core.exceptions import RAGError
from app.services.vector_store import VectorStore


class RAGService:
    """Service for managing RAG operations."""

    def __init__(self, vector_store: VectorStore) -> None:
        """Initialize RAG service.

        Args:
            vector_store: Vector store instance for document retrieval
        """
        self.vector_store = vector_store

        # Initialize LLM
        self.tokenizer = AutoTokenizer.from_pretrained(settings.LLM_MODEL_NAME)
        self.model = AutoModelForCausalLM.from_pretrained(
            settings.LLM_MODEL_NAME,
            torch_dtype=torch.float16,
            device_map="auto",
        )

        # Create pipeline
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=settings.MAX_NEW_TOKENS,
            temperature=settings.TEMPERATURE,
            top_p=settings.TOP_P,
            device_map="auto",
        )

    def _create_prompt(
        self,
        query: str,
        context_docs: Sequence[tuple[dict[str, Any], float, str | None]],
    ) -> str:
        """Create a prompt for the language model using retrieved documents.

        Args:
            query: User's query
            context_docs: Retrieved relevant documents with scores and snippets

        Returns:
            str: Generated prompt with context
        """
        prompt = f"Question: {query}\n\nContext:\n"
        for doc, score, snippet in context_docs:
            if snippet:
                prompt += f"\n- {snippet} (relevance: {score:.2f})"
        prompt += "\n\nAnswer:"
        return prompt

    async def query(self, query: str, limit: int = 5) -> str:
        """Process a single query using RAG.

        Args:
            query: User query
            limit: Maximum number of documents to retrieve

        Returns:
            str: Generated response

        Raises:
            RAGError: If there's an error during processing
        """
        try:
            # Retrieve relevant documents
            context_docs = await self.vector_store.search(query, limit)

            # Create prompt with context
            prompt = self._create_prompt(query, context_docs)

            # TODO: Implement actual LLM call with prompt
            return f"This is a mock response based on prompt: {prompt}"

        except Exception as e:
            raise RAGError(f"Error processing RAG query: {str(e)}")

    async def chat(self, messages: list[dict[str, str]], limit: int = 5) -> str:
        """Process a chat conversation using RAG.

        Args:
            messages: List of chat messages
            limit: Maximum number of documents to retrieve

        Returns:
            str: Generated response

        Raises:
            RAGError: If there's an error during processing
        """
        try:
            # Extract the latest user message
            latest_msg = messages[-1]["content"]

            # Retrieve relevant documents
            context_docs = await self.vector_store.search(latest_msg, limit)

            # Create prompt with context
            prompt = self._create_prompt(latest_msg, context_docs)

            # TODO: Implement actual chat completion with prompt
            return f"This is a mock chat response based on prompt: {prompt}"

        except Exception as e:
            raise RAGError(f"Error processing RAG chat: {str(e)}")

    async def generate_response(
        self, query: str, num_chunks: int = 3
    ) -> dict[str, Any]:
        """Generate a response using RAG.

        Args:
            query: User's question
            num_chunks: Number of context chunks to retrieve

        Returns:
            dict[str, Any]: Generated response with context and prompt

        Raises:
            RAGError: If there's an error during generation
        """
        try:
            # Retrieve relevant chunks
            context = await self.vector_store.search(query, limit=num_chunks)

            # Create prompt
            prompt = self._create_prompt(query, context)

            # Generate response
            response = self.pipe(prompt)[0]["generated_text"]

            # Extract the actual response (after the prompt)
            response_text = response.split("[/INST]")[-1].strip()

            return {"answer": response_text, "context": context, "prompt": prompt}
        except Exception as e:
            raise RAGError(f"Error generating response: {str(e)}")

    async def generate_streaming_response(
        self, query: str, num_chunks: int = 3
    ) -> AsyncGenerator[str, None]:
        """Generate a streaming response using RAG.

        Args:
            query: User's question
            num_chunks: Number of context chunks to retrieve

        Yields:
            str: Generated response tokens and context

        Raises:
            RAGError: If there's an error during generation
        """
        try:
            # Retrieve relevant chunks
            context = await self.vector_store.search(query, limit=num_chunks)

            # Create prompt
            prompt = self._create_prompt(query, context)

            # Stream the response
            response_text = ""
            for output in self.pipe(
                prompt,
                max_new_tokens=settings.MAX_NEW_TOKENS,
                temperature=settings.TEMPERATURE,
                top_p=settings.TOP_P,
                stream=True,
            ):
                if output and len(output) > 0:
                    token = output[0]["generated_text"][len(response_text) :]
                    response_text = output[0]["generated_text"]

                    if token:
                        yield json.dumps({"token": token, "finished": False}) + "\n"

            # Send the context at the end
            yield json.dumps({"context": context, "finished": True}) + "\n"

        except Exception as e:
            raise RAGError(f"Error generating response: {str(e)}")
