from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

def get_conexao():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="usuario",
        port=3306,
        use_pure=True
    )

# HOME
@app.route("/home")
def home():
    return render_template("home.html")

# FORMOSA
@app.route("/usuarios")
def usuarios():
    conexao = get_conexao()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
            SELECT 
                ROW_NUMBER() OVER (ORDER BY inicio DESC, fim DESC) AS ordem,
                id,
                nome,
                inicio,
                fim
            FROM informacoes_formosa;
    """)

    usuarios = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template("usuarios.html", usuarios=usuarios)

if __name__ == "__main__":
    app.run(debug=True, port=5002)
