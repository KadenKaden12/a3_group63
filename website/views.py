from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from .forms import RegisterForm, EventRegisterForm, OrderForm, EventUpdateForm
from .models import User, Category, Status, Event, Order
from flask_bcrypt import generate_password_hash
from flask_login import current_user, login_required
from datetime import datetime
from . import auth
from . import db
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    search_query = request.args.get('search', '')
    selected_category_id = request.args.get('category', type=int)
    query = Event.query
    if search_query:
        query = query.filter( Event.event_name.ilike(f'%{search_query}%'))
    if selected_category_id:
        query = query.filter_by(category_id = selected_category_id)
    user = current_user
    categories = Category.query.all()
    events = query.all()
    return render_template('main.html',user=user, events=events, categories=categories, selected_category=selected_category_id)

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Create a new user instance
        new_user = User(
            user_name=form.user_name.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data), 
            first_name=form.first_name.data,
            sur_name=form.sur_name.data,
            contact_no=form.contact_no.data,
            stress_address=form.stress_address.data
        )
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))  # Redirect to login or another page
    return render_template('register.html', form=form)

@main_bp.route('/register-event', methods=['GET', 'POST'])
@login_required
def registerEvent():
    user = current_user
    form = EventRegisterForm()
    form.category_id.choices = [(category.id, category.category_name) for category in Category.query.all()]
    form.status_id.choices = [(status.id, status.status_name) for status in Status.query.all()]

    if form.validate_on_submit():
        event = Event(
            event_name=form.event_name.data,
            location=form.location.data,
            event_date=form.event_date.data,
            start_from=form.start_from.data,
            end_to=form.end_to.data,
            description=form.description.data,
            image_path=form.image_path.data,
            no_of_tickets=form.no_of_tickets.data,
            owner_id=user.id,
            category_id=form.category_id.data,
            status_id=form.status_id.data
        )
        
        db.session.add(event)
        db.session.commit()
        
        return redirect(url_for('main.index'))  # Redirect to event list or any page after successful registration

    return render_template('register_event.html', form=form, user=user)

@main_bp.route('/event/<id>/edit', methods=['GET', 'POST'])
@login_required
def editEvent(id):
    user = current_user
    event = Event.query.get_or_404(id)

    if event.owner_id != user.id:
        return redirect(url_for('main.index'))  # Or show a 403 error
    
    form = EventUpdateForm(obj=event)
    form.category_id.choices = [(category.id, category.category_name) for category in Category.query.all()]

    if form.validate_on_submit():

        event.event_name = form.event_name.data
        event.location = form.location.data
        event.event_date = form.event_date.data
        event.start_from = datetime.strptime(form.start_from.data, '%H:%M:%S').time()
        event.end_to = datetime.strptime(form.end_to.data, '%H:%M:%S').time()
        event.description = form.description.data
        event.image_path = form.image_path.data
        event.no_of_tickets = form.no_of_tickets.data
        event.category_id = form.category_id.data
        
        db.session.commit()
        
        return redirect(url_for('main.getEvent', id=event.id))

    return render_template('edit_event.html', form=form, event=event, user=user) 

@main_bp.route('/event/<id>')
def getEvent(id):
    user = current_user
    event = Event.query.get(id)
    form = OrderForm()
    if not event:
        abort(494)
    return render_template('event.html', event=event, user=user, form=form)

@main_bp.route('/my-events')
@login_required
def getMyEvents():
    user = current_user
    events = Event.query.filter_by(owner_id = user.id).all()
    return render_template('my_events.html', events=events, user=user)


@main_bp.route('/event/<id>/order', methods=['POST'])
@login_required
def order(id):
    user = current_user
    form = OrderForm()
    event = Event.query.get_or_404(id)
    if form.validate_on_submit():
        order = Order(
            order_date=datetime.now(),
            user_id=user.id, 
            event_id=event.id,        
            no_of_tickets=form.no_of_tickets.data
        )
        
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('main.orderDetail', id = order.id))

    return redirect(url_for('main.getEvent', id=id))
    
@main_bp.route('/order/<id>')
@login_required
def orderDetail(id):
    order = Order.query.get_or_404(id)
    return render_template('order_Detail.html', order=order)

@main_bp.route('/orders')
@login_required
def getOrders():
    user = current_user
    orders = Order.query.filter_by(user_id=user.id).all()
    return render_template('orders.html', orders=orders, user=user)
    


