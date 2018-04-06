DROP TRIGGER `update`
DELIMITER |
CREATE TRIGGER `update` before update ON `ticket_sales` 
FOR EACH ROW BEGIN
IF((SELECT idswitch_trigger FROM switch_trigger) = 1)
THEN
  IF(NEW.date< CURDATE()) then 
  SET NEW.binocular = OLD.binocular; 
  SET NEW.row = OLD.row; 
  SET NEW.sit = OLD.sit; 
  SET NEW.idticket_type = OLD.idticket_type; 
  SET NEW.idvisitor = OLD.idvisitor;
  SET NEW.idticket_type = OLD.idticket_type; 
  SET NEW.idperformance = OLD.idperformance; 
  END IF;
END IF;
END;
