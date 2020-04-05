from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import Http404
import requests

from .models import Question, Choice


def index(request):
    direccion = 'https://rickandmortyapi.com/api/episode/'
    response = requests.get(url=direccion)
    information = response.json()
    direccion2 = 'https://rickandmortyapi.com/api/episode?page=2'
    response2 = requests.get(url=direccion2)
    information['results2'] = response2.json()
    return render(request, 'rick/index.html', information)


def detail(request, item_id):
    direccion = 'https://rickandmortyapi.com/api/episode/' + str(item_id)
    response = requests.get(url=direccion)
    information = response.json()
    personajes = []
    for personaje in information['characters']:
        direc = personaje
        resp = requests.get(url=direc)
        info = resp.json()
        personajes.append(info)
    information['item_id'] = item_id
    information['personajes'] = personajes
    return render(request, 'rick/detail.html', information)


def character(request, character_id):
    direccion = 'https://rickandmortyapi.com/api/character/' + str(character_id)
    response = requests.get(url=direccion)
    information = response.json()
    information['character_id'] = character_id
    episodios = []
    for episodio in information['episode']:
        direc = episodio
        resp = requests.get(url=direc)
        info = resp.json()
        episodios.append(info)
    information['episodios'] = episodios
    resp2 = requests.get(url=information['origin']['url'])
    origin = resp2.json()
    information['origin2'] = origin
    resp3 = requests.get(url=information['location']['url'])
    location = resp3.json()
    information['location2'] = location
    return render(request, 'rick/character.html', information)


def location(request, location_id):
    direccion = 'https://rickandmortyapi.com/api/location/' + str(location_id)
    response = requests.get(url=direccion)
    information = response.json()
    information['location_id'] = location_id
    personajes = []
    for personaje in information['residents']:
        direc = personaje
        resp = requests.get(url=direc)
        info = resp.json()
        personajes.append(info)
    information['personajes'] = personajes
    return render(request, 'rick/location.html', information)


def search(request):
    entry = str(request.GET["name"]).lower()
    information = {}

    direccion1 = 'https://rickandmortyapi.com/api/episode/'
    response1 = requests.get(url=direccion1)
    information1 = response1.json()
    direccion2 = 'https://rickandmortyapi.com/api/episode?page=2'
    response2 = requests.get(url=direccion2)
    information2 = response2.json()
    episodios = []
    for episodio in information1['results']:
        if episodio['name'].lower().find(entry) != -1:
            episodios.append(episodio)
    for episodio in information2['results']:
        if episodio['name'].lower().find(entry) != -1:
            episodios.append(episodio)
    information['episodios'] = episodios

    direccion3 = 'https://rickandmortyapi.com/api/character/'
    response3 = requests.get(url=direccion3)
    information3 = response3.json()
    personajes = []
    for personaje in information3['results']:
        if personaje['name'].lower().find(entry) != -1:
            personajes.append(personaje)
    vacio = information3['info']['next']
    while vacio:
        direc = vacio
        resp = requests.get(url=direc)
        info = resp.json()
        for personaje in info['results']:
            if personaje['name'].lower().find(entry) != -1:
                personajes.append(personaje)
        vacio = info['info']['next']
    information['personajes'] = personajes

    direccion4 = 'https://rickandmortyapi.com/api/location/'
    response4 = requests.get(url=direccion4)
    information4 = response4.json()
    lugares = []
    for lugar in information4['results']:
        if lugar['name'].lower().find(entry) != -1:
            lugares.append(lugar)
    vacio = information4['info']['next']
    while vacio:
        direc = vacio
        resp = requests.get(url=direc)
        info = resp.json()
        for lugar in info['results']:
            if lugar['name'].lower().find(entry) != -1:
                lugares.append(lugar)
        vacio = info['info']['next']
    information['lugares'] = lugares

    return render(request, 'rick/search.html', information)


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'rick/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'rick/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('rick:results', args=(question.id,)))

