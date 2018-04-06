
delimiter //
CREATE PROCEDURE findmaxprice (OUT price INT)
BEGIN
SELECT max(price) INTO price 
FROM ticket_type;
END;
//


#CALL findmaxprice (@price);
SELECT @price as maxprice;
