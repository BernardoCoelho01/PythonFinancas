import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import mplcyberpunk

# Pegar cotações históricas dos ativos selecionados abaixo:
tickers = ['^BVSP', '^GSPC', 'BRL=X']

# Tabela Original:
dados_mercado = yf.download(tickers, period='6mo')
# Tabela Manipulada
dados_mercado = dados_mercado['Adj Close']

# Tabela Manipulada
dados_mercado = dados_mercado.dropna() # Limpar dias que a bolsa não operou (feriados)

dados_mercado.columns = ["DOLAR", "IBOVESPA", "S&P500"] # nomeando colunas

# Gráfico de performance
plt.style.use('cyberpunk')

# IBOVESPA
fig, ax = plt.subplots()
ax.plot(dados_mercado['IBOVESPA'])
ax.set_title('Ibovespa')
plt.savefig('imagens/Ibovespa.png')

# S&P500
fig, ax = plt.subplots()
ax.plot(dados_mercado['S&P500'])
ax.set_title('S&P500')
plt.savefig('imagens/S&P500.png')

# DÓLAR
fig, ax = plt.subplots()
ax.plot(dados_mercado['DOLAR'])
ax.set_title('Dolar')
plt.savefig('imagens/Dolar.png')

# Calculando retorno diário:
retornos_diarios = dados_mercado.pct_change(periods= 5).dropna() * 100

data_hora = retornos_diarios.iloc[-1].name
data = data_hora.date()

# Fechamento diário em tempo real:
retorno_dolar = retornos_diarios['DOLAR'].iloc[-1]
retorno_dolar = str(round(retorno_dolar, 2)) + '%'
print(f'USD: {retorno_dolar}')

retorno_sep = retornos_diarios['S&P500'].iloc[-1]
retorno_sep = str(round(retorno_sep, 2)) + '%'
print(f'S%P500: {retorno_sep}')

retorno_ibov = retornos_diarios['IBOVESPA'].iloc[-1]
retorno_ibov = str(round(retorno_ibov, 2)) + '%'
print(f'IBOVESPA: {retorno_ibov}')

# Configurando envio por e-mail:
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Definindo a lista de caminhos de arquivo de imagem
image_paths = ['imagens/Ibovespa.png', 'imagens/S&P500.png', 'imagens/Dolar.png']

# Criando o objeto MIMEMultipart
msg = MIMEMultipart('related')

# Adicione o texto do email
msg_text = MIMEText(f'<h1>Gráficos de Performance Semestral</h1><p>Retorno Diário ({data}) IBOVESPA: {retorno_ibov}<p><img src="cid:image1"><p><p><br>Retorno Diário ({data}) S&P500: {retorno_sep}<p><img src="cid:image2"><p><p><br>Retorno Diário ({data}) DÓLAR: {retorno_dolar}<p><img src="cid:image3"></p>', 'html')
msg.attach(msg_text)

# Iterando sobre a lista de caminhos de arquivo de imagem
for i, image_path in enumerate(image_paths):
    # Abrindo o arquivo de imagem
    with open(image_path, 'rb') as file:
        # Criando o objeto MIMEImage
        img = MIMEImage(file.read(), name=os.path.basename(image_path))
        img.add_header('Content-ID', f'<image{i+1}>')
        # Anexando o objeto MIMEImage ao objeto MIMEMultipart
        msg.attach(img)

# Envie o email
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('seu_email@gmail.com', 'seu_código_de_acesso')
server.sendmail('seu_email@gmail.com', 'seu_email@gmail.com', msg.as_string())
server.quit()