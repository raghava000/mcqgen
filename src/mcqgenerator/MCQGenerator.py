import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.logger import logging

#importing necessary packages from langchain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMchain
from langchain.chains import SequentialChain

# load environment variables from the .env fiule
load_dotenv()

#Access the env variable
key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(openai_api_key=key,model_name="gpt-3.5-turb0", temperature=0.7)
logging.info("Succesfully used ChatOpenAI")

TEMPLATE="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \ creatre a quiz of {number} multiple choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}

"""

quiz_generative_promt = PromptTemplate(
    input_variables=["text","number", "subject", "tone", "response_json"],
    template=TEMPLATE
)
logging.info("Used the first template to generate the quiz")

quiz_chain= LLMchain(llm=llm,prompt=quiz_generative_promt, output_key="quiz", verbose=True)
logging.info("Used llmchain to use prompt and store output in quiz variable")

TEMPLATE2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students. \
You need to evaluate the complexity if the question and give a complete analusis of the quiz. Only use at max 50 words for complexity .
If the quiz is not as per the cognitive and anlytical abilities of the students,\
update the quiz questions which needs to changed and change the tone such that it perfectly fits the student abilities.
Quiz_MCQs:
{quiz}

Check from tan expert English Writer of the above quiz:
"""

quiz_evaluation_promt=PromptTemplate(input_variables=["subject","quiz"], template=TEMPLATE2)
logging.info("Used the second template to evaluate the quiz")



review_chain= LLMchain(llm=llm,prompt=quiz_evaluation_promt, output_key="review", verbose=True)
logging.info("Used llmchain to use prompt and store output in review variable")

generate_evaluate_chain=SequentialChain(chains=[quiz_chain, review_chain], input_variables=["text","number", "subject", "tone", "response_json"],
                        output_variables=["quiz", "review"], verbose=True,)



