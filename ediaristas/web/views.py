from django.shortcuts import render, redirect
from .forms import diarista_form
from .models import Diaristas

# Create your views here.

def cadastrar_diarista(request):
    if request.method == "POST":
        form_diarista = diarista_form.DiaristaForm(request.POST, request.FILES)
        if form_diarista.is_valid():
            form_diarista.save()
            return redirect('listar_diaristas')
    else:
        form_diarista = diarista_form.DiaristaForm()
    return render(request, 'form_diaristas.html', {'form_diarista': form_diarista})

def listar_diarista(request):
    diaristas = Diaristas.objects.all()
    return render(request, 'lista-diaristas.html', {'diaristas': diaristas})

def editar_diarista(request, diarista_id):
    diarista = Diaristas.objects.get(id=diarista_id)
    if request.method == 'POST':
        form_diarista = diarista_form.DiaristaForm(request.POST or None, request.FILES, instance=diarista)
        if form_diarista.is_valid():
            form_diarista.save()
            return redirect('listar_diaristas')
    else:
        form_diarista = diarista_form.DiaristaForm(instance=diarista)

    return  render(request, 'form_diaristas.html', {'form_diarista': form_diarista})

def remover_diarista(request, diarista_id):
    diarista = Diaristas.objects.get(id=diarista_id)
    diarista.delete()
    return  redirect('listar_diaristas')