from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__, static_folder='static') 

# Arquivo onde os dados serão salvos
JSON_FILE = 'confirmacoes.json'

def load_data():
    """Carrega os dados do arquivo JSON"""
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_data(data):
    """Salva os dados no arquivo JSON"""
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/confirmar', methods=['POST'])
def confirmar():
    nome = request.form['nome']
    telefone = request.form['telefone']
    presenca = request.form['presenca']
    mensagem = request.form.get('mensagem', '')

    # Carrega dados existentes
    confirmados = load_data()
    
    # Adiciona nova confirmação
    confirmados.append({
        "nome": nome,
        "telefone": telefone,
        "presenca": presenca,
        "mensagem": mensagem
    })

    # Salva no arquivo
    save_data(confirmados)

    if presenca == 'sim':
        return redirect(url_for('obrigado', nome=nome, resposta='confirmada'))
    else:
        return redirect(url_for('obrigado', nome=nome, resposta='recusada'))

@app.route('/obrigado')
def obrigado():
    nome = request.args.get('nome')
    resposta = request.args.get('resposta')
    return render_template('obrigado.html', nome=nome, resposta=resposta)

@app.route('/lista')
def lista():
    confirmados = load_data()
    return render_template('lista.html', confirmados=confirmados)

if __name__ == '__main__':
    app.run(debug=True)