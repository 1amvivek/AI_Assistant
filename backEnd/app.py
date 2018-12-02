from flask import Flask, render_template, session
import requests
import json
import ast
URL = "http://18.222.204.247:3000/"
app = Flask(__name__)
app.secret_key = 'sansa'


@app.route('/chart')
def chart():
    #for pie chart for a particular user
    user_logs = logAnalysis("user")

    catlist = ast.literal_eval(user_logs)

    chart_user = {"Technology": catlist['technology'],
                  "Social Networking": catlist['social_networking'],
                  "Google": catlist['google'],
                  "Blogs": catlist['blogs'],
                  "E-Commerce": catlist['ecommerce'],
                  "E-mail": catlist['e-mail'],
                  "Finance": catlist['finance'],
                  "Health": catlist['health'],
                  "Miscellaneous": catlist['misc']}

    #for bar chart avg visits of all users
    total_users = count_users()

    user_logs_all = logAnalysis("all")

    catlist_all = ast.literal_eval(user_logs_all)

    avg_visits_tech = (catlist_all['technology'] / total_users)
    avg_visits_social = (catlist_all['social_networking'] / total_users)
    avg_visits_google = (catlist_all['google'] / total_users)
    avg_visits_blogs = (catlist_all['blogs'] / total_users)
    avg_visits_ecommerce = (catlist_all['ecommerce'] / total_users)
    avg_visits_email = (catlist_all['e-mail'] / total_users)
    avg_visits_finance = (catlist_all['finance'] / total_users)
    avg_visits_health = (catlist_all['health'] / total_users)
    avg_visits_misc = (catlist_all['misc'] / total_users)

    avg_user = {"Technology": avg_visits_tech,
                "Social Networking": avg_visits_social,
                "Google": avg_visits_google,
                "Blogs": avg_visits_blogs,
                "E-Commerce": avg_visits_ecommerce,
                "E-mail": avg_visits_email,
                "Finance": avg_visits_finance,
                "Health": avg_visits_health,
                "Miscellaneous": avg_visits_misc}

    all_user = {"Technology": catlist_all['technology'],
                "Social Networking": catlist_all['social_networking'],
                "Google": catlist_all['google'],
                "Blogs": catlist_all['blogs'],
                "E-Commerce": catlist_all['ecommerce'],
                "E-mail": catlist_all['e-mail'],
                "Finance": catlist_all['finance'],
                "Health": catlist_all['health'],
                "Miscellaneous": catlist_all['misc']}



    return render_template('chart.html', chart_user=chart_user, avg_user=avg_user, all_user=all_user)


@app.route('/login')
def login():
    try:
        r = requests.post(URL, json={"logemail": "cnk90@gmail.com", "logpassword": "cnk90"})
        if r.status_code is not None:
            if r.status_code == 401:
                print("Wrong password attempted")
                return r.text
            elif r.status_code == 200:
                resp = json.loads(r.text)
                print("Successfully logged in")
                session['user_id'] = resp["id"]
                return "Logged in as {} <br>".format(session['user_id'])
            else:
                return "Something wrong with the response {}".format(r.status_code)
        else:
            return "No status code, something wrong!"
    except:
        message = 'Connection failed to establish for {}'.format(URL)
        print(message)
        return message


@app.route('/signup')
def signup():
    r = requests.post(URL, json={"email": "cnk91@gmail.com", "username": "cnk91@gmail.com", "password": "cnk91", "passwordConf": "cnk91"})

    resp = r.text

    return resp


# @app.route('/logAnalysis', methods=['GET'])
def logAnalysis(logs_for):
    try:
        if 'user_id' in session:
            if logs_for == "user":
                r = requests.get(URL + "logs/" + session['user_id'])
                print("Successfully hit the url")
            else:
                r = requests.get(URL + "logs/")
                print("Successfully hit the url")

            resp = json.loads(r.text)

            length = len(resp)
            print(length)

            categories = {"social_networking": 0, "google": 0, "blogs": 0, "ecommerce": 0, "misc": 0,
                        "e-mail": 0, "technology": 0, "finance": 0, "health": 0}

            for i in range(length):
                if resp[i]["url"].find("www.google.com") != -1:
                    categories["google"] += 1
                elif resp[i]["url"].find("facebook.com") != -1 or resp[i]["url"].find("twitter.com") != -1:
                    categories["social_networking"] += 1
                elif resp[i]["url"].find("amazon.com") != -1 or resp[i]["url"].find("shutterfly.com") != -1 or resp[i]["url"].find("ebay.com") != -1:
                    categories["ecommerce"] += 1
                elif resp[i]["url"].find("medium.com") != -1 or resp[i]["url"].find("blogger.com") != -1 or resp[i]["url"].find("wordpress.com") != -1:
                    categories["blogs"] += 1
                elif resp[i]["url"].find("mail.google.com") != -1 or resp[i]["url"].find("outlook.office365.com") != -1:
                    categories["e-mail"] += 1
                elif resp[i]["url"].find("chase.com") != -1 or resp[i]["url"].find("usbank.com") != -1 or resp[i]["url"].find("online.citi.com") != -1:
                    categories["finance"] += 1
                elif resp[i]["url"].find("stackoverflow.com") != -1 or resp[i]["url"].find("kaggle.com") != -1:
                    categories["technology"] += 1
                elif resp[i]["url"].find("health") != -1:
                    categories["health"] += 1
                else:
                    categories["misc"] += 1
            return str(categories)
        else:
            return "Login into the application to see view the logs"
    except:
        message = 'Unable to fetch logs for {}'.format(session['user_id'])
        print(message)
        return message


def count_users():
    try:
        if 'user_id' in session:
            r = requests.get(URL + "logs/")
            print("Successfully hit the url")

            resp = json.loads(r.text)

            length = len(resp)
            print(length)

            users_list = []

            for i in range(length):
                if resp[i]["user_id"] not in users_list:
                    users_list.append(resp[i]["user_id"])

            return len(users_list)
        else:
            return "Login into the application to see view the log analysis"
    except:
        message = 'Unable to fetch count of all users'
        print(message)
        return message


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return "Logged out successfully"


if __name__ == '__main__':
    app.run(debug=True)
