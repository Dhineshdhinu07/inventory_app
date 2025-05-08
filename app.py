from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Product, Location, ProductMovement
from forms import ProductForm, LocationForm, ProductMovementForm
from sqlalchemy import func, text
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'inventory-management-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create database tables if they don't exist
@app.before_first_request
def create_tables():
    db.create_all()

# Home page
@app.route('/')
def index():
    products_count = Product.query.count()
    locations_count = Location.query.count()
    movements_count = ProductMovement.query.count()
    return render_template('index.html', 
                          products_count=products_count,
                          locations_count=locations_count,
                          movements_count=movements_count)

# Product routes
@app.route('/products')
def list_products():
    products = Product.query.all()
    return render_template('product/list.html', products=products)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        # Check if product_id already exists
        existing_product = Product.query.filter_by(product_id=form.product_id.data).first()
        if existing_product:
            flash(f'Product ID {form.product_id.data} already exists!', 'danger')
            return render_template('product/add.html', form=form)
            
        product = Product(
            product_id=form.product_id.data,
            product_name=form.product_name.data,
            description=form.description.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('list_products'))
    return render_template('product/add.html', form=form)

@app.route('/products/edit/<string:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    
    if form.validate_on_submit():
        # Don't allow product_id to be changed
        product.product_name = form.product_name.data
        product.description = form.description.data
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('list_products'))
    
    return render_template('product/edit.html', form=form, product=product)

@app.route('/products/view/<string:product_id>')
def view_product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product/view.html', product=product)

@app.route('/products/delete/<string:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Check if product has movements
    if product.movements:
        flash('Cannot delete product with associated movements!', 'danger')
        return redirect(url_for('list_products'))
    
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('list_products'))

# Location routes
@app.route('/locations')
def list_locations():
    locations = Location.query.all()
    return render_template('location/list.html', locations=locations)

@app.route('/locations/add', methods=['GET', 'POST'])
def add_location():
    form = LocationForm()
    if form.validate_on_submit():
        # Check if location_id already exists
        existing_location = Location.query.filter_by(location_id=form.location_id.data).first()
        if existing_location:
            flash(f'Location ID {form.location_id.data} already exists!', 'danger')
            return render_template('location/add.html', form=form)
            
        location = Location(
            location_id=form.location_id.data,
            location_name=form.location_name.data,
            description=form.description.data
        )
        db.session.add(location)
        db.session.commit()
        flash('Location added successfully!', 'success')
        return redirect(url_for('list_locations'))
    return render_template('location/add.html', form=form)

@app.route('/locations/edit/<string:location_id>', methods=['GET', 'POST'])
def edit_location(location_id):
    location = Location.query.get_or_404(location_id)
    form = LocationForm(obj=location)
    
    if form.validate_on_submit():
        # Don't allow location_id to be changed
        location.location_name = form.location_name.data
        location.description = form.description.data
        db.session.commit()
        flash('Location updated successfully!', 'success')
        return redirect(url_for('list_locations'))
    
    return render_template('location/edit.html', form=form, location=location)

@app.route('/locations/view/<string:location_id>')
def view_location(location_id):
    location = Location.query.get_or_404(location_id)
    return render_template('location/view.html', location=location)

@app.route('/locations/delete/<string:location_id>', methods=['POST'])
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)
    
    # Check if location has incoming or outgoing movements
    if location.incoming_movements or location.outgoing_movements:
        flash('Cannot delete location with associated movements!', 'danger')
        return redirect(url_for('list_locations'))
    
    db.session.delete(location)
    db.session.commit()
    flash('Location deleted successfully!', 'success')
    return redirect(url_for('list_locations'))

# Product Movement routes
@app.route('/movements')
def list_movements():
    movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all()
    return render_template('movement/list.html', movements=movements)

@app.route('/movements/add', methods=['GET', 'POST'])
def add_movement():
    form = ProductMovementForm()
    
    # Populate product choices
    products = Product.query.all()
    form.product_id.choices = [(p.product_id, f"{p.product_id} - {p.product_name}") for p in products]
    
    # Populate location choices
    locations = Location.query.all()
    form.from_location.choices = [('', 'Select Location')] + [(l.location_id, f"{l.location_id} - {l.location_name}") for l in locations]
    form.to_location.choices = [('', 'Select Location')] + [(l.location_id, f"{l.location_id} - {l.location_name}") for l in locations]
    
    if form.validate_on_submit():
        # Check if movement_id already exists
        existing_movement = ProductMovement.query.filter_by(movement_id=form.movement_id.data).first()
        if existing_movement:
            flash(f'Movement ID {form.movement_id.data} already exists!', 'danger')
            return render_template('movement/add.html', form=form)
        
        # Validate additional constraints
        product_id = form.product_id.data
        from_location = form.from_location.data or None
        to_location = form.to_location.data or None
        qty = form.qty.data
        
        # If moving from a location, check if there's enough quantity
        if from_location:
            balance = get_product_balance(product_id, from_location)
            if balance < qty:
                flash(f'Not enough stock! Available: {balance}, Requested: {qty}', 'danger')
                return render_template('movement/add.html', form=form)
        
        movement = ProductMovement(
            movement_id=form.movement_id.data,
            product_id=product_id,
            from_location=from_location,
            to_location=to_location,
            qty=qty,
            timestamp=datetime.utcnow()
        )
        db.session.add(movement)
        db.session.commit()
        flash('Product movement added successfully!', 'success')
        return redirect(url_for('list_movements'))
    
    return render_template('movement/add.html', form=form)

