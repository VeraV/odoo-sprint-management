from odoo import models, fields, api

class ProjectSprint(models.Model):
    _name = 'project.sprint'
    _description = 'Project Sprint'
    _order = 'start_date desc'

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
    available_task_ids = fields.Many2many(
        'project.task',
        'sprint_task_add_rel',
        'sprint_id',
        'task_id',
        string='Add Existing Tasks',
    )

    @api.depends('task_ids')
    def _compute_task_count(self):
        for sprint in self:
            sprint.task_count = len(sprint.task_ids)

    @api.model_create_multi
    def create(self, vals_list):
        sprints = super().create(vals_list)
        sprints._assign_available_tasks()
        # sprints._validate_task_projects()  # Temporarily disabled for debugging
        return sprints

    def write(self, vals):
        res = super().write(vals)
        if 'available_task_ids' in vals:
            self._assign_available_tasks()
        return res

    def _assign_available_tasks(self):
        """Assign tasks from available_task_ids to this sprint, then clear picker."""
        for sprint in self:
            if sprint.available_task_ids:
                sprint.available_task_ids.write({'sprint_id': sprint.id})
                sprint.available_task_ids = [(5, 0, 0)]

    @api.onchange('project_id')
    def _onchange_project_id(self):
        """Prevent changing project if sprint has tasks."""
        if self._origin.project_id and self.task_ids:
            self.project_id = self._origin.project_id
            return {
                'warning': {
                    'title': 'Cannot Change Project',
                    'message': 'Remove all tasks first before changing the project.'
                }
            }