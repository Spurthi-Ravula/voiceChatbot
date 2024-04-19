from langchain.llms import CTransformers
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from typing import Any, Dict, List, Union
import sys

model_id = 'TheBloke/Mistral-7B-codealpaca-lora-GGUF'
config = {'temperature': 0.00, 'context_length': 8000}

llm = CTransformers(model=model_id,
                    model_type='mistral',
                    config=config)

prompt = PromptTemplate.from_template("you are an assistant answer the following :{query}")

chain = LLMChain(llm=llm, prompt=prompt)

def genai_engine(query):
    response = chain.run(query)
    return response
