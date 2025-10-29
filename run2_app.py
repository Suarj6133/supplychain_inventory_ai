#objective to seee the output from AI 
#importing AI function 
from llm_agent import get_sql_from_llama
from database import run_sql_query
from load_csv import DB_PATH


#defining userinput
user_input = 'What is inventory for SKU-2?'


#output from AI
sql_output = get_sql_from_llama(user_input)

print(sql_output)

df_results = run_sql_query(DB_PATH,sql_output)
print (df_results)