@app.route('/movements/edit/<string:movement_id>', methods=['GET', 'POST'])
def edit_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    form = ProductMovementForm(obj=movement)
    
    # Populate product choices
    products = Product.query.all()
    form.product_id.choices = [(p.product_id, f"{p.product_id} - {p.product_name}") for p in products]
    
    # Populate location choices
    locations = Location.query.all()
    form.from_location.choices = [('', 'Select Location')] + [(l.location_id, f"{l.location_id} - {l.location_name}") for l in locations]
    form.to_location.choices = [('', 'Select Location')] + [(l.location_id, f"{l.location_id} - {l.location_name}") for l in locations]
    
    # We won't allow editing of movement_id
    if request.method == 'GET':
        form.movement_id.render_kw = {'readonly': True}
    
    if form.validate_on_submit():
        old_from = movement.from_location
        old_to = movement.to_location
        old_qty = movement.qty
        old_product = movement.product_id
        
        # Validate additional constraints for inventory balance
        product_id = form.product_id.data
        from_location = form.from_location.data or None
        to_location = form.to_location.data or None
        qty = form.qty.data
        
        # If product or source location changed, or quantity increased, check stock
        if (from_location and (old_from != from_location or old_product != product_id or old_qty < qty)):
            # Calculate balance excluding this movement
            movements_in = ProductMovement.query.filter_by(to_location=from_location, product_id=product_id).filter(ProductMovement.movement_id != movement_id).all()
            movements_out = ProductMovement.query.filter_by(from_location=from_location, product_id=product_id).filter(ProductMovement.movement_id != movement_id).all()
            
            total_in = sum(m.qty for m in movements_in)
            total_out = sum(m.qty for m in movements_out)
            balance = total_in - total_out
            
            if balance < qty:
                flash(f'Not enough stock! Available: {balance}, Requested: {qty}', 'danger')
                return render_template('movement/edit.html', form=form, movement=movement)
        
        movement.product_id = product_id
        movement.from_location = from_location
        movement.to_location = to_location
        movement.qty = qty
        
        db.session.commit()
        flash('Product movement updated successfully!', 'success')
        return redirect(url_for('list_movements'))
    
    return render_template('movement/edit.html', form=form, movement=movement)

@app.route('/movements/view/<string:movement_id>')
def view_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    return render_template('movement/view.html', movement=movement)

@app.route('/movements/delete/<string:movement_id>', methods=['POST'])
def delete_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    
    # If deleting a movement that takes inventory out of a location, check if this would result in negative balance
    if movement.from_location:
        # Calculate current balance
        balance = get_product_balance(movement.product_id, movement.from_location)
        
        # Add back the quantity from this movement (since we're going to delete it)
        adjusted_balance = balance + movement.qty
        
        # If there were subsequent movements depending on this one, we might end up with negative inventory
        future_movements = ProductMovement.query.filter(
            ProductMovement.from_location == movement.from_location,
            ProductMovement.product_id == movement.product_id,
            ProductMovement.timestamp > movement.timestamp
        ).all()
        
        for future in future_movements:
            adjusted_balance -= future.qty
            if adjusted_balance < 0:
                flash('Cannot delete this movement as it would result in negative inventory for subsequent movements!', 'danger')
                return redirect(url_for('list_movements'))
    
    db.session.delete(movement)
    db.session.commit()
    flash('Product movement deleted successfully!', 'success')
    return redirect(url_for('list_movements'))

# Helper function to calculate product balance at a location
def get_product_balance(product_id, location_id):
    # Calculate incoming quantity
    incoming = db.session.query(func.sum(ProductMovement.qty))\
        .filter(ProductMovement.to_location == location_id, ProductMovement.product_id == product_id)\
        .scalar() or 0
    
    # Calculate outgoing quantity
    outgoing = db.session.query(func.sum(ProductMovement.qty))\
        .filter(ProductMovement.from_location == location_id, ProductMovement.product_id == product_id)\
        .scalar() or 0
    
    # Calculate balance
    balance = incoming - outgoing
    return balance

# Report route for balance quantity
@app.route('/report/balance')
def balance_report():
    # Get all products and locations
    products = Product.query.all()
    locations = Location.query.all()
    
    # Create a balance matrix
    balance_data = []
    
    for product in products:
        for location in locations:
            balance = get_product_balance(product.product_id, location.location_id)
            if balance != 0:  # Only show non-zero balances
                balance_data.append({
                    'product_id': product.product_id,
                    'product_name': product.product_name,
                    'location_id': location.location_id,
                    'location_name': location.location_name,
                    'balance': balance
                })
    
    return render_template('report/balance.html', balance_data=balance_data)

if __name__ == '__main__':
    app.run(debug=True)