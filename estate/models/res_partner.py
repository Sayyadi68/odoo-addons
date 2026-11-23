from odoo import models, fields, api
import datetime
from random import randint


class Partner(models.Model):
    _inherit = 'res.partner'
    
    customer_code = fields.Char(string="کد مشتری")

    gender = fields.Selection(
        string="جنسیت کاربر",
        selection=[
            ('men', 'مرد'),
            ('women', 'زن'),
            ('not_selected', 'مشخص نشده')
        ],
    )

    _sql_constraints = [
        (
            'Unique_customer_code',
            'unique(customer_code)',
            'کد مشتری نباید تکراری باشد'
        )
    ]



    @api.model_create_multi
    def create(self, vals_list):
        today_str = fields.Date.context_today(self).strftime('%Y%m%d')
        
        for vals in vals_list:
            gender = vals.get('gender')
            new_code = 0

            if gender == 'men':
                partners = self.env['res.partner'].search(
                    [('gender', '=', 'men'), ('customer_code', 'ilike', f'%-{today_str}')],
                    order='id desc', limit=1
                )
                last_code = int(partners.customer_code.split('-')[0]) if partners else 0
                
                if last_code == 0:
                    new_code = 2
                else:
                    new_code = last_code + 2
                    if new_code % 10 == 0:
                        new_code += 2

            elif gender == 'women':
                partners = self.env['res.partner'].search(
                    [('gender', '=', 'women'), ('customer_code', 'ilike', f'%-{today_str}')],
                    order='id desc', limit=1
                )
                last_code = int(partners.customer_code.split('-')[0]) if partners else 0
                
                if last_code == 0:
                    new_code = 1
                else:
                    new_code = last_code + 2

            elif gender == 'not_selected':
                reserved_zero = self.env['res.partner'].search([('customer_code', '=', f'000-{today_str}')], limit=1)
                
                if not reserved_zero:
                    new_code = 0
                else:
                   
                    partners = self.env['res.partner'].search(
                        [('gender', '=', 'not_selected'), ('customer_code', 'ilike', f'%-{today_str}')],
                        order='id desc', limit=1
                    )
                    last_code = int(partners.customer_code.split('-')[0]) if partners else 0
                    
                    if last_code == 0:
                        new_code = 10
                    else:
                        new_code = last_code + 10

            base_str = str(new_code).zfill(3)
            vals['customer_code'] = f"{base_str}-{today_str}"

        return super(Partner, self).create(vals_list)