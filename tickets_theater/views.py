# -*- coding: utf-8 -*-
import uuid

from django.shortcuts import render_to_response
from django.template.context_processors import csrf
from django.template.loader import get_template
from django.template import Context, RequestContext, context
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from tickets_theater.database import Database
import datetime
from tickets_theater.models import Visitor
from tickets_theater.models import Performance
from tickets_theater.models import Ticket_sales
from tickets_theater.models import Place
from django.shortcuts import redirect


def generate_id():
    id = uuid.uuid1().int >> 115
    return id

@csrf_exempt
def tickets(request):
    db = Database()

    if request.method == 'POST':
        if (len(request.POST) > 2):
            if request.POST['binoc'] == 'True':
                bin = 1
            else:
                bin = 0
            idperf = Performance.objects.get(idperformance=request.POST['performance'])
            idplace = Place.objects.get(idplace=request.POST['type'])
            idvis = Visitor.objects.get(name='Freddy', surname = "Bond")
            id=generate_id()

            Ticket_sales.objects.create(idticket_sales=id, date=request.POST['date'] , binocular=bin, row=request.POST['row'], sit=request.POST['sit'], idperformance=idperf, idplace=idplace, idvisitor=idvis)
            template = get_template('date.html')
            context = {"db": Ticket_sales.objects.all(), "dbper": Performance.objects.all(), "dbtype": Place.objects.all(), "data": 1, "id": -5}
            return HttpResponse(template.render(context, request))
        elif (request.POST['action']=='refresh'):
            template = get_template('date.html')
            db.update()
            context = {"db": Ticket_sales.objects.all(),  "dbper": Performance.objects.all(), "dbtype": Place.objects.all(), "data": 1, "id": -5}
            return HttpResponse(template.render(context, request))

        else:
            obj = Ticket_sales.objects.filter(idticket_sales=request.POST['action'])
            print(obj[0].date)
            obj[0].delete()
            template = get_template('date.html')
            context = {"db": Ticket_sales.objects.all(),  "dbper": Performance.objects.all(), "dbtype": Place.objects.all(), "data": 1, "id": -5}
            return HttpResponse(template.render(context, request))


    if request.method == 'GET':
        template = get_template('date.html')
        context = {"db": Ticket_sales.objects.all(), "dbper": Performance.objects.all(), "dbtype": Place.objects.all(), "data": 1, "id": -5}
        return HttpResponse(template.render(context, request))




def performances(request):
    db = Database()
    if request.method == 'GET':
        template = get_template('date.html')
        context = {"db": Performance.objects.all(), "dbper": Performance.objects.all(), "dbtype": Place.objects.all(), "data": 0, "id": -5}
        return HttpResponse(template.render(context, request))


def search (request):
    db = Database()

    if request.method == 'GET':
        template = get_template('date.html')
        context = {"db": Ticket_sales.objects.all(), "dbper": Performance.objects.all(), "dbtype": Place.objects.all(), "data":2, "id": -5}
        return HttpResponse(template.render(context, request))
    if request.method == 'POST':
        if (len(request.POST) > 2):
            template = get_template('date.html')
            context = {"db": db.search(request.POST), "dbper": Performance.objects.all(), "dbtype": Place.objects.all(), "data": 2, "id": -5}
            return HttpResponse(template.render(context, request))
        else:
            db.deleteTicket(request.POST['action'])
            template = get_template('date.html')
            context = {"db": Ticket_sales.objects.all(), "dbper": Performance.objects.all(), "dbtype": Place.objects.all(),  "data": 2, "id": -5}
            return HttpResponse(template.render(context, request))


@csrf_exempt
def eachticket(request, id):
    db = Database()

    if request.method == 'POST':
        if (request.POST['action']=='update'):
            if request.POST['binoc'] == 'True':
                bin = 1
            else:
                bin = 0
            idperf = Performance.objects.get(idperformance=request.POST['performance'])
            idplace = Place.objects.get(idplace=request.POST['type'])
            idvis = Visitor.objects.get(name='Freddy', surname = "Bond")

            Ticket_sales.objects.filter(idticket_sales=id).update(idticket_sales=id, date=request.POST['date'], binocular=bin,
                                        row=request.POST['row'], sit=request.POST['sit'], idperformance=idperf,
                                        idplace=idplace, idvisitor=idvis)
            return redirect(tickets)
        else:
            obj = Ticket_sales.objects.filter(idticket_sales=id)
            obj[0].delete()
            return redirect(tickets)
    if request.method == 'GET':
        template = get_template('date.html')
        context = {"db": Ticket_sales.objects.filter(idticket_sales=id), "dbper": Performance.objects.all(), "dbtype": Place.objects.all(), "data": 1, "id": id}
        return HttpResponse(template.render(context, request))

