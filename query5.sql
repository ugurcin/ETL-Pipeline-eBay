WITH Seller(id) AS (SELECT DISTINCT seller_id FROM Item)
SELECT Count(*)
FROM Seller, Member
WHERE Seller.id = Member.user_id
AND Member.rating > 1000;