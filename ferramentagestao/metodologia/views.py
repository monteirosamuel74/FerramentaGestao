from django.shortcuts import render, redirect, get_object_or_404
from .models import Ferramenta, InstanciaFerramenta, Metodologia, User, PDCA
from .forms import EditarInstanciaForm,PDCAForm,AdicionarParticipanteForm
from django.contrib.auth.decorators import login_required


@login_required
def criar_instancia(request, ferramenta_id):
    ferramenta = get_object_or_404(Ferramenta, id=ferramenta_id)
    if request.method == 'POST':
        instancia = InstanciaFerramenta(ferramenta=ferramenta, dono=request.user)
        instancia.save()
        return redirect('detalhes_instancia', instancia_id=instancia.id)
    return render(request, 'metodologia/criar_instancia.html', {'ferramenta': ferramenta})

@login_required
def home(request):
    metodologias = Metodologia.objects.all()
    return render(request, 'metodologia/home.html', {'metodologias': metodologias})

@login_required
def minhas_instancias(request):
    instancias = InstanciaFerramenta.objects.filter(dono=request.user)
    return render(request, 'metodologia/minhas_instancias.html', {'instancias': instancias})

@login_required
def detalhes_instancia(request, instancia_id):
    instancia = get_object_or_404(InstanciaFerramenta, id=instancia_id)
    return render(request, 'metodologia/detalhes_instancia.html', {'instancia': instancia})

@login_required
def adicionar_participante(request, ferramenta_id):
    ferramenta = get_object_or_404(Ferramenta, id=ferramenta_id)

    if request.method == 'POST':
        form = AdicionarParticipanteForm(request.POST, instance=ferramenta)
        if form.is_valid():
            form.save()
            return redirect('detalhes_ferramenta', ferramenta_id=ferramenta.id)
    else:
        form = AdicionarParticipanteForm(instance=ferramenta)

    return render(request, 'metodologia/adicionar_participante.html', {
        'ferramenta': ferramenta,
        'form': form,
    })


@login_required
def editar_instancia(request, instancia_id):
    instancia = get_object_or_404(InstanciaFerramenta, id=instancia_id, dono=request.user)
    
    # Verifica se a instância já tem um PDCA associado
    pdca, created = PDCA.objects.get_or_create(instancia=instancia)
    
    if request.method == 'POST':
        instancia_form = EditarInstanciaForm(request.POST, instance=instancia)
        pdca_form = PDCAForm(request.POST, instance=pdca)
        if instancia_form.is_valid() and pdca_form.is_valid():
            instancia_form.save()
            pdca_form.save()
            return redirect('detalhes_instancia', instancia_id=instancia.id)
    else:
        instancia_form = EditarInstanciaForm(instance=instancia)
        pdca_form = PDCAForm(instance=pdca)
    
    return render(request, 'metodologia/editar_instancia.html', {
        'instancia_form': instancia_form,
        'pdca_form': pdca_form,
        'instancia': instancia,
    })
    
    
@login_required
def excluir_instancia(request, instancia_id):
    instancia = get_object_or_404(InstanciaFerramenta, id=instancia_id, dono=request.user)
    if request.method == 'POST':
        instancia.delete()
        return redirect('minhas_instancias')
    return render(request, 'metodologia/excluir_instancia.html', {'instancia': instancia})

def detalhes_metodologia(request, metodologia_id):
    metodologia = get_object_or_404(Metodologia, id=metodologia_id)
    return render(request, 'metodologia/detalhes_metodologia.html', {'metodologia': metodologia})


def detalhes_ferramenta(request, ferramenta_id):
    ferramenta = get_object_or_404(Ferramenta, id=ferramenta_id)
    pdcas = PDCA.objects.filter(ferramenta=ferramenta)

    if request.method == 'POST':
        form = PDCAForm(request.POST)
        if form.is_valid():
            pdca = form.save(commit=False)
            pdca.ferramenta = ferramenta
            pdca.dono = request.user
            pdca.save()
            return redirect('detalhes_ferramenta', ferramenta_id=ferramenta.id)
    else:
        form = PDCAForm()

    return render(request, 'metodologia/detalhes_ferramenta.html', {
        'ferramenta': ferramenta,
        'form': form,
        'pdcas': pdcas,
    })