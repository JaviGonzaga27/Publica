from django.shortcuts import render, redirect
from .models import Persona
from .forms import PersonaForm

def lista_personas(request):
    personas = Persona.objects.all()
    return render(request, 'personas/lista_personas.html', {'personas': personas})

def nueva_persona(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_personas')
    else:
        form = PersonaForm()
    return render(request, 'personas/nueva_persona.html', {'form': form})

def editar_persona(request, id):
    persona = Persona.objects.get(id=id)
    if request.method == 'POST':
        form = PersonaForm(request.POST, instance=persona)
        if form.is_valid():
            form.save()
            return redirect('lista_personas')
    else:
        form = PersonaForm(instance=persona)
    return render(request, 'personas/editar_persona.html', {'form': form})

def eliminar_persona(request, id):
    persona = Persona.objects.get(id=id)
    if request.method == 'POST':
        persona.delete()
        return redirect('lista_personas')
    return render(request, 'personas/eliminar_persona.html', {'persona': persona})

def horario(request):
    horarios = [
        "6-8", "8-10", "10-12", "12-14", "14-16", "16-18", "18-20"
    ]
    
    dias = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]

    territorios = Persona.objects.values_list('territorio', flat=True).distinct()
    tabla_horarios = {}

    for territorio in territorios:
        tabla_horarios[territorio] = {h: {d: [] for d in dias} for h in horarios}
        personas = Persona.objects.filter(territorio=territorio)
        for persona in personas:
            for dia in dias:
                if getattr(persona, dia):
                    tabla_horarios[territorio][persona.jornada][dia].append(f"{persona.nombre} {persona.apellido}")

    return render(request, 'personas/horario.html', {'tabla_horarios': tabla_horarios, 'horarios': horarios, 'dias': dias})

