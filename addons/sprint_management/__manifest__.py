{
    'name': 'Sprint Management',
    'version': '1.0',
    'category': 'Project',
    'summary': 'Organize project tasks into sprints',
    'description': """
        Sprint Management for Odoo Projects
        ====================================
        Adds sprint functionality to organize tasks into time-boxed iterations.
    """,
    'author': 'Vera Fileyeva',
    'depends': ['project'],
    'data': [
        'security/ir.model.access.csv',
        'views/sprint_views.xml',
        'views/project_task_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}