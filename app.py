from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///stable.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(
        page=page, per_page=5, error_out=False)
    return render_template('home.html', posts=posts)

@app.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    
    if request.method == 'POST' and current_user.is_authenticated:
        content = request.form.get('content')
        if content:
            comment = Comment(content=content, user_id=current_user.id, post_id=post.id)
            db.session.add(comment)
            db.session.commit()
            flash('Your comment has been added!', 'success')
            return redirect(url_for('post', id=id))
    
    comments = Comment.query.filter_by(post_id=id).order_by(Comment.date_posted.asc()).all()
    return render_template('post.html', post=post, comments=comments)

@app.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    # Only admin can write posts
    if not current_user.is_admin:
        flash('Only the stable owner can write tales!', 'error')
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        if title and content:
            post = Post(title=title, content=content, user_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Your stable tale has been shared!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Please fill in all fields', 'error')
    
    return render_template('write.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
        else:
            # First user becomes admin (stable owner)
            is_first_user = User.query.count() == 0
            user = User(username=username, 
                       password_hash=generate_password_hash(password),
                       is_admin=is_first_user)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            if is_first_user:
                flash('Welcome to your stable! You are now the stable owner.', 'success')
            else:
                flash('Welcome to the stable! You can read tales and leave comments.', 'success')
            return redirect(url_for('home'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
