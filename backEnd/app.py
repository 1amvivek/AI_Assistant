import requests
import json
import ast
from models.habits_model import get_habits
from models.interests_model import get_interests
from models.spent_model import get_spent

from flask import Flask, render_template, session, request, redirect, url_for
import numpy as np

URL = "http://18.222.204.247:3000/"

app = Flask(__name__)
app.secret_key = 'sansa'


@app.route('/')
def landing_page():
    return render_template('index.html')


@app.route('/chart')
def chart():
	chart_user_has_content = True
	#for pie chart for a particular user

	username = session['username']

	user_logs = logAnalysis("user")

	catlist = ast.literal_eval(user_logs)

	if (sum(list(catlist.values())) == 0):
		chart_user_has_content = False

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

	return render_template('chart.html', username=username, chart_user=chart_user, avg_user=avg_user, all_user=all_user,
						   chart_user_has_content=chart_user_has_content)


@app.route('/login_page')
def login_page():
	return render_template('login.html')



@app.route('/signup_page')
def signup_page():
	return render_template('signup.html')


@app.route('/login', methods=['POST'])
def login():
    try:
        logemail = request.form['logemail']
        logpassword = request.form['logpassword']


        print(logemail)
        print(logpassword)

        if logemail == 'admin' and logpassword == 'admin':
        	return redirect(url_for('admin'))

        if logemail is None or logpassword is None:
            return "Correct Details"

        r = requests.post(URL, json={"logemail": logemail, "logpassword": logpassword})

        print("Hit the login URL")

        if r.status_code is not None:
            if r.status_code == 401:
                print("Wrong password attempted")
                return r.text
            elif r.status_code == 200:
                resp = json.loads(r.text)
                print("Successfully logged in")

                session['user_id'] = resp["id"]
                session['username'] = resp["username"]
                session['gender'] = resp["gender"]
                session['occupation'] = resp["occupation"]
                session['interests1'] = resp["interests1"]
                session['interests2'] = resp["interests2"]
                session['interests3'] = resp["interests3"]
                session['maritalStatus'] = resp["maritalStatus"]
                session['age'] = resp["age"]

                return redirect(url_for('chart'))
            else:
                return "Something wrong with the response {}".format(r.status_code)
        else:
            return "No status code, something wrong!"
    except Exception as e:
        print(e)
        return str(e)


@app.route('/signup', methods=['POST'])
def signup():
    try:
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        passwordConf = request.form['passwordConf']
        gender = request.form['options']
        occupation = request.form['occupation']
        interests1 = request.form['interests1']
        interests2 = request.form['interests2']
        interests3 = request.form['interests3']
        maritalStatus = request.form['maritalStatus']
        age = request.form['age']

        requests.post(URL, json={"email": email,
                                "username": username,
                                "password": password,
                                "passwordConf": passwordConf,
                                "gender": gender,
                                "occupation": occupation,
                                "interests1": interests1,
                                "interests2": interests2,
                                "interests3": interests3,
                                "maritalStatus": maritalStatus,
                                "age": age
                                })

        return render_template('index.html')
    except Exception as e:
        print(e)
        return str(e)


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
	except Exception as e:
		print(e)
		return str(e)


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
	except Exception as e:
		print(e)
		return str(e)



@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return render_template('index.html')


# http://localhost:5000/habits?id=5bf0c3889c7cd00010aa1134
@app.route('/habits')
def habits_model():
	print("In habits model")
	if session['user_id']:
		habits, aggr_logs =  get_habits(session['user_id'])
		session['habits'] = habits
		session['max_day'] = habits["max_day"]
		return render_template('habits_chart.html', habits=habits, aggr_logs=aggr_logs)
	else:
		return "Login to check your habits"

