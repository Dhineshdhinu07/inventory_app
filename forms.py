from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange

class ProductForm(FlaskForm):
    product_id = StringField('Product ID', validators=[DataRequired()])
    product_name = StringField('Product Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Submit')

class LocationForm(FlaskForm):
    location_id = StringField('Location ID', validators=[DataRequired()])
    location_name = StringField('Location Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Submit')

class ProductMovementForm(FlaskForm):
    movement_id = StringField('Movement ID', validators=[DataRequired()])
    product_id = SelectField('Product', validators=[DataRequired()])
    from_location = SelectField('From Location', validators=[Optional()], choices=[('', 'Select Location')])
    to_location = SelectField('To Location', validators=[Optional()], choices=[('', 'Select Location')])
    qty = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Submit')
    
    def validate(self):
        if not super(ProductMovementForm, self).validate():
            return False
        
        # Custom validation to ensure at least one location is specified
        if not self.from_location.data and not self.to_location.data:
            self.from_location.errors.append('At least one location must be specified')
            self.to_location.errors.append('At least one location must be specified')
            return False
            
        # Check that from_location and to_location are not the same if both are provided
        if self.from_location.data and self.to_location.data and self.from_location.data == self.to_location.data:
            self.from_location.errors.append('Source and destination cannot be the same')
            self.to_location.errors.append('Source and destination cannot be the same')
            return False
            
        return True