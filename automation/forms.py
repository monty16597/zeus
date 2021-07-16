from django import forms

class AutomationForm(forms.Form):
    project_name = forms.CharField(label='Project Name', max_length=100)
    repo_url = forms.CharField(label='Repo Git URL', max_length=2083)

class PatchJenkinsfile(forms.Form):
    jenkinsfile = forms.CharField(label='Jenkinsfile', widget=forms.Textarea(attrs={'cols': 100, 'rows': 20}), required=False)
    branches = forms.ChoiceField(widget=forms.Select())
    commit_message = forms.CharField(label='Commit Message', max_length=100, required=False)

    def set_branches(self, branches=None):
        self.fields['branches'].choices = [(branch, branch) for branch in branches]