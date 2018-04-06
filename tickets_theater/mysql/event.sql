#set global event_scheduler = ON;
#show variables like 'event_scheduler'
 
CREATE EVENT `eventDelete`
ON SCHEDULE
      EVERY 1 MONTH
      ON COMPLETION PRESERVE
    DO
      DELETE FROM ticket_sales WHERE date<CURDATE()
