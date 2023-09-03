from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import sqlite3

import bcrypt
from utilities.helper import login_required, toTime, toSeconds

# config = {
#   'user': 'root',
#   'password': 'Bobo24680',
#   'host': '127.0.0.1',
#   'database': 'fithub',
#   'raise_on_warnings': True
# }S
# SQL_user = ("SELECT * FROM users " 
#             "WHERE username = %s")

con = sqlite3.connect("fithub.db", check_same_thread=False)
cursor = con.cursor()

# cnx = mysql.connector.connect(**config)
# cursor = cnx.cursor(buffered=True)

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def page_error(var):
    return render_template('error.html', var = var)

@app.route('/')
@login_required
def root():
    submissions = []
    workouts = {}
    workout_max = []
    muscle_usage = []
    #TODO load data from database
    #calendar -----
    #workout
    try:
        data = [session["user_id"], 1]
        cursor.execute("SELECT * FROM exercise WHERE user_id = ? OR user_id = ?", data)
        exercises_db = cursor.fetchall()
        for exercise in exercises_db:
            type = exercise[2]
            data = [session["user_id"], exercise[0]]
            cursor.execute("SELECT * FROM workoutEntry WHERE user_id = ? and workout_id = ? ORDER BY max DESC", data)
            max_history = cursor.fetchone()
            if max_history:
                workout_max_dict = {
                    "id": exercise[0],
                    "type": exercise[2],
                    "muscle": exercise[3],
                    "name": exercise[1],
                    "max": max_history[5],
                    "data1": max_history[2],
                    "data2": max_history[3],
                    "date": max_history[8]
                }
                workout_max.append(workout_max_dict)

            data = [session["user_id"], exercise[0]]
            cursor.execute("SELECT * FROM workoutLog WHERE user_id = ? AND workout_id = ? ORDER BY id ASC", data)
            history = cursor.fetchall()

            
            # return page_error(history)

            Ldate = []
            Ltotal_data1 = []
            Ltotal_data2 = []
            Lmax = []

            for item in history:
                if type == "Duration":
                    Ltotal_data1.append(toSeconds(item[3]))
                else:
                    Ltotal_data1.append(item[3])
                Ltotal_data2.append(item[4])
                Ldate.append(item[8])
            
            data = [session["user_id"], exercise[0]]
            cursor.execute("SELECT * FROM workoutEntry WHERE id IN (SELECT max_id FROM workoutLog WHERE user_id = ? AND workout_id = ? ORDER BY id ASC)", data)
            max_history = cursor.fetchall()
            if max_history:
                for max in max_history:
                    if type == "Duration":
                        Lmax.append(toSeconds(max[5]))
                    else:
                        Lmax.append(max[5])
                
                history_dict = {
                    "date": Ldate,
                    "total_data1": Ltotal_data1,
                    "total_data2": Ltotal_data2,
                    "max": Lmax
                }
                workouts[exercise[0]] = history_dict
    except:
        pass
    
    #log
    #FUTURE: perhaps also call the exercises from the workoutLogs
    try:
        data = [session["user_id"],]
        cursor.execute("SELECT * FROM workoutSubmission WHERE user_id = ? ORDER BY id DESC", data)
        submission_db = cursor.fetchall()
        for submission in submission_db:
            submission_dict = {
                "collective_weight": submission[1],
                "collective_reps": submission[2],
                "collective_duration":submission[3],
                "collective_sets":submission[4],
                "date": submission[6]
            }
            submissions.append(submission_dict)
    except:
        pass

    try: 
        muscles = ["Abdominals","Abductors","Adductors","Biceps","Calves","Cardio","Chest","Forearms","Fullbody","Glutes","Hamstrings","Lats","Lower Back","Quadriceps","Shoulders","Traps","Triceps","Upper Back"]
        for muscle in muscles:
            data = [session["user_id"], session["user_id"], 1, muscle]
            cursor.execute("SELECT COUNT (*) FROM workoutEntry WHERE user_id = ? AND workout_id = (SELECT id FROM exercise WHERE (user_id = ? OR user_id = ?) AND primary_muscle = ?)", data)
            number = cursor.fetchone()
            muscle_usage.append(number[0])
    except:
        pass

    # TODO: find the ratios of the muscles
    if len(submissions) > 0:
        if len(workouts) > 0:
            return render_template('index.html', submissions= submissions, workouts = workouts, workout_max = workout_max, muscle_usage = muscle_usage)
        return render_template('index.html', submissions= submissions)
    return render_template('index.html')