@app.route('/interests')
def interests():
	if session['user_id'] == '5bf0bf6f9c7cd00010aa112a':
		interests = {	'Sports' : 
						["Cricket is a beatiful sport. Baseball, hockey are not. Dhoni is the best!!", 
						"Sergio Garcia\'s 13-Stroke Masters Hole Shows Even A Champ Can Epically Fail 'It\'s just one of those things,'' he said.",
						"Super Runner Semenya Faces New Testosterone Limits In Sports Gender Battle Officials grapple again with fair competition and gender definition"], 
						
						'Technology' : 
						["Facebook Pledges To Add More Local News To Newsfeeds 'People who know what happening around them are more likely to get involved and help make a difference,' said CEO Mark Zuckerberg.",
						 "Elon Musk Pulls Tesla, SpaceX Facebook Pages In Nod To #DeleteFacebook He also deleted his personal profile",
						 "Google Cancels 'Town Hall' On Gender Dispute Over Fears Of Online Harassment By Far-Right The company-wide meeting was slated to discuss the controversy over a memo opposing diversity policies."], 
						
						'Entertainment' : 
						['Will Smith Joins Diplo And Nicky Jam For The 2018 World Cups Official Song Of course it has a song.', 
						'Hugh Grant Marries For The First Time At Age 57 The actor and his longtime girlfriend Anna Eberstein tied the knot in a civil ceremony.',
						'Morgan Freeman \'Devastated\' That Sexual Harassment Claims Could Undermine Legacy "It is not right to equate horrific incidents of sexual assault with misplaced compliments or humor," he said in a statement.'] }
	else:
		interests = {
						'Technology' : 
						["Facebook Pledges To Add More Local News To Newsfeeds 'People who know what happening around them are more likely to get involved and help make a difference,' said CEO Mark Zuckerberg.",
						 "Elon Musk Pulls Tesla, SpaceX Facebook Pages In Nod To #DeleteFacebook He also deleted his personal profile",
						 "Google Cancels 'Town Hall' On Gender Dispute Over Fears Of Online Harassment By Far-Right The company-wide meeting was slated to discuss the controversy over a memo opposing diversity policies."], 
						
						'Health Living' : 
						["An Expert-Backed, Foolproof Guide To 'Going Dry' For A Month How to cut down on everything from sugar to alcohol to social media.",
						"Exactly What Those Words On Your Beauty Products Mean \u201cYou wouldn\u2019t eat a plate of food without checking what was on your plate, so you should have that same mentality with your skin care.",
						"World Health Organization\u2019s Junk Diagnosis For 'Gaming Disorder' Trivializes Mental Illness News media reported this week that the World Health Organization (WHO) is moving ahead with the inclusion of gaming disorder"],
						
						'Entertainment' : 
						['Will Smith Joins Diplo And Nicky Jam For The 2018 World Cups Official Song Of course it has a song.', 
						'Hugh Grant Marries For The First Time At Age 57 The actor and his longtime girlfriend Anna Eberstein tied the knot in a civil ceremony.',
						'Morgan Freeman \'Devastated\' That Sexual Harassment Claims Could Undermine Legacy "It is not right to equate horrific incidents of sexual assault with misplaced compliments or humor," he said in a statement.'] }
	session['interests'] = list(interests.keys())
	return render_template('interests.html', interests=interests)

@app.route('/interests_exp')
def interests_exp():
	print("In interests explainer")
	# input_val = [u"Cricket is a beatiful sport. Baseball, hockey. Dhoni is the best!!!", u'steve']
	input_val = [request.args.get('input_val'), 'steve']
	interest, explainer = get_interests(input_val)
	return render_template('interests_exp.html', input_val=input_val, interest=interest, explainer=explainer)

@app.route('/show_info')
def show_info():
	return render_template('show_info.html')

@app.route('/spent')
def spent_exp():
	input_val = np.asarray([2, 1, 4, 5, 6])
	predicted_val, explainer = get_spent(input_val)
	return str(explainer)


@app.route('/admin')
def admin():
	return render_template('admin.html')

@app.route('/dummy')
def dummy():
	return render_template('base.html')

if __name__ == '__main__':
	app.run(debug=True)
