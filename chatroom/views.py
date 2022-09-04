from django.shortcuts import render

def socket(request):
    return render(request, 'show.html', {})