from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from email_validator import validate_email
from flask_ckeditor import CKEditor, CKEditorField
from datetime import datetime, time

from helpers import check_password, login_required, get_unique_values, get_number_items

# Configure application
app = Flask(__name__)
# Add CKEditor
ckeditor = CKEditor(app)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/main")
def main():
    return render_template("main.html")

@app.route("/myaccount", methods=["GET", "POST"])
@login_required
def myaccount():
    user_id = session["user_id"]

    firstname_db = db.execute("SELECT firstname FROM users WHERE id = ?", user_id)
    firstname = firstname_db[0]["firstname"]

    lastname_db = db.execute("SELECT lastname FROM users WHERE id = ?", user_id)
    lastname = lastname_db[0]["lastname"]

    username_db = db.execute("SELECT username FROM users WHERE id = ?", user_id)
    username = username_db[0]["username"]

    email_db = db.execute("SELECT emailadress FROM users WHERE id = ?", user_id)
    email = email_db[0]["emailadress"]


    return render_template("myaccount.html", firstname = firstname, lastname = lastname, username = username, email = email)

@app.route("/editinfo", methods=["GET", "POST"])
@login_required
def editinfo():
    if request.method == "GET":
        user_id = session["user_id"]

        firstname_db = db.execute("SELECT firstname FROM users WHERE id = ?", user_id)
        firstname = firstname_db[0]["firstname"]

        lastname_db = db.execute("SELECT lastname FROM users WHERE id = ?", user_id)
        lastname = lastname_db[0]["lastname"]

        username_db = db.execute("SELECT username FROM users WHERE id = ?", user_id)
        username = username_db[0]["username"]

        email_db = db.execute("SELECT emailadress FROM users WHERE id = ?", user_id)
        email = email_db[0]["emailadress"]

        return render_template("editinfo.html", firstname = firstname, lastname = lastname, username = username, email = email)

    else :
        user_id = session["user_id"]
        # Edit Username
        if request.form.get("username"):
            username = request.form.get("username")
            db.execute("UPDATE users SET username = ? WHERE id = ?", username, user_id)

        else :
            username = db.execute("SELECT username FROM users WHERE id = ?", user_id)

        # Edit Firstname
        if request.form.get("firstname") :
            firstname = request.form.get("firstname")
            db.execute("UPDATE users SET firstname = ? WHERE id = ?", firstname, user_id)

        else :
            firstname = db.execute("SELECT firstname FROM users WHERE id = ?", user_id)

        # Edit Lastname
        if request.form.get("lastname") :
            lastname = request.form.get("lastname")
            db.execute("UPDATE users SET lastname = ? WHERE id = ?", lastname, user_id)

        else :
            lastname = db.execute("SELECT lastname FROM users WHERE id = ?", user_id)


        # Edit Email
        if request.form.get("email") :
            email = request.form.get("email")

            if validate_email(email):
                db.execute("UPDATE users SET emailadress = ? WHERE id = ?", email, user_id)

            else :
                return render_template("apology.html", apology = "emailerror")

        else :
            email = db.execute("SELECT emailadress FROM users WHERE id = ?", user_id)

        return redirect("/myaccount")


@app.route("/editpassw", methods=["GET", "POST"])
@login_required
def editpassw():
    if request.method == "GET":
        return render_template("editpassw.html")

    else :
        user_id = session["user_id"]
        oldpassw = request.form.get("oldpassword")
        passw = request.form.get("password")
        confpassw = request.form.get("confpassword")

        rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)
        if not check_password_hash(rows[0]["hash"], oldpassw):
            return render_template("apology.html", apology="invalid old password")

        if not check_password(passw):
            return render_template("apology.html", apology="invalid passw")

        if passw != confpassw :
            return render_template("apology.html", apology="invalid conf")

        hash = generate_password_hash(passw)

        db.execute("UPDATE users SET hash = ? WHERE id = ?", hash, user_id)

        return redirect("/myaccount")




