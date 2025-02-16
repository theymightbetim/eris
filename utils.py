def is_it_wednesday():
    """
    check if today is wednesday
    :return:
    """
    if datetime.today().weekday() == 2:
        print("It's Wednesday!")
        return True
    else:
        print("It's not Wednesday.")
        return False