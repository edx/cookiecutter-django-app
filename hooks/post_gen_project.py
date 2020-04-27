def remove(filepaths):
    for unnecessary_file_or_folder in filepaths:
        full_path = os.path.join(os.getcwd(), '{{cookiecutter.package_name}}', unnecessary_file_or_folder)
        if os.path.isfile(filepath):
            os.remove(filepath)
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath)
        print("unnecessary_file_or_folder not in cookiecutter output")

# TODO(jinder): make sure cookiecutter.app_name is the right variable
CDA_remove = [
    ".bowerrc",
    "Dockerfile",
    "docker-compose.yml",
    "CONTRIBUTING.md",
    "{{cookiecutter.app_name}}/settings",
    "{{cookiecutter.app_name}}/apps",
    "{{cookiecutter.app_name}}/static",

]

CDI_remove = [
"CHANGELOG.rst",
"MANIFEST.in",
"setup.py",
"tox.ini",
"{{cookiecutter.app_name}}/models.py",
"{{cookiecutter.app_name}}/apps.py",
]

if {{cookiecutter.project_type}} == "App":
    remove(CDA_remove):
else:
    remove(CDI_remove):


