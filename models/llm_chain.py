
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

from config import settings
from core import constants


class LLMChainManager:
    """Manages LLM chain operations."""
    
    def __init__(self):
        """Initialize LLM model and chain."""
        self.model = OllamaLLM(model=settings.LLM_MODEL)
        self.chain = self._create_chain()
    
    def _create_chain(self):
        """Create the prompt chain."""
        prompt = ChatPromptTemplate.from_template(constants.PROMPT_TEMPLATE)
        return prompt | self.model
    
    def invoke_chain(self, reviews: str, question: str) -> str:
        """Invoke the chain with given inputs."""
        return self.chain.invoke({
            "reviews": reviews,
            "question": question
        })


_chain_manager = LLMChainManager()
chain = _chain_manager.chain
invoke_chain = _chain_manager.invoke_chain