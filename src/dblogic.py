
import sqlite3
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_task_type(task_name):

    try:
        cur.execute("SELECT type FROM Tarefa WHERE name = '" + task_name + "';")
        type = cur.fetchall()

    except:
        print("Tarefa não encontrada")

    return type[0][0]

##############    LOGICA PROCESSO

def add_processo():

    proc_name = input("Process name? ")
    query = "INSERT INTO Processo VALUES ('{}');".format(proc_name)
    cur.execute(query)    
    con.commit()

    print("Adicionado o Processo "+ proc_name)
    input()
    clear_screen()

def remove_processo():
    print("Selecione o processo que quer remover")
    proc_name = list_elements('Processo')

    try: 
        query = "DELETE FROM Processo WHERE name = ('{}');".format(proc_name)
        cur.execute(query)
        con.commit()
    except:
        print("Nome inválido")

    input()
    clear_screen()

def execute_final_task(current_task):
    print('\n')
    print("Executando tarefa "+ current_task +" do tipo Final")
    
    print("\nPROCESSO FINALIZADO!")

def execute_condit_task(current_task):

    print('\n')
    print("Executando tarefa "+ current_task +" do tipo Condicional.")
    
    cur.execute("SELECT next_task1 FROM Tarefa_condicional WHERE name = '"+ current_task +"';")
    condit1 = cur.fetchall()[0][0]

    cur.execute("SELECT next_task2 FROM Tarefa_condicional WHERE name = '"+ current_task +"';")
    condit2 = cur.fetchall()[0][0]

    print("Condic. 1 = " + condit1)
    print("Condic. 2 = " + condit2)
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

    tasks = [x[0] for x in tasks]

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
        tasks = cur.fetchall()
        qtd_tarefas = len(tasks)

        print("O processo " + processos[opt][0] + " tem: " + str(qtd_pools) + " Pools e " + str(qtd_tarefas) + " Tarefas")

        run_task_order(tasks)

##############    LOGICA TAREFA 

def add_tarefa():

    task_name = input("Nome da tarefa? ")
    
    print("Qual o tipo da tarefa?")
    print("1 - Normal")
    print("2 - Inicio")
    print("3 - Fim")
    print("4 - Condicional")

    types = ['normal', 'inicial', 'final', 'condicional']

    opt = int(input("Opção: "))
    try:
        type = types[opt-1]
        
        query = "INSERT INTO Tarefa(name, type) VALUES ('{}', '{}');".format(task_name, type)
        cur.execute(query)

        query = "INSERT INTO Tarefa_" + type + "(name) VALUES ('{}');".format(task_name)
        cur.execute(query)
        
        con.commit()

        print("Adicionada a tarefa " +  task_name + " do tipo " + type)
    except:
        print("Valor inválido")

    input()

    return task_name

def remove_tarefa():

    print("Selecione a tarefa a ser removida")
    task_name = list_elements('Tarefa')

    try:
        type = get_task_type(task_name)
        cur.execute("DELETE FROM Tarefa_{} WHERE name = '{}';".format(type, task_name))
        cur.execute("DELETE FROM Tarefa WHERE name = '{}';".format(task_name))
        
        print("Removida a Tarefa " + task_name + " do tipo " + type)

        con.commit()
    
    except:
        print("Nome inválido")

    input()
    clear_screen()

def add_prox_condicional(task_name, type):

    print("Selecione a tarefa da primeira condição")
    condit1 = list_elements('Tarefa')
    print('\n')
    print("Selecione a tarefa da segunda condição")
    condit2 = list_elements('Tarefa')

    cur.execute(""" UPDATE Tarefa_""" + type + """
                    SET next_task1 = '""" + condit1 + """',
                        next_task2 = '""" + condit2 + """'
                    WHERE name = '""" + task_name + """'; """)
    con.commit()

    print("Adicinadas as tarefas "+ condit1 +" e "+ condit2 +" como próximas à tarefa " + task_name)

def add_prox_tarefa(task_name, type, next_task = None):

    if(next_task == None):

        print("Selecione a tarefa a proxima")
        next_task = list_elements('Tarefa')

    cur.execute(""" UPDATE Tarefa_""" + type + """
                    SET next_task = '""" + next_task + """'
                    WHERE name = '""" + task_name + """'; """)
    con.commit()

def set_task_pool(task_name):

    print("Selecione a pool que esta tarefa faz parte")
    pool_name = list_elements("Pool")

    cur.execute(""" UPDATE Tarefa
                SET Pool = '""" + pool_name + """'
                WHERE name = '""" + task_name + """'; """)
    con.commit()

    print("Adicionada a tarefa " + task_name + " à pool " + pool_name)

def update_tarefa():

    print("Selecione a tarefa a ser atualizada")    
    task_name = list_elements("Tarefa")

    try:
        type = get_task_type(task_name)

        print("\n")
        print("Tarefa " + task_name + " do tipo " + type + " selecionada")
        print("\n")

        print("1 - Alterar Pool")
        print("2 - Adicionar próxima tarefa")

        opt = input("Opção: ")
        print('\n')

        if (opt == '1'):        
            set_task_pool(task_name)

        elif (opt == '2'):

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

    except:
        print("Nome inválido")

    input()
    clear_screen()

##############    LOGICA POOL

def add_pool():

    pool_name = input("Nome da pool? ")

    print("Selecione o processo do qual a Pool faz parte: ")
    proc = list_elements("Processo")

    cur.execute("INSERT INTO Pool(name, Processo) VALUES('"+ pool_name +"','"+ proc  +"');")
    con.commit()

    print("Adicionada a Pool " +  pool_name + " ao processo " + proc)

    input()
    clear_screen()

def remove_pool():

    print("Selecione a pool a ser removida: ")
    pool_name = list_elements('Pool')

    try:
        cur.execute(" UPDATE Tarefa SET Pool = NULL WHERE Pool = '" + pool_name +"';")
        cur.execute("DELETE FROM Pool WHERE name = '"+ pool_name +"';")
        con.commit()

        print("Removida a pool " + pool_name)
    except:
        print("Nome inválido")

    input()
    clear_screen()

##############    LOGICA BD

def remove_tables():

    print("DROP ALL TABLES")

    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    res = cur.fetchall()

    for tables in res:
        cur.execute("DROP TABLE IF EXISTS " + tables[0])

    input()
    clear_screen()

def list_elements(table_name):

    cur.execute("SELECT name FROM " + table_name + ";")
    elements = cur.fetchall()
    elements = [x[0] for x in elements]

    print("-------------------------------------")
    count = 1
    for el in elements:
        print( str(count) + " - " + el)
        count += 1
    print("-------------------------------------")

    opt = int(input("Selecione um: "))

    if(opt <= len(elements)):
        opt -= 1
        return elements[opt]

def check():

    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    res = cur.fetchall()

    tables = [x[0] for x in res]

    print("-------------------------------------")
    if not(tables):
        print("No tables")

    count = 1
    for tbl in tables:
        print(str(count) + " - " + tbl)
        count+=1
    print("-------------------------------------")

    opt = int(input("Opção: "))
    print('\n')

    try:
        if(opt <= len(res)):
            opt-=1

            cur.execute("SELECT * FROM " + tables[opt] + ";")
            data = cur.fetchall()

            for d in data:
                print(d)
        
        else:
            print("Opção inválida!")
    except:
        print("Opção inválida")
        
    input()
    clear_screen()

con = sqlite3.connect("bpm.db")
cur = con.cursor()