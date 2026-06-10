from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

class DocumentSource:
    def __init__(self, vectorstore, llm):
        self.vectorstore = vectorstore
        self.llm = llm
        self.name = "document"

    def query(self, question:str):
        #search ChromaDB
        #A retriever is responsible for:
            # Taking a user query.
            # Converting it into an embedding.
            # Searching the vector database.
            # Returning the most relevant documents.
        retriever = self.vectorstore.as_retriever(
            search_kwargs = {"k" : 3} #k specifies how many documents to retrieve.
        )

        #get relevant chunks
        docs = retriever.invoke(question) #invoke() is the standard LangChain method used to run or execute an object with a given input.

        if not docs:
            return None #no relevant docs found

        #build context
        context = "\n".join([doc.page_content for doc in docs]) #takes the content from all retrieved documents and combines it into a single string separated by newlines.

        #get answer from llm
        prompt = f"""
        Answer based only on this context : 
        {context}

        Question : {question}

        If you cannot answer from context, say "NOT FOUND"
        """

        answer = self.llm.invoke(prompt) #invoke means take this input and get output

        #return answer with confidence
        return{
            "source" : "document",
            "answer" : answer,
            "context" : context,
            "confidence" : self._calculate_confidence(docs)
        }
    
    def _calculate_confidence(self, docs): #The _ prefix means: "This is a private method — only used inside this class"
        #more relevant docs = higher confidence
        if len(docs) >= 3:
            return "high"
        elif len(docs) == 2:
            return "medium"
        else:
            return "low"


    #this is more correct approach
    # def _calculate_confidence(self, docs):
    #     #more relevant docs = higher confidence
    #     if avg_similarity > 0.85:
    #         return "high"
    #     elif avg_similarity > 0.70:
    #         return "medium"
    #     else:
    #         return "low"


