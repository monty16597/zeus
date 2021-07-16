from django.shortcuts import render,redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .utils import create_automation_workspace, GitController
from django.contrib.auth.decorators import login_required
from .forms import AutomationForm, PatchJenkinsfile
import os
import uuid

@login_required
def index(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AutomationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            git_c = GitController(project_name=form.data.get('project_name'), url=form.data.get('repo_url'))
            git_c.repo_clone()
            request.session['automation_project_name'] = form.data.get('project_name')
            return redirect('automation.patch.jenkinsfile',)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AutomationForm()
    template = loader.get_template('automation/index.html')
    context = {'form': form}
    return HttpResponse(template.render(context, request))

@login_required
def patch_jenkinsfile(request):
    git_c = GitController(project_name=request.session.get('automation_project_name'))
    git_c.set_repo()
    branches = [branch.name for branch in git_c.repo.remote().refs]
    form = PatchJenkinsfile(initial={'jenkinsfile': ""},)
    form.set_branches(branches=branches)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PatchJenkinsfile(request.POST)
        form.set_branches(branches=branches)
        # check whether it's valid:
        if form.is_valid() and "Load" in dict(request.POST)['button']:
            selected_branch = dict(form.data)['branches'][0]
            git_c.repo.git.checkout(selected_branch)
            f = open(os.path.join(git_c.project_path, 'Jenkinsfile'))
            jenkinsfle_data = ''.join(line for line in f)
            form = PatchJenkinsfile(initial={'jenkinsfile': jenkinsfle_data},)
            form.set_branches(branches=branches)

        elif form.is_valid() and "Submit" in request.POST['button']:
            automation_branch = 'feature/zeus-automation-%s' % uuid.uuid4().hex[:4]
            automation_branch_head = git_c.repo.create_head(automation_branch)
            git_c.repo.git.checkout(automation_branch)
            f = open(os.path.join(git_c.project_path, 'Jenkinsfile'), mode="w")
            f.writelines(form.data.get('jenkinsfile'))
            f.close()

            git_c.repo.index.add(["Jenkinsfile"])
            git_c.repo.index.commit(form.data.get('commit_message'))
            git_c.repo.git.push('--set-upstream', 'origin', automation_branch_head)
            return redirect('automation.patch.jenkinsfile')

    # if a GET (or any other method) we'll create a blank form
    template = loader.get_template('automation/patch_jenkinsfile.html')
    context = {'form': form,}
    return HttpResponse(template.render(context, request))