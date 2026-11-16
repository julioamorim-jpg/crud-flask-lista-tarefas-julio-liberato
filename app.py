from flask import Flask, render_template, request, redirect
import psycopg2
app = Flask(__name__)

def ligar_banco():
    banco = psycopg2.connect(
        database="Viagens",
        host="localhost",
        user="postgres",
        password="senai",
        port="5432"
    )
    return banco

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/viagem/cadastro')
def cadastro_viagem():
    return render_template('cadastrar_viagem.html')


@app.route('/viagem/criar', methods=['POST'])
def cadastro_criar():
    destino=request.form['destino']
    transporte=request.form['transporte']
    dias=int(request.form['dias'])
    orcamento=int(request.form['orcamento'])

    banco = ligar_banco()
    cursor = banco.cursor()
    sql = """
        INSERT INTO viagem
        (destino, transporte, dias, orcamento)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (destino, transporte, dias, orcamento))
    banco.commit()
    cursor.close()
    banco.close()
    return redirect('/viagem/exibir')


@app.route('/viagem/exibir')
def exibir_viagem():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM viagem")
    viagem = cursor.fetchall()
    cursor.close()
    banco.close()
    return render_template('exibir_viagem.html', viagem = viagem)

@app.route('/viagem/editar/<int:id_viagem>')
def editar_viagem(id_viagem):
    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute('SELECT * FROM viagem WHERE id_viagem = %s',
                   (id_viagem,))

    viagem = cursor.fetchone()
    cursor.close()
    banco.close()
    return render_template('editar_viagem.html', viagem = viagem )


@app.route('/viagem/alterar/<int:id_viagem>', methods=['POST'])
def alterar_viagem(id_viagem):
    destino = request.form['destino']
    transporte = request.form['transporte']
    dias = request.form['dias']
    orcamento = request.form['orcamento']
    banco = ligar_banco()
    cursor = banco.cursor()
    sql = """
        UPDATE viagem SET destino = %s, transporte = %s, dias = %s, 
            orcamento = %s WHERE id_viagem = %s
    """
    cursor.execute(sql, (destino, transporte, dias, orcamento, id_viagem))
    banco.commit()
    cursor.close()
    banco.close()
    return redirect('/viagem/exibir')

@app.route('/viagem/excluir/<int:id_viagem>')
def excluir_viagem(id_viagem):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute( "DELETE FROM viagem WHERE id_viagem = %s",
        (id_viagem,))
    banco.commit()
    cursor.close()
    banco.close()
    return redirect('/viagem/exibir')


#parte lib

@app.route('/criarhotel',methods=['POST'])
def criar():
    nome = request.form['nome']
    cidade = request.form['cidade']
    estrelas = request.form['estrelas']
    diaria = request.form['diaria']
    banco = ligar_banco()
    cursor = banco.cursor()
    sql = """
          INSERT INTO hotel (nome, cidade, estrelas, diaria)
          VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (nome, cidade, estrelas, diaria))
    banco.commit()
    cursor.close()
    banco.close()
    return redirect('/exibirhotel')



@app.route('/exibirhotel')
def exibir():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM hotel")
    lista = cursor.fetchall()
    cursor.close()
    banco.close()
    return render_template('exibir_hotel.html', lista=lista)




@app.route('/editarhotel/<int:id_hotel>')
def editar(id_hotel):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute(
        'SELECT * FROM hotel WHERE id_hotel = %s',
        (id_hotel,)
    )
    hotel = cursor.fetchone()
    cursor.close()
    banco.close()
    return render_template('editar_hotel.html', hotel=hotel)



@app.route('/alterarhotel/<int:id_hotel>', methods=['POST'])
def alterar(id_hotel):
    nome = request.form['nome']
    cidade = request.form['cidade']
    estrelas = request.form['estrelas']
    diaria = request.form['diaria']
    banco = ligar_banco()
    cursor = banco.cursor()
    sql = """
        UPDATE hotel SET nome = %s, cidade = %s, estrelas = %s, diaria = %s  WHERE id_hotel = %s
    """
    cursor.execute( sql, (nome, cidade, estrelas, diaria, id_hotel))
    banco.commit()
    cursor.close()
    banco.close()
    return redirect('/exibirhotel')



@app.route('/excluirhotel/<id_hotel>')
def excluir(id_hotel):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute(
        'DELETE FROM hotel WHERE id_hotel = %s',
        (id_hotel,)
    )
    banco.commit()
    cursor.close()
    banco.close()
    return redirect('/exibirhotel')



@app.route('/cadastrohotel')
def cadastro():
    return render_template('cadastro_hotel.html')

if __name__ == '__main__':
    app.run()
