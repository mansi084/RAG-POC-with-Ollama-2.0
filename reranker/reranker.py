class Reranker:
    def __init__(self, llm):
        self.llm = llm

    def rerank(self, question:str, answers: list):
        #if only one answer - return it directly
        if len(answers) == 1:
            return answers[0]["answer"]
        
        #if multiple answers - pick best one

        # build answers dynamically based on source
        answers_text = ""
        for answer in answers:
            answers_text += f"\nAnswer from {answer['source']}: {answer['answer']}\n"

        prompt = f"""
        Given this question and multiple answers from different sources,
        combine them into one best, accurate, complete answer.
        Avoid repetition and noise.
        
        Question: {question}

        {answers_text}
        
        Provide one clear combined answer:
        """

        return self.llm.invoke(prompt)
    