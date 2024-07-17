from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property.type"
    _description = "Type of property"
    _order = "sequence"

    name = fields.Char('Title', required=True)
    sequence = fields.Integer('Sequence', default=1)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    
    _sql_constraints =[
        ('unique_type_name', 'UNIQUE(name)', 'Property type name must be unique.')
    ] 