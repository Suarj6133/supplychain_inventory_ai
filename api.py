from flask import Flask, request, jsonify
from query import process_user_query
import pandas as pd

app = Flask(__name__)

@app.route('/api/query', methods=['POST'])
def handle_query():
    """
    API endpoint that:
    - Accepts a JSON payload: {"query": "user question"}
    - Uses the LLM + SQL engine to get results
    - Returns a formatted text response
    """
    data = request.get_json()
    user_query = data.get("query")

    if not user_query:
        return jsonify({"answer": "❌ No query provided."}), 400

    try:
        # Run the query pipeline (AI → SQL → DB)
        df_results = process_user_query(user_query)

        # Format the response
        if df_results is None:
            answer = "ℹ️ Metadata query executed successfully."
        elif df_results.empty:
            answer = "⚠️ No matching records found."
        else:
            # Nicely formatted table
            answer = f"✅ Query Results:\n\n{df_results.to_string(index=False)}"

        return jsonify({"answer": answer})

    except Exception as e:
        print(f"[API] Error: {e}")
        return jsonify({"answer": f"❌ Error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000, use_reloader=False)
