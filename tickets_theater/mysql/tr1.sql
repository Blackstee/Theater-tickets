#SET SQL_SAFE_UPDATES=0;

#Потерянное обновление
start transaction; #1
update ticket_sales set  row = row + 1; #2
SELECT * FROM theater_db.ticket_sales; #3
commit; #7
SELECT * FROM theater_db.ticket_sales; #9

#«Грязное» чтение
start transaction; #2
update ticket_sales set row = row + 2 where sit>2;  #3
rollback; # 5
#commit;

#Неповторяющееся чтение
start transaction; #3 
update ticket_sales set row = row + 2 where sit>2; #4
commit; #5

#Фантомное чтение
start transaction; #3
insert into ticket_sales values(3456, '2017-11-02 12:12:00', 0, 5, 5, 6438, 6442, 6445); #4
commit; #5