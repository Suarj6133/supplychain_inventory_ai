def build_prompt(user_input: str) -> str:
    return f"""

The data is stored in a SQLite database with one table. The data is about a grocery shops with different SKUs  with other details.

Table1: report
Below are the column lables in the report with meaning:
-`SKU`: Unique Id of each of the items that is being sold in the store (eg: SKU-1 to be already read together)
-`Inventory`: Current stock available / quality available in the shop
-`daily_order_qty`: this is expected sales quantity for each day of the SKU
-`expiry_data`: This is the expiry beyond which the SKUs is of no use
-`unit_price`: This is unit cost for each of the SKUs


Use only valid SQLite syntax
---

#Special Instructions:
-Always treat values in the 'SKU' columns as exact string matches. Do not split them or apply partial matching unless explicity asked.

- If the user asks for **SKU range**, use:  
  `SELECT DISTINCT(SKU) FROM report;`

- If the user asks for **What is inventory for SKU-2**, return:
    `Select Inventory from report where SKU = 'SKU-2'




---
Write the correct SQLite query for:

Question: {user_input}

Return only the valid SQLite query. Do not prefix or explain anything. Do not say 'Here is the query:' or any other sentence. Just start from SELECT or PRAGMA.
"""