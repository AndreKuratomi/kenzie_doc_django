# kenzie_doc_django

- [Traduções](#traduções)
- [Sobre](#sobre)
- [Diagrama](#diagrama)
- [Descrição](#descrição)
- [Instalação](#instalação)
- [Documentação](#documentação)
- [Desenvolvedores da API](#desenvolvedores-da-api)
- [Referências](#referências)
- [Termos de uso](#termos-de-uso)

<br>

## Traduções

- [🇬🇧 / 🇺🇸 English / Inglês](https://github.com/AndreKuratomi/kenzie_doc_django)
- [🇧🇷 Português brasileiro / Brazilian portuguese](./README_pt-br.md)

<br>

## Sobre

<p>A API <b>kenzie_doc_django</b> se propõe a cadastrar médicos e pacientes na plataforma possibilitando o agendamento de consultas de maneira simples e intuitiva, além de fazer a gestão de consultas agendadas e da lista de espera.

A aplicação também possibilita ao paciente fazer uma busca pelo profissional mais adequado para sua necessidade e agendar a consulta de forma confortável, prática e rápida.

<b>kenzie_doc</b> também faz o <b>envio de emails</b> tanto para o paciente quanto para o profissional quando a consulta é agendada, alterada, finalizada ou mesmo cancelada. O mesmo para <b>mensagens de whatsapp</b>.

Esta aplicação utiliza a linguagem <strong>[Python](https://www.python.org/downloads/)</strong>, seu framework <strong>[Django](https://www.djangoproject.com/)</strong> e o banco de dados <strong>[SQLite3](https://docs.python.org/3/library/sqlite3.html)</strong>. Para o envio de emails é usada a funçaõ nativa de Django <strong>[sendmail](https://docs.djangoproject.com/en/5.1/topics/email/)</strong> e para o envio de menssagens whatsapp a lib <strong>[PyWhatKit](https://pypi.org/project/pywhatkit/)</strong>.</p>

<br>

## Diagrama

<figure>
    <img src="../kenzie_doc_django.drawio.png" alt="diagrama api kenzie_doc_django">
    <figcaption style="text-align: center">Diagrama API kenzie_doc_django</figcaption>
</figure>

<br>

## Descrição

A seguir uma breve descrição de cada tabela exibida acima, suas permissões (permissions) e seus endpoints:

Por causa do contexto desta API trabalhar com 3 diferentes tipos de usuário que logam nela e executam operações diferentes decidiu-se por utilizar User models personalizadas. As user models usadas são 'User', 'Patient', 'Professional' e 'Admin':

<h3>User</h3>

<h4>Model</h4>

A User model poderia ser descrita como o metausuário da API. Para esta API ela foi desenvolvida para ser a model que possui os campos que todas as models relacionadas tem em comum. As user models possuem relacionamento <b>OneToOne</b> com ela.

Esta model também tem relacionamento <b>OneToMany</b> com a model <b>Address</b> que será tratada mais para frente.

User não possui suas próprias views e endpoints.

<br>

<h3>Patient</h3>

<h4>Model</h4>
A model patient possui relacionamento <b>OneToOne</b> com a model User e se define como tendo os campos 'is_admin' e 'is_prof' em User como False. Seu campo específico é a <b>'register_number'</b>, uma string com 6 letras (case-sensitive), 1 hyphen e 1 número. Este campo é gerado após o cadastro do novo usuário.

<h4>Views e permissions</h4>
<b>PatientsView:</b> class view para cadastro do paciente (POST) e listagem de todos os pacientes cadastrados (GET).
<br>
<b>Permissions:</b> qualquer usuário pode se cadastrar como paciente, mas apenas administradores podem listar todos os pacientes.
<br><br>

<b>PatientByIdView:</b> class view para listagem (GET), atualização de dados (PATCH) e deleção (DELETE) de um paciente pelo id (register_number).
<br>
<b>Permissions:</b> qualquer administrador e o próprio paciente podem listar dados do paciente e atualizar alguns deles, mas apenas os administradores podem deletar o usuário.

<h4>Endpoints</h4>
<b>patient/</b>
<br>
<b>patient/&ltstr:register_number&gt/</b>
<br>
<b>Obs:</b> para esta versão 'register_number' é case-sensitive.

<br>

<h3>Professional</h3>

<h4>Model</h4>
A model professional tem relacionamento <b>OneToOne</b> com a model User e pode ser definida na model User como tendo apenas o campo 'is_prof' como True. Seus campos específicos são:<br><br>
    1. <b>'council_number'</b>, uma string com 4 dígitos, 1 hyphen e 2 letras geradas pelo CEP do profissional (ver mais adiante) e<br> 
    2. <b>'specialty'</b> (especialidade).

<h4>Views e permissions</h4>
<b>ProfessionalsView:</b> class view para cadastro do profissional (POST) e listagem de todos eles (GET).
<br>
<b>Permissions:</b> apenas admins podem cadastrar e listar profissionais.
<br><br>

<b>ProfessionalByIdView:</b> class view para listagem (GET), atualização (PATCH) e deleção (DELETE) de dados de um profissional por 'council_number'.
<br>
<b>Permissions:</b> qualquer administrador logado ou o próprio profissional podem listar e atualizar alguns campos dos próprios dados, mas apenas administradores podem deletá-los.<br>
<b>Obs:</b> se o usuário permitido atualizar o CEP do profissional para um estado diferente o final da council_number será automaticamente atualizado para o estado correspondente.

<br>

<b>ProfessionalBySpecialtyView:</b> class view para listar todos os profissionais registrados na especialidade procurada.<br>
<b>Permissions:</b> qualquer usuário logado pode fazer esta busca.<br><br>

<h4>Endpoints</h4>

<b>professional/:</b><br>
<b>professional/&ltstr:council_number&gt/:</b> -> A API transformará o council_number digitado automaticamente para uppercase.<br>
<b>professional/specialty/&ltstr:specialty&gt/:</b> -> A API capitalizará a especialidade digitada automaticamente.

<br>

<h3>Admin</h3>

<h4>Model</h4>
A model do administrador (secretária) tem relacionamento <b>OneToOne</b> com a model User e pode ser definida na model User como tendo apenas o campo 'is_admin' como True. Nesta versão ela não possui campo específico.

<h4>Views e permissions</h4>
<b>AdminView:</b> class view para cadastro (POST) de administrador e listagem de todos os administradores (GET).<br>
<b>Permissions:</b> apenas administradores podem cadastrar e listar outros administradores.

<h4>Endpoints</h4>
<b>admin/</b>

<br>

<h3>Address</h3>

<h4>Model</h4>

A model address possui relacionamento <b>OneToMany</b> com a model User. Ela tem apenas dois campos de preenchimento obrigatório: <b>house_number</b> e <b>post_code</b> (CEP).

Esta model utiliza a biblioteca brasiliera <strong>brazilcep</strong> que fornece todos os campos opcionais 'street', 'city', 'state' se o CEP for fornecido. Esta lib é utilizada tanto para registro do endereço do usuário quanto para o council_number do profissional:

Ex: se o administrador digitar '9876' para o council_number e digitar '20031-170' para o CEP a response será '9876-RJ'.

Assim como User, address não possui suas próprias views e endpoints.

<br>

<h3>Appointments</h3>

<h4>Model</h4>
A model appointment (consulta) possui relacionamento <b>ManyToOne</b> tanto para Patients quanto para Professionals. Ambos podem ter várias consultas, mas cada uma tem apenas um paciente com um profissional.

<h4>Views e permissions</h4>

<b>CreateAppointment:</b> class view para agendamento de consulta (POST).<br>
<b>Permissions:</b> Apenas administradores podem agendar uma consulta.
<br><br>

<b>SpecificAppointmentView:</b> class view para listagem, atualização e deleção de uma consulta por ID.<br>
<b>Permissions:</b> Apenas administradores podem operar nesta view.
<br><br>

<b>SpecificPatientView:</b> class view para listagem das consultas de um paciente pelo seu register_number (GET).<br>
<b>Permissions:</b> Apenas o próprio paciente ou administradores podem listar essas consultas.
<br>

<b>SpecificProfessionalView:</b> class view para listagem das consultas de um profissional pelo seu council_number (GET).<br>
<b>Permissions:</b> Apenas o próprio profissional ou administradores podem listar essas consultas.
<br>

<b>NotFinishedAppointmentsView:</b> class view para a fila de espera do dia.<br>
<b>Permissions:</b> Apenas administradores podem listar a fila de espera.
<br>

<b>ProfessionalAppointmentsTodayView:</b> class view para as consultas do profissional não finalizadas do dia.<br>
<b>Permissions:</b> Apenas administradores podem listar as consultas em aberto do dia.
<br>

<b>NotFinishedAppointmentsView:</b> class view para a fila de espera do dia por profissional. É retornada uma mensagem como esta: .<br>
```
    "msg": "There are 2 patients waiting for their appointments with Dr. Jefferson today. The average waiting time is ca 2 hours and 0 minutes"
```
<b>Permissions:</b> Apenas administradores podem retornar a duração da fila de espera.
<br>

<b>FinishAppointmentView:</b> class view para finalizar uma consulta pelo seu ID (PATCH).<br>
<b>Permissions:</b> Apenas administradores podem finalizar uma consulta.
<br>

<b>Obs:</b> Todas as operações nestas views com POST, PATCH e DELETE possuem notificações configuradas para serem enviadas para os emails e números de whatsapp do paciente e do profissional automaticamente.

<h4>Endpoints</h4>
<b>appointments/</b><br>
<b>appointments/professional/&ltstr:council_number&gt/</b><br>
<b>appointments/&ltstr:appointment_id&gt/</b><br>
<b>appointment_finish/&ltstr:appointment_id&gt/</b><br>
<b>appointments/patient/&ltstr:register_number&gt/</b><br>
<b>appointments/open_24/&ltstr:council_number&gt/</b><br>
<b>appointments/open/&ltstr:council_number&gt/</b><br>

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

Para ter acesso ao descrições detalhes das rotas e seus retornos, conferir documentação completa neste [link](https://insomnia-nhes2xv3h-abkuras-projects.vercel.app/#req_3aa20fbf10544effb17218fe1a267ff0).

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
- [PyWhatKit](https://pypi.org/project/pywhatkit/)
- [sendmail](https://docs.djangoproject.com/en/5.1/topics/email/)
- [SQLite3](https://docs.python.org/3/library/sqlite3.html)
- [Visual Studio Code (VSCode)](https://code.visualstudio.com/)

<br>

## Termos de uso

Esse projeto atende a fins exclusivamente didáticos e sem nenhum intuito comercial.
