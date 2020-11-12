use my_store;
SET SQL_SAFE_UPDATES = 0;


-- Important query to update total in order_products

-- Update order_products o_p
-- inner join products p
-- on p.id = o_p.Product_ID
-- set o_p.total = p.Unit_price * o_p.Amount;


-- Important query to update total_price in orders

-- update orders ord ,
-- (select sum(o_p.total) as total_sum, o_p.Order_ID from  orders ord
-- inner join order_products o_p
-- on ord.id = o_p.Order_ID
-- group by ord.ID) as s
-- SET ord.total_price = s.total_sum
-- WHERE ord.ID = s.Order_ID;


-- Important query to check if total_price in orders and total in order_products are correct

-- select ac.username, ord.id as Order_id,ord.total_price, 
-- o_p.total,  o_p.amount, 
-- p.Unit_price 
-- from accounts ac
-- join orders ord
-- on ac.id = ord.Account_id
-- join order_products o_p
-- on o_p.Order_id = ord.ID
-- join products p
-- on p.id = o_p.Product_ID;


-- Query to check average rating given by all users

-- select username, avg(Rating) as Average_Rating, count(*) as Counter
-- from accounts ac
-- 	join product_ratings pr 
--     on ac.id = pr.Account_ID
--     group by id
--     order by Average_Rating desc, Counter desc;

-- Query to check average rating for products

-- select p.Product_name, avg(Rating) as Average_rating, count(*) as Rating_Counter
-- from products p
-- join product_ratings pr
-- on p.id= pr.Product_id
-- group by product_name
-- order by Average_rating desc, Rating_Counter  desc;

-- Query to check who makes the most orders

-- select username, address, city, count(*) as orders
-- from accounts
-- join account_details
-- using (id)
-- join orders ord
-- on ord.Account_id = accounts.id
-- group by username
-- order by orders desc;

-- Query to check who spends the most on orders in our store

-- select username, address, city, ROUND(sum(total_price),2) as Total_spending
-- from accounts
-- join account_details
-- using (id)
-- join orders ord
-- on ord.Account_id = accounts.id
-- group by username
-- order by Total_spending desc;


-- Query to check which city spends the most money

-- select city, ROUND(sum(total_price),2) as Total_spending
-- from accounts
-- join account_details
-- using (id)
-- join orders ord
-- on ord.Account_id = accounts.id
-- group by city
-- order by Total_spending desc;

-- Query to check which user orders the most products

-- select username, sum(o_p.amount) as products_amount, ROUND(sum(total_price),2) as total
-- from accounts ac
-- join orders ord
-- on ord.account_id = ac.id
-- join order_products o_p
-- on o_p.Order_id = ord.id
-- group by username
-- order by products_amount desc;

-- Query to check what product sold best in July 2020 and generated most value for store

-- select pr.id, pr.product_name, sum(o_p.amount) as sold, round(sum(o_p.total),2) as Money_made 
-- from orders ord
-- join order_products o_p
-- on ord.id = o_p.Order_id
-- join products pr
-- on o_p.Product_id = pr.id
-- where order_date >= "2020-07-01" and order_date <="2020-07-31"
-- group by pr.product_name
-- order by sold desc,Money_made desc;


-- query to check which users didn't make orders

-- select username, ord.id as order_id
-- from accounts ac
-- left join orders ord 
-- on ord.account_id = ac.id
-- where ord.id is null;


-- query to check what products didn't sell at all

-- select product_name, order_id
-- from products pr 
-- left join order_products o_p
-- on pr.id = o_p.Order_ID
-- where order_id is null;











