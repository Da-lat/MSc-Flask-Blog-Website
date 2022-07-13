from flask import render_template, url_for, redirect, flash, request
from blog import app, db
from blog.models import Rating, User, Post, Comment
from blog.forms import LoginForm, RegistrationForm, CommentForm, RatingForm, SortingForm
from flask_login import login_user, logout_user, current_user

@app.route("/", methods=["POST", "GET"])
@app.route("/home", methods=["GET", "POST"])
def home():
  posts = Post.query.order_by(Post.date.asc()).all()
  sorting_form = SortingForm()
  if sorting_form.validate_on_submit():
    sorting_info = sorting_form.sort.data
    if sorting_info == "date_asc":
      return redirect(url_for('home'))
    elif sorting_info == "date_desc":
      return redirect(url_for('home_desc'))
  return render_template('home.html', posts=posts,sorting_form=sorting_form)

@app.route("/home/desc", methods=["GET", "POST"])
def home_desc():
  posts = Post.query.order_by(Post.date.desc()).all()
  sorting_form = SortingForm()
  if sorting_form.validate_on_submit():
    sorting_info = sorting_form.sort.data
    if sorting_info == "date_asc":
      return redirect(url_for('home'))
    elif sorting_info == "date_desc":
      return redirect(url_for('home_desc'))
  return render_template('home.html', posts=posts,sorting_form=sorting_form)

@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def post(post_id):
  post=Post.query.get_or_404(post_id)
  comment_form = CommentForm()
  if comment_form.validate_on_submit():
        comment = Comment(body=comment_form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('.post', post_id=post.id, page=-1))

  page = request.args.get('page', 1, type=int)
  if page == -1:
      page = (post.comments.count() - 1) // \
      app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
  pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
    page, per_page=app.config['FLASKY_COMMENTS_PER_PAGE'],
    error_out=False)
  comments = pagination.items
  rating_form = RatingForm()
  if rating_form.validate_on_submit():
    ratinginfo = Rating(rating=rating_form.rating.data, post=post)
    db.session.add(ratinginfo)
    db.session.commit()

  all_ratings = Rating.query.filter_by(post_id=post.id).all()
  count=0
  sum=0
  for i in all_ratings:
    count+=1
    sum+=i.rating
  avg_rating = round(sum/count,1)
  return render_template('post.html',title=post.title,post=post, comments=comments, pagination=pagination, comment_form=comment_form, rating_form=rating_form,avg_rating=avg_rating)

@app.route("/register", methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(first_name=form.first_name.data,email=form.email.data, password=form.password.data)
    db.session.add(user)
    db.session.commit()
    flash(f'Registration successful, Thank you {form.first_name.data}')
    login_user(user)
    flash('You\'ve successfully logged in,'+' '+ current_user.first_name +'!')
    return redirect(url_for('home'))
  return render_template('register.html', title='Register',form=form)

@app.route("/registered")
def registered():
  return render_template('registered.html', title='Thank you for registering!')

@app.route("/login", methods=['GET','POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  loginform = LoginForm()
  if loginform.validate_on_submit():
    user = User.query.filter_by(email=loginform.email.data).first()
    if user is not None and user.verify_password(loginform.password.data):
      login_user(user, remember=loginform.remember.data)
      flash('You\'ve successfully logged in,'+' '+ current_user.first_name +'!')
      return redirect(url_for('home'))
    else:
      return redirect(url_for('error'))
  return render_template('login.html', title='Login', form=loginform)

@app.route("/logout")
def logout():
  logout_user()
  flash('You\'re now logged out. Thanks for your visit!')
  return redirect(url_for('home'))

@app.route("/error")
def error():
  return render_template("error.html")


