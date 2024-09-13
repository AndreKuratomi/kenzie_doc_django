# kenzie_doc_django

- [Translations](#translations)
- [About](#about)
- [Diagram](#diagram)
- [Instalation](#instalation)
- [Documentation](#documentation)
- [API developers](#api-developers)
- [References](#references)
- [Terms of use](#terms-of-use)

<br>

## Translations

- [Português brasileiro / Brazilian portuguese](./.multilingual_readmes/README_pt-br.md)
- [English](https://github.com/AndreKuratomi/kenzie_doc_django)

<br>

## About


<p>The API <b>kenzie_doc_django</b> was made for a clinic logistic. It makes CRUD operations for patients, physicians and secretaries (admins), creates and manages appointments in a simple and intuitive way, as well as manages the waiting queue of the day.

This API also gives the user the possibility to look for professionals by its specialty and also to schedule appointments with the professional chosen in a very simple way.

It uses the language <strong>[Python](https://www.python.org/downloads/)</strong>, its framework <strong>[Django](https://www.djangoproject.com/)</strong> and the database <strong>[SQLite3](https://docs.python.org/3/library/sqlite3.html)</strong>.</p>

<br>

## Diagram

<figure>
    <img src="./kenzie_doc_django.drawio.png" alt="diagram of table relationships">
    <figcaption style="text-align: center">kenzie_doc_django API diagram</figcaption>
</figure>

<br>

## Instalation:

<h3>0. It is first necessary to have instaled the following devices:</h3>

- The code versioning <b>[Git](https://git-scm.com/downloads)</b>.

- A <b>code editor</b>, also known as <b>IDE</b>. For instance, <strong>[Visual Studio Code (VSCode)](https://code.visualstudio.com/)</strong>.

- The programming language <strong>[Python](https://www.python.org/downloads/)</strong>.

- A <b> client API REST </b> program. <strong>[Insomnia](https://insomnia.rest/download)</strong> or <b>[Postman](https://www.postman.com/product/rest-client/)</b>, for instance.

- <p> And versioning your directory to receive the aplication clone:</p>

```
git init
```
<br>

<h3>1. Clone the repository <b>kenzie_doc_django</b> by your machine terminal or by the IDE's:</h3>

```
git clone https://github.com/AndreKuratomi/kenzie_doc_django.git
```

WINDOWS:

Obs: In case of any mistake similar to this one: 

```
unable to access 'https://github.com/AndreKuratomi/kenzie_doc_django.git/': SSL certificate problem: self-signed certificate in certificate chain
```

Configure git to disable SSL certification:

```
git config --global http.sslVerify "false"
```

<p>Enter the directory:</p>

```
cd kenzie_doc_django
```
<br>

<h3>2. After cloning the repository install:</h3>

<h4>Virtual enviroment* and update its dependencies with the following command:</h4>


LINUX:
```
python3 -m venv venv --upgrade-deps
```

WINDOWS:
```
py -m venv venv --upgrade-deps
```

In case an error like this one is returned just follow the command displayed:

```
The virtual environment was not created successfully because ensurepip is not
available.  On Debian/Ubuntu systems, you need to install the python3-venv
package using the following command.

    apt install python3.10-venv

You may need to use sudo with that command.  After installing the python3-venv
package, recreate your virtual environment.
```

*It is a good practice to work with virtual enviroments because different projects may need different dependencies. A virtual enviroment is only a separated enviroment from the user machine. If not used, the user's machine may have lots of dependencies intalled that may only be used in a single project.
<br>
<h4>Ativate your virtual enviroment with the command:</h4>

LINUX:
```
source venv/bin/activate
```

WINDOWS:

On Windows operational system it is necessary to configure the Execution Policy at PowerShell:

```
Get-ExecutionPolicy # to check the Execution policy type
Set-ExecutionPolicy RemoteSigned # to change the type of policy if the command above shows 'Restricted'
```
Obs: It may often be necessary to open PowerShell as administrador for that.

```
.\env\Scripts\activate
```
<br>
<h4>Install its dependencies:</h4>

```
pip install -r requirements.txt
```
<br>


WINDOWS:

In case any error similar to the one bellow be returned:

```
ERROR: Could not install packages due to an OSError: [Errno 2] No such file or directory: 'C:\\Users\\andre.kuratomi\\OneDrive - Company\\Área de Trabalho\\kenzie_doc_django\\kenzie_doc_django\\env\\Lib\\site-packages\\jedi\\third_party\\django-stubs\\django-stubs\\contrib\\contenttypes\\management\\commands\\remove_stale_contenttypes.pyi'
HINT: This error might have occurred since this system does not have Windows Long Path support enabled. You can find information on how to enable this at https://pip.pypa.io/warnings/enable-long-paths
```

Run cmd as adminstrador with the following command:

```
reg.exe add HKLM\SYSTEM\CurrentControlSet\Control\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1 /f
```
<br>

<h3>3. Open the aplication with your IDE:</h3>

```
code .
```
<br>

<h3>4. Create <b>.env</b> file:</h3>

./
```
touch .env
```

Inside it we need to put our enviroment variables taking as reference the given file <b>.env.example</b>:

```
# DJANGO:
SECRET_KEY=secret_key

# EMAIL VARIABLES:
EMAIL_HOST_USER=host_email
EMAIL_HOST_PASSWORD=host_password

```

Obs: Do not share info from .env file. It is already mentioned in <b>.gitignore</b> for not being pushed to the repo.

<br>
<h3>5. And run django:</h3>

LINUX:
```
python manage.py runserver
```

or  

```
./manage.py runserver
```

WINDOWS:
```
py manage.py runserver
```


<br>

## Documentation

For full description of endpoints and its responses check the insomnia documentation on the link bellow (necessary free login account) click [here](https://kenziedoc-django-api-documentation.vercel.app/).

<br>

## API developers

<div>
    <p>Pierre Kalil - Techlead</p><a href="https://www.linkedin.com/in/pierre-kalil/" target="_blank" ><img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank"></a> 
    <a href = "https://github.com/Pierre-Kalil"><img src="https://www.kindpng.com/picc/m/128-1280187_github-logo-png-github-transparent-png.png" width= 106px height=27px target="_blank"> </a>
</div>

<br>

<div>
    <p>Leonardo Pereira - Product Owner</p><a href="https://www.linkedin.com/in/leonardo-m-pereira/" target="_blank" ><img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank"></a> 
    <a href = "https://github.com/leokito"><img src="https://www.kindpng.com/picc/m/128-1280187_github-logo-png-github-transparent-png.png" width= 106px height=27px target="_blank"> </a>
</div>

<br>

<div>
    <p>André Kuratomi - Scrum Master</p><a href="https://www.linkedin.com/in/andre-kuratomi/" target="_blank" ><img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank"></a>
    <a href = "https://github.com/AndreKuratomi"><img src="https://www.kindpng.com/picc/m/128-1280187_github-logo-png-github-transparent-png.png" width= 106px height=27px target="_blank"> </a>
</div>

<br>

<div>
    <p>Keila Passos - Developer</p><a href="https://www.linkedin.com/in/keila-aparecida-rodrigues-passos" target="_blank" ><img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank"></a> 
    <a href = "https://github.com/keilapassos"><img src="https://www.kindpng.com/picc/m/128-1280187_github-logo-png-github-transparent-png.png" width= 106px height=27px target="_blank"> </a>
</div>

<br>

<div>
    <p>Kaio Iwakiri - Developer</p><a href="https://www.linkedin.com/in/kaio-iwakiri/" target="_blank" ><img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank"></a> 
    <a href = "https://github.com/kaio-ti/"><img src="https://www.kindpng.com/picc/m/128-1280187_github-logo-png-github-transparent-png.png" width= 106px height=27px target="_blank"> </a>
</div>

<br>

## References

- [Django](https://www.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Generic views](https://www.django-rest-framework.org/api-guide/generic-views/)
- [Git](https://git-scm.com/downloads)
- [Insomnia-documenter](https://www.npmjs.com/package/insomnia-documenter)
- [Insomnia-documenter (quick tutorial)](https://www.youtube.com/watch?v=pq2u3FqVVy8)
- [Python](https://www.python.org/downloads/)
- [SQLite3](https://docs.python.org/3/library/sqlite3.html)
- [Visual Studio Code (VSCode)](https://code.visualstudio.com/)

<br>

## Terms of use

This project is exclusively for didatic purposes and has no commercial intent.
