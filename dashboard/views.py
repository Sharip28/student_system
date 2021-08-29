from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import *
from django.views import generic
import requests
import wikipedia


# Create your views here.
from .models import *

from youtubesearchpython import VideosSearch


def home(request):
    return render(request, 'home.html')


def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()
        messages.success(request, f'Notes added by {request.user.username} successfully!')
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {'notes': notes, 'form': form}
    return render(request, 'notes.html', context)


def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect('notes')


class NotesDetailView(generic.DetailView):
    model = Notes
    template_name = 'notes_detail.html'


def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = HomeWork(
                user=request.user,
                subject=request.POST['subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                due=request.POST['due'],
                is_finished=finished
            )
            homeworks.save()
            messages.success(request, f'Homework added from {request.user.username} !')
    else:
        form = HomeworkForm()
    homework = HomeWork.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {'homeworks': homework,
               'homeworks_done': homework_done,
               'form': form}
    return render(request, 'homework.html', context)


def update_homework(request, pk=None):
    homework = HomeWork.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')


def delete_homework(request, pk=None):
    HomeWork.objects.get(id=pk).delete()
    return redirect('homework')


def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']

        try:
            video = VideosSearch(text, limit=10)
            result_list = []
            for i in video.result()['result']:
                result_dict = {
                    'input': text,
                    'title': i['title'],
                    'duration': i['duration'],
                    'thumbnail': i['thumbnails'][0]['url'],
                    'channel': i['channel']['name'],
                    'link': i['link'],
                    'views': i['viewCount']['short'],
                    'published': i['publishedTime'],
                }
                desc = ''
                if i['descriptionSnippet']:
                    for j in i['descriptionSnippet']:
                        desc += j['text']
                result_dict['description'] = desc
                result_list.append(result_dict)
                context = {
                    'form': form,
                    'results': result_list
                }
                return render(request, 'youtube.html', context)

        except:
            context = {
                'form': form,
                'results': ''
            }
            return render(request, 'youtube.html', context)
    else:
        form = DashboardForm()
    context = {'form': form}
    return render(request, 'youtube.html', context)


def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(
                user=request.user,
                title=request.POST['title'],
                is_finished=finished
            )
            todos.save()
            messages.success(request, f'Todo added from {request.user.username}!')
    else:
        form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False

    context = {
        'todos': todo,
        'form': form,
        'todos_done': todos_done
    }
    return render(request, 'todo.html', context)


def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')


def delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')


def books(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = 'https://www.googleapis.com/books/v1/volumes?q=' + text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title': answer['items'][i]['volumeInfo']['title'],
                'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                'description': answer['items'][i]['volumeInfo'].get('description'),
                'categories': answer['items'][i]['volumeInfo'].get('categories'),
                'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview': answer['items'][i]['volumeInfo'].get('previewLink'),
                'rating': answer['items'][i]['volumeInfo'].get('pageRating'),
                'count': answer['items'][i]['volumeInfo'].get('pageCount')

            }

            result_list.append(result_dict)
            context = {
                'form': form,
                'results': result_list
            }

        return render(request, 'books.html', context)
    else:
        form = DashboardForm()
    context = {'form': form}
    return render(request, 'books.html', context)


def dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = 'https://api.dictionaryapi.dev/api/v2/entries/en_US/' + text
        r = requests.get(url)
        answer = r.json()
        print(answer)
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form': form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                'example': example,
                'synonyms': synonyms
            }
        except:
            context = {
                'form': form,
                'input': ''

            }
        return render(request, 'dictionary.html', context)
    else:
        form = DashboardForm()
        context = {
            'form': form
        }
    return render(request, 'dictionary.html', context)


def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)
        try:
            search = wikipedia.page(text)
            context = {
                'form': form,
                'title': search.title,
                'link': search.url,
                'details': search.summary
            }
        except:
            context = {
                'form': form,
                'title': ''

            }
        return render(request, 'wiki.html', context)
    else:

        form = DashboardForm()
        context = {
            'form': form
        }
    return render(request, 'wiki.html', context)


def conversion(request):
    if request.method == 'POST':
        form = ConversionForm()
        if request.POST['measurement'] == 'length':
            measurement_form = ConversionLengthForm()
            context = {
                'form': form,
                'm_form': measurement_form,
                'input': True

            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >=0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} yard = {int(input)*3} foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} foot = {(int(input)/3)} yard'
                context = {
                    'form': form,
                    'm_form': measurement_form,
                    'input': True,
                    'answer': answer
                }
        if request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm()
            context = {
                'form': form,
                'm_form': measurement_form,
                'input': True

            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >=0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} pound = {int(input)*0.453492} kilogram'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input} kilogram = {int(input)*2.20462} pound'
                context = {
                    'form': form,
                    'm_form': measurement_form,
                    'input': True,
                    'answer': answer
                }

    else:
        form = ConversionForm()
        context = {
            'form': form,
            'input': False
        }
    return render(request, 'conversion.html', context)


# not done yet,wanna make with email authentication
def register(request):
    form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'register.html', context)