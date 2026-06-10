import sqlite3
import csv
import os

# Step 1 - Define paths
CSV_PATH = "WA_Fn-UseC_-HR-Employee-Attrition.csv"
DB_PATH = "my_db.sqlite"

def setup_database():
    # Step 2 - Connect to SQLite (creates file automatically!)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Step 3 - Create employees table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            attrition TEXT,
            department TEXT,
            job_role TEXT,
            monthly_income INTEGER,
            overtime TEXT,
            performance_rating INTEGER,
            job_satisfaction INTEGER,
            years_at_company INTEGER,
            gender TEXT,
            education_field TEXT,
            marital_status TEXT,
            work_life_balance INTEGER,
            total_working_years INTEGER,
            training_times_last_year INTEGER,
            percent_salary_hike INTEGER,
            years_since_last_promotion INTEGER
        )
    """)

    print("Table created successfully!")

    # Step 4 - Read CSV and insert rows
    with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        count = 0

        for row in reader:
            cursor.execute("""
                INSERT INTO employees (
                    age,
                    attrition,
                    department,
                    job_role,
                    monthly_income,
                    overtime,
                    performance_rating,
                    job_satisfaction,
                    years_at_company,
                    gender,
                    education_field,
                    marital_status,
                    work_life_balance,
                    total_working_years,
                    training_times_last_year,
                    percent_salary_hike,
                    years_since_last_promotion
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                int(row["Age"]),
                row["Attrition"],
                row["Department"],
                row["JobRole"],
                int(row["MonthlyIncome"]),
                row["OverTime"],
                int(row["PerformanceRating"]),
                int(row["JobSatisfaction"]),
                int(row["YearsAtCompany"]),
                row["Gender"],
                row["EducationField"],
                row["MaritalStatus"],
                int(row["WorkLifeBalance"]),
                int(row["TotalWorkingYears"]),
                int(row["TrainingTimesLastYear"]),
                int(row["PercentSalaryHike"]),
                int(row["YearsSinceLastPromotion"])
            ))
            count += 1

    # Step 5 - Commit and close
    conn.commit()
    conn.close()

    print(f"Successfully inserted {count} employee records!")
    print(f"Database saved at: {DB_PATH}")


if __name__ == "__main__":
    # check if CSV exists
    if not os.path.exists(CSV_PATH):
        print(f"CSV file not found at: {CSV_PATH}")
        print("Please place the CSV file in the project folder!")
    else:
        setup_database()

        