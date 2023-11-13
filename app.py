from flask import *
from dbhelper import *

#PRE SET 1
app = Flask(__name__)
app.secret_key="2023kUr!$t@t!0nKKEEYYv0id(\./);"

#GLOBALS CONSTS
headers : list = ["IDNO", "LASTNAME", "FIRSTNAME", "COURSE", "LEVEL", "ACTIONS"]

#1. ADD DATA
@app.route("/add_data", methods=['POST'])
def add_data_attempt():
    if request.method == 'POST':
        idno = request.form["idno"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        course = request.form["course"]
        level = request.form["level"]

        result : bool = exists('idno', str(idno))
        print("HEY")
        print(result)
        if not result:
            result = add_data('student', idno = idno, firstname = firstname, lastname = lastname, level = level, course = course)
            if result == 1:
                flash("Added successfully!")
                return redirect("/")
            else:
                flash("Failed!")
                return redirect("/")
        else:
            flash(f"Id number: "+ idno + " already exists!")
            return redirect("/")

#2. EDIT DATA
@app.route("/update_data", methods=['POST'])
def update_data_attempt():
    if request.method == 'POST':
        unique_id = request.form["id"]
        idno = request.form["idno"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        course = request.form["course"]
        level = request.form["level"]

        result = update_data('student', id = unique_id, idno = idno, firstname = firstname, lastname = lastname, level = level, course = course)
        if result == 1:
            flash("Edited successfully!")
            return redirect("/")
        else:
            flash("Failed!")
            return redirect("/")

#3. DELETE DATA
@app.route("/delete_data", methods=['GET'])
def delete_data_attempt():
     if request.method == 'GET':
        unique_id = request.args.get('id')
        result = delete_data('student', id = unique_id)
        if result == 1:
            flash(f"Student was deleted successfully!")
        else:
            flash("Failed!")
        return redirect("/")

#4. GET DATA
@app.route("/search_data", methods=['GET'])
def search_data_attempt():
    if request.method == 'GET':
        search_query : str = request.args.get('search_query')
        data = get_all_data('student')

        finalstudent = []

        for datum in data:
             if any(search_query.lower() in str(value).lower() for key, value in datum.items() if key != 'id'):
                 
                tempdict = {
                    "id" : datum['id'],
                    "idno" : datum['idno'],
                    "firstname" : datum['firstname'],
                    "lastname" : datum['lastname'],
                    "course" : datum['course'],
                    "level" : datum['level']
                }
                finalstudent.append(tempdict)


    print("Hey")
    print(finalstudent)
    global headers
    return render_template("searchquery.html", data = finalstudent, search_query = search_query, headers = headers) 





#ROUTES:
@app.route("/routeaddstudent")
def route_add_student():
    return render_template("addstudent.html")  

@app.route("/routeeditstudent", methods=['POST'])     
def route_edit_student(): 
    unique_id = request.form["id"]
    data = get_data('student', id = unique_id)
    return render_template("editstudent.html", data = data)    

@app.route("/")
def main():
    data = get_all_data('student')
    global headers
    return render_template("index.html", data = data, headers = headers)




#PRE SET 2
if __name__=="__main__":
    app.run(host="0.0.0.0", port="5000", debug=True, use_reloader=True)