from sqlalchemy import create_engine
from sqlalchemy.sql import text

engine = create_engine('sqlite:///rpg.db')
class HeroiNaoExisteException(Exception):
    pass

#funções adicionais implementadas abaixo

def heroi_existe(id_h):
    with engine.connect() as con:  #conecta no meu banco de dados
        #query com "buraco" com o nome heroi    
        statement = text ('SELECT * FROM Heroi WHERE id = :heroi')
        # :jogador -> buraco que vai ser preenchido quando eu chamar con.execute
        # :jogador -> O ":" marca o buraco. Sem ":" nao tem buraco, e coisas estranhas vao acontecer
       
        rs = con.execute(statement, heroi=id_h) #e usei esse buraco
        herois = rs.fetchall()                 #pega todos os resultados
        if herois == []:                       #se nao tinha nenhuma linha
            return False
        return True

def consultar_heroi(id_h):
    with engine.connect() as con: 
        statement = text ("""SELECT * FROM Heroi WHERE id = :heroi""")
        rs = con.execute(statement, heroi=id_h)
        herois = rs.fetchall()
        if herois == []:
            raise HeroiNaoExisteException
        return dict(herois[0])

def consulta_por_nome(nome_heroi):
    with engine.connect() as con:
        statement = text ("""SELECT * FROM Heroi WHERE nome = :name""")
        rs = con.execute(statement, name=nome_heroi)
        nomes_heroi = rs.fetchall()
        if nomes_heroi == []:
            raise HeroiNaoExisteException
        return dict(nomes_heroi[0])

