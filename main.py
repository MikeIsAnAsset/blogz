from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    body = db.Column(db.String(1024))

    def __init__(self, title, body):
        self.title = title
        self.body = body

# @app.route('/', methods['POST', 'GET'])
#     def index():

#         if request.method == Post:
#             blog_post = request.form['blog']
#             blog_title = reuqest.form['title']
           
#         #    verify form fields
#         # show errors(flash)
           
#             blog = Blog(blog_post, blog_title)
#             db.session.add(blog)
#             db.session.commit()

# redirect to main blog page

        # else:
# render new blog temp




@app.route('/blog', methods=['GET'])
def index():

    if request.method == 'GET':
        blogs = Blog.query.all()
        # completed_tasks = Task.query.filter_by(completed=True).all()
        return render_template('main_blog_page.html', title='Build a Blog',
        body_title='Build a Blog', blogs=blogs)
            # , completed_tasks=completed_tasks)

@app.route('/newpost', methods=['GET', 'POST'])
def newblog():
    if request.method == 'GET':
        return render_template('add_new_blog.html', body_title='Add a Blog Entry')

    if request.method == 'POST':

        title = request.form['title']
        body = request.form['body']
        
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
            blog = Blog(title, body)
            db.session.add(blog)
            db.session.commit()
            # id = request.form['id']
            # blog = Blog.query.get(id)
            # return render_template('post.html', blog=blog)
            # return redirect('/blog')
            return redirect('/post?id={0}'.format(blog.id))

@app.route('/post', methods=['GET'])
def post():

    id = request.args.get('id')
    blog = Blog.query.get(id)
    # blog_id = blog.id
    # blog = Blog.query.filter_by(id=id)
    # return render_template('post.html', blog=blog)
    # return redirect('/post?id={0}'.format(id))
    return render_template('post.html', blog=blog)


# tasks = Task.query.filter_by(completed=False).all()
#     completed_tasks = Task.query.filter_by(completed=True).all()
#     return render_template('todos.html',title="Get It Done!", 
#         tasks=tasks, completed_tasks=completed_tasks)





    # task_id = int(request.form['task-id'])
    # task = Task.query.get(task_id)
    # task.completed = True
    # db.session.add(task)
    # db.session.commit()

    # return redirect('/')


if __name__ == '__main__':
    app.run()