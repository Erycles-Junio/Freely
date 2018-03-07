from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from freela.forms import UserRegistrationForm
from freela.forms import ProjectRegistrationForm
from freela.forms import ServiceRegistrationForm
from freela.forms import CommentRegistrationForm
from freela.models import Project
from freela.models import Comment
from freela.models import Message
from freela.models import Service
from freela.forms import EditProjectForm
from freela.forms import EditServiceForm

def login_view(request):
    if request.method == 'GET':
        return render(request, 'freela/login_form.html', {})
    
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)

        if user is not None:
            #request.session['user'] = user
            request.session['user_name'] = user.username
            request.session['user_id'] = user.id
            login(request, user)
            lista = Project.objects.all()
            return redirect(index_projects)
        else:
            return HttpResponse("Seu nome de usuário e senha não conferem!")

def index_projects(request):
    if request.method == 'GET':
        query = request.GET.get('search_by', None)
        
        if query is None:
            #user_id = request.session['user_id']
            lista = Project.objects.all()
            #user = User.objects.get(id=user_id)
            return render(request, 'freela/index_projects.html', {'lista': lista})
        else:
            lista = Project.objects.filter(name__icontains=query)
            return render(request, "freela/index_projects.html", {'lista': lista})

def index_services(request):
    if request.method == 'GET':
        query = request.GET.get('search_by', None)
        
        if query is None:
            #user_id = request.session['user_id']
            lista = Service.objects.all()
            #user = User.objects.get(id=user_id)
            return render(request, 'freela/index_services.html', {'lista': lista})
        else:
            lista = Service.objects.filter(name__icontains=query)
            return render(request, "freela/index_services.html", {'lista': lista})

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email =  userObj['email']
            password =  userObj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                user = User.objects.create_user(username, email, password)
                user.save()
                return redirect(login_view)
            else:
                return HttpResponse('Parece que um usuário com este email já existe')
    else:
        return render(request, 'freela/register001.html', {})

def register_project(request):
    #user = request.session.get('user_id', '')
    user_id = request.session['user_id']
    user_name = request.session['user_name']
    if request.method == 'POST':
        form = ProjectRegistrationForm(request.POST)
        if form.is_valid():
            projectObj = form.cleaned_data
            name = projectObj['name']
            budget = projectObj['budget']
            description = projectObj['description']
            owner = User.objects.get(id=user_id)
            project = Project.objects.create(name=name, budget=budget, description=description, owner=owner)

            return redirect(index_projects)
        else:
            return HttpResponse('Algo deu errado')
    else:
        return render(request, 'freela/register_project.html', {})
            

def project_details(request, pid):
    projectObj = Project.objects.get(auto_increment_id=pid)
    projectComments = Comment.objects.filter(post=pid) #colocar exceção caso nao exista comentarios para este post
    if request.method == 'GET':
            return render(request, 'freela/project_details.html', {'project': projectObj, 'comments': projectComments})
    if request.method == 'POST':
        form = CommentRegistrationForm(request.POST)
        if form.is_valid():
            commentObj = form.cleaned_data
            user_id = request.session['user_id']
            user = User.objects.get(id=user_id)
            text = commentObj['text']
            comment = Comment.objects.create(post=projectObj, author=user, text=text)

            return redirect(project_details, pid)
        else:
            return HttpResponse('Algo deu errado')


def register_service(request):
    #user = request.session.get('user_id', '')
    user_id = request.session['user_id']
    user_name = request.session['user_name']
    if request.method == 'POST':
        form = ServiceRegistrationForm(request.POST)
        if form.is_valid():
            serviceObj = form.cleaned_data
            name = serviceObj['name']
            budget = serviceObj['budget']
            description = serviceObj['description']
            area = serviceObj['area']
            owner = User.objects.get(id=user_id)
            service = Service.objects.create(name=name, budget=budget, description=description, owner=owner, area=area)

            return redirect(index_projects)
        else:
            return HttpResponse('Algo deu errado')
    else:
        return render(request, 'freela/register_service.html', {})



def services_view(request):
    if request.method == 'GET':
        return render(request, 'freela/services_view.html', {})


def my_projects(request):
    if request.method == 'GET':
        owner_id = request.session['user_id']
        user = User.objects.get(id=owner_id)
        projects = Project.objects.filter(owner=user)
        return render(request, "freela/my_projects.html", {'projects': projects})


def my_services(request):
    if request.method == 'GET':
        owner_id = request.session['user_id']
        user = User.objects.get(id=owner_id)
        services = Service.objects.filter(owner=user)
        return render(request, "freela/my_services.html", {'services': services})


def delete_project(request, pk):
    project = Project.objects.get(auto_increment_id=pk)
    project.delete()
    return redirect(my_projects)

def delete_service(request, pk):
    service = Service.objects.get(auto_increment_id=pk)
    service.delete()
    return redirect(my_services)


def message_list(request):
    if request.method == "GET":
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        return render(request, "freela/messages.html",
                      {'messages': Message.objects.filter(receiver=user)})  


def send_message(request, receiver, sender):
    receiverObj = User.objects.get(id=receiver)
    senderObj = User.objects.get(id=sender)
    if request.method == 'GET':
        return render(request, "freela/send_message.html", {})
    if request.method == 'POST':
        messageObj = request.POST.get('message', '')
        Message.objects.create(message=messageObj, receiver=receiverObj, sender=senderObj)
        return redirect(index_projects)


def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    message.delete()
    return redirect(message_list)

def edit_project(request, pk):
    instance = Project.objects.get(auto_increment_id=pk)
    if request.method == 'GET':
        return render(request, "freela/edit_project.html", {})
    if request.method == 'POST':
        form = EditProjectForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(my_projects)
        else:
            return HttpResponse('Algo deu errado')

def edit_service(request, pk):
    instance = Service.objects.get(auto_increment_id=pk)
    if request.method == 'GET':
        return render(request, "freela/edit_service.html", {})
    if request.method == 'POST':
        form = EditServiceForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(my_services)
        else:
            return HttpResponse('Algo deu errado')
