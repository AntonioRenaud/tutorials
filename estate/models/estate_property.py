from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"

    name = fields.Char('Title', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available From', copy=False, default=fields.Date.add(fields.Date.today(),months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area(sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection( 
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('west', 'West'), ('east', 'East')]

    )
    active = fields.Boolean('Active',default=True)
    state = fields.Selection(
        string='State',
        selection=[('new','New'), ('offer received','Offer Received'), ('offer accepted','Offer Accepted'), ('sold','Sold'),('cancelled','Cancelled')],
        default='new'
    )
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    saleperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area= fields.Float(compute="_total_area")
    best_price = fields.Float(compute="_best_price")

    def cancel_property(self):
        for record in self:
            if record.state == "sold":
               raise UserError("A sold property cannot be cancelled")
            elif record.state == "cancelled":
               
               raise UserError("The property sell was already cancelled")
            else:
                record.state = "cancelled"
                
        return True
    
    def sell_property(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("A cancelled property cannot be sold")
            elif record.state == "sold":
                raise UserError("The property is already sold")
            else:
                record.state = "sold"
        return True


    @api.depends("living_area","garden_area")
    def _total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
        
    @api.depends("offer_ids.price")
    def _best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.expected_price, precision_digits=2):
                    continue
            if float_compare(record.selling_price, record.expected_price*0.9, 2) < 0:
                raise ValidationError("The offer cannot be lower than 90 percent of the expected price")
      

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The expected price must be a positive number larger than 0.'),
         ('check_selling_price', 'CHECK(selling_price > 0)',
         'The selling price must be a positive number larger than 0.'),
        
    ]