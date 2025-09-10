import openai
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser



class InterfaceLLM:
    def __init__(self):
        self.openai_key = ''
        self.openai_model = 'gpt-3.5-turbo'
        self.vectorstore_url = ''
        self.vectorstore_apikey = ''
        self.vector_quantity = 20

    def send_message(self):
        openai.api_key = self.openai_key
        usr_prompt = input("Enter your message: ")
       
        embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key)
       
        qdrant = QdrantClient(
            url = self.vectorstore_url,
            api_key=self.vectorstore_apikey
        )

        vectordb = Qdrant(client=qdrant, collection_name='TEST', embeddings=embeddings)

        retriever = vectordb.as_retriever()
        retriever.search_kwargs['k'] = self.vector_quantity

        ## f'{self.config_prompt}, Context: {info_vectorstore}, Question: {usr_prompt}'
        template = """You are a expert in intelligent solar microgrids, 
            your name is YofreePT, i want you to answer answer a question based only on the provided information, i want yo to always answer extensively and in detail.

            {context},
            Question: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)

        try: 
            model = ChatOpenAI(
                openai_api_key=openai.api_key,
                model=self.openai_model,
                temperature=0.9,
                max_tokens=4096,
                top_p=1,
                presence_penalty=0
            )
            chain = (
                {"context": retriever, "question": RunnablePassthrough()}
                | prompt
                | model
                | StrOutputParser()
            )

            result = chain.invoke(usr_prompt)
            print(f'Answer: {result}')
        except Exception as e:
            print(f'Error: {e}')


InterfaceLLM().send_message()







     


