import sqlite3

def create_tables():

    cur.execute( """ CREATE TABLE IF NOT EXISTS Processo (

                    name VARCHAR[50] PRIMARY KEY
    )""")

    cur.execute( """ CREATE TABLE IF NOT EXISTS Pool (

                    name VARCHAR[50] PRIMARY KEY,

                    Processo VARCHAR[50] NOT NULL,

                    FOREIGN KEY (Processo)
                        REFERENCES Processo (name)
    );""")

    cur.execute( """ CREATE TABLE IF NOT EXISTS Tarefa (

                    name VARCHAR[50] PRIMARY KEY,
                    type VARCHAR[20] NOT NULL,

                    Pool VARCHAR[50],

                    FOREIGN KEY (Pool)
                        REFERENCES Pool (name)

    );""")

    cur.execute( """ CREATE TABLE IF NOT EXISTS Tarefa_normal (

                    name VARCHAR[50] NOT NULL,

                    next_task VARCHAR[50],
                    FOREIGN KEY (name, next_task) REFERENCES Tarefa (name, name)

                    PRIMARY KEY(name)
    );""")

    cur.execute( """ CREATE TABLE IF NOT EXISTS Tarefa_inicial (

                    name VARCHAR[50] NOT NULL,

                    next_task VARCHAR[50],
                    FOREIGN KEY (name, next_task) REFERENCES Tarefa (name, name)

                    PRIMARY KEY(name)
    );""")

    cur.execute( """ CREATE TABLE IF NOT EXISTS Tarefa_final (

                    name VARCHAR[50] NOT NULL,
                    status VARCHAR[15],

                    FOREIGN KEY (name) REFERENCES Tarefa (name),
                    PRIMARY KEY (name)
    );""")

    cur.execute( """ CREATE TABLE IF NOT EXISTS Tarefa_condicional (

                    name VARCHAR[50] NOT NULL,
                    next_task1 VARCHAR[50],
                    next_task2 VARCHAR[50],
                    FOREIGN KEY (name, next_task1, next_task2) REFERENCES Tarefa (name, name, name),
                    PRIMARY KEY (name)
    );""")



def create_relations() :

    cur.execute( """ CREATE TABLE IF NOT EXISTS next_task (

                    id_current INT NOT NULL,
                    id_next INT NOT NULL,


                    next_task INT NOT NULL,
                        FOREIGN KEY (id_current)
                            REFERENCES Tarefa (id)
                        FOREIGN KEY (id_next)
                            REFERENCES Tarefa (id)

                    PRIMARY KEY(id_current, id_next)
    );""")

    cur.execute( """ CREATE TABLE IF NOT EXISTS next_task_conditional (

                    id_current INT NOT NULL,
                    id_next_if INT NOT NULL,
                    id_next_else INT NOT NULL,


                    next_task INT NOT NULL,
                        FOREIGN KEY (id_current)
                            REFERENCES Tarefa (id)
                        FOREIGN KEY (id_next_if)
                            REFERENCES Tarefa (id)
                        FOREIGN KEY (id_next_else)
                            REFERENCES Tarefa (id)

                    PRIMARY KEY(id_current, id_next_if, id_next_else)
    );""")



    return

con = sqlite3.connect("bpm.db")
cur = con.cursor()

cur.execute("PRAGMA foreign_keys = 1")

create_tables()

# con.close()
