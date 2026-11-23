# -*- coding: utf-8 -*-
{
    'name': "مهدی صیادی",
    'version': '1.0',
    'depends': ['base','sale'],
    'author': "مهدی صیادی",
    'category': 'شخصی/اداری',
    'sequence':1,
    'description': """
    به خفن ترین برنامه نویس دنیا سلام کن
    """,
    'license': 'LGPL-3',
    'application': True,
    'installable': True,
    'data': [
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'views/estate_menus.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/res_users_view.xml',
        'views/res_partner_view.xml',
        'reports/estate_property_reports.xml',
    ],
}