#OLD rag_service.py:
# Question → directly to ChromaDB → LLM → Answer
# NEW rag_service.py:
# Question → Router → ChromaDB OR SQLite OR Both → Reranker → Best Answer

from factories.embedding_factory import get_embedding_model #factory folder
from factories.llm_factory import get_llm
from factories.vectorstore_factory import get_vectorstore
from loaders.document_loader import load_document #loaders folder
from sources.document_source import DocumentSource
from sources.database_source import DatabaseSource
from router.query_router import QueryRouter
from reranker.reranker import Reranker


import yaml #read config.yaml to this file
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter #Splits your documents into small chunks
# from langchain_core.prompts import ChatPromptTemplate #Creates a template for how you ask questions to the LLM
# from langchain_core.output_parsers import StrOutputParser #Converts LLM's response into a clean readable string
# from langchain_core.runnables import RunnablePassthrough #Passes te user's question as it is through the chain without changing it


#train(): 1. Load document (using loaders) 2. Split into chunks (using splitter) 3. Save to ChromaDB (using vectorstore)
#OLD ask() : 1. Create retriever from vectorstore 2. Create prompt template 3. Build chain → retriever | prompt | llm | parser 4. Return answer
#NEW ask() : 1. ask router which source, 2. query right source(s), 3. reranker picks best answer

class RAGService():
    def __init__(self):
        #loading config.yaml file
        with open("config.yaml","r") as f:
            self.config = yaml.safe_load(f) #converts yaml to dict format

        #calling embedding factory
        self.embedding = get_embedding_model(self.config) 

        #calling LLM factory
        self.llm = get_llm(self.config)

        #calling vectorstore factory
        self.vectorstore = get_vectorstore(self.config, self.embedding)

        #setting text splitter
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = self.config["chunking"]["chunk_size"],
            chunk_overlap = self.config["chunking"]["chunk_overlap"]
        )

        self.doc_source = DocumentSource(self.vectorstore, self.llm)
        self.db_source = DatabaseSource(self.llm)
        self.router = QueryRouter(self.llm)
        self.reranker = Reranker(self.llm)


   
    def train(self, file_path: str):
        # Load document from loaders folder
        documents = load_document(file_path)  #uses loaders/document_loader.py
        
        #split into chunks
        chunks = self.splitter.split_documents(documents)

        #save to ChromoDB
        self.vectorstore.add_documents(chunks)

        return f"Successfully trained on {len(chunks)} chunks!"


    def ask(self, question:str):
        #Step 1 - Route the question 
        route = self.router.route(question)
        print(f"Routing to : {route}")

        answers = []

        # Step 2 - Query the right source(s)
        if route == "document" or route == "both":
            doc_answer = self.doc_source.query(question)
            if doc_answer:
                answers.append(doc_answer)
   
        if route == "database" or route == "both":
            db_answer = self.db_source.query(question)
            if db_answer:
                answers.append(db_answer)

        # Step 3 - Handle no answers
        if not answers:
            print(f"No answers found from {route} — trying fallback!")

            if route == "document":
                # router said document but nothing found
                # fallback → try database!
                print("Fallback: trying database...")
                db_answer = self.db_source.query(question)
                if db_answer:
                    answers.append(db_answer)

            elif route == "database":
                # router said database but nothing found
                # fallback → try documents!
                print("Fallback: trying documents...")
                doc_answer = self.doc_source.query(question)
                if doc_answer:
                    answers.append(doc_answer)

        # Step 4 - Still no answers after fallback
        if not answers:
            return "I could not find relevant information from any source!"

        # Step 5 - Rerank and return best answer
        return self.reranker.rerank(question, answers)
    