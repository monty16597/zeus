import os
from django.conf import settings
from  git import repo, remote
import shutil

AUTOMATION_WORKSPACE_NAME = "automation"
AUTOMATION_WORKSPACE_DIR = os.path.join(settings.TEMP_WORKSPACE_DIR,AUTOMATION_WORKSPACE_NAME)

def get_base_dir():
    return settings.BASE_DIR

def create_automation_workspace():
    if settings.TEMP_WORKSPACE_NAME in os.listdir(settings.BASE_DIR):
        try:
            os.mkdir(AUTOMATION_WORKSPACE_DIR)
            return True
        except Exception as e:
            print("%s is already exists" % AUTOMATION_WORKSPACE_DIR)
            return False

class GitController:
    def __init__(self, project_name, url=None):
        self.project_name = project_name
        self.url = url
        self.repo = repo.base.Repo()
        self.project_path = None

    def repo_clone(self):
        PROJECT_WORKSPACE = os.path.join(AUTOMATION_WORKSPACE_DIR, self.project_name)
        if not os.path.exists(AUTOMATION_WORKSPACE_DIR):
            os.mkdir(AUTOMATION_WORKSPACE_DIR)
        if os.path.exists(PROJECT_WORKSPACE):
            shutil.rmtree(PROJECT_WORKSPACE)
        os.mkdir(PROJECT_WORKSPACE)
        self.repo.clone_from(url=self.url, to_path=PROJECT_WORKSPACE)
        self.project_path = PROJECT_WORKSPACE
    
    def set_repo(self):
        PROJECT_WORKSPACE = os.path.join(AUTOMATION_WORKSPACE_DIR, self.project_name)
        self.repo = repo.base.Repo(PROJECT_WORKSPACE)
        self.project_path = PROJECT_WORKSPACE

class JenkinsfileController:
    def __init__(self):
        self.path = ""
    
    def replace_jenkinsfile(self, content):
        pass