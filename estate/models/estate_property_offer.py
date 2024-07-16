from odoo import api, fields, models, exceptions
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description ="Offers made on property"

    price = fields.Float(string="Price")
    status = fields.Selection(selection=[('accepted','Accepted'),('refused','Refused')], copy=False, string="Status")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(string="Validity", default="7")
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    def accept_offer(self):
        if "accepted" in self.property_id.offer_ids.mapped("status"):
            raise exceptions.UserError("An offer has already been accepted")
        else:
            self.status = "accepted"
            self.property_id.selling_price = self.price
            self.property_id.state = "sold"
            self.property_id.buyer_id = self.partner_id.id
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
    
    _sql_constraints = [
        ('check_price', 'CHECK(price >= 0)',
         'The offer price needs to be a positive number.')
    ]