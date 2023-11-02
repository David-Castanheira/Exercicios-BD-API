from sqlalchemy import create_engine
from sqlalchemy.sql import text

#eu nao estou usando um servidor, como MySQL,
#ou postgres.
#estou usando essa biblioteca sqlite3, 
#que cria meu banco de dados em um arquivo.
#tanto que eu posso mandar esse arquivo para o site
#sqliteonline.com e todos os dados estão lá

engine = create_engine('sqlite:///rpg.db') #abre esse arquivo como se fosse um banco de dados
                                           # o arquivo no caso é rpg.db, da pasta atual

# sqlalchemy.create_engine("mysql://root:123456@localhost:3306/aula")
# bancodedados://usuario:senha@nomedamaquina:porta/tabela

class JogadorNaoExisteException(Exception):
    pass

def consultar_jogador(id_j):
    with engine.connect() as con:  #conecta no meu banco de dados
        #query com "buraco" com o nome jogador    
        statement = text ("""SELECT * FROM Jogador WHERE id = :jogador""") 
        # :jogador -> buraco que vai ser preenchido quando eu chamar con.execute
        # :jogador -> O ":" marca o buraco. Sem ":" nao tem buraco, e coisas estranhas vao acontecer
        
        rs = con.execute(statement, jogador=id_j) #e usei esse buraco
        jogadores = rs.fetchall()                 #pega todos os resultados
        if jogadores == []:                       #se nao tinha nenhuma linha
            raise JogadorNaoExisteException
        return dict(jogadores[0])                   #converte o jogador para dicionário
        
def conta_jogadores():
    with engine.connect() as con:    
        statement = text ("""SELECT * FROM Jogador""") #todos os jogadores
        rs = con.execute(statement) 
        jogadores = len(rs.fetchall()) 
        return jogadores


# OPCIONAL

# fetchall é perigoso. 
# Monta uma lista com todas as linhas que vieram da query. 
# Pode encher a sua RAM (se o banco for grande)

# Alternativa ? fetchone: pega o "próximo" jogador, e retorna None
# se não tem mais nenhum

def conta_jogadores2():
    with engine.connect() as con:    
        statement = text ("""SELECT * FROM Jogador""") #todos os jogadores
        rs = con.execute(statement) 
        jogadores = 0
        while (rs.fetchone() != None): # Pego um jogador. Uma linha do resultado. 
                                       # Se acabaram os jogadores, vou receber um None
            jogadores += 1
        return jogadores

#fetch one
#pega  um

#fetch all
#pega todos

#fetch many
#pega muitos

def consultar_jogador2(id_j):
    with engine.connect() as con:  #conecta no meu banco de dados
        #query com "buraco" com o nome jogador    
        statement = text ("""SELECT * FROM Jogador WHERE id = :jogador""") 
        # :jogador -> buraco que vai ser preenchido quando eu chamar con.execute
        # :jogador -> O ":" marca o buraco. Sem ":" nao tem buraco, e coisas estranhas vao acontecer
        
        rs = con.execute(statement, jogador=id_j) #e usei esse buraco
        jogador = rs.fetchone()                   #pega a primeira linha do resultado
        if jogador == None:                       #se nao tinha nenhuma linha, 
                                                  #jogador vale None
                                                  # (None tb aparece quando a gente
                                                  # já leu várias linhas e acabou 
                                                  # a consulta)
            raise JogadorNaoExisteException
        return dict(jogador)                      #converte o jogador para dicionário

def jogador_por_email(email):
    with engine.connect() as con:   #conecta e depois desconecta automaticamente :) 
        statement = text ("""SELECT * FROM Jogador WHERE email = :email""")
        rs = con.execute(statement, email=email) 
        jogador = rs.fetchone() 
        if jogador == None: 
            raise JogadorNaoExisteException
        return dict(jogador) 