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
    available_task_ids = fields.Many2many(
        'project.task',
        'sprint_task_add_rel',
        'sprint_id',
        'task_id',
    )

    @api.depends('task_ids')#mark as compute method, call each time task_ids changes
    def _compute_task_count(self):
        for sprint in self:
            sprint.task_count = len(sprint.task_ids)

    #called when created
    @api.model_create_multi
    def create(self, vals_list):
        sprints = super().create(vals_list)
        sprints._assign_available_tasks()
        # sprints._validate_task_projects()  # Temporarily disabled for debugging
        return sprints

    #Ensures tasks are assigned when they are selected from the picker.
    #called when updated
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
        
    @api.constrains('task_ids', 'project_id')
    def _check_task_projects(self):
        """Ensure all tasks belong to the sprint's project."""
        for sprint in self:
            if sprint.task_ids:
                wrong_tasks = sprint.task_ids.filtered(lambda t: t.project_id != sprint.project_id)
                if wrong_tasks:
                    raise models.ValidationError(
                        f"All tasks must belong to project '{sprint.project_id.name}'. "
                        f"Invalid tasks: {', '.join(wrong_tasks.mapped('name'))}"
                    )    