@app.route('/wTemplate')
def get_workout_template():
    workout = request.args.get('workout')
    muscle = request.args.get('muscle')
    type = request.args.get('type')
    id = request.args.get('id')
    notes_text = "start journaling your exercises..."
    #get workout id
    workout_id = 0;
    try:
        data = [workout, session["user_id"], 1]
        cursor.execute("SELECT * FROM exercise WHERE name = ? AND (user_id = ? OR user_id = ?)", data)
        workout_id = cursor.fetchone()[0]
    except:
        page_error ("invalid workout")


    total_data1 = "N/A"
    total_data2 = "N/A"
    total_sets = "N/A"
    history_dict = None
    max_data = None

    try:
        data = [workout_id, session["user_id"]]
        cursor.execute("SELECT * FROM workoutLog WHERE workout_id = ? AND user_id = ? ORDER BY id DESC", data)
        log = cursor.fetchone()
        notes_text = log[2]
        total_data1 = log[3]
        total_data2 = log[4]
        total_sets = log[5]
    except:
        pass
    
    try:
        data =[session["user_id"], workout_id]
        cursor.execute("SELECT * FROM workoutEntry WHERE user_id = ? AND workout_id = ? ORDER BY max ASC", data)
        max_db = cursor.fetchone()
        max_data = {"data1": max_db[2],
               "data2": max_db[3],
               "max": max_db[5]
            }
    except:
        pass


    try:
        data = [session["user_id"], workout_id]
        cursor.execute("SELECT * FROM workoutLog WHERE user_id = ? AND workout_id = ? ORDER BY id ASC", data)
        history = cursor.fetchall()

        
        # return page_error(history)

        Ldate = []
        Ltotal_data1 = []
        Ltotal_data2 = []
        Lmax = []

        for item in history:
            if type == "Duration":
                Ltotal_data1.append(toSeconds(item[3]))
            else:
                Ltotal_data1.append(item[3])
            Ltotal_data2.append(item[4])
            Ldate.append(item[8])
        
        data = [session["user_id"], workout_id]
        cursor.execute("SELECT * FROM workoutEntry WHERE id IN (SELECT max_id FROM workoutLog WHERE user_id = ? AND workout_id = ? ORDER BY id ASC)", data)
        max_history = cursor.fetchall()
        if max_history:
            for max in max_history:
                if type == "Duration":
                    Lmax.append(toSeconds(max[5]))
                else:
                    Lmax.append(max[5])
            
            history_dict = {
                "date": Ldate,
                "total_data1": Ltotal_data1,
                "total_data2": Ltotal_data2,
                "max": Lmax
            }
    except:
        pass
    
    #TODO: refactor due to error from DURATION
    if history_dict:
        if max_data:
            return render_template("workout_template/"+type+".html", workout=workout, muscle=muscle, type=type, id=id, notes = notes_text, total_data1 = total_data1, total_data2 = total_data2, total_sets = total_sets, max_data = max_data, history = history_dict)
        return render_template("workout_template/"+type+".html", workout=workout, muscle=muscle, type=type, id=id, notes = notes_text, total_data1 = total_data1, total_data2 = total_data2, total_sets = total_sets, history = history_dict)
    else:
        return render_template("workout_template/"+type+".html", workout=workout, muscle=muscle, type=type, id=id, notes = notes_text, total_data1 = total_data1, total_data2 = total_data2, total_sets = total_sets)

@app.route('/sTemplate')
def get_set_template():
    workout = request.args.get('workout')
    exercise_id = request.args.get('id')
    type = request.args.get('type')
    number = request.args.get('number')
    
    data = [workout]
    cursor.execute("SELECT id FROM exercise WHERE name = ?", data)
    workout_id = cursor.fetchone()[0]

    try:
        data = [workout_id, number, type, session["user_id"]]
        cursor.execute("SELECT * FROM workoutEntry WHERE workout_id = ? AND set_number = ? AND type = ? AND user_id = ? ORDER BY id DESC", data)
        set_data = cursor.fetchone()
        data1 = set_data[2]
        data2 = set_data[3]
        #convert seconds into time data for duration based
    except:
        pass
    if set_data:
        return render_template("set_template/"+type+".html", workout=workout, id = number, exercise_id = exercise_id, data1 = data1, data2 = data2)
    return render_template("set_template/"+type+".html", workout=workout, id = number, exercise_id = exercise_id)

