import mysql.connector as database
from params.sql import *
import sys

def Get_EmployeeData(card_id, actual_date):
    try:
        conn = database.connect(
            user=sql_user,
            password=sql_password,
            host=sql_host,
            database=sql_database
        )
        employee_dict = {}
        get_sql = conn.cursor()
        
        #Get basic data about employee
        get_sql.execute("SELECT id, imie, nazwisko, admin FROM pracownicy WHERE karta = '%s'" % card_id)
        try:
            result = get_sql.fetchall()[0]
            employee_dict['id'] = result[0]
            employee_dict['fname'] = result[1]
            employee_dict['lname'] = result[2]
            employee_dict['admin'] = result[3]
        except:
            result = None
            employee_dict['id'] = None
            employee_dict['fname'] = None
            employee_dict['lname'] = None
            employee_dict['admin'] = None
        
        #Get employee entries
        try:
            sql_query = "SELECT action FROM obecnosc WHERE pracownik = %s AND time LIKE '%s%%' ORDER BY action" % (employee_dict['id'], actual_date)
            get_sql.execute(sql_query)
            employee_dict['entry_list'] = []
            try:
                entry_list = get_sql.fetchall()
            except:
                entry_list = []
            for item in entry_list:
                employee_dict['entry_list'].append(item[0])
        except:
            print("ERROR")

        conn.close()
        print(employee_dict)
        return employee_dict
        
    except database.Error as e:
        print(f"Nie udalo sie polaczyc z baza danych MariaDB: {e}")
        sys.exit(1)
        
def Get_Actual_Breaks():
    try:
        conn = database.connect(
            user=sql_user,
            password=sql_password,
            host=sql_host,
            database=sql_database
        )
        get_sql = conn.cursor()
        
        breaks_dict = {}
        #Get all employees on breaks
        get_sql.execute("SELECT id_emp FROM act_breaks")
        result = get_sql.fetchall()
        
        for item in result:
            get_sql.execute("SELECT imie, nazwisko FROM pracownicy WHERE id = %s" % item)
            fname_lname = get_sql.fetchall()
            fname = fname_lname[0][0]
            lname = fname_lname[0][1]
            i = len(lname)
            lname = lname[:1]
            j = 1
            while j < i:
                lname += "*"
                j+=1
            employee = fname + " " + lname
            breaks_dict[item[0]] = employee
        
        conn.close()
        return breaks_dict
        
    except database.Error as e:
        print(f"Nie udalo sie polaczyc z baza danych MariaDB: {e}")
        sys.exit(1)
        
def Update_EmployeeData(emp_id, action, actual_time, emp_name):
    try:
        conn = database.connect(
            user=sql_user,
            password=sql_password,
            host=sql_host,
            database=sql_database
        )
        get_sql = conn.cursor()
        get_sql.execute("INSERT INTO obecnosc (pracownik, action) VALUES (%s, %s)", (emp_id, action))
        conn.commit()
        
        if action == 1:
            action_text = "WEJŚCIE "
        elif action == 2:
            action_text = "WYJŚCIE "
        elif action == 3:
            action_text = "PRZERWA "
            sql_check = "SELECT id FROM act_breaks WHERE id_emp = %s" % emp_id
            get_sql.execute(sql_check)
            result = get_sql.fetchall()
            if not result:
                get_sql.execute("INSERT INTO act_breaks (id_emp) VALUES (%s)" % emp_id)
                conn.commit()
        elif action == 4:
            action_text = "KONIEC PRZERWY "
            sql_check = "SELECT id FROM act_breaks WHERE id_emp = %s" % emp_id
            get_sql.execute(sql_check)
            result = get_sql.fetchall()
            if not result:
                print("Kontynuje")
            else:
                get_sql.execute("DELETE FROM act_breaks WHERE id_emp = %s" % emp_id)
                conn.commit()
        else:
            action_text = ""
        
        sql_check = "SELECT id FROM obecnosc WHERE action = " + str(action) + " AND pracownik = " + str(emp_id) + " AND time LIKE '" + actual_time + "%'"
        get_sql.execute(sql_check)
        result = get_sql.fetchall()
        if not result:
            text1 = "ERROR - Coś poszło nie tak"
            text2 = "Spróbuj jeszcze raz %s" % emp_name
            conn.close()
            return text1, text2, (165, 42, 42)
        else:
            text1 = "%s - SUKCES!" % action_text
            text2 = "Dobrego dnia %s" % emp_name
            conn.close()
            return text1, text2, (0, 158, 96)
        conn.close()
        
    except:
        print(f"Nie udalo sie polaczyc z baza danych MariaDB: {e}")
        sys.exit(1)