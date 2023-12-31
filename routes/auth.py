from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user
from app import app, db
from app.models import User

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_data = {}
    if request.method == 'POST':
        form_data['username'] = request.form.get('username')
        form_data['password'] = request.form.get('password')

        user = User.query.filter_by(username=form_data['username']).first()

        if user and user.check_password(form_data['password']):
            # Log in the user and redirect to the home page
            login_user(user)
            return redirect(url_for('home'))

        flash('Invalid username or password')

    return render_template('login.html', form_data=form_data)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form_data = {}
    if request.method == 'POST':
        form_data['username'] = request.form.get('username')
        form_data['password'] = request.form.get('password')
        form_data['password_confirm'] = request.form.get('password_confirm')

        # Add your validation and registration logic here

        # Check if username already exists
        if User.query.filter_by(username=form_data['username']).first():
            flash('Username already exists. Please try again.', 'error')
            return redirect(url_for('register'))
        
        # Password validation
        if len(form_data['password']) < 8:
            flash('Password must be at least 8 characters.', 'error')
            return redirect(url_for('register'))
        elif len(form_data['password']) > 50:
            flash('Password must be less than 50 characters.', 'error')
            return redirect(url_for('register'))

        # If passwords match
        if form_data['password'] == form_data['password_confirm']:
            # Create a new user
            new_user = User(username=form_data['username'])
            new_user.set_password(form_data['password']) 
            db.session.add(new_user)  # Add new user to the database session
            db.session.commit()  # Commit the changes to the database
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Passwords do not match. Please try again.', 'error')
    return render_template('register.html', title='Register', form_data=form_data)

