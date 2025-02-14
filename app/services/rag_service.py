from typing import List, Dict, Any, AsyncGenerator
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from fastapi.responses import StreamingResponse
import json

from app.core.config import settings
from app.services.vector_store import VectorStore
from app.core.exceptions import RAGError

class RAGService:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        
        # Initialize LLM
        self.tokenizer = AutoTokenizer.from_pretrained(settings.LLM_MODEL_NAME)
        self.model = AutoModelForCausalLM.from_pretrained(
            settings.LLM_MODEL_NAME,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        
        # Create pipeline
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=settings.MAX_NEW_TOKENS,
            temperature=settings.TEMPERATURE,
            top_p=settings.TOP_P,
            device_map="auto"
        )

    def _create_prompt(self, query: str, context: List[Dict[str, Any]]) -> str:
        """Create a prompt for the LLM using the retrieved context"""
        context_str = "\n\n".join([chunk["chunk"] for chunk in context])
        
        prompt = f"""<s>[INST] You are a helpful AI assistant. Use the following context to answer the question. 
        If you cannot find the answer in the context, say so.

        Context:
        {context_str}

        Question: {query}

        Answer: [/INST]"""
        
        return prompt

    async def generate_response(self, query: str, num_chunks: int = 3) -> Dict[str, Any]:
        """Generate a response using RAG"""
        try:
            # Retrieve relevant chunks
            context = await self.vector_store.search(query, limit=num_chunks)
            
            # Create prompt
            prompt = self._create_prompt(query, context)
            
            # Generate response
            response = self.pipe(prompt)[0]["generated_text"]
            
            # Extract the actual response (after the prompt)
            response_text = response.split("[/INST]")[-1].strip()
            
            return {
                "answer": response_text,
                "context": context,
                "prompt": prompt
            }
        except Exception as e:
            raise RAGError(f"Error generating response: {str(e)}")

    async def generate_streaming_response(
        self, 
        query: str, 
        num_chunks: int = 3
    ) -> AsyncGenerator[str, None]:
        """Generate a streaming response using RAG"""
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
                stream=True
            ):
                if output and len(output) > 0:
                    token = output[0]["generated_text"][len(response_text):]
                    response_text = output[0]["generated_text"]
                    
                    if token:
                        yield json.dumps({
                            "token": token,
                            "finished": False
                        }) + "\n"
            
            # Send the context at the end
            yield json.dumps({
                "context": context,
                "finished": True
            }) + "\n"
                
        except Exception as e:
            raise RAGError(f"Error generating response: {str(e)}")