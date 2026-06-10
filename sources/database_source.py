import sqlite3 #The built-in Python module for working with SQLite databases.

class DatabaseSource:
    def __init__(self, llm, db_path = "my_db.sqlite"):
        self.llm = llm 
        self.db_path = db_path
        self.name = "database"

    def query(self, question : str):
        #Convert Question to SQL using LLM
        sql_prompt = f"""
        Convert this question to a SQL query.
        Return ONLY the SQL query, nothing else.

        Question: {question}
    
        Available tables:
        - employees (
            id, age, attrition, department, job_role,
            monthly_income, overtime, performance_rating,
            job_satisfaction, years_at_company, gender,
            education_field, marital_status, work_life_balance,
            total_working_years, training_times_last_year,
            percent_salary_hike, years_since_last_promotion
          )
        """

        sql_query = self.llm.invoke(sql_prompt)

        # clean up LLM response
        sql_query = sql_query.strip()
        # remove markdown code blocks if present
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

        try:
            #Run SQL query
            conn = sqlite3.connect(self.db_path) #creates a connection to an SQLite database.
            cursor = conn.cursor() #creates a cursor object from the database connection. cursor is used to send SQL commands and retrieve results.
            cursor.execute(sql_query) #tells the cursor to execute the SQL statement stored in the variable sql_query
            results = cursor.fetchall() #retrieves all rows returned by the most recent SELECT query and stores them in the variable results
            conn.close()

            if not results:
                return None
            
            #Convert results to natural language
            answer_prompt = f"""
            Convert these database results to a natural answer:
            Question: {question}
            Results: {results}
            """

            answer = self.llm.invoke(answer_prompt)

            return{
                "source": "database",
                "answer": answer,
                "raw_results": results,
                "confidence": "high" if results else "low"        
            }
    
        except Exception as e:
            print(f"Database error: {e}")
            print(f"SQL query attempted: {sql_query}")
            return None