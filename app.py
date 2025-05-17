import os
import requests
from flask import Flask, request, jsonify, render_template, send_from_directory

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/SEU_WEBHOOK_AQUI"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/autenticar', methods=['POST'])
def autenticar():
    dados = request.json

    if not all(key in dados for key in ['id', 'nome', 'nick', 'idade']):
        return jsonify({"mensagem": "Preencha todos os campos!"}), 400

    mensagem_discord = {
        "content": f"✅ Usuário autenticado!\n**Nome:** {dados['nome']}\n**Nick:** {dados['nick']}\n**ID:** {dados['id']}\n**Idade:** {dados['idade']}"
    }

    try:
        requests.post(DISCORD_WEBHOOK_URL, json=mensagem_discord)
    except Exception as e:
        print(f"Erro ao enviar mensagem para o Discord: {e}")

    return jsonify({"mensagem": f"Bem-vindo, {dados['nick']}! Autenticação bem-sucedida."}), 200

@app.route('/public/<path:nome_arquivo>')
def public_files(nome_arquivo):
    return send_from_directory("static", nome_arquivo)

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)