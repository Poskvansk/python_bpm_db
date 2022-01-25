
import sqlite3
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def run_process():

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

def update_tarefa():

    task_name = input("Nome da tarefa? ")
    
    cur.execute("SELECT type FROM Tarefa WHERE name = '{}';".format(task_name))
    type = cur.fetchall()
    type = type[0][0]

    print("1 - Alterar nome")
    print("2 - Alterar tipo")
    print("3 - Adicionar próxima tarefa")
    opt = input("Opção: ")

    if (opt == '3'):
        print("\n1 - Tarefa já existente")
        print("2 - Nova tarefa")
        opt = input("Opção: ")

        if(opt == '1'):
            if(type == 'condicional'):
                condit1 = input('Nome da primeira tarefa? ')
                condit2 = input('Nome da segunda tarefa? ')
                cur.execute(""" UPDATE Tarefa_""" + type + """
                                SET next_task1 = '""" + condit1 + """',
                                    next_task2 = '""" + condit2 + """'
                                WHERE name = '""" + task_name + """'; """)
                con.commit()

            else:
                next_task = input('Nome da tarefa próxima? ')

                cur.execute(""" UPDATE Tarefa_""" + type + """
                                SET next_task = '""" + next_task + """'
                                WHERE name = '""" + task_name + """'; """)
                con.commit()

        elif (opt == '2'):
            print('\n')
            next_task = add_tarefa()
            cur.execute(""" UPDATE Tarefa_""" + type + """
                            SET next_task = '""" + next_task + """'
                            WHERE name = '""" + task_name + """'; """)
            con.commit()

    else:
        print("Nao implementado")

    input()
    clear_screen()


def add_pool():

    pool_name = print("Nome da pool? ")

    input()
    clear_screen()


def remove_pool():

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

    query = "SELECT name FROM sqlite_master WHERE type='table'; "
    cur.execute(query)
    res = cur.fetchall()
    for tables in res:
        print(tables)
        
    input()
    clear_screen()

con = sqlite3.connect("bpm.db")
cur = con.cursor()