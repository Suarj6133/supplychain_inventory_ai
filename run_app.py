#objective to seee the output from AI 
#importing AI function 
from llm_agent import get_sql_from_llama


#defining userinput
user_input = 'What is inventory for SKU-2?'


#output from AI
sql_output = get_sql_from_llama(user_input)

print(sql_output)