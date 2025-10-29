from flask import Flask, request, jsonify
from llm_agent import get_sql_from_llama
from database import run_sql_query
from load_csv import DB_PATH
import pandas as pd

app = Flask(__name__)

@app.route('/api/query', methods=['POST'])
def handle_query():
    """
    Receives user query from the Telegram bot, orchestrates the LLM to generate SQL, 
    executes the SQL against the local database, and returns a formatted result.
    """
    data = request.get_json()
    user_query = data.get("query")

    if not user_query:
        return jsonify({"answer": "Error: No query provided."}), 400

    try:
        # 1. GENERATE SQL: Ask the LLM agent for the SQL query
        sql_query = get_sql_from_llama(user_query)
        
        # Log for debugging 
        print(f"[API] User Query: {user_query}")
        print(f"[API] Generated SQL: {sql_query.strip()}")

        # 2. EXECUTE SQL: Run the generated query against the SQLite database
        df_results = run_sql_query(DB_PATH, sql_query)
        
        # 3. FORMAT ANSWER: Convert the DataFrame results into a user-friendly string
        if df_results is None:
             # This happens if a PRAGMA query was run successfully
             answer = "Metadata query successful. Check database for structure update (e.g., column names)."
        elif df_results.empty:
            answer = "The query ran successfully, but no matching items were found in the database."
        else:
            # Use markdown table for clean output in Telegram
            answer = f"✅ Query Results:\n\n{df_results.to_markdown(index=False)}"

        return jsonify({"answer": answer})

    except RuntimeError as e:
        print(f"Runtime Error: {e}")
        # Return the error message to the bot
        return jsonify({"answer": f"❌ Error processing request: {str(e)}"}), 500
    except Exception as e:
        print(f"Unhandled Error: {e}")
        return jsonify({"answer": f"❌ An unexpected error occurred in the backend."}), 500

if __name__ == '__main__':
    # Flask will run on http://127.0.0.1:5000/
    # use_reloader=False prevents double execution of the LLM agent on startup
    app.run(debug=True, port=5000, use_reloader=False)