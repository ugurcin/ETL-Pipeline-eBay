SELECT Count(DISTINCT ItemCategory.category_name)
FROM Item, ItemCategory
WHERE Item.item_id = ItemCategory.item_id AND Item.number_of_bids > 0 AND Item.currently > 100;