@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    else :
        username = request.form.get("username")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")


        if not firstname :
            apology = "no first"
            return render_template('register.html', apology = apology)

        if not lastname :
            apology = "no last"
            return render_template('apology.html', apology = apology)

        if not username :
            apology = "no username"
            return render_template('apology.html', apology = apology)

        if not email :
            apology = "no email"
            return render_template('apology.html', apology = apology)

        if not password :
            apology = "no passw"
            return render_template('apology.html', apology = apology)

        if not confirmation :
            apology = "no confirmation"
            return render_template('apology.html', apology = apology)

        if password != confirmation :
            apology = "passw match error"
            return render_template('apology.html', apology = apology)

        if not check_password(password):
            apology = "passw error"
            return render_template('apology.html', apology = apology)

        hash = generate_password_hash(password)

        try :
            new_user = db.execute("INSERT INTO users (username, firstname, lastname, emailadress, hash) VALUES(?, ?, ?, ?, ?)", username, firstname, lastname, email, hash)
        except :
            apology = "username error"
            return render_template('apology.html', apology = apology)

        session["user_id"] = new_user

        flash(f"Welcome {username}!")

        return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "GET" :
        return render_template("login.html")

    else:
        username = request.form.get("user")
        password = request.form.get("passw")

        if not username:
            apology = "must provide username"
            return render_template('apology.html', apology = apology)

        elif not password:
            apology = "must provide password"
            return render_template('apology.html', apology = apology)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return render_template('apology.html', apology="invalid username and/or password")

        session["user_id"] = rows[0]["id"]

        flash(f"Welcome back {username}!")

        return redirect("/")



@app.route("/logout")
def logout():
    session.clear()
    flash("Goodbye !")
    return render_template("main.html")


@app.route("/todo_main", methods=["GET", "POST"])
@login_required
def todo_main():
    user_id = session["user_id"]
    #lists_db = db.execute("SELECT list FROM todo WHERE user_id = ? ORDER BY list ASC", user_id)
    #lists_unique = get_unique_values(lists_db)
    dict_db = db.execute("SELECT list FROM todo WHERE user_id = ? ORDER BY list ASC", user_id)
    count = {}
    for item in dict_db:
        list = item.get('list')
        if list in count :
            count[list] += 1
        else :
            count[list] = 1

    if not dict_db :
        return render_template("todo_main.html", content = "none")

    else :
        return render_template("todo_main.html", content = "lists", lists = count)


@app.route("/create_list", methods=["GET", "POST"])
@login_required
def create_list():
    if request.method == "GET" :
        return render_template("createlist.html")
    else :
        user_id = session["user_id"]
        name_list = request.form.get("name_list").strip()
        task = request.form.get("task").strip()
        now = datetime.now()
        date = now.strftime("%Y-%m-%d (%H:%M:%S)")

        if not name_list :
            return render_template("apology.html", apology = "no name of list")

        if not task :
            return render_template("apology.html", apology = "no task")

        existingLists = db.execute("SELECT list FROM todo WHERE user_id = ?", user_id)

        for list in existingLists :
            if list["list"] == name_list:
                return render_template("apology.html", apology = "existinglist", list = list["list"])

        db.execute("INSERT INTO todo (list, task, date, user_id) VALUES (?, ?, ?, ?)", name_list, task, date, user_id)

        return redirect("/todo_main")

@app.route("/create_task", methods=["GET", "POST"])
@login_required
def create_task():
    if request.method == "GET" :
        user_id = session["user_id"]
        lists_db = db.execute("SELECT list FROM todo WHERE user_id = ?", user_id)
        lists = get_unique_values(lists_db)
        return render_template("createtask.html", lists = lists)

    else :
        user_id = session["user_id"]
        name_task = request.form.get("name_task").strip()
        list_selected = request.form.get("lists")
        now = datetime.now()
        date = now.strftime("%Y-%m-%d (%H:%M:%S)")

        if not name_task:
            return render_template("apology.html", apology = "no content of task")

        if not list_selected:
            return render_template("apology.html", apology = "no name of list_task")

        existingTasks = db.execute("SELECT task FROM todo WHERE (list = ? AND user_id = ?)", list_selected, user_id)

        for task in existingTasks :
            if task["task"].lower() == name_task.lower():
                return render_template("apology.html", apology = "existingtask", task = task["task"], list = list_selected)

        db.execute("INSERT INTO todo(list, task, date, user_id) VALUES (?, ?, ?, ?)", list_selected, name_task, date, user_id)

        flash("Task added ! ")

        return redirect(url_for('list', listName = list_selected))

