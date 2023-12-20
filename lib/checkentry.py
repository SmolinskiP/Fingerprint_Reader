def Check_Entry(action, entries_list, emp_name):
    
    if 2 in entries_list:
        if emp_name[-1] == 'a':
            text1 = "Już wychodziłaś z pracy"
        else:
            text1 = "Już wychodziłeś z pracy"
        text2 = "Odpoczywaj %s :)" % emp_name
        return text1, text2
    elif action != 1 and 1 not in entries_list:
        text1 = "Nie odnotowano wejścia."
        text2 = "Zaloguj się najpierw do pracy"
        return text1, text2
    elif action == 1 and 1 in entries_list:
        text1 = "Już odnotowano wejście"
        text2 = "Miłej pracy %s :)" % emp_name
        return text1, text2
    
    else:
        return "OK"
        
