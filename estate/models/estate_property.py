from odoo import models , fields , api
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char(required=True,string="عنوان")
    description = fields.Text(string="توضیحات")
    postcode = fields.Char(string="کد پستی")
    date_availability = fields.Date(string="مدت اعتبار",default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True,string="قیمت پیشنهادی")
    selling_price = fields.Float(copy=False,string="قیمت فروش")
    bedrooms = fields.Integer(default=2,string="تهداد اتاق")
    living_area = fields.Integer(string="متراژ داخلی",required=True)
    facades = fields.Integer(string="نما")
    garage = fields.Boolean(string="پارکینگ")
    garden = fields.Boolean(string="حیاط")
    garden_area =fields.Integer(string="متراژ حیاط")
    garden_orientation = fields.Selection(
        string="جهت حیاط",
        selection=[('north','شمال'),('south','جنوب'),('east','شرق'),('west','غرب')],
    )
    active = fields.Boolean(default=True,string="فعال")
    state = fields.Selection(
        string="وضعیت",
        selection=[("new","جدید"),("offer_received","پیشنهاد دریافت شده"),("canceled","لفو شده"),
                   ("offer_accepted","پیشنهاد قبول شده"),("sold","فروخته شده")],
        default="new",
        copy=False,
        required=True,
    )
    property_type_id = fields.Many2one("estate.property.type",string="نوع")
    buyer_id = fields.Many2one("res.partner",string="خریدار",copy=False , ondelete="cascade")
    salesperson_id = fields.Many2one("res.users",string="فروشنده",default=lambda self: self.env.user , ondelete="cascade")
    tag_ids = fields.Many2many("estate.property.tag",string="تگ")
    offer_ids = fields.One2many("estate.property.offer","property_id",string="پیشنهاد ها")

    total_area = fields.Float(compute="_compute_total_area",string="متراژ کل")

    _sql_constraints = [('cheack_expected_price' , 'CHECK(expected_price > 0)',
         'قیمت پیشنهاد ها نباید منفی یا برابر صفر باشد'),

         ('cheack_selling_price' , 'CHECK(selling_price > 0)',
         'قیمتهای فروشها نباید منفی یا برابر صفر باشد')
    ]

    best_price = fields.Float(compute="_compute_best_price",string="بیشترین قیمت داده شده")

    salles_person_id = fields.Many2one('res.users', default=lambda self: self.env.user)





    @api.ondelete(at_uninstall=False)
    def no_delete(self):
        for rec in self:
            if rec.state == "new" or rec.state == "canceled":
                raise UserError("املاک جدید و حذف شده امکان حذف شدن ندارد")
            



    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for record in self:
            if record.garden:
                record.total_area = record.living_area + record.garden_area
            else:
                record.total_area = record.living_area


    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            price = record.offer_ids.mapped("price")
            if price:
                
                record.best_price = max(price)
            else:
                record.best_price = 0


    def action_sold(self):
        if self.state == "canceled":
            raise UserError("یک ملک لغو شده نمی‌تواند فروخته شود.")
        self.state = "sold"
        return True

    def action_canceled(self):
        if self.state == "sold":
            raise UserError("یک ملک فروخته شده نمی‌تواند لغو شود.")
        self.state = "canceled"
        return True


    @api.constrains('selling_price','expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < record.expected_price * 0.9:
                raise ValidationError("قیمیت خیلی پایینه")