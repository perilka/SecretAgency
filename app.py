from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Настройка базы данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация базы данных
db = SQLAlchemy(app)

# Модель задачи (таблица Task)
class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    number = db.Column(db.Integer(), nullable=False)
    email = db.Column(db.String, nullable=False)
    level = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Agent {self.name}>"

# Создаем таблицу в базе данных
with app.app_context():
    db.create_all()

#Главная страница: список агентов
@app.route('/', methods=['GET', 'POST'])
@app.route('/agents', methods=['GET', 'POST'])
def get_agents():
    if request.method == "GET":
        search_query = request.args.get('search', '').strip()
        if search_query:
            agents = Agent.query.filter(Agent.name.ilike(f'%{search_query}%')).all()
        else:
            agents = Agent.query.all()
        return render_template('agents.html', agents=agents)
    agents = Agent.query.all()
    return render_template('agents.html', agents=agents)

#Добавление нового агента
@app.route('/add', methods=['GET', 'POST'])
def add_agent():
    if request.method == 'POST':
        name = request.form['name']
        number = request.form['number']
        email = request.form['email']
        level = request.form['level']
        if name.strip() and number.strip() and email.strip():
            new_agent = Agent(name=name, number=number, email=email, level=level)
            db.session.add(new_agent)
            db.session.commit()
            return redirect(url_for('get_agents'))
        return render_template('error_input.html')
    return render_template('add_agent.html')

# 📌 Редактирование задачи
@app.route('/agent/<int:id>')
def show_agent(id):
    agent = Agent.query.get_or_404(id)
    name = agent.name
    number = agent.number
    email = agent.email
    level = agent.level
    return render_template('show_agent.html', id=id, name=name, number=number, email=email, level=level)

@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit_agent(id):
    agent = Agent.query.get_or_404(id)
    name = agent.name
    number = agent.number
    email = agent.email
    level = agent.level
    if request.method == 'POST':
        new_name = request.form['name']
        new_number = request.form['number']
        new_email = request.form['email']
        new_level = request.form['level']
        if new_name.strip() and new_number.strip() and new_email.strip():
            agent.name = new_name
            agent.number = new_number
            agent.email = new_email
            agent.level = new_level
            db.session.commit()
            return redirect(url_for('show_agent', id=id))
        return render_template('error_edit.html', id=id, name=name, number=number, email=email, level=level)
    return render_template('edit_agent.html', id=id, name=name, number=number, email=email, level=level)

# 📌 Удаление задачи
@app.route('/delete/<int:id>')
def delete_agent(id):
    agent = Agent.query.get_or_404(id)  # Получаем задачу по ID
    db.session.delete(agent)  # Удаляем из базы
    db.session.commit()  # Подтверждаем изменения
    return redirect(url_for('get_agents'))

@app.route("/random", methods=["POST", "GET"])
def get_random_name():
    if request.method == 'POST':
        name = request.form['name']
        number = request.form['number']
        email = request.form['email']
        level = request.form['level']
        if name.strip() and number.strip() and email.strip():
            new_agent = Agent(name=name, number=number, email=email, level=level)
            db.session.add(new_agent)
            db.session.commit()
            return redirect(url_for('get_agents'))
        return render_template('error_input.html')
    import random
    consonants = [chr(i) for i in range(65, 91) if chr(i) not in 'AEIOU']
    random_name = random.choice(consonants) + 'u' + random.choice(consonants) + 'a'
    return render_template('add_agent.html', random_name=random_name.capitalize())

# Запуск сервера
if __name__ == "__main__":
    app.run(debug=True)