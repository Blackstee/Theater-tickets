

#Потерянное обновление
start transaction; #4
update ticket_sales set row = row + 5; #5
SELECT * FROM theater_db.ticket_sales; #6
commit; #8

#«Грязное» чтение
start transaction; #1
select * from ticket_sales where sit>2; #4
commit; #6

#Неповторяющееся чтение
start transaction; #1
select * from ticket_sales where sit>2; #2
select * from ticket_sales where sit>2; #6
commit; #7

#Фантомное чтение
start transaction; #1
select date from ticket_sales; #2
select date from ticket_sales; #6
commit; #7

