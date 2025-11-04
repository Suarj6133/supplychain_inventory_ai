from load_csv import DB_PATH
from llm_agent import get_sql_from_llama
from database import run_sql_query

def process_user_query(user_input:str):
    #step 1 loading user_input into AI
    sql_query = get_sql_from_llama(user_input)
    #step2 passgin output from Ai to blue box
    df_results = run_sql_query(DB_PATH, sql_query)
    return df_results
