from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Characteristic that can be given to the property"

    name = fields.Char('Name', required=True)