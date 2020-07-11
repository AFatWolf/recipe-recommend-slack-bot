from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.core.exceptions import SuspiciousOperation
from django.views.decorators.csrf import csrf_exempt
import urllib
import json

from .models import Student

WEBHOOK_URL = 'https://hooks.slack.com/services/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'
VERIFICATION_TOKEN = 'HtrHxcXNVVbW9QlNwWwRH04Y'
NUM_TEAMS = 7

def index(request):
    teams = []
    for i in range(NUM_TEAMS):
        team = {
            'index' : i + 1,
            'students' : Student.objects.filter(group=i)
        }
        teams.append(team)
    context = {
        'teams': teams
    }
    return render(request, 'team/index.html', context)

def send(request):
    if request.method == 'POST':
        data = {
            'text': request.POST['message']
        }
        postMessage(data)

    return redirect(index)

@csrf_exempt
def join(request):
    if request.method != 'POST':
        return JsonResponse({})
    
    if request.POST.get('token') != VERIFICATION_TOKEN:
        raise SuspiciousOperation('Invalid request.')
    
    user_name = request.POST['user_name']
    user_id = request.POST['user_id']
    text = request.POST['text']

    student = Student(user_name=user_name, user_id=user_id, message=text)
    student.group = Student.objects.all().count() % NUM_TEAMS
    student.save()

    result = {
        'text': '_Hi_ <@{}>! *かっこいい* ~おまえ~.\n\
            Have a drink?\n\
            >This is quoted text\n\
            >This is still quoted text.\n\
            Let\' start `coding` :smile:'.format(user_id),
        'response_type': 'in_channel',
    }
    
    return JsonResponse(result)

def announce(request):
    for i in range(NUM_TEAMS):
        blocks = []
        blocks.append({
            'type': 'section',
            'text' : {
                'type': 'mrkdwn',
                'text': '*Team {}*'.format(i + 1)
            }
        })

        for student in Student.objects.filter(group=i):
            block = {
                'type': 'section',
                'text' : {
                    'type': 'mrkdwn',
                    'text': ':bust_in_silhouette: *{}*\n{}'.format(student.user_name, student.message)
                }
            }
            blocks.append(block)
        blocks.append({
            'type': 'divider'
        })

        data = {
            'blocks': blocks
        }
        postMessage(data)

    Student.objects.all().delete()
    return redirect(index)

def postMessage(data):
    headers = {
        'Content-Type': 'application/json',
    }
    req = urllib.request.Request(WEBHOOK_URL, json.dumps(data).encode(), headers)
    with urllib.request.urlopen(req) as res:
        body = res.read()