from odoo import models , fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name desc"

    name = fields.Char(required=True,string="تگ")

    color = fields.Char(required=True,string="تگ")
    
    _sql_constraints = [('unique_tags_name' , 'unique(name)',
         'نام تگ ها نباید تکراری باشد'),

    ]