def getDetails(cursor , id):
    prompt = f"""
    select * from todos
    where userid={id}
    """
    cursor.execute(prompt)
    result = cursor.fetchall()
    return result


def addDetails(cursor , task , id):
    promp=f"""
    insert into todos 
    ( userid , datecreated , datemodified , task ) 
    values ( {id}, NOW(), NOW(), '{task}' );
    """
    cursor.execute(promp)


def updateDetails(cursor , task , id):
    promp=f"""
    update todos 
    set task='{task}', 
    datemodified=now() 
    where todoid={id};
    """
    cursor.execute(promp)


def markUpdate(cursor , id):
    prompt=f"""
    update todos
    set done = not done
    where todoid = {id};
    """
    cursor.execute(prompt)


def deleteItem(cursor , id):
    prompt=f"""
    delete from todos
    where todoid= {id};
    """
    cursor.execute(prompt)
