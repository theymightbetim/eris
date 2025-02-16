from datetime import datetime

def is_it_wednesday():
    """
    check if today is wednesday
    :return:
    """
    if datetime.today().weekday() == 2:
        print("It's Wednesday!")
        return True
    print("It's not Wednesday.")
    return False