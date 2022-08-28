# -*- coding: utf-8 -*-
{
    'name': "Base Agile ",
    'summary': """
            Base Agile
    """,
    'description': """
            Base Agile
    """,
    'version': '15.0.0.1',
    'category': 'project',
    'sequence': 1,
    'author': "Eng-Mahmoud Ramadan",
    'website': 'mramadan271193@gmail.com',
    'depends': [
        'base',
        'hr',
        'project',
    ],

    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/project_project_view.xml',
        'views/project_task_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'images': [],
    'price': 0.0,
    'currency': 'EUR',
}
