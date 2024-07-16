from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property.type"
    _description = "Type of property"

    name = fields.Char('Title', required=True)
    
    
    _sql_constraints =[
        ('unique_type_name', 'UNIQUE(name)', 'Property type name must be unique.')
    ] 