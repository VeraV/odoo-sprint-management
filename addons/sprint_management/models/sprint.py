from odoo import models, fields, api

class ProjectSprint(models.Model):
    #Odoo model attributes
    _name = 'project.sprint'#creates table project_sprint, required
    _description = 'Project Sprint' #shows in logs, good for docs
    _order = 'start_date desc'#SQL: ORDER BY start_date DESC

    name = fields.Char(string='Sprint Name', required=True)
    project_id = fields.Many2one('project.project', string='Project', required=True, ondelete='cascade')
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', required=True)
    goal = fields.Text(string='Sprint Goal')
    task_ids = fields.One2many('project.task', 'sprint_id', string='Tasks')
    task_count = fields.Integer(string='Task Count', compute='_compute_task_count')

    @api.depends('task_ids')#mark as compute method, call each time task_ids changes
    def _compute_task_count(self):
        for sprint in self:
            sprint.task_count = len(sprint.task_ids)