from odoo import models, fields,api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name"
    
    name = fields.Char(required=True, string="نوع خانه")
    offer_ids = fields.One2many('estate.property.offer','property_type_id',string='پیشنهاد ها')
    offer_count = fields.Integer(string='تعداد پیشنهاد ها',compute='_compute_offer_count')
    property_ids = fields.One2many(
        "estate.property",
        "property_type_id",
        string="Properties"
    )

    sequence = fields.Integer()


    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)