
import sqlite3
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


##############    LOGICA PROCESSO

def run_process():

    cur.execute("SELECT * FROM Processo;")
    processos = cur.fetchall()

    count = 1
    for p in processos:
        print(str(count) + " - " + p[0])
        count+=1

    opt = int(input("Opção: "))
    print('\n')

    if(opt <= len(processos)):
        opt-=1
        qtd_pools = 0
        qtd_tarefas = 0
        print("O processo " + processos[opt][0] + " tem: ")


    proc_name = input("Qual ")

    return

def add_processo():

    proc_name = input("Process name? ")
    query = "INSERT INTO Processo VALUES ('{}');".format(proc_name)
    cur.execute(query)    
    con.commit()

    input()
    clear_screen()

def remove_processo():

    proc_name = input("Process name? ")    
    query = "DELETE FROM Processo WHERE name = ('{}');".format(proc_name)
    cur.execute(query)
    con.commit()

    input()
    clear_screen()

##############    LOGICA TAREFA 

def add_tarefa():

    task_name = input("Nome da tarefa? ")
    
    print("Qual o tipo da tarefa?")
    print("1 - Normal")
    print("2 - Inicio")
    print("3 - Fim")
    print("4 - Condicional")
    opt = input("Opção: ")

    if(opt == '2'):
        type = 'inicial'

    elif(opt == '3'):
        type = 'final'

    elif(opt == '4'):
        type = 'condicional'

    else:
        type = 'normal'

    query = "INSERT INTO Tarefa(name, type) VALUES ('{}', '{}');".format(task_name, type)
    cur.execute(query)

    query = "INSERT INTO Tarefa_" + type + "(name) VALUES ('{}');".format(task_name)
    cur.execute(query)
    con.commit()

    return task_name

def remove_tarefa():

    task_name = input("Nome da tarefa? ")

    cur.execute("SELECT type FROM Tarefa WHERE name = '{}';".format(task_name))
    type = cur.fetchall()
    type = type[0][0]

    cur.execute("DELETE FROM Tarefa_{} WHERE name = '{}';".format(type, task_name))
    cur.execute("DELETE FROM Tarefa WHERE name = '{}';".format(task_name))
    
    con.commit()

    input()
    clear_screen()

def add_prox_condicional(task_name, type):

    condit1 = input('Nome da primeira tarefa? ')
    condit2 = input('Nome da segunda tarefa? ')
    cur.execute(""" UPDATE Tarefa_""" + type + """
                    SET next_task1 = '""" + condit1 + """',
                        next_task2 = '""" + condit2 + """'
                    WHERE name = '""" + task_name + """'; """)
    con.commit()

def add_prox_tarefa(task_name, type, next_task = None):

    if(next_task == None):
        next_task = input('Nome da tarefa próxima? ')

    cur.execute(""" UPDATE Tarefa_""" + type + """
                    SET next_task = '""" + next_task + """'
                    WHERE name = '""" + task_name + """'; """)
    con.commit()

def update_tarefa():

    task_name = input("Nome da tarefa? ")
    
    cur.execute("SELECT type FROM Tarefa WHERE name = '{}';".format(task_name))
    type = cur.fetchall()
    type = type[0][0]

    print("1 - Alterar nome")
    print("2 - Alterar tipo")
    print("3 - Alterar Pool")
    print("4 - Adicionar próxima tarefa")
    opt = input("Opção: ")
    print('\n')

    if (opt == '3'):
        pool_name = input("De qual pool esta tarefa faz parte? ")
        cur.execute(""" UPDATE Tarefa
                    SET Pool = '""" + pool_name + """'
                    WHERE name = '""" + task_name + """'; """)
        con.commit()


    elif (opt == '4'):

        print("1 - Tarefa já existente")
        print("2 - Nova tarefa")
        opt = input("Opção: ")
        print('\n')

        if(opt == '1'):
            if(type == 'condicional'):
                add_prox_condicional(task_name, type)

            else:
                add_prox_tarefa(task_name, type)

        elif (opt == '2'):
            next_task = add_tarefa()
            add_prox_tarefa(task_name, type, next_task)
    
    else:
        print("Nao implementado")

    input()
    clear_screen()


##############    LOGICA POOL

def add_pool():

    pool_name = input("Nome da pool? ")
    proc = input("Parte de qual processo? ")

    cur.execute("INSERT INTO Pool(name, Processo) VALUES('"+ pool_name +"','"+ proc  +"');")
    con.commit()

    input()
    clear_screen()

def remove_pool():

    pool_name = input("Nome da pool? ")
    cur.execute(" UPDATE Tarefa SET Pool = NULL WHERE Pool = '" + pool_name +"'; ")
    cur.execute("DELETE FROM Pool WHERE name = '"+ pool_name +"';")
    con.commit()

    input()
    clear_screen()


def remove_tables():

    print("DROP ALL TABLES")
    cur.execute("DROP TABLE IF EXISTS Processo;")
    cur.execute("DROP TABLE IF EXISTS Pool;")
    cur.execute("DROP TABLE IF EXISTS Tarefa;")
    cur.execute("DROP TABLE IF EXISTS Tarefa_normal;")
    cur.execute("DROP TABLE IF EXISTS Tarefa_inicial;")
    cur.execute("DROP TABLE IF EXISTS Tarefa_final;")
    cur.execute("DROP TABLE IF EXISTS Tarefa_condicional;")

    input()
    clear_screen()

def check():

    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    res = cur.fetchall()

    count = 1
    for tables in res:
        print(str(count) + " - " + tables[0])
        count+=1

    opt = int(input("Opção: "))
    print('\n')

    if(opt <= len(res)):
        opt-=1
        cur.execute("SELECT * FROM " + res[opt][0] + ";")
        data = cur.fetchall()
        for d in data:
            print(d)
        
    input()
    clear_screen()

con = sqlite3.connect("bpm.db")
cur = con.cursor()