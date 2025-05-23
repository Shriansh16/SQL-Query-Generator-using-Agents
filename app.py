from crewai import Agent, Task, Crew, Process
import streamlit as st
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()


# Initialize the LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)

# Streamlit UI
st.title("SQL Query Generator")

with st.form("sql_query_form"):
    natural_language_query = st.text_area("Enter your question (in natural language)")
    submit = st.form_submit_button("Generate SQL Query")

if submit:
    with st.spinner("Generating and validating SQL query..."):

        sql_query_generator = Agent(
            role="SQL Query Generator",
            goal="Convert natural language questions into accurate and optimized SQL queries",
            backstory=(
                "You are an expert in understanding natural language requests and translating them into SQL queries. "
                "The database is a Synapse SQL warehouse with the following tables:\n"
                "1. Profile: contains contactID, name, email, address, age, and other demographics.\n"
                "2. EmailEngagement: contains contactID, clicks, and click_date.\n"
                "3. Orders: contains orderID, contactID, product_name, and order_date.\n"
                "4. LandingWebPages: contains visit data and submissions.\n"
                "Use this schema to write correct and optimized SQL queries."
            ),
            verbose=True,
            llm=llm,
            allow_delegation=False
        )

        sql_query_validator = Agent(
            role="SQL Query Validator",
            goal="Validate and correct an SQL query based on schema and user intent.",
            backstory="You are a SQL syntax and logic expert who ensures all queries work accurately with the given schema in Synapse SQL.",
            verbose=True,
            llm=llm,
            allow_delegation=False
        )

        generate_sql_task = Task(
            description=f"""
You are provided with the following natural language user request:

"{natural_language_query}"

Schema Information:
1. Profile table:
   - contactID (PK), name, email, address, age, and other customizable demographic info.
2. EmailEngagement table:
   - contactID (FK), sends, opens, clicks, click_date.
3. LandingWebPages table:
   - contactID (FK), visit_date, page_name, clicks, form_submissions.
4. Orders table:
   - orderID (PK), contactID (FK), product_name, order_date.

Convert this user request into a valid and complete T-SQL query using Synapse SQL syntax.

Only output the SQL query. Do NOT include any explanation or extra text.
""",
            agent=sql_query_generator,
            expected_output="A single valid SQL query as a string, and nothing else."
        )

        validate_sql_task = Task(
            description=f"""
The following SQL query was generated based on a user's request. Validate and correct it based on the schema.

User Request:
"{natural_language_query}"

Schema Information:
1. Profile table:
   - contactID (PK), name, email, address, age, and other customizable demographic info.
2. EmailEngagement table:
   - contactID (FK), sends, opens, clicks, click_date.
3. LandingWebPages table:
   - contactID (FK), visit_date, page_name, clicks, form_submissions.
4. Orders table:
   - orderID (PK), contactID (FK), product_name, order_date.


Ensure this query is correct and matches the intent. If any issues are found, fix them.

⚠️ Output ONLY the final corrected SQL query. No extra explanation or commentary.
""",
            agent=sql_query_validator,
            expected_output="A final, corrected SQL query string.",
            context=[generate_sql_task]
        )

        crew = Crew(
            agents=[sql_query_generator, sql_query_validator],
            tasks=[generate_sql_task, validate_sql_task],
            verbose=True,
            process=Process.sequential
        )

        result = crew.kickoff()

        # Output the final result
        st.markdown("### Final SQL Query:")
        st.code(result, language='sql')

