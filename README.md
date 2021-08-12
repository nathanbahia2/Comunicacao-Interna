# Sistema de comunicação interna

### Sistema desenvolvido para melhorar a comunicação interna de uma empresa na qual atuei como assistente administrativo por 2 anos. Essa é a segunda versão deste sistema que desenvolvo.
### Teve como objetivo eliminar o uso de ocorrências anotadas em papel sobre falhas dos colaboradores e através do envio de e-mails, comunicar imediatamente aos diretores os problemas ocorridos na empresa.

### Nesta segunda versão, utilizei uma comunicação com uma API de envio de e-mails desenvolvida por mim, para que seja possível enviar e-mails via G-mail com uma aplicação hospedada no Heroku.
### Essa API pode ser acessada clicancando aqui: [API-Transmissor-Gmail-PythonAnywhere---Heroku](https://github.com/nathanbahia2/API-Transmissor-Gmail-PythonAnywhere---Heroku)

Para utilização local do sistema, siga os passos abaixo:

```
# Criação do ambiente virtual
python -m venv venv


# Ativação do ambiente virtual

- Windows
venv\script\activate

- Linux e MAC-OS
source venv\bin\activate


# Instalação dos pacotes
pip install -r requirements.txt


# Aplicação das migrações do banco de dados
python manage.py migrate


# Criação de um superusuário
python manage.py createsuperuser


# Execução do servidor local
python manage.py runserver 
```