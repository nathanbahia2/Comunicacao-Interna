from apps.core import models
import requests

from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from decouple import config


URL_APIGMAIL = config('URL_APIGMAIL')
ID_APIGMAIL = config('ID_APIGMAIL')
USER_APIGMAIL = config('USER_APIGMAIL')
PASSWORD_APIGMAIL = config('PASSWORD_APIGMAIL')


def send_ocorrencia(ocorrencia):
    filial = ocorrencia.funcionario.filial
    emails = ",".join([user.email for user in filial.emailresponsaveis_set.all()])

    if emails:
        assunto = f'{ocorrencia.funcionario.filial.nome} - {ocorrencia.get_motivo_display} - {ocorrencia.funcionario.nome}'
        mensagem = f"""
            <div style="text-align: center">
                <img src="https://casadoscereaissupercenter.pythonanywhere.com/static/images/logo.png" width="300" />
            </div>
            <h1 style="background-color: red; color: white; text-align: center;">CASA DOS CEREAIS SUPER CENTER</h1>
            <h2 style="text-align: center;">REGISTRO DE OCORRÊNCIAS</h2>
            <hr>
            <p style="font-family: arial; font-size: 14pt;"><b>Data:</b> {ocorrencia.data.strftime('%d/%m/%Y')}</p>
            <p style="font-family: arial; font-size: 14pt;"><b>Motivo:</b> {ocorrencia.get_motivo_display}</p>
            <p style="font-family: arial; font-size: 14pt;"><b>Funcionário:</b> {ocorrencia.funcionario.nome}</p>
            <p style="font-family: arial; font-size: 14pt;"><b>Cargo:</b> {ocorrencia.funcionario.cargo.nome}</p>
            <p style="font-family: arial; font-size: 14pt;"><b>Filial:</b> {ocorrencia.funcionario.filial}</p>
            <p style="font-family: arial; font-size: 14pt;"><b>Criação:</b> {ocorrencia.cadastro}</p>
            <p style="font-family: arial; font-size: 14pt;"><b>Observação:</b> {ocorrencia.observacao}</p>
            """

        send(
            filial=filial,
            tipo='Ocorrência',
            data={
                "de": ID_APIGMAIL,
                "para": emails,
                "assunto": assunto,
                "mensagem": mensagem
            }
        )


def send_elogio(elogio):
    filial = elogio.funcionario.filial
    emails = ",".join([user.email for user in filial.emailresponsaveis_set.all()])

    if emails:
        assunto = f'{elogio.funcionario.filial.nome} - {elogio.funcionario.nome}'
        mensagem = f"""
            <div style="text-align: center">
                <img src="https://casadoscereaissupercenter.pythonanywhere.com/static/images/logo.png" width="300" />
            </div>
            <h1 style="background-color: red; color: white; text-align: center;">CASA DOS CEREAIS SUPER CENTER</h1>
            <h2 style="text-align: center;">REGISTRO DE ELOGIOS</h2>
            <hr>
            <p style="font-family: arial; font-size: 14pt;"><b>Data:</b> {elogio.data.strftime('%d/%m/%Y')}</p>
            <p style="font-family: arial; font-size: 14pt;"><b>Funcionário:</b> {elogio.funcionario.nome}</p>
            <p style="font-family: arial; font-size: 14pt;"><b>Cargo:</b> {elogio.funcionario.cargo.nome}</p>
            <p style="font-family: arial; font-size: 14pt;"><b>Filial:</b> {elogio.funcionario.filial}</p>
            <p style="font-family: arial; font-size: 14pt;"><b>Criação:</b> {elogio.cadastro}</p>
            <p style="font-family: arial; font-size: 14pt;"><b>Observação:</b> {elogio.observacao}</p>
            """

        send(
            filial=filial,
            tipo='Elogio',
            data={
                "de": ID_APIGMAIL,
                "para": emails,
                "assunto": assunto,
                "mensagem": mensagem
            }
        )


def send(filial, tipo, data):
    email = requests.post(
            url=URL_APIGMAIL,
            auth=(USER_APIGMAIL, PASSWORD_APIGMAIL),
            data=data
        )

    if email.status_code not in [200, 201]:
        models.EmailNaoEntregue.objects.create(
            filial=filial,
            tipo=tipo,
            assunto=data.get('assunto'),
            mensagem=data.get('mensagem'),
            retorno=email.json()
        )
