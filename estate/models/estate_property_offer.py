from odoo import models , fields , api
from odoo.exceptions import UserError

from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="قیمت")
    status = fields.Selection(
        selection=[("accepted", "پذیرفته شده"),("refused","رد شده")],
    copy = False,
    string="وضعیت")
    validity = fields.Integer(default=7,string="اعتبار")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverce_date_deadline",string="تاریخ انقضا")

    partner_id = fields.Many2one("res.partner",required=True,string="پیشمهاد دهنده")
    property_id = fields.Many2one("estate.property",required=True,string="ملک")

    property_type_id = fields.Many2one("estate.property.type",related="property_id.property_type_id",ondelete="cascade")
    
    _sql_constraints = [('cheack_offer_price' , 'CHECK(price > 0)',
         'قیمت پیشنهادی کاربران نباید منفی یا برابر صفر باشد')
    ]

    @api.model
    def create(self, vals):
        property = self.env['estate.property'].browse(vals['property_id'])

        if property and vals['price'] < property.selling_price:
            raise UserError("نمیتوانید پیشنهاد زیر قیمت بدهید")

        offer = super(EstatePropertyOffer, self).create(vals)

        if property and property.state == 'new':
            property.state = 'offer_received'

        return offer


    @api.depends("validity","create_date")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date :
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = False

    def _inverce_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days 


    def action_accept(self):
        for record in self:
            accepted_offers = record.property_id.offer_ids.filtered(lambda o: o.status == "accepted")
            
            if accepted_offers:
                raise UserError("برای این ملک قبلاً یک پیشنهاد قبول شده است. نمی‌توانید پیشنهاد دیگری را قبول کنید.")

            record.status = "accepted"
            record.property_id.state = "offer_accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price 

        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True