@app.route('/delete_list/<listName>')
@login_required
def delete_list(listName):
    user_id = session["user_id"]
    db.execute("DELETE FROM todo WHERE (list = ? AND user_id = ?)", listName, user_id)
    return redirect("/todo_main")

@app.route('/edit_list/<listName>', methods=["GET", "POST"])
@login_required
def edit_list(listName):
    if request.method == "GET" :
        return render_template("todo_main.html")

    else:
        user_id = session["user_id"]
        newName = request.form.get("newList")

        if not newName :
            return render_template("apology.html", apology = "no name list", listName = listName)

        existingLists = db.execute("SELECT list FROM todo WHERE user_id = ?", user_id)

        for list in existingLists :
            if list["list"] == newName.lower():
                return render_template("apology.html", apology = "existinglistEdit", list = listName)

        db.execute("UPDATE todo SET list = ? WHERE (list = ? AND user_id = ?)", newName, listName, user_id)

        return redirect("/todo_main")

@app.route('/list/<listName>', methods=["GET", "POST"])
@login_required
def list(listName):
    user_id = session["user_id"]
    lists = db.execute("SELECT task, date, id FROM todo WHERE (list = ? AND user_id = ?) ORDER BY date ASC", listName, user_id)
    if not lists :
        return render_template("lists.html", content = "none", nameList = listName)
    else :
        return render_template("lists.html", lists = lists, nameList = listName)



@app.route('/edit_task/<taskID>/<listName>', methods=["GET", "POST"])
@login_required
def edit_task(taskID, listName):
    if request.method == "GET" :
        return redirect(url_for('list', listName = listName))

    else:
        user_id = session["user_id"]
        newContent = request.form.get("newContent")


        if not newContent :
            return render_template("apology.html", apology = "noContentTask")

        existingTasks = db.execute("SELECT task FROM todo WHERE (list = ? AND user_id = ?)", listName, user_id)

        for task in existingTasks :
            if task["task"].lower() == newContent.lower():
                return render_template("apology.html", apology = "existingtaskEdit", task = task["task"], list = listName)

        db.execute("UPDATE todo SET task = ? WHERE (list = ? AND id = ? AND user_id = ?)", newContent, listName, taskID, user_id)

        return redirect(url_for('list', listName = listName))

@app.route('/delete_task/<taskID>/<listName>')
@login_required
def delete_task(taskID, listName):
    user_id = session["user_id"]
    db.execute("DELETE FROM todo WHERE (list = ? AND id = ? AND user_id = ?)", listName, taskID, user_id)
    return redirect(url_for('list', listName = listName))


@app.route('/check_task/<taskID>/<listName>/<taskContent>', methods=["GET", "POST"])
@login_required
def check_task(taskID, listName, taskContent):
    user_id = session["user_id"]
    now = datetime.now()
    date = now.strftime("%Y-%m-%d (%H:%M:%S)")

    db.execute("INSERT INTO todo_done (list, task, date_done, user_id) VALUES (?, ?, ?, ?)", listName, taskContent, date, user_id)
    db.execute("DELETE from todo WHERE (list = ? AND id = ? AND user_id = ?)", listName, taskID, user_id)

    return redirect(url_for('list', listName = listName))


@app.route('/completed_tasks', methods=["GET", "POST"])
@login_required
def completed_tasks():
    user_id = session["user_id"]
    lists = db.execute("SELECT list, task, date_done FROM todo_done WHERE user_id = ? ORDER BY date_done ASC", user_id)

    if not lists :
        return render_template("completed_tasks.html", content = "none")

    else :
        return render_template("completed_tasks.html", lists = lists)


