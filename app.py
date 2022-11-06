from flask import Flask, render_template, url_for, flash, redirect
import os
from forms import RegForm, LoginForm, ContactForm, PostForm
from flask_bcrypt import Bcrypt
from db import db
from models import User, Blogpost, Contact
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_migrate import Migrate




base_dir = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(base_dir, 'blog.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = '6b7df753406f6c861b7bd2b6'

db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)
bcrypt = Bcrypt(app)
login_manager  = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Primary route, the home page. Returns a dynamic data of posts created in the database.
@app.route('/')
def index():
    posts = Blogpost.query.all()
    return render_template('index.html', posts=posts)

# route that leads to the about page
@app.route('/about')
def about():
    return render_template('about.html')

# route for contact page
# contact form is a flask wtf form model
@app.route('/contact')
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        new_contact = Contact(name=form.name.data, email=form.email.data, message=form.message.data)
        db.session.add(new_contact)
        db.session.commit()
        flash('Thank you for contacting us!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)

# register user route
# logic validates password and adds users to the database
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if form.validate_on_submit():
        hashed_pword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstname=form.first_name.data, lastname=form.last_name.data, email=form.email.data, password=hashed_pword)
        db.session.add(user)
        db.session.commit()
        flash('Account has been created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful, please check that email and password is correct.', 'error')
    return render_template('login.html', title='Login', form=form)

# log out route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# create_post route allows an authenticated user to make posts on the blog
@app.route('/post', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Blogpost(title=form.title.data, category=form.category.data, content=form.content.data, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash('Post created successfully!',  'success')
        return redirect(url_for('index'))
    return render_template('post.html', form=form)

# post route enables the user get a particular post by id
@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.get_or_404(post_id)
    return render_template('blog_post.html', post=post)

# short-stories route helps to filter posts made on the blog based on user interest 
# returns a dynamic homepage with posts that users made under the short stories category
@app.route('/Short-stories')
def short_stories():
    posts = Blogpost.query.filter_by(category='Short stories').all()
    return render_template('index.html', posts=posts)

# returns a dynamic homepage with posts that users made under the relationships category
@app.route('/relationships')
def relationships():
    posts = Blogpost.query.filter_by(category='Relationships').all()
    return render_template('index.html', posts=posts)

# returns a dynamic homepage with posts that users made under the technology category
@app.route('/technology')
def tech():
    posts = Blogpost.query.filter_by(category='Technology').all()
    return render_template('index.html', posts=posts)

# returns a dynamic homepage with posts that users made under the health category
@app.route('/health')
def health():
    posts = Blogpost.query.filter_by(category='Health').all()
    return render_template('index.html', posts=posts)

# route to return a dynamic category on the post display
@app.route('/category/<cate>')
def cat(cate):
    posts = Blogpost.query.filter_by(category=cate).all()
    return render_template('index.html', posts=posts)

# enables  users edit a post created by them
@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Blogpost.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.category = form.category.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    form.title.data = post.title
    form.category.data = post.category
    form.content.data = post.content   
    return render_template('post.html', post=post, form=form)

# enables user delete a post
@app.route('/post/<int:post_id>/delete', methods=['POST', 'GET'])
def del_post(post_id):
    post = Blogpost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted!',  'success')
    return redirect(url_for('index'))

# returns only posts made by the current user.
@app.route('/my posts')
def user_posts():
    posts = Blogpost.query.all()
    return render_template('user_posts.html', posts=posts)