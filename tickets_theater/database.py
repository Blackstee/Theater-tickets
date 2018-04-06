import MySQLdb as mdb
import sys
import uuid
import json
import os
from tickets_theater.models import Visitor
from tickets_theater.models import Performance
from tickets_theater.models import Ticket_sales
from tickets_theater.models import Place


class Database:

    def __init__(self):
        self.con = mdb.connect('localhost', 'root', 'password', 'theater_db')




    def generate_id(self):
        id = uuid.uuid1().int >> 115
        if (Visitor.objects.filter(idvisitor = id).exists() or Place.objects.filter(idplace = id).exists() or Performance.objects.filter(idperformance= id).exists()):
            return self.generate_id()
        return id


    #TICKETS=====================


    def selectTickets(self):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM ticket_sales;")
        return cur.fetchall()

    def selectTicketbyID(self, id):
        cur = self.con.cursor()
        com = "SELECT * FROM ticket_sales WHERE idticket_sales = %s;"
        cur.execute(com, (id,))
        return cur.fetchall()

    def addTicket(self, data):
        cur = self.con.cursor()
        try:
            id = self.generate_id()
            if data['binoc'] == 'True':
                bin = 1
            else:
                bin = 0
            print (data)
            mysql = ("INSERT INTO ticket_sales (idticket_sales, date, binocular, row, sit, idperformance, idticket_type) VALUES(%s, %s, %s, %s, %s, %s, %s)")
            cur.execute(mysql, (id, data['date'], bin, data['row'], data['sit'], int(data['performance']), int(data['type'])))
        except:
            return self.addTicket()
        else:
            self.con.commit()

    def deleteTicket(self, id):
        cur = self.con.cursor()
        delstatmt = "DELETE FROM ticket_sales WHERE idticket_sales = %s;"
        cur.execute(delstatmt, (id,))
        self.con.commit()

    def updateTicket(self, data):
        id = data ['update']
        cur = self.con.cursor()
        if data['binoc'] == 'True':
            bin = 1
        else:
            bin = 0
        com = "UPDATE ticket_sales SET date = %s, binocular = %s, row = %s, sit = %s, idperformance = %s, idticket_type = %s WHERE idticket_sales = %s;"
        cur.execute(com, (data['date'], bin, data['row'], data['sit'], int(data['performance']), int(data['type']), id))
        self.con.commit()


    #PERFORMANCES================

    def addPerformance(self, data):
        cur = self.con.cursor()
        try:
            id = self.generate_id()
            mysql = ("INSERT INTO performance (idperformance, name, style, actors, author) VALUES (%s, %s, %s, %s, %s);")
            cur.execute(mysql, (id, data['name'], data['style'],  data['actors'],  data['author']))
        except:
            return self.addPerformance(data)
        else:
            self.con.commit()

    def selectPerformances(self):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM performance;")
        return cur.fetchall()


    #ACTORS=====================

    def addActor(self, data):
        cur = self.con.cursor()
        try:
            id = self.generate_id()
            if data['sex'] == 'man':
                sex = 1
            else:
                sex = 0
            mysql = ("INSERT INTO actor (idactor, name, surname, age, sex) VALUES (%s, %s, %s, %s, %s);")
            cur.execute(mysql, (id, data['name'], data['surname'], int(data['age']), sex))
        except:
            return self.addActor(data)
        else:
            self.con.commit()


    #VISITORS===================

    def addVisitor(self, data):
        cur = self.con.cursor()
        try:
            id = self.generate_id()
            if data['category'] == 'adult':
                category = 1
            else:
                category = 0
            print(data)
            mysql = ("INSERT INTO visitor (idvisitor, name, surname, category_vis) VALUES (%s, %s, %s, %s);")
            cur.execute(mysql, (id, data['name'], data['surname'], category))

        except:
            return self.addVisitor(data)
        else:
            self.con.commit()


    #TICKET_TYPES===============

    def addTicket_Type(self, data):
        cur = self.con.cursor()
        try:
            id = self.generate_id()
            mysql = ("INSERT INTO ticket_type (idticket_type, sector, price) VALUES (%s, %s, %s);")
            cur.execute(mysql, (id, int(data['sector']), int(data['price'])))
        except:
            return self.addTicket_Type(data)
        else:
            self.con.commit()

    def selectTicket_Type(self):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM ticket_type;")
        return cur.fetchall()


    #SEARCH=====================

    def search (self, data):
        cur = self.con.cursor()
        if data['way'] == 'datebetween':
            search = "SELECT * FROM ticket_sales WHERE DATE BETWEEN %s AND %s;"
            cur.execute(search, (data['date1'], data['date2']))
        if data['way'] == 'binocular':
            if data['binoc'] == 'yes':
                bin = 1
            else:
                bin = 0
            search = "SELECT * FROM ticket_sales WHERE binocular = %s;"
            cur.execute(search, (bin,))
        if data['way'] == 'notmatch':
            search = "SELECT * FROM ticket_sales WHERE NOT MATCH (%s, %s) AGAINST (%s IN BOOLEAN MODE);"
            cur.execute(search, ('date', 'row', data['wordin']))
        if data['way'] == 'match':
            word = "+" + data['wordin']
            search = "SELECT * FROM ticket_sales WHERE idperformance in (SELECT idperformance FROM performance WHERE MATCH (name, actors) AGAINST (%s IN BOOLEAN MODE));"
            cur.execute(search, (word,))
        return cur.fetchall()

    #UPDATE FROM JSON===========

    def update(self):
        script_dir = os.path.dirname(__file__)
        actors = os.path.join(script_dir, 'static/tickets_theater/actors.json')
        visitors = os.path.join(script_dir, 'static/tickets_theater/visitors.json')
        performances = os.path.join(script_dir, 'static/tickets_theater/perf.json')
        places = os.path.join(script_dir, 'static/tickets_theater/places.json')
        cur = self.con.cursor()
        cur.execute("DELETE FROM tickets_theater_ticket_sales;")
        cur.execute("ALTER TABLE tickets_theater_ticket_sales AUTO_INCREMENT = 1;")
        cur.execute("DELETE FROM tickets_theater_visitor;")
        cur.execute("ALTER TABLE tickets_theater_visitor AUTO_INCREMENT = 1;")
        cur.execute("DELETE FROM tickets_theater_performance;")
        cur.execute("ALTER TABLE tickets_theater_performance AUTO_INCREMENT = 1;")
        cur.execute("DELETE FROM tickets_theater_place;")
        cur.execute("ALTER TABLE tickets_theater_place AUTO_INCREMENT = 1;")
        self.con.commit()


        visitorsdata = open(visitors, 'r')
        data = json.load(visitorsdata)
        for i in data['visitors']['visitor']:
            id = self.generate_id()
            Visitor.objects.create(idvisitor=id, name=i['name'], surname=i['surname'], category_vis=int(i['category']))
        visitorsdata.close()

        performancesdata = open(performances, 'r')
        data = json.load(performancesdata)
        for i in data['performances']['performance']:
            id = self.generate_id()
            Performance.objects.create(idperformance=id, name=i['name'], style=i['style'], actors=i['actors'],
                                 author=i['author'])
        performancesdata.close()

        placesdata = open(places, 'r')
        data = json.load(placesdata)
        for i in data['places']['place']:
            id = self.generate_id()
            Place.objects.create(idplace=id, country=i['country'], city=i['city'], address=i['address'], category_pl=int(i['category_pl']))
        placesdata.close()




    def close(self):
        self.con.close()