@app.route('/delete_taskDone/<taskContent>/<listName>')
@login_required
def delete_taskDone(taskContent, listName):
    user_id = session["user_id"]
    db.execute("DELETE FROM todo_done WHERE (list = ? AND task = ? AND user_id = ?)", listName, taskContent, user_id)
    lists = db.execute("SELECT list, task, date_done FROM todo_done WHERE user_id = ? ORDER BY date_done ASC", user_id)
    return render_template("completed_tasks.html", lists = lists)

@app.route("/quit_todo")
@login_required
def quit_todo():
    flash("You exited To-do !")
    return redirect("/")

@app.route("/EmptyCompletedTasks", methods=["GET", "POST"])
@login_required
def EmptyCompletedTasks():
    user_id = session["user_id"]
    db.execute("DELETE FROM todo_done WHERE user_id = ?", user_id)
    return redirect("/completed_tasks")

@app.route("/notes_main", methods=["GET","POST"])
@login_required
def notes_main():
    user_id = session["user_id"]
    notes_db = db.execute("SELECT id, title, content, date, color FROM notes WHERE (user_id = ? AND archived = ?)", user_id, "0")

    if not notes_db :
        return render_template("notes_main.html", content = "none")
    else:
        return render_template("notes_main.html", content = "notes", notes = notes_db)

@app.route("/create_note", methods=["GET", "POST"])
@login_required
def create_note():
    if request.method == "GET" :
        return render_template("createnote.html")
    else :
        user_id = session["user_id"]
        title_note = request.form.get("title_note").strip()
        content_note = request.form.get("content_note").strip()
        color_note = request.form.get("color_note")

        now = datetime.now()
        date = now.strftime("%Y-%m-%d (%H:%M)")

        if not title_note :
            return render_template("apology.html", apology = "no title_note")

        if not content_note :
            return render_template("apology.html", apology = "no content_note")

        db.execute("INSERT INTO notes(title, content, date, archived, color, user_id) VALUES (?, ?, ?, ?, ?, ?)",
                   title_note, content_note, date, "0", color_note, user_id)

        flash("Note added !")

        return redirect("/notes_main")

@app.route("/edit_note/<noteID>/<fromWhere>", methods=["GET", "POST"])
@login_required
def edit_note(noteID, fromWhere):
    if request.method == "GET" :
        return redirect("/notes_main")
    else :
        user_id = session["user_id"]
        newContent = request.form.get("newContent").strip()
        newTitle = request.form.get("newTitle").strip()
        newColor = request.form.get("newColor")

        if not newContent :
            return render_template("apology.html", apology = "no new Note Content")

        if not newTitle :
            return render_template("apology.html", apology = "no new Note title")

        db.execute("UPDATE notes SET content = ?, title = ?, color = ? WHERE (id = ? AND user_id = ?)", newContent, newTitle, newColor, noteID, user_id)

        if fromWhere == "note_html":
            note = db.execute("SELECT id, title, content, date, color FROM notes WHERE (id = ? AND user_id = ?)", noteID, user_id)
            return render_template("note.html", note = note[0])

        if fromWhere == "notes_main_html":
            return redirect("/notes_main")


@app.route("/archive_note/<noteID>")
@login_required
def archive_note(noteID):
    user_id = session["user_id"]

    db.execute("UPDATE notes SET archived = ? WHERE (id = ? AND user_id = ?)", "1", noteID, user_id)

    flash("Note archived!")

    return redirect("/notes_main")


@app.route("/maximize_note/<noteID>")
@login_required
def maximize_note(noteID):
    user_id = session["user_id"]

    note = db.execute("SELECT id, title, content, date, color FROM notes WHERE (id = ? AND user_id = ?)", noteID, user_id)

    return render_template("note.html", note = note[0])

@app.route("/archived_notes")
@login_required
def archived_notes():
    user_id = session["user_id"]
    archivedNotes_db = db.execute("SELECT id, title, content, date, color FROM notes WHERE (user_id = ? AND archived = ?)", user_id, "1")

    if not archivedNotes_db :
        return render_template("archived_notes.html", content = "none")
    else :
        return render_template("archived_notes.html", content = "archived_notes", notes = archivedNotes_db)

