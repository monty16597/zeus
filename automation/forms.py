from django import forms

class AutomationForm(forms.Form):
    project_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Project Name'}))
    repo_url = forms.CharField(label='', max_length=2083, widget=forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Repo Git URL'}))

class PatchJenkinsfile(forms.Form):
    branches = forms.ChoiceField(label='Branch', widget=forms.Select(attrs={'class': 'custom-input mb-3'}))
    jenkinsfile = forms.CharField(label='Jenkinsfile', widget=forms.Textarea(attrs={'class': 'custom-input', 'cols': 100, 'rows': 20, 'id': 'jenkinsfileTextArea',}), required=False)
    commit_message = forms.CharField(label='', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'custom-input mt-3', 'placeholder': 'Commit Message'}))

    def set_branches(self, branches=None):
        self.fields['branches'].choices = [(branch, branch) for branch in branches]