from odoo import api, fields, models, exceptions
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description ="Offers made on property"

    price = fields.Float(string="Price", default="0.0")
    status = fields.Selection(selection=[('accepted','Accepted'),('refused','Refused')], copy=False, string="Status", default="Pendant")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(string="Validity", default="7")
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    def accept_offer(self):
        for record in self:
                record.status = "accepted"
        return True
    
    def reject_offer(self):
        for record in self:
                record.status = "refused"
        return True


    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date + timedelta(days=offer.validity)
            else:
                offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            if offer.date_deadline and offer.create_date:
                offer.validity = (offer.date_deadline - fields.Date.to_date(offer.create_date)).days
    

    