from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Characteristic that can be given to the property"

    name = fields.Char('Name', required=True)

    _sql_constraints =[
        ('unique_tag_name', 'UNIQUE(name)', 'Property tag name must be unique.')
    ]    