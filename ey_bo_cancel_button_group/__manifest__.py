{
    'name': 'Hide Cancel Button of Sale Order and Invoice',
    'version': '10.0.1.0',
    'description': 'Hide Cancel button according the group of a user in Sale order and Invoice form view',
    'summary': 'Hide Cancel button according the group of a user in Sale order and Invoice form view',
    'author': 'Moises Edson Yanez Villa',
    'website': '',
    'license': 'LGPL-3',
    'category': '',
    'depends': [
        'base',
        'sale',
        'dev_customer_credit_limit',
        'account',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/view_order_form.xml',
        'views/account_invoice_view.xml',
    ],
    'auto_install': False,
    'application': False,
}
