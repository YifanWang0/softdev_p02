# import sqlite3   #enable control of an sqlite database
#
# DB_FILE = "database.db"
#
# db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
# c = db.cursor()               #facilitate db ops
#
# command = "DROP TABLE IF EXISTS users;" # delete table
# c.execute(command)
#
# command = "DROP TABLE IF EXISTS stories;" # delete table
# c.execute(command)
#
# command = "DROP TABLE IF EXISTS edits;" # delete table
# c.execute(command)
#
# command = "CREATE TABLE IF NOT EXISTS users (user_id INTEGER, username TEXT, password TEXT);" # create table
# c.execute(command)    # run SQL statement
#
# command = "CREATE TABLE IF NOT EXISTS stories (story_id INTEGER, story_name TEXT, story_text TEXT, last_edit TEXT);" # create table
# c.execute(command)    # run SQL statement
#
# command = "CREATE TABLE IF NOT EXISTS edits (user_id INTEGER, story_id INTEGER);" # create table
# c.execute(command)    # run SQL statement
#
# db.commit()
# db.close()
