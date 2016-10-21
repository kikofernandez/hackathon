from django.shortcuts import render, reverse
from django.http import HttpResponse
from .models import Repo
from .forms import repoForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
import requests
import urllib2

def index(request):
    context = {'projects': Repo.objects.all(),
               'total':Repo.objects.all().count()}
    return render(request, 'acmuu/index.html', context)

def add_repo(request):
    if request.method == 'GET':
        form = repoForm.RepoForm()
    else:
        form = repoForm.RepoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('acmuu:index'))
    return render(request, 'acmuu/repoForm.html', { 'form': form, })

def detail(request, username, repo):
    repo = get_object_or_404(Repo, path="%s/%s" % (username, repo))
    return HttpResponse("You're looking at user: %s, %s." % (username, repo.path))

def user(request, username):
    print username
    return HttpResponse("You're looking at user: %s." % (username))

# def events(request, ):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % repo_name)


def commits(request, username, repo):
    import json
    repo = get_object_or_404(Repo, path="%s/%s" % (username, repo))

    url = "https://api.github.com/repos/" + repo.path + "/commits"
    data = json.load(urllib2.urlopen(url))
    list_commits = []

    for i in range(len(data)):
        try:
            commit = data[i]

            name = commit['commit']['committer']['name']
            email = commit['commit']['committer']['email']
            avatar = commit['author']['avatar_url']
            message = commit['commit']['message']

            list_commits.append({'author': name,
                                 'email': email,
                                 'avatar': avatar,
                                 'message': message})
        except:
            None
    # print str(list_commits)
    return render(request, 'acmuu/commits.html',
                  {'commits': list_commits})