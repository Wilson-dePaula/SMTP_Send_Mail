#Robô Whatsapp

# Essa automação tem como objetivo enviar mensagens individuais e automáticas
# pelo gmail com base em uma lista de contatos

# Desenvolvedor: Wilson de Paula Alves
# Ano: 2022

#-----------------------------------------

import smtplib
import email.message
import time
from datetime import datetime, timedelta
import logging
import pandas as pd
import sys
import random


log_format = '%(asctime)s %(message)s'
logging.basicConfig(filename='Robô_Email.log',
                    filemode='a',
                    level=logging.INFO,
                    format=log_format)
logger = logging.getLogger('root')

logger.info('Iniciando Robô')
#saudacao
hora = datetime.now().hour
if hora < 12:
    saudacao = "Bom dia"
elif 12 <= hora < 18:
    saudacao = "Boa tarde"
else:
    saudacao = "Boa noite"

logger.info('Saudação linda com sucesso')

#Ler base
tabela_contatos = pd.read_csv('contatos.csv', delimiter=";", encoding='utf-8')
tabela_contatos = tabela_contatos.replace('servidor publico', "servidor público")

logger.info('Base de contatos lida com sucesso')

#Range horas rodando
now = datetime.now()
end_cod = now + timedelta(minutes=55)
logger.info('Horário limite estabelecido')

#ler ultimo contato enviado
with open('contador_contatos.txt', 'r') as cont:
    ultimo_contato = int(cont.read())

logger.info('Arquivo contador ok')

if __name__ == "__main__":
    while now < end_cod:
        wait_t = random.randint(75, 105)

        if len(tabela_contatos['Nome']) <= ultimo_contato:
            break

        try:
            #Ler nome
            pessoa = tabela_contatos.loc[ultimo_contato, 'Nome']
            email_contatos = tabela_contatos.loc[ultimo_contato, 'Email']
            orgao = tabela_contatos.loc[ultimo_contato, 'Orgao']
            preposicao = tabela_contatos.loc[ultimo_contato, 'Preposicao']

            # configurar as informações do seu e-mail

            corpo_email = f"""
            <p>Fala {pessoa}, {saudacao}!</p>
            """

            msg = email.message.Message()
            msg['Subject'] = "Teste Gmail"
            msg['From'] = 'roboteste@gmail.com'
            msg['To'] = f"{email_contatos}"
            password = 'cugqojbtinseuwec'
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(corpo_email)

            s = smtplib.SMTP('smtp.gmail.com: 587')
            s.starttls()
            # Login Credentials for sending the mail
            s.login(msg['From'], password)
            s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))

            logger.info('Email enviado')
            print("Email Enviado")
            tabela_contatos.loc[ultimo_contato, 'Status'] = 'Email Enviado'
            tabela_contatos.to_csv('contatos.csv', sep=';', index=False)
            print(wait_t)
            time.sleep(wait_t)

            with open("contador_contatos.txt", "w") as cont:
                ultimo_contato += 1
                cont.write(str(ultimo_contato))
        except:
            logger.info('Erro ao enviar email')
            print('Erro')
            tabela_contatos.loc[ultimo_contato, 'Status'] = 'Erro no envio da email'
            tabela_contatos.to_csv('contatos.csv', sep=';', index=False)
            sys.exit()

        now = datetime.now()

print('Fim da execução')
sys.exit()