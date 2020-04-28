import os
import shutil


def remove(filepaths):
    for unnecessary_file_or_folder in filepaths:
        full_path = os.path.join(os.getcwd(), unnecessary_file_or_folder)
        if os.path.isfile(full_path):
            os.remove(full_path)
        elif os.path.isdir(full_path):
            shutil.rmtree(full_path)
        else:
            print("{path} not in cookiecutter output".format(path=full_path))

# TODO(jinder): make sure cookiecutter.sub_dir_name is the right variable
CDA_remove = [
    ".bowerrc",
    "Dockerfile",
    "docker-compose.yml",
    "CONTRIBUTING.md",
    "{{cookiecutter.sub_dir_name}}/settings",
    "{{cookiecutter.sub_dir_name}}/apps",
    "{{cookiecutter.sub_dir_name}}/static",

]

CDI_remove = [
"CHANGELOG.rst",
"MANIFEST.in",
"setup.py",
"tox.ini",
"{{cookiecutter.sub_dir_name}}/models.py",
"{{cookiecutter.sub_dir_name}}/apps.py",
]

if "{{cookiecutter.project_type}}" == "App":
    remove(CDA_remove)
else:
    remove(CDI_remove)


