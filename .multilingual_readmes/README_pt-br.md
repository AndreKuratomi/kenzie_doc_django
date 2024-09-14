# kenzie_doc_django

- [Sobre](#sobre)
- [Diagrama](#diagrama)
- [Instalação](#instalação)
- [Documentação](#documentação)
- [Desenvolvedores da API](#desenvolvedores-da-api)
- [Referências](#referências)
- [Termos de uso](#termos-de-uso)

<br>

## Traduções

- [English / Inglês](https://github.com/AndreKuratomi/kenzie_doc_django)
- [Português brasileiro / Brazilian portuguese](./README_pt-br.md)

<br>

## Sobre

<p>A API <b>kenzie_doc_django</b> se propõe a cadastrar médicos e pacientes na plataforma possibilitando o agendamento de consultas de maneira simples e intuitiva, além de fazer a gestão de consultas agendadas e da lista de espera.

A aplicação também possibilita ao paciente fazer uma busca pelo profissional mais adequado para sua necessidade e agendar a consulta de forma confortável, prática e rápida.

<b>kenzie_doc</b> também faz o <b>envio de emails</b> tanto para o paciente quanto para o profissional quando a consulta é agendada, alterada, finalizada ou mesmo cancelada. O mesmo para <b>mensagens de whatsapp</b>.

Esta aplicação utiliza a linguagem <strong>[Python](https://www.python.org/downloads/)</strong>, seu framework <strong>[Django](https://www.djangoproject.com/)</strong> e o banco de dados <strong>[SQLite3](https://docs.python.org/3/library/sqlite3.html)</strong>.</p>

<br>

## Diagrama

<figure>
    <img src="../kenzie_doc_django.drawio.png" alt="diagrama api kenzie_doc_django">
    <figcaption style="text-align: center">Diagrama API kenzie_doc_django</figcaption>
</figure>

<br>

## Instalação


<h3>0. Primeiramente, é necessário já ter instalado na própria máquina:</h3>

- O versionador de codigo <b>[Git](https://git-scm.com/downloads)</b>.

- A linguagem de programação <b>[Python](https://www.python.org/downloads/)</b>.

- Um <b>editor de código</b>, conhecido também como <b>IDE</b>. Por exemplo, o <b>[Visual Studio Code (VSCode)](https://code.visualstudio.com/)</b>.

- Uma <b>ferramenta cliente de API REST</b>. Por exemplo, o <b>[Insomnia](https://insomnia.rest/download)</b> ou o <b>[Postman](https://www.postman.com/product/rest-client/)</b>.

- <p> E versionar o diretório escolhido para receber o clone da aplicação:</p>

```
git init
```
<br>

<h3>1. Fazer o clone do reposítório <b>kenzie_doc_django</b> na sua máquina pelo terminal do computador ou pelo do IDE:</h3>

```
git clone https://github.com/AndreKuratomi/kenzie_doc_django.git
```

WINDOWS:

Obs: Caso apareca algum erro semelhante a este: 

```
unable to access 'https://github.com/AndreKuratomi/kenzie_doc_django.git': SSL certificate problem: self-signed certificate in certificate chain
```

Configure o git para desabilitar a certificação SSL:

```
git config --global http.sslVerify "false"
```


<p>Entrar na pasta criada:</p>

```
cd kenzie_doc_django
```
<br>

<h3>2. Após feito o clone do repositório, instalar:</h3>

<h4>O ambiente virtual* e atualizar suas dependências com o seguinte comando:</h4>

LINUX:
```
python3 -m venv venv --upgrade-deps
```

WINDOWS:
```
py -m venv venv --upgrade-deps
```

Caso seja retornado algum erro semelhante a este basta seguir as instruções:

```
The virtual environment was not created successfully because ensurepip is not
available.  On Debian/Ubuntu systems, you need to install the python3-venv
package using the following command.

    apt install python3.10-venv

You may need to use sudo with that command.  After installing the python3-venv
package, recreate your virtual environment.
```

*É interessante seguir esta prática porque diferentes projetos exigem diferentes dependências. Um ambiente virtual nada mais é do que um ambiente separado da sua máquina. Caso contrário, a máquina do usuário pode se encher de dependências que serão utilizadas apenas em um único projeto.

<h4>Ative o seu ambiente virtual com o comando:</h4>

LINUX:
```
source/venv/bin/activate
```

WINDOWS:

No sistema operacional Windows é necessário antes configurar o Execution Policy do PowerShell:

```
Get-ExecutionPolicy # para verificar o tipo de política de execução
Set-ExecutionPolicy RemoteSigned # para alterar o tipo de política se o comando acima mostrar 'Restricted'
```
Obs: Eventualmente, pode ser necessário abrir o PowerShell como administrador.

```
.\venv\Scripts\activate
```


<h4>Instalar suas dependências:</h4>

```
pip install -r requirements.txt
```

WINDOWS:

Caso seja retornado algum erro semelhante a este:

```
ERROR: Could not install packages due to an OSError: [Errno 2] No such file or directory: 'C:\\Users\\andre.kuratomi\\OneDrive - Company\\Área de Trabalho\\kenzie_doc_django\\kenzie_doc_django\\env\\Lib\\site-packages\\jedi\\third_party\\django-stubs\\django-stubs\\contrib\\contenttypes\\management\\commands\\remove_stale_contenttypes.pyi'
HINT: This error might have occurred since this system does not have Windows Long Path support enabled. You can find information on how to enable this at https://pip.pypa.io/warnings/enable-long-paths
```

Rode no cmd como adminstrador o seguinte comando:

```
reg.exe add HKLM\SYSTEM\CurrentControlSet\Control\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1 /f
```
<br>

<h3>3. Abrir a aplicação no IDE:</h3>

```
code .
```
<br>

<h3>4. E executá-la:</h3>

LINUX:
```
python manage.py runserver
```
ou
```
./manage.py runserver
```

WINDOWS:
```
py manage.py runserver
```

<br>

## Documentação

Para ter acesso ao descrições detalhes das rotas e seus retornos, conferir documentação completa neste [link](https://kenziedoc-django-api-documentation.vercel.app/).

<br>

## Desenvolvedores da API

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

## Referências

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

## Termos de uso

Esse projeto atende a fins exclusivamente didáticos e sem nenhum intuito comercial.
