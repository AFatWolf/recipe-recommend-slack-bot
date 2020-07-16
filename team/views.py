from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.core.exceptions import SuspiciousOperation
from django.views.decorators.csrf import csrf_exempt
import urllib
import json
#HIEU AND HAI
from .command_info import *
from .command_info import list_of_commands_name
from .command_info import commands
#HIEU AND HAI
from .models import Student

#Hieu changes to webhooks and token of Team task
WEBHOOK_URL = 'https://hooks.slack.com/services/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'
VERIFICATION_TOKEN = 'StcVP7qHCrkoleAzGlSJs2ho'
NUM_TEAMS = 7
#HIEU AND HAI help function-----
@csrf_exempt
def team_help (request):
    if request.method != 'POST':
        return JsonResponse({})
    
    if request.POST.get('token') != VERIFICATION_TOKEN:
        raise SuspiciousOperation('Invalid request.')
    user_name = request.POST['user_name']
    user_id = request.POST['user_id']
    text = request.POST['text']
    if (text ==''):
        cmd_lists =''
        for cmd in list_of_commands_name :
            cmd_lists+= '   •`'+cmd+'`\n'

        result = {
            'text': ('Hi, <@{}>! Here are the commands that you can try: \n'+ cmd_lists+'Typle `/team_help command` for help about the command.').format(user_id),
            'response_type': 'in_channel'
        }
    elif (text in list_of_commands_name):
        output = commands[text].formatted_info()
        result = {
            'text': output,
            'response_type': 'in_channel'
        }
    else:
        result = {
            'text': ('There are no such command. Here are the commands that you can try: \n'+ cmd_lists+'Typle `\help(command`) for help about the command)'),
            'response_type': 'in_channel'
        }   
    return JsonResponse(result)
#end help function HIEU AND HAI 
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