@app.route('/create_workout', methods=['POST', 'GET'])
@login_required
def create_workout():
    if request.method == 'POST':
        name = request.form.get('name')
        muscle = request.form.get('muscle')
        type = request.form.get('type')

        data = [name, type, muscle, session["user_id"]]
        cursor.execute("INSERT INTO exercise(name, type, primary_muscle, user_id) VALUES(?, ?, ?, ?)", data)
        con.commit()
        return redirect('/')
    
    #update when changing
    muscles = ["Abdominals","Abductors","Adductors","Biceps","Calves","Cardio","Chest","Forearms","Fullbody","Glutes","Hamstrings","Lats","Lower Back","Quadriceps","Shoulders","Traps","Triceps","Upper Back"]
    types = ["Weight Reps", "Bodyweight Reps", "Duration"]
    return render_template("create_workout.html", muscles = muscles, types = types)


@app.route('/workout', methods=['POST', 'GET'])
@login_required
def workout_log():
    if request.method == 'POST':
        # grab data from sets 
        #   set name structure: exercise_id_set_id_weight, exercise_id_set_id_reps. ect
        #   we should grab using the key dict and try for each 

        #grab data from notes (easy) formatted like: exercise_id_notes

        #finnally create workout journal entry get workouts and total set number
        date = request.form.get('date');
        keys = request.form.getlist('key');

        # for data entry in submission as whole
        collective_weight = 0
        collective_reps = 0
        collective_duration = 0
        collective_sets = 1

        #translate exercise id to workout number
        #exercise1...
        keyDict = {}
        for key in keys:
            workout, exercise_id =key.split('_')
            keyDict[exercise_id] = workout
        
        for key in keyDict:
            if request.form.get(str(key)+"_counter") == "0":
                return page_error("error when submitting workout: empty exercise found")
        
        #iterate through dictionary returns the key. In this case key is the exercise id
        #we must use this to gather data based on teh workout templates
        #for each workout
        for key in keyDict:
            greatest_max = 0;
            greatest_max_id = None;
            total_data2 = 0
            total_data1 = 0
            total_sets = 1
            workout_name = keyDict[key]
            data = [workout_name, session["user_id"], "1"]
            cursor.execute("SELECT * FROM exercise WHERE name = ? AND (user_id = ? OR user_id = ?)", data)
            workout = cursor.fetchone()
            if workout == None:
                return page_error("Exercise Invalid")
            #add other data outside of match statement which sorts by type



            #find type of the workout in the database
            workout_id = workout[0]
            type = workout[2];
            set_amount = int(request.form.get(str(key)+"_counter"))

            #setlogging
            data1 = 0
            data2 = 0
            max = 0
            
            #for each set
            for set_id in range(1, set_amount + 1):
                try:
                    data1 = request.form.get(str(key)+"_set"+str(set_id)+"_data1")
                except:
                    pass
                if data1:
                    if type == "Duration":
                        total_data1 += toSeconds(data1)
                        max = data1
                    else:
                        data1_toadd = data1
                        if data1.isdigit() == False:
                            return page_error("error when reading values")
                    
                        if data1_toadd is None:
                            return page_error("error when reading values")

                try:
                    data2 = request.form.get(str(key)+"_set"+str(set_id)+"_data2")
                except:
                    pass

                if data2:
                    if data2.isdigit() == False:
                        return page_error("error when reading values")
                    total_data2 += int(data2)
                    if type == "Bodyweight Reps":
                        max = data2
                    elif type == "Weight Reps":
                        max = round(int(data1) * (1 + (int(data2) / 30) ), 2)
                        if data1:
                            total_data1 += int(data1_toadd) * int(data2)
                        else:
                            return page_error("error when reading values")
                
                
                id = None
                if data1 and data2:
                    data = [workout_id, data1, data2, set_id, max, type, session["user_id"], date]
                    cursor.execute("INSERT INTO workoutEntry (workout_id, data1, data2, set_number, max, type, user_id, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?) RETURNING id", data)
                    id = cursor.fetchone()[0]
                    con.commit()
                elif data1:
                    data = [workout_id, data1, set_id, max, type, session["user_id"], date]
                    cursor.execute("INSERT INTO workoutEntry (workout_id, data1, set_number, max, type, user_id, date) VALUES (?, ?, ?, ?, ?, ?, ?) RETURNING id", data)
                    id = cursor.fetchone()[0]
                    con.commit()
                elif data2:
                    data = [workout_id, data2, set_id, max, type, session["user_id"], date]
                    cursor.execute("INSERT INTO workoutEntry (workout_id, data2, set_number, max, type, user_id, date) VALUES (?, ?, ?, ?, ?, ?, ?) RETURNING id", data)
                    id = cursor.fetchone()[0]
                    con.commit()
                else:
                    return page_error("invalid workout")
                
                if id:
                    if greatest_max:
                        if type == "Duration":
                            if toSeconds(greatest_max) < toSeconds(max):
                                greatest_max = max
                                greatest_max_id = id
                            total_sets += 1
                            collective_sets += 1
                        else:
                            if float(greatest_max) < float(max):
                                greatest_max = float(max)
                                greatest_max_id = id
                            total_sets += 1
                            collective_sets += 1
                    else:
                        if type == "Duration":
                            greatest_max = max
                        else:
                            greatest_max = float(max)
                        greatest_max_id = id
                else:
                    return page_error("invalid workout")

            notes = request.form.get("notes")
            if type == "Duration":
                collective_duration += total_data1
                total_data1 = toTime(total_data1)
            else:
                collective_weight += total_data1
                collective_reps += total_data2
            data = [workout_id, notes, total_data1, total_data2, total_sets, greatest_max_id, session["user_id"], date]
            cursor.execute("INSERT INTO workoutLog (workout_id, text, total_data1, total_data2, total_sets, max_id, user_id, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)
            con.commit()

        #TODO: submit workout SUBMISSION TO D
        data = [collective_weight, collective_reps, collective_duration, collective_sets, session["user_id"], date]
        cursor.execute("INSERT INTO workoutSubmission (collective_weight, collective_reps, collective_duration, collective_sets, user_id, date) VALUES (?, ? ,? ,? ,?, ?)", data)
        con.commit()
        #this is where submit goes to
        return redirect('/')
    data = [session["user_id"]]
    cursor.execute("SELECT * FROM exercise WHERE user_id = ?", data)
    custom_workout_call = cursor.fetchall()
    custom_workout_data = []
    for custom_workout in custom_workout_call:
        temp = {"name": custom_workout[1], "type": custom_workout[2], "primary_muscle": custom_workout[3]}
        custom_workout_data.append(temp)

    data = [1]
    cursor.execute("SELECT * FROM exercise WHERE user_id = ?", data)
    exercise_call = cursor.fetchall()
    exercise_data = [];
    for exercise in exercise_call:
        data = {"name": exercise[1], "type": exercise[2], "primary_muscle": exercise[3]} 
        exercise_data.append(data)
    
    return render_template('log_workout.html', custom_exercise_data = custom_workout_data, exercise_data = exercise_data)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            return page_error("username and or password not found")

        data = [username]
        cursor.execute("SELECT * FROM users WHERE username = ?", data)
        row = cursor.fetchone()
        if row is None:
            return page_error("username not found")
        
        if not bcrypt.checkpw(password.encode('utf-8'), row[2]):
            return page_error("password incorrect")
        
        #set cookies
        session["user_id"] = row[0]

        return redirect('/')
    session.clear()
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if not username or not password or not confirm:
            return page_error("username, password and or confirm not found")
        
        if password != confirm:
            return page_error("password does not match confirmation")
        
        username_sql = (username, )
        cursor.execute("SELECT * FROM users WHERE username = ?", username_sql)
        if cursor.fetchone() is not None:
            return page_error("username in use")
        
        salt = bcrypt.gensalt()
        bytes = password.encode('utf-8')
        insert_data= [username, bcrypt.hashpw(bytes, salt)]
        cursor.execute("INSERT INTO users (username, hash) VALUES (?, ?)", insert_data)
        con.commit()
        session["user_id"] = cursor.lastrowid
        return redirect('/')
    session.clear()
    return render_template('register.html')

@app.route('/about')
def about():
    return render_template('about.html')