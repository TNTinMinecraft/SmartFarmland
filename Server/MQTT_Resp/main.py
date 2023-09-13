import MySQL

clint_st = ('3213213', 'NAME', 'status')

if __name__ == '__main__':
    #MySQL.db_write(clint_st)
    #id_in = MySQL.get_MAC("123123")
    #print(id_in)
    MySQL.switch_status('123123', 1)
    MySQL.print_db()