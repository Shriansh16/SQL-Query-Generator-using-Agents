# SQL Query Generator with CrewAI and Streamlit

This project is a web application built with Streamlit that converts natural language questions into valid, optimized SQL queries targeting a Synapse SQL data warehouse. It leverages **CrewAI** to orchestrate intelligent agents for query generation and validation, powered by a GPT-4o-mini model via **LangChain's** OpenAI integration.

---

## Features

- Convert plain English questions into SQL queries based on a predefined database schema.
- Validate and correct the generated SQL queries to ensure syntactic and semantic correctness.
- Uses a two-agent system:
  - **SQL Query Generator**: Translates user requests into SQL.
  - **SQL Query Validator**: Checks and corrects the generated SQL query.
- Interactive UI via Streamlit for easy input and result display.
- Supports Synapse SQL syntax and respects the database schema.

---

## Database Schema

The SQL queries are generated based on the following schema in a Synapse SQL warehouse:

1. **Profile**
   - `contactID` (Primary Key)
   - `name`
   - `email`
   - `address`
   - `age`
   - Other demographic fields

2. **EmailEngagement**
   - `contactID` (Foreign Key)
   - `sends`
   - `opens`
   - `clicks`
   - `click_date`

3. **LandingWebPages**
   - `contactID` (Foreign Key)
   - `visit_date`
   - `page_name`
   - `clicks`
   - `form_submissions`

4. **Orders**
   - `orderID` (Primary Key)
   - `contactID` (Foreign Key)
   - `product_name`
   - `order_date`

---