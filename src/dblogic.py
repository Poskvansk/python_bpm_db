
import sqlite3
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


##############    LOGICA PROCESSO
def get_task_type(task_name):

    cur.execute("SELECT type FROM Tarefa WHERE name = '" + task_name + "';")
    type = cur.fetchall()

    return type[0][0]

def execute_final_task(current_task):
    print('\n')
    print("Executando tarefa "+ current_task +" do tipo Final")
    
    print("\nPROCESSO FINALIZADO!")

def execute_condit_task(current_task):

    print('\n')
    print("Executando tarefa "+ current_task +" do tipo Condicional.")
    opt = input("Qual condição foi cumprida? (1 ou 2) ")

    if(opt =='1'):
        cur.execute("SELECT next_task1 FROM Tarefa_condicional WHERE name = '" + current_task + "';")

    else:
        cur.execute("SELECT next_task2 FROM Tarefa_condicional WHERE name = '" + current_task + "';")

    current_task = cur.fetchall()

    return current_task[0][0]

def execute_normal_task(current_task, type):

    print('\n')
    print("Executando tarefa "+ current_task +" do tipo "+ type)

    cur.execute("SELECT next_task FROM Tarefa_" + type + " WHERE name = '" + current_task + "';")

    current_task = cur.fetchall()
    
    return current_task[0][0]

def run_task_order(tasks):

    for tsk in tasks:

        type = get_task_type(tsk)

        if(type == "inicial"):
            current_task = tsk
            break

    while(type != 'final'):

        type = get_task_type(current_task)

        if(type == "condicional"):
            current_task = execute_condit_task(current_task)
        
        elif(type == "final"):
            execute_final_task(current_task)

        else:
            current_task = execute_normal_task(current_task, type)

        input("Pressione ENTER para continuar ")




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
        cur.execute("SELECT * FROM Pool WHERE Processo ='" + processos[opt][0] + "';")
        pools = cur.fetchall()
        qtd_pools = len(pools)


        
        query = "SELECT * FROM Tarefa WHERE Pool IN ("
        for i in range(qtd_pools):
            query+= "'" + pools[i][0] + "'"
            if(i < qtd_pools-1):
                query+= ", "
        query += ");"

        cur.execute(query)
        tarefas = cur.fetchall()
        tarefas = [x[0] for x in tarefas]
        qtd_tarefas = len(tarefas)
        print("O processo " + processos[opt][0] + " tem: " + str(qtd_pools) + " Pools e " + str(qtd_tarefas) + " Tarefas")

        run_task_order(tarefas)

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
    type = get_task_type(task_name)

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
    cur.execute(" UPDATE Tarefa SET Pool = NULL WHERE Pool = '" + pool_name +"';")
    cur.execute("DELETE FROM Pool WHERE name = '"+ pool_name +"';")
    con.commit()

    input()
    clear_screen()


def remove_tables():

    print("DROP ALL TABLES")

    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    res = cur.fetchall()

    for tables in res:
        cur.execute("DROP TABLE IF EXISTS " + tables[0])

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