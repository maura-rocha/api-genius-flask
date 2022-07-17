#  API REST que consume a API do Genius 
Essa API tem como objetivo consume a API do Geniu para retornar as 10 músicas mais populares do artista pesquisado.


## Requisitos:
Python 3.10
Conta no Genius API, Redis Server , DynamoDB  e Conta no Genius API

Instale, crie e ative a virtualenv em sua máquina e instale as bibliotecas.

Para fazer a instalação use o comando: pip install -r requirements.txt

Existe um arquivo chamado exemple.env. Edite esse arquivo com suas credenciais AWS e Genius e renomei para apenas .env. 

Para rodar a aplicação, use python app.py

Para fazer uma consulta buscando por nome do artista:

http://127.0.0.1:5000/app/artist/Nome Artista
