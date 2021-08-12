# Sistema de comunicação interna

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