from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from .models import Challenge
from .forms import ChallengeForm
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
import datetime
import json

def showChallenges(request):
    challenges = Challenge.objects.all() # na stronie chcemy wyswietlic wszystkie obiekty tabeli Challenge, wiec zapisujemy to do zmiennej
    if request.method == 'POST':        
        form = ChallengeForm(request.POST) # jezeli zostal wyslany formularz (czyli request HTTP POST) to tworzymy obiekt formularza z wpisanymi danymi
        if form.is_valid(): # sprawdzamy poprawnosc wpisanych danych
            form.save() # zapisujemy obiekt o danych przeslanych w formularzu do bazy danych
            return HttpResponseRedirect('/') # dobra praktyka: przeladowujemy strone, aby po wcisnieciu F5 nie zostaly znowu wyslane dane, a pokazal sie ekran koncowy formularza (tutaj: zwykla strona)
    else:
        form = ChallengeForm() # request HTTP GET, czyli nie zostal wyslany formularz - tworzymy obiekt niewypelnionego formularza
    return render(request, 'challenges/challenges.html', locals()) # bierzemy nasz request i slownik zmiennych lokalnych (w sumie interesuje nas aby mial klucze 'challenge' i 'form') i przesylamy go do szablonu HTML do przetworzenia i wyslania userowi

def ajaxIncrement(request):
    challenge = get_object_or_404(Challenge, pk=request.GET['id'])
    challenge.counter = min(challenge.counter + 1, challenge.days)
    challenge.save()
    res = {"counter": challenge.counter, "fraction": challenge.fraction()}
    return HttpResponse(json.dumps(res), content_type='application/json')

@csrf_protect
def ajaxSaveChallenge(request):
    challenge = get_object_or_404(Challenge, pk=request.POST['id'])
    challenge.name = request.POST['name']
    challenge.counter = request.POST['counter']
    challenge.days = request.POST['days'] 
    challenge.begin = datetime.datetime.strptime(request.POST['begin'], '%Y-%m-%d').date()
    version = request.POST.get('ver')
    if str(challenge.version) == version:
        challenge.version += 1
    challenge.description = request.POST['description']
    challenge.save()
    return HttpResponse('0')

@csrf_protect
def ajaxDeleteChallenge(request):
	challenge = get_object_or_404(Challenge, pk=request.POST['id'])
	challenge.delete()
	return HttpResponse('0')

def ajaxGetChallenge(request):
    challenge = get_object_or_404(Challenge, pk=request.POST['id'])
    data = {
        'name': challenge.name, 
        'description': challenge.description, 
        'days': challenge.days, 
        'counter': challenge.counter,
        'ver': challenge.version,
        'begin': challenge.beginStr()
    }

    return HttpResponse(json.dumps(data))

def ajaxGetData(request):
    challenge = get_object_or_404(Challenge, pk=request.GET['id'])
    res = {"fraction": challenge.fraction()}
    res = {"begin": challenge.beginStr()}

    return HttpResponse(json.dumps(res), content_type='application/json')

