# Router decides where to look, Confidence measures how good the answer is, and 
# Reranker is the safety net that fixes mistakes and combines the best answers — together they ensure accuracy!
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
        
#CASE 1
# Question: "Do high performing employees get 
#            more leaves than policy states?"

# Router → "both" 
#       ↓
# Document source searches → 
#   finds leave policy → confidence HIGH 
#       ↓
# Database source searches →
#   finds performance data → confidence HIGH 
#       ↓
# Reranker combines:
#   "Policy says 20 days"
#   "High performers average 22 days"
#   → "Yes, high performers get 2 extra days" 

#CASE 2
#Question: "How many Sales employees left the company?"

# Router → "document" --> wrong decision!
#       ↓
# Document searches → 
#   finds nothing relevant → confidence LOW 
#       ↓
# Without reranker:
#   returns weak answer 

# With reranker:
#   sees LOW confidence
#   says "I couldn't find enough information"
#   → honest response 

