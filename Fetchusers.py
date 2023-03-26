import mysql.connector


def connection():
  con = mysql.connector.connect(
    user='gkcl2n9xm2kzgm7ye6np',
    host='ap-south.connect.psdb.cloud',
    password='pscale_pw_V3ExLmyM5XA0PBYeUFcVYndD6NfkipdNfEqEVSOa6er',
    database='todo',
    ssl_ca='/etc/ssl/cert.pem')
  return con


def createAccount(cursor, name, username, password):
  prompt = f"""
    insert into users 
    (name , username , pass ) 
    values ('{name}','{username}','{password}');
    """
  try:
    cursor.execute(prompt)
    return True
  except:
    print("username already exits")
    return False


def verify(cursor, username, password):

  prompt = f"""
    select * from users 
    where username = '{username}'
    """
  cursor.execute(prompt)
  res = cursor.fetchall()
  if (len(res) == 0):
    print("username wrong")
    return False

  if (res[0]['pass'] == password):
    return True
  else:
    print("password wrong")
    return False


def getId(cursor, username):
  prompt = f"""
    select * from users 
    where username = '{username}'
    """
  cursor.execute(prompt)
  res = cursor.fetchall()
  return res[0]['userid']


def getName(cursor, id):
  prompt = f"""
    select * from users 
    where userid = '{id}'
    """
  cursor.execute(prompt)
  res = cursor.fetchall()
  return res[0]['name']