@app.route("/recover_note/<noteID>")
@login_required
def recover_note(noteID):
    user_id = session["user_id"]

    db.execute("UPDATE notes SET archived = ? WHERE (id = ? AND user_id = ?)", "0", noteID, user_id)

    flash("Note recovered!")

    return redirect("/archived_notes")


@app.route("/delete_note/<noteID>")
@login_required
def delete_note(noteID):
    user_id = session["user_id"]

    db.execute("DELETE FROM notes WHERE (id = ? AND user_id = ?)", noteID, user_id)

    flash("Note deleted!")

    return redirect("/archived_notes")

@app.route("/quit_notes")
@login_required
def quit_notes():
    flash("You exited Notes !")
    return redirect("/")



@app.route("/planning_main")
@login_required
def planning_main():
    user_id = session["user_id"]
    planning_db = db.execute("SELECT * FROM planning WHERE (user_id = ? AND begDate >= CURRENT_TIMESTAMP) ORDER BY begDate", user_id)

    if not planning_db :
        return render_template("planning_main.html", content = "none")

    else :
        return render_template("planning_main.html", content = "planning", planning = planning_db)

@app.route("/create_event", methods=["GET", "POST"])
@login_required
def create_event():
    if request.method == "GET" :
        return render_template("createevent.html")
    else:
        user_id = session["user_id"]
        now = datetime.now()
        creaDate = now.strftime("%Y-%m-%d (%H:%M)")
        # declarations
        uniqueDate = False
        uniqueTime = False
        color = "white"

        # TITLE
        title_event = request.form.get("title_event").strip()

        # CATEGORY
        category_event = request.form.get("category_event").title()

        # DESCRIPTION
        details_event = request.form.get("details_event").strip().capitalize()

        # BEGDATE
         # get the date in a string format
        begDateInput = request.form.get("beg_date")
        bdyear, bdmonth, bdday = begDateInput.split("-")
         # cast the date to a datetype format
        begDate = datetime(int(bdyear), int(bdmonth), int(bdday))

        # ENDDATE
        endDateInput = request.form.get("end_date")
        edyear, edmonth, edday = endDateInput.split("-")
        endDate = datetime(int(edyear), int(edmonth), int(edday))


        # test if begdate happens after enddate
        if begDate > endDate :
            # error apology : "you must enter a begDate that happens before the endDate"
            return render_template("apology.html", apology = "error date")
        # else keep going in the programm

        # BEGTIME
         # get the time in a string format
        begTimeInput = request.form.get("beg_time")
        if begTimeInput:
            bthour, btmin = begTimeInput.split(":")
            # cast the date to a timetype
            begTime = time(int(bthour), int(btmin))

        # ENDTIME
        endTimeInput = request.form.get("end_time")
        if endTimeInput :
            if not begTimeInput :
                return render_template("apology.html", apology = "error endtime")
            else :
                ethour, etmin = endTimeInput.split(":")
                endTime = time(int(ethour), int(etmin))

        if not endTimeInput :
            if begTimeInput :
                return render_template("apology.html", apology = "error begtime")

        # test if begdate = enddate
        if begDate == endDate :
            # set uniqueDate to True
            uniqueDate = True

            if begTimeInput and endTimeInput :
            # test if begtime happens after endtime
                if endTime < begTime :
                    # error apology : "you must enter a begTime that happens before the endTime"
                    return render_template("apology.html", apology = "error time")

        if begTimeInput and endTimeInput :
            # test if begtime = endtime
            if begTime == endTime :
                # set uniqueTime to True
                uniqueTime = True

        # set the variable 'color' with tests
        if category_event == "Personal":
            # if personal -> bg-pink-100
            color = "pink-100"

        if category_event == "Professional":
            # if profesional -> bg-blue-100
            color = "blue-100"

        if category_event == "Appointment":
            # if appoitment -> bg-red-100
            color = "red-100"

        if category_event == "Birthday":
            # if birthday -> bg-green-100
            color = "green-100"

        if category_event == "Other":
            color = "gray-100"

        # cast date and time back into a string format
        begDate = begDate.strftime('%Y-%m-%d')
        endDate = endDate.strftime('%Y-%m-%d')
        if begTimeInput and endTimeInput :
            begTime = begTime.strftime('%H:%M')
            endTime = endTime.strftime('%H:%M')
        else :
            begTime = False
            endTime = False

        # set the database
        db.execute("INSERT INTO planning (title, category, begDate, endDate, begTime, endTime, description, creaDate, user_id, color, uniqueDate, uniqueTime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   title_event, category_event, begDate, endDate, begTime, endTime, details_event, creaDate, user_id, color, uniqueDate, uniqueTime)

        return redirect("/planning_main")

@app.route("/delete_event/<eventID>/<fromwhere>")
@login_required
def delete_event(eventID, fromwhere):
    user_id = session["user_id"]

    db.execute("DELETE FROM planning WHERE (id = ? AND user_id = ?)", eventID, user_id)

    flash("Event deleted!")

    if fromwhere == 'past_events' :
        return redirect("/past_events")
    else :
        return redirect("/planning_main")

@app.route("/search_event_main", methods=["POST", "GET"])
@login_required
def search_event_main():
    if request.method == "GET" :
        return redirect("/planning_main")
    else :
        user_id = session["user_id"]

        category_event = request.form.get("category_event")

        if category_event == "All":
            planning_db = db.execute("SELECT * FROM planning WHERE (user_id = ? AND begDate >= CURRENT_TIMESTAMP) ORDER BY begDate", user_id)

        if category_event == "Personal" :
            planning_db = db.execute("SELECT * FROM planning WHERE (category = ? AND user_id = ? AND begDate >= CURRENT_TIMESTAMP) ORDER BY begDate", "Personal", user_id)

        if category_event == "Professional":
            planning_db = db.execute("SELECT * FROM planning WHERE (category = ? AND user_id = ? AND begDate >= CURRENT_TIMESTAMP) ORDER BY begDate", "Professional", user_id)

        if category_event == "Appointment":
            planning_db = db.execute("SELECT * FROM planning WHERE (category = ? AND user_id = ? AND begDate >= CURRENT_TIMESTAMP) ORDER BY begDate", "Appointment", user_id)

        if category_event == "Birthday":
            planning_db = db.execute("SELECT * FROM planning WHERE (category = ? AND user_id = ? AND begDate >= CURRENT_TIMESTAMP) ORDER BY begDate", "Birthday", user_id)

        if category_event == "Other":
            planning_db = db.execute("SELECT * FROM planning WHERE (category = ? AND user_id = ? AND begDate >= CURRENT_TIMESTAMP) ORDER BY begDate", "Other", user_id)

        if not planning_db :
            return render_template("apology.html", apology = "failed search")


        return render_template("planning_main.html", content = "planning", planning = planning_db)

@app.route("/search_event_past", methods=["POST", "GET"])
@login_required
def search_event_past():
    if request.method == "GET" :
        return redirect("/past_events")
    else :
        user_id = session["user_id"]

        category_event = request.form.get("category_event")

        if category_event == "All":
            planning_db = db.execute("SELECT * FROM planning WHERE (user_id = ? AND begDate < CURRENT_TIMESTAMP) ORDER BY begDate", user_id)

        if category_event == "Personal" :
            planning_db = db.execute("SELECT * FROM planning WHERE (category = ? AND user_id = ? AND begDate < CURRENT_TIMESTAMP) ORDER BY begDate", "Personal", user_id)

        if category_event == "Professional":
            planning_db = db.execute("SELECT * FROM planning WHERE (category = ? AND user_id = ? AND begDate < CURRENT_TIMESTAMP) ORDER BY begDate", "Professional", user_id)

        if category_event == "Appointment":
            planning_db = db.execute("SELECT * FROM planning WHERE (category = ? AND user_id = ? AND begDate < CURRENT_TIMESTAMP) ORDER BY begDate", "Appointment", user_id)

        if category_event == "Birthday":
            planning_db = db.execute("SELECT * FROM planning WHERE (category = ? AND user_id = ? AND begDate < CURRENT_TIMESTAMP) ORDER BY begDate", "Birthday", user_id)

        if category_event == "Other":
            planning_db = db.execute("SELECT * FROM planning WHERE (category = ? AND user_id = ? AND begDate < CURRENT_TIMESTAMP) ORDER BY begDate", "Other", user_id)

        if not planning_db :
            return render_template("apology.html", apology = "failed search past")


        return render_template("past_events.html", content = "planning", planning = planning_db)

@app.route("/past_events")
@login_required
def past_event():
    user_id = session["user_id"]
    planning_db = db.execute("SELECT * FROM planning WHERE (user_id = ? AND begDate < CURRENT_TIMESTAMP) ORDER BY begDate", user_id)

    if not planning_db :
        return render_template("past_events.html", content = "none")

    else :
        return render_template("past_events.html", content = "planning", planning = planning_db)

@app.route("/quit_planning")
@login_required
def quit_planning():
    flash("You exited your Planning !")
    return redirect("/")


@app.route("/edit_event/<eventID>/<fromwhere>", methods=["GET", "POST"])
@login_required
def edit_event(eventID, fromwhere):
    if request.method == "GET" :
        if fromwhere == "planning_main":
            return redirect("/planning_main")
        else :
            return redirect("/past_events")

    else:
        user_id = session["user_id"]
        uniqueDate = False
        uniqueTime = False
        color = "white"
        title_event = request.form.get("newTitle").strip()
        category_event = request.form.get("newCategory").title()
        details_event = request.form.get("newDetails_event").capitalize()

        begDateInput = request.form.get("newBeg_date")
        bdyear, bdmonth, bdday = begDateInput.split("-")
        begDate = datetime(int(bdyear), int(bdmonth), int(bdday))

        endDateInput = request.form.get("newEnd_date")
        edyear, edmonth, edday = endDateInput.split("-")
        endDate = datetime(int(edyear), int(edmonth), int(edday))

        if begDate > endDate :
            return render_template("apology.html", apology = "error edit date")

        begTimeInput = request.form.get("newBeg_time")
        if begTimeInput:
            bthour, btmin = begTimeInput.split(":")
            begTime = time(int(bthour), int(btmin))

        endTimeInput = request.form.get("newEnd_time")
        if endTimeInput :
            if not begTimeInput :
                return render_template("apology.html", apology = "error edit endtime")
            else :
                ethour, etmin = endTimeInput.split(":")
                endTime = time(int(ethour), int(etmin))

        if not endTimeInput :
            if begTimeInput :
                return render_template("apology.html", apology = "error edit begtime")

        if begDate == endDate :
            uniqueDate = True

            if begTimeInput and endTimeInput :
                if endTime < begTime :
                    return render_template("apology.html", apology = "error edit time")

        if begTimeInput and endTimeInput :
            if begTime == endTime :
                uniqueTime = True

        if category_event == "Personal":
            color = "pink-100"

        if category_event == "Professional":
            color = "blue-100"

        if category_event == "Appointment":
            color = "red-100"

        if category_event == "Birthday":
            color = "green-100"

        if category_event == "Other":
            color = "gray-100"

        begDate = begDate.strftime('%Y-%m-%d')
        endDate = endDate.strftime('%Y-%m-%d')
        if begTimeInput and endTimeInput :
            begTime = begTime.strftime('%H:%M')
            endTime = endTime.strftime('%H:%M')
        else :
            begTime = False
            endTime = False

        # set the database
        db.execute("UPDATE planning SET title = ?, category = ?, begDate = ?, endDate = ?, begTime = ?, endTime = ?, description = ?, color = ?, uniqueDate = ?, uniqueTime = ? WHERE (id = ? AND user_id = ?)",
                   title_event, category_event, begDate, endDate, begTime, endTime, details_event, color, uniqueDate, uniqueTime, eventID, user_id)

        if fromwhere == "planning_main":
            return redirect("/planning_main")
        else :
            return redirect("/past_events")
