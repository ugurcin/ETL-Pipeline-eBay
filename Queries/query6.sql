WITH Seller(id) AS (SELECT DISTINCT seller_id FROM Item)
SELECT Count(Seller.id)
FROM Seller
WHERE Seller.id IN (SELECT bidder_id FROM Bid);