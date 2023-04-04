WITH ItemBelongs(item_id, number_of_categories) AS (SELECT Item.item_id, Count(DISTINCT ItemCategory.category_name) AS the_number
FROM Item, ItemCategory
WHERE Item.item_id = ItemCategory.item_id
GROUP BY Item.item_id)
SELECT Count(item_id)
FROM ItemBelongs
WHERE number_of_categories = 4;