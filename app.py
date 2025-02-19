from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sus.db'  # Banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo do banco de dados
class Noticia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)

# Criar banco de dados
with app.app_context():
    db.create_all()

# Página inicial (exibe as notícias)
@app.route('/')
def index():
    noticias = Noticia.query.all()
    return render_template('index.html', noticias=noticias)

# Página para adicionar notícias
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        titulo = request.form['titulo']
        conteudo = request.form['conteudo']
        categoria = request.form['categoria']
        nova_noticia = Noticia(titulo=titulo, conteudo=conteudo, categoria=categoria)
        db.session.add(nova_noticia)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('adicionar.html')

if __name__ == "__main__":
    app.run(debug=True)
