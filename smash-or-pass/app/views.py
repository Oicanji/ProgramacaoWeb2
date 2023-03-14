from flask import Blueprint
from flask import render_template
from flask_login import login_required, current_user
from flask import request, jsonify

from .models import *

views = Blueprint('views', __name__)

@views.route('/')
def home():
    # get user name to display on the page
    user = current_user

    return render_template("pages/home.html", user=user)

# '/cadastrar'
# Caso venha o parâmetro 'id', verificar se o 'id' corresponde a um quiz editável pelo usuário, se sim pegar e enviar o objeto com todas as informações do quiz, menos a categoria e perguntas, já vou pedir elas...
# Caso não enviar o objeto da mesma forma mais com valor de NULL.
@views.route('/cadastrar', methods=['GET'])
def cadastrar_quiz():
    id = request.args.get('id')
    args = '{}'
    if id:
        quiz = Quiz.query.filter_by(id=id).first()
        if quiz:
            if quiz.user_id == current_user.id:
                args = jsonify(quiz)
    
    return render_template("pages/cadastrar.html", args=args)

# '/get/quiz'
# Pega com um id o valor, negocio pra iniciar um quiz ou fazer a rota de cima.
# Me devolva um json com todos os valores dentro de um data:
# data = { nome: ... }.
@views.route('/get/quiz/<int:id>', methods=['GET'])
def get_quiz(id):
    quiz = Quiz.query.filter_by(id=id).first()
    if quiz:
        if quiz.user_id == current_user.id:
            return jsonify(quiz)
    return jsonify({})

# '/get/category'
# Caso venha um parâmetro 'id', pegar referente a relação do listCategories.
# Pega um do parâmetro 'from' ao parâmetro 'to' do banco, caso não venha o parâmetro, enviar do 0 até o 25.
@views.route('/get/category', methods=['GET'])
def get_category():
    id = request.args.get('id')
    from_ = request.args.get('from')
    to = request.args.get('to')
    if id:
        category = Category.query.filter_by(id=id).first()
        if category:
            return jsonify(category)
    if from_ and to:
        categories = Category.query.filter_by(id=id).first()
        if categories:
            return jsonify(categories)
    return jsonify({})

# '/get/question'
# Verificar se o parâmetro enviado como 'id' pertence ao user.
# Enviar todas as questões nesse formato json na ordem:
# data { response = [...] }

# '/set/answers'
# Vou enviar um json 'data', que vai ficar nessa estrutura:
# data { response = [...] }

# '/set/category'
# Vou te enviar um json da seguinte forma:
# data {
#   name
#   color: #hex;
# }

# '/set/category_to_quiz'
# Vou te mandar um parâmetro 'category_id' e um 'quiz_id' e faz o teu, só lembra de ver que a sessão pode assinar naquele quiz.

# '/set/question'
# Vou te mandar um json da seguinte forma:
# data {
#   name
#   image: "vai ter a url aqui"
#   quiz_id
#   atributes "negocio que eu esqueci, deixa isso só no front mesmo, eu me viro"
# }
# Só lembra da parada de ver se a sessão pode apontar para esse quiz.

# '/set/quiz'
# Vou te enviar um json gigante toma:
# data {
#   name, description, super_allow_alias, allow_alias, deny_alias, super_allow_color, allow_color, deny_color
# }

# '/quiz'
# Vou te mandar um 'id' tu retorna só as info, que no caso, aqui é onde o usuário acessa a ferramenta.

# '/get/anwsers'
# Te passo 'id"
# Quiero:
# data: { results = [...] }
# JSON favorcito
# Y...
# Vê se não precisa ver o o quiz é do usuário pois qualquer usuário pode fazer um quiz.
