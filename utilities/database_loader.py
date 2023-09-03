#small app that converts json to sqlite database
import sqlite3
import json
import sys
import os


if len(sys.argv) == 2:
    if sys.argv[1] == "clear":
        if os.path.exists("../fithub.db"):
            os.remove("../fithub.db")
            open("../fithub.db")
    sys.exit(0)
        
con = sqlite3.connect("../fithub.db", check_same_thread=False)
cursor = con.cursor()

#TODO: update when updataing database
try:
    
    cursor.execute("DROP TABLE users")
    cursor.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, username TEXT UNIQUE, hash TEXT)")
    con.commit()
    
    cursor.execute("DROP TABLE exercise")
    cursor.execute("CREATE TABLE exercise(id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT NOT NULL, primary_muscle TEXT NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY(user_id)REFERENCES users(id));")
    con.commit()
    
    #submission of workoutSet in the Template
    cursor.execute("DROP TABLE workoutEntry")
    cursor.execute("CREATE TABLE workoutEntry (id INTEGER PRIMARY KEY, workout_id INTEGER NOT NULL, data1 INTEGER, data2 INTEGER, set_number INTEGER, max NUMERIC, type TEXT, user_id INTEGER NOT NULL, date NUMERIC , FOREIGN KEY(workout_id) REFERENCES exercise(id), FOREIGN KEY(user_id) REFERENCES users(id));")
    con.commit()

    #submission of workoutTemplate
    cursor.execute("DROP TABLE workoutLog")
    cursor.execute("CREATE TABLE workoutLog (id INTEGER PRIMARY KEY, workout_id INTEGER NOT NULL, text TEXT, total_data1 NUMERIC, total_data2 INTEGER, total_sets INTEGER, max_id INTEGER, user_id INTEGER NOT NULL, date NUMERIC, FOREIGN KEY(workout_id) REFERENCES exercise(id), FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(max_id) REFERENCES workoutEntry(id));")
    con.commit()

    #submission of Workout as whole
    cursor.execute("DROP TABLE workoutSubmission")
    cursor.execute("CREATE TABLE workoutSubmission (id INTEGER PRIMARY KEY, collective_weight NUMERIC NOT NULL, collective_reps NUMERIC NOT NULL, collective_duration NUMERIC NOT NULL, collective_sets INTEGER NOT NULL,  user_id INTEGER NOT NULL, date NUMERIC, FOREIGN KEY(user_id) REFERENCES users(id));")
    con.commit()

except:
    pass

data = ["_", "fake_hash"]
cursor.execute("INSERT INTO users (username, hash) VALUES(?, ?)", data)
con.commit()

f = open("../workouts.json")
data = json.load(f)
list = []
for d in data['workouts']:
    insert = [d["name"], d["type"], d["primary_muscle"], "1"]
    cursor.execute("INSERT INTO exercise (name, type, primary_muscle, user_id) VALUES(?, ?, ?, ?)", insert)
    con.commit()