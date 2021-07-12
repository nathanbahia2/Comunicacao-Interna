from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_ocorrencia(ocorrencia):
    filial = ocorrencia.funcionario.filial
    emails = [user.email for user in filial.emailresponsaveis_set.all()]

    if emails:
        title = f'{ocorrencia.funcionario.filial.nome} - {ocorrencia.get_motivo_display} - {ocorrencia.funcionario.nome}'
        html_content = f"""
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

        text_content = title
        from_mail = settings.EMAIL_HOST_USER
        msg = EmailMultiAlternatives(
            title,
            text_content,
            from_email=from_mail,
            to=emails
        )
        msg.attach_alternative(html_content, "text/html")
        try:
            msg.send()

        except Exception as e:
            print(e)


def send_elogio(elogio):
    filial = elogio.funcionario.filial
    emails = [user.email for user in filial.emailresponsaveis_set.all()]

    if emails:
        title = f'{elogio.funcionario.filial.nome} - {elogio.funcionario.nome}'
        html_content = f"""
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

        text_content = title
        from_mail = settings.EMAIL_HOST_USER
        msg = EmailMultiAlternatives(
            title,
            text_content,
            from_email=from_mail,
            to=emails
        )
        msg.attach_alternative(html_content, "text/html")
        try:
            msg.send()

        except Exception as e:
            print(e)
