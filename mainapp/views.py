from django.shortcuts import render

def home(request):
    context = {
        'title': 'Головна сторінка Лаби 3',
        'message': 'Це контент, переданий через контекст!'
    }
    return render(request, 'mainapp/index.html', context)

def other_page(request):
    context = {
        'title': 'Друга сторінка',
        'message': 'Ви перейшли сюди через Django views.'
    }
    return render(request, 'mainapp/other.html', context)