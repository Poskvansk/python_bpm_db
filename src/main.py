import bpschema
import dblogic

def menu():

    quit = False
    
    while(not quit):
        print("-------------------------------------")
        print("1 - Add processo")
        print("2 - Remover processo")
        print("3 - Add tarefa em processo")
        print("4 - Remover tarefa")
        print("5 - Add Pool")
        print("6 - Remover Pool")

        print("8 - Alterar tarefa")
        
        print("\n0 - Sair")
        print("check - Run")
        print("check - Check DB")
        print("drop - Drop DB")
        print("init - Init DB")
        print("-------------------------------------")

        opt = input()

        if(opt == '1'):
            dblogic.clear_screen()
            dblogic.add_processo()

        elif(opt == '2'):
            dblogic.clear_screen()
            dblogic.remove_processo()

        elif(opt == '3'):
            dblogic.clear_screen()
            dblogic.add_tarefa()

        elif(opt == '4'):
            dblogic.clear_screen()
            dblogic.remove_tarefa()

        elif(opt == '5'):
            dblogic.clear_screen()
            dblogic.add_pool()

        elif(opt == '6'):
            dblogic.clear_screen()
            dblogic.remove_pool()

        elif(opt == 'drop'):
            dblogic.clear_screen()
            dblogic.remove_tables()
        
        elif(opt == 'init'):
            dblogic.clear_screen()
            bpschema.create_tables()
        
        elif(opt == 'check'):
            dblogic.clear_screen()
            dblogic.check()
        
        elif(opt == 'run'):
            dblogic.clear_screen()
            dblogic.run_process()
        
        elif(opt == '8'):
            dblogic.clear_screen()
            dblogic.update_tarefa()

        elif(opt == '0'):
            quit = True
        
        else:
            print("Option not valid.")
  
menu()