from odoo import models, fields

class ProjectTask(models.Model):
    _inherit = 'project.task'

    sprint_id = fields.Many2one('project.sprint', string='Sprint', ondelete='set null')