# app.py

from flask import Flask, render_template, request, redirect, url_for

# Inicializa a aplicação Flask
app = Flask(__name__)

# --- Base de Dados Simples (em memória) ---
# Em uma aplicação real, isso seria substituído por um banco de dados (SQLite, PostgreSQL, etc.)
clientes_devedores = [
    {
        'id': 1,
        'nome': 'João da Silva',
        'contato': 'joao.silva@email.com',
        'valor_divida': 1500.50,
        'data_vencimento': '2025-08-20',
        'status': 'Pendente' # Status pode ser: Pendente, Em Negociação, Pago
    },
    {
        'id': 2,
        'nome': 'Maria Oliveira',
        'contato': '(11) 98765-4321',
        'valor_divida': 850.00,
        'data_vencimento': '2025-07-15',
        'status': 'Em Negociação'
    }
]
# Para gerar IDs únicos para novos clientes
next_id = 3

# --- Rotas da Aplicação ---

# Rota principal: exibe a lista de devedores
@app.route('/')
def index():
    """Renderiza a página inicial com a lista de clientes."""
    return render_template('index.html', clientes=clientes_devedores)

# Rota para adicionar um novo cliente devedor
@app.route('/adicionar', methods=['POST'])
def adicionar_cliente():
    """Adiciona um novo cliente à lista."""
    global next_id
    
    # Coleta os dados do formulário
    nome = request.form['nome']
    contato = request.form['contato']
    valor_divida = float(request.form['valor_divida'])
    data_vencimento = request.form['data_vencimento']
    
    # Cria o novo cliente
    novo_cliente = {
        'id': next_id,
        'nome': nome,
        'contato': contato,
        'valor_divida': valor_divida,
        'data_vencimento': data_vencimento,
        'status': 'Pendente' # Status inicial padrão
    }
    
    # Adiciona à "base de dados" e incrementa o ID
    clientes_devedores.append(novo_cliente)
    next_id += 1
    
    # Redireciona de volta para a página inicial
    return redirect(url_for('index'))

# Rota para atualizar o status de uma dívida
@app.route('/atualizar/<int:cliente_id>', methods=['POST'])
def atualizar_status(cliente_id):
    """Atualiza o status de um cliente específico."""
    novo_status = request.form['status']
    
    # Encontra o cliente pelo ID e atualiza o status
    for cliente in clientes_devedores:
        if cliente['id'] == cliente_id:
            cliente['status'] = novo_status
            break
            
    return redirect(url_for('index'))

# Rota para deletar um cliente
@app.route('/deletar/<int:cliente_id>', methods=['POST'])
def deletar_cliente(cliente_id):
    """Remove um cliente da lista."""
    global clientes_devedores
    clientes_devedores = [c for c in clientes_devedores if c['id'] != cliente_id]
    
    return redirect(url_for('index'))

# --- Execução da Aplicação ---
if __name__ == '__main__':
    app.run(debug=True)