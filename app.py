from flask import Flask,request,redirect,url_for,render_template,make_response,jsonify
app=Flask(__name__)
users={} #to store user data
@app.route('/')
def home():
    return render_template('welcome.html')
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        print(request.form)
        username=request.form['username']
        userpassword=request.form['password']
        user_pinno=request.form['userpinno']
        if username not in users:
            users[username]={'user_password':userpassword,'user_pinno':user_pinno,'Amount':0} 
            print(users)
            return redirect(url_for('login'))
        else:
            return 'user already existed'
    return render_template('register.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        login_username=request.form['username']
        login_password=request.form['password']
        if login_username in users:
            if users[login_username]['user_password']==login_password:
                resp=make_response(redirect(url_for('dashboard')))
                resp.set_cookie('user',login_username)
                return resp
            else:
                return 'password wrong'
        else:
            return 'Username was wrong'
    return render_template('login.html')
@app.route('/dashboard',methods=['GET'])
def dashboard():
    if request.cookies.get('user'):
        return render_template('dashboard.html')
    else:
        return 'pls login view dashboard'
@app.route('/deposit',methods=['GET','PUT'])
def deposit():
    if request.cookies.get('user'):
        if request.method=='PUT':
            username=request.cookies.get('user')
            print(request.get_json())
            deposit_amount=int(request.get_json()['amount']) #500
            if deposit_amount>0:
                if deposit_amount %100 ==0:
                    if deposit_amount<=50000:
                        users[username]['Amount']=users[username]['Amount']+deposit_amount
                        return f'{deposit_amount}'
                    else:
                        return jsonify({'message':'Amount should be <= 50000'})
                else:
                    return jsonify({'message':'Amount should be multiple 100'})
            else:
                return jsonify({"message":'Amount should be > 0'})
        return render_template('deposit.html') 
    else:
        return 'pls login view deposit'
app.run(use_reloader=True,debug=True)