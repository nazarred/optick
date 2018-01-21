from django.shortcuts import render


def glasses_search(request):
    return render(request, 'glasses/glass.html')
