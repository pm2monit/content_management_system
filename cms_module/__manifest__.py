{
    'name': 'cms_module',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Manage website content with categories, tags, and public API',
    'description': """
Content Management System
========================
This module provides a comprehensive content management system for Odoo.
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'web',
    ],
    'data': [
        'security/content_management_system_groups.xml',
        'security/ir.model.access.csv',
        'views/cms_menu.xml',
        'views/cms_content_type_views.xml',
        'views/cms_category_views.xml',
        'views/cms_tag_views.xml',
        'views/cms_content_views.xml',  
    ],
    'assets': {
        'web.assets_backend': [
            'content_management_system/static/src/js/cms_dashboard.js',
            'content_management_system/static/src/css/cms_style.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}


