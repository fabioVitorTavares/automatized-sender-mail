from django.shortcuts import redirect, render
import pyperclip as pc
from .forms import AdicionarTutorialForm, FormDadosUsuario
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm

import pyperclip as pc

from .forms import AdicionarTutorialForm, TutorialForm, LoginForm
from .models import Usuario, Marcacao, Tutorial, Comentario, Codigo, TutorialConteudo


class register(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'account/register.html'


def inicio(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/index')
    return render(request, "inicio.html")


def cadastrar(request):
    form = UserCreationForm(request.POST)
    formDadosUsuario = FormDadosUsuario(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data = form.cleaned_data
            username = data.get('username')
            if formDadosUsuario.is_valid():
              dataUser = formDadosUsuario.cleaned_data
              nome  = dataUser.get('nome')
              sobrenome = dataUser.get('sobrenome')
              email = dataUser.get('email')
              novoUsuario = Usuario()
              novoUsuario.__setattr__('username', username)
              novoUsuario.__setattr__('nome',nome )
              novoUsuario.__setattr__('sobrenome',sobrenome)
              novoUsuario.__setattr__('email',email)
              novoUsuario.save()
              userCadastrado = Usuario.objects.get(username=username)
              print(userCadastrado)
        else:
          print("invalid form")
    context = {'form': form}
    return render(request, 'cadastrar.html', context)


def loginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,
                                username=data['login'],
                                password=data['senha'])
            if user != None:
                login(request, user)
                return HttpResponseRedirect('/index')
    return render(request, 'login.html')


@login_required(login_url="../login")
def index(request):
    if request.user.is_authenticated:
        username = request.user.username
        dadosUsuario = Usuario.objects.get(username=username)
        print(dadosUsuario.nome)
        if request.method == 'POST':
            form = TutorialForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                print(data)
                like = bool(data.get('like'))
                id = data.get('id')
                tutoriais = Tutorial.objects.all()

                sair = bool(data.get('sair'))

                if (sair):
                    logout(request)
                    return render(request, 'inicio.html')

                if like:
                    tutorial_like = Tutorial.objects.get(id=id)
                    likes = tutorial_like.total_likes
                    tutorial_like.__setattr__('total_likes', 1+likes)
                    tutorial_like.save()
                    context = {
                        'tutoriais': tutoriais,
                        'usuario':  dadosUsuario,
                    }
                    return render(request, 'tutoriais_index.html', context=context)

                if bool(id):
                    return tutorial(request)

                pesquisa = data.get('pesquisa')
                tutoriais_filtrados = []
                for tut in tutoriais:
                    if (pesquisa.upper() in tut.titulo.upper()):
                        tutoriais_filtrados.append(tut)
                context = {
                    'tutoriais': tutoriais_filtrados,
                    'usuario':  dadosUsuario,
                }
                return render(request, 'tutoriais_index.html', context=context)
        else:
            tutoriais = Tutorial.objects.all()
            context = {
                'tutoriais': tutoriais,
                'usuario':  dadosUsuario,
            }
            return render(request, 'tutoriais_index.html', context=context)
    else:
        return render(request, 'inicio.html')


@login_required(login_url="../login")
def tutorial(request):
    if request.method == 'POST':
        form = TutorialForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            id = data.get('id')
            like = bool(data.get('like'))
            copy = bool(data.get('copy'))

            tutorial = Tutorial.objects.get(id=id)
            tutoriais_conteudos = TutorialConteudo.objects.all()
            conteudos = []
            for tutorial_conteudo in tutoriais_conteudos:
                if tutorial_conteudo.tutorial.id == int(id):
                    if tutorial_conteudo.marcacao:
                        conteudos.append(tutorial_conteudo.marcacao)
                    elif tutorial_conteudo.codigo:
                        conteudos.append(tutorial_conteudo.codigo)
            codigos = [conteudo for conteudo in conteudos if type(
                conteudo) == Codigo]
            marcacoes = [conteudo for conteudo in conteudos if type(
                conteudo) == Marcacao]

            if like:
                likes = tutorial.total_likes
                tutorial.__setattr__('total_likes', 1+likes)
                tutorial.save()

            if copy:
                id_codigo = data.get('copy')
                codigo_copy = Codigo.objects.get(id=id_codigo)
                pc.copy(codigo_copy.texto)

            comentario = data.get('comentario')

            if bool(comentario):
                username = request.user.username
                usuario = Usuario.objects.get(username=username)
                novo_comentario = Comentario(usuario=usuario,
                                             tutorial=tutorial,
                                             texto=comentario)
                novo_comentario.save()

            comentarios = Comentario.objects.filter(tutorial_id=id)
            context = {
                'conteudos': conteudos,
                'comentarios': comentarios,
                'tutorial': tutorial,
                'id': id
            }
            return render(request, 'tutorial.html', context=context)


@login_required(login_url="../login")
def adicionar_tutorial(request):
    if request.method == 'POST':
        form = AdicionarTutorialForm(request.POST)
        if form.is_valid():
            data = form.data
            titulo = data.get('titulo')
            descricao = data.get('descricao')
            conteudos = data.getlist('conteudos')
            conteudos_tipo = data.getlist('conteudos_tipo')
            username = request.user.username
            usuario = Usuario.objects.get(username=username)
            tutorial = Tutorial(titulo=titulo,
                                descricao=descricao,
                                usuario=usuario)
            tutorial.save()
            for i in range(len(conteudos)):
                texto = conteudos[i]
                if conteudos_tipo[i] == "m":
                    marcacao = Marcacao(texto=texto, usuario=usuario)
                    marcacao.save()
                    tutorial_conteudo = TutorialConteudo(
                        tutorial=tutorial, marcacao=marcacao)
                    tutorial_conteudo.save()
                elif conteudos_tipo[i] == "c":
                    codigo = Codigo(texto=texto, usuario=usuario)
                    codigo.save()
                    tutorial_conteudo = TutorialConteudo(
                        tutorial=tutorial, codigo=codigo)
                    tutorial_conteudo.save()
            id = tutorial.id
            comentarios = Comentario.objects.filter(tutorial_id=id)
            tutoriais_conteudos = TutorialConteudo.objects.all()
            conteudos = []
            for tutorial_conteudo in tutoriais_conteudos:
                if tutorial_conteudo.tutorial.id == int(id):
                    if tutorial_conteudo.marcacao:
                        conteudos.append(tutorial_conteudo.marcacao)
                    elif tutorial_conteudo.codigo:
                        conteudos.append(tutorial_conteudo.codigo)

            context = {'conteudos': conteudos,
                       'comentarios': comentarios,
                       'tutorial': tutorial,
                       'id': id}
            return render(request, 'tutorial.html', context=context)
    else:
        form = AdicionarTutorialForm()
    return render(request, 'adicionar_tutorial.html', {'form': form})
