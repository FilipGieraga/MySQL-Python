# MySQL-Python Database

This program creates sql database from scratch. It has a schema shown below and allows you to generate data for all tables.
![alt tag](https://github.com/FilipGieraga/MySQL-Python/blob/main/schema.png)
Python script is responsible for creating ficticious data which can then be executed in mysql workbench program.
Script has a class called Dataset and this class gives us the ability to specify how many users, orders, products and so on we want to have in our database.
In order for this script to work correctly we need to run methods of this class in correct order, for example program needs to know the ids of products
we have in our database in order to create valid data for order_products table or product_ratings table.
If we want to make whole dataset for our schema here is the best order to run methods for an instance of our class:<br>
1 create_accounts ---> 2 create_account_details ---> 3 create_orders ---> <br>
4 create_products ---> 5 create order_products ---> 6 create_product_ratings<br>
All those methods, except create_account_details take 1 parameter which is number of rows for each table. Only create_account_details
doesn't take any parameters, because all accounts we created will have details assigned to them.
Once this process is done, insert_data.sql file is generated and we can move on to sql workbench.
The order of running the files is simple:<br>
Firstly we create a schema with my_store_schema.sql file, once it's done we can execute insert_data.sql file to insert our data.
Lastly we can move on to query_data.sql and this script allows us to get some informations about our store.
First two queries update two values (total in order_products & total_price in orders) because defaultly those are set to null.
Then we can get some information like:
- average rating given by all users
- average rating of individual products
- which user makes the most orders
- who spends the most on orders in our store
- which city spends the most money
- which user orders the most products
- which users didn't make orders
- what products didn't sell at all
- what product sold best in one month and generated most money for a store
