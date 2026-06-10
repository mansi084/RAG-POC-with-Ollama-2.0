class QueryRouter:
    def __init__(self, llm):
        self.llm = llm

    def route(self, question:str):
        #Ask LLM which source to use
        prompt = f"""
        Classify this question into one of these categories:
        - "database" → questions about specific data, numbers, records
          Examples: "What is John's salary?", "How many employees in HR?"
        
        - "document" → questions about policies, guidelines, general info
          Examples: "What is the leave policy?", "What are office timings?"
        
        - "both" → questions that need data AND context
          Examples: "Does John's salary match the policy range?"

        Question: {question}
        
        Return ONLY one word: database, document, or both
        """

        route = self.llm.invoke(prompt).strip().lower()
        
        #clean up response 
        if "database" in route:
            return "database"
        elif "both" in route:
            return "both"
        else:
            return "document"
        