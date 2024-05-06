from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langserve import add_routes
import uvicorn
import os
from langchain_community.llms import HuggingFaceEndpoint
from dotenv import load_dotenv
from decouple import config


HUGGINGFACEHUB_API_TOKEN = config("Huggingfacehub_api_key")

load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")


repo_id = "mistralai/Mistral-7B-Instruct-v0.2"


model=HuggingFaceEndpoint(
    repo_id=repo_id,
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN
)


app=FastAPI(
    title="Langchain Server",
    version="1.0",
    decsription="A simple API Server"

)

add_routes(
    app,
    model,
    path="/openai"
)
model=model
##ollama llama2
llm=model
prompt1=ChatPromptTemplate.from_template("Write me an essay about {topic} with 100 words")
prompt2=ChatPromptTemplate.from_template("Write me an poem about {topic} for a 5 years child with 100 words")

add_routes(
    app,
    prompt1|model,
    path="/essay"


)

add_routes(
    app,
    prompt2|llm,
    path="/poem"


)


if __name__=="__main__":
    uvicorn.run(app,host="localhost",port=8000)

