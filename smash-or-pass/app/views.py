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
                args = '{"code": 200, "message": "Quiz encontrado", "action": "edit", "quiz": ' + str(quiz) + '}'
            else:
                args = '{"code": 403, "message": "Você não tem permissão para editar esse quiz", "action": "create", "quiz": "{}"}'
        else:
            args = '{"code": 404, "message": "Quiz não encontrado", "action": "create", "quiz": "{}"}'
    else:
        args = '{"code": 400, "message": "Parâmetro id não enviado", "action": "create", "quiz": "{}"}'
            
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
@views.route('/get/question', methods=['GET'])
def get_question():
    id = request.args.get('id')
    if id:
        question = Question.query.filter_by(id=id).first()
        if question:
            return jsonify(question)
    return jsonify({})

# '/set/answers'
# Cadastrar as respostas do usuário
# data { response = [...] }
@views.route('/set/answers', methods=['POST'])
def set_answers():
    data = request.get_json()
    if data:
        for answer in data['response']:
            if answer['id'] and answer['answer']:
                answer = Answer.query.filter_by(id=answer['id']).first()
                if answer:
                    answer.answer = answer['answer']
                    db.session.commit()
    
    return jsonify({'code': 200, 'message': 'Respostas cadastradas com sucesso'})

# '/set/category'
# Vou te enviar um json da seguinte forma:
# data {
#   name
#   color: #hex;
# }
@views.route('/set/category', methods=['POST'])
def set_category():
    data = request.get_json()
    if data:
        category = Category(name=data['name'], color=data['color'])
        db.session.add(category)
        db.session.commit()
        return jsonify({'code': 200, 'message': 'Categoria cadastrada com sucesso'})
    return jsonify({'code': 400, 'message': 'Parâmetros inválidos'})

# '/set/category_to_quiz'
# Vou te mandar um parâmetro 'category_id' e um 'quiz_id' e faz o teu, só lembra de ver que a sessão pode assinar naquele quiz.
@views.route('/set/category_to_quiz', methods=['POST'])
def set_category_to_quiz():
    category_id = request.args.get('category_id')
    quiz_id = request.args.get('quiz_id')
    if category_id and quiz_id:
        quiz = Quiz.query.filter_by(id=quiz_id).first()
        if quiz:
            if quiz.user_id == current_user.id:
                quiz.category_id = category_id
                db.session.commit()
                return jsonify({'code': 200, 'message': 'Categoria adicionada com sucesso'})
            else:
                return jsonify({'code': 403, 'message': 'Acesso negado'})
        else:
            return jsonify({'code': 404, 'message': 'Quiz não encontrado'})
    else:
        return jsonify({'code': 400, 'message': 'Parâmetros inválidos'})


# '/set/question'
# Vou te mandar um json da seguinte forma:
# data {
#   name
#   image: "vai ter a url aqui"
#   quiz_id
#   atributes "negocio que eu esqueci, deixa isso só no front mesmo, eu me viro"
# }
# Só lembra da parada de ver se a sessão pode apontar para esse quiz.
@views.route('/set/question', methods=['POST'])
def set_question():
    data = request.get_json()
    if data:
        if data['quiz_id']:
            quiz = Quiz.query.filter_by(id=data['quiz_id']).first()
            if quiz:
                if quiz.user_id == current_user.id:
                    question = Question(name=data['name'], image=data['image'], quiz_id=data['quiz_id'], atributes=data['atributes'])
                    db.session.add(question)
                    db.session.commit()
                    return jsonify({'code': 200, 'message': 'Questão adicionada com sucesso'})
                else:
                    return jsonify({'code': 403, 'message': 'Acesso negado'})
            else:
                return jsonify({'code': 404, 'message': 'Quiz não encontrado'})
        else:
            return jsonify({'code': 400, 'message': 'Parâmetros inválidos'})
    else:
        return jsonify({'code': 400, 'message': 'Parâmetros inválidos'})

# '/set/quiz'
# Vou te enviar um json gigante toma:
# data {
#   name, description, create_by, super_allow_alias, allow_alias, deny_alias, super_allow_color, allow_color, deny_color
# }
@views.route('/set/quiz', methods=['POST'])
def set_quiz():
    data = request.get_json()
    if data:
        if data['name'] and data['description'] and data['create_by'] and data['super_allow_alias'] and data['allow_alias'] and data['deny_alias'] and data['super_allow_color'] and data['allow_color'] and data['deny_color']:
            if data['create_by'] == current_user.id:
                quiz = Quiz(name=data['name'], description=data['description'], create_by=data['create_by'], super_allow_alias=data['super_allow_alias'], allow_alias=data['allow_alias'], deny_alias=data['deny_alias'], super_allow_color=data['super_allow_color'], allow_color=data['allow_color'], deny_color=data['deny_color'])
                db.session.add(quiz)
                db.session.commit()
                return jsonify({'code': 200, 'message': 'Quiz criado com sucesso', 'results': quiz})
            else:
                return jsonify({'code': 403, 'message': 'Acesso negado', 'results': {}})
        else:
            return jsonify({'code': 400, 'message': 'Parâmetros inválidos', 'results': {}})
    else:
        return jsonify({'code': 400, 'message': 'Parâmetros inválidos', 'results': {}})

# '/quiz'
# Vou te mandar um 'id' tu retorna só as info, que no caso, aqui é onde o usuário acessa a ferramenta.
@views.route('/quiz', methods=['GET'])
def quiz():
    id = request.args.get('id')
    if id:
        quiz = Quiz.query.filter_by(id=id).first()
        if quiz:
            return jsonify({'code': 200, 'message': 'Quiz encontrado.', 'results': quiz})
        else:
            return jsonify({'code': 400, 'message': 'Parâmetros inválidos', 'results': {}})
    return jsonify({'code': 404, 'message': 'Quiz não encontrado', 'results': {}})

# '/get/anwsers'
# Te passo 'id"
# Quiero:
# data: { results = [...] }
# JSON favorcito
# Y...
# Vê se não precisa ver o o quiz é do usuário pois qualquer usuário pode fazer um quiz.
@views.route('/get/answers', methods=['GET'])
def get_answers():
    id = request.args.get('id')
    if id:
        answers = Answer.query.filter_by(question_id=id).all()
        if answers:
            return jsonify({'code': 200, 'message': 'Respostas encontradas', 'results': answers})
        else:
            return jsonify({'code': 404, 'message': 'Nenhuma resposta encontrada', 'results': {}})
    else:
        return jsonify({'code': 400, 'message': 'Parâmetros inválidos', 'results': {}})