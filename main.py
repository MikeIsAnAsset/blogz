from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = "y337kGcys&zP3B"
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    body = db.Column(db.String(1024))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   
    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'blog', 'signup', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/blog', methods=['GET'])
def blog():
    user = request.args.get('user')
    query_id = request.args.get('id')
    
    if query_id != None:
        blog = Blog.query.get(query_id)
        user_object = User.query.filter_by(id=blog.owner_id).first()
        return render_template('post.html', blog=blog, user=user_object)

    if user == None:
        blogs = Blog.query.all()
        return render_template('main_blog_page.html', body_title='Blogz:', blogs=blogs)
    
    else:
        user_object = User.query.filter_by(username=user).first()
        user_blogs = Blog.query.filter_by(owner_id=user_object.id).all()
        return render_template('user_page.html', body_title=user_object.username + "'s blogz", 
                                blogs=user_blogs, user=user_object)

@app.route('/newpost', methods=['GET', 'POST'])
def newblog():
    if request.method == 'GET':
        return render_template('add_new_blog.html', body_title='Add a Blog Entry')

    if request.method == 'POST':

        title = request.form['title']
        body = request.form['body']
        owner = User.query.filter_by(username=session['username']).first()
        
        error_title = ''
        error_body = ''

        if title == '':
            error_title = 'Please fill in the title'
            # return render_template('add_new_blog.html', error_title=error_title, 
            # body_title="Add a Blog Entry", title=title, body=body)
        
        if body == '':
            error_body = 'Please fill in the body'
            
        if body == '' or title == '':
            return render_template('add_new_blog.html', error_title=error_title, error_body=error_body,
            body_title="Add a Blog Entry", title=title, body=body)
        else:
            blog = Blog(title, body, owner)
            db.session.add(blog)
            db.session.commit()
            # id = request.form['id']
            # blog = Blog.query.get(id)
            # return render_template('post.html', blog=blog)
            # return redirect('/blog')
            return redirect('/blog?id={0}'.format(blog.id))

@app.route('/post', methods=['GET'])
def post():

    id = request.args.get('id')
    blog = Blog.query.get(id)
    user_object = User.query.filter_by(id=blog.owner_id).first()
    
    # blog_id = blog.id
    # blog = Blog.query.filter_by(id=id)
    # return render_template('post.html', blog=blog)
    # return redirect('/post?id={0}'.format(id))
    return render_template('post.html', blog=blog, user=user_object)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.form:
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        print(user)
        if user and user.password == password:
            session['username'] = username
            return redirect('/newpost')
        if user == None:
            error_username = 'Invalid username'
            return render_template('login.html', error=error_username)
        if user.password != password:
            error_password = 'Invalid password'
            return render_template('login.html', error=error_password)
    
    # store username in session
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.form:
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        user = User.query.filter_by(username=username).first()
        error_username = ''
        error_password = ''
        error_verify = ''
        if user:
            error_username = 'A user with that username already exists'
            password = ''
            verify = ''
            return render_template('signup.html', error_username=error_username, Username=username)
        if username == '' or len(username) <3 or len(username) >20:
            error_username = "That's not a valid username"
            username = ''
            password = ''
            verify = ''
        if password == '' or len(password) <3 or len(password) >20:
            error_password = "That's not a valid password"
            password = ''
            verify = ''
        if verify == '' or verify != password:
            error_verify = "Passwords don't match"
            verify = ''
            password = ''
        if error_username or error_password or error_verify :
            return render_template('signup.html', error_username=error_username,
                                                  error_password=error_password,
                                                  error_verify=error_verify,
                                                  Username=username)        
        else:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect ('/newpost')
            user = User(username, password)

    return render_template('signup.html')

# task_id = int(request.form['task-id'])
# task = Task.query.get(task_id)

@app.route('/logout')
def logout():
    del session['username']
    return redirect ('/blog')








if __name__  == '__main__':
    app.run()