from odoo import models, fields, api
from odoo.exceptions import UserError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    sprint_id = fields.Many2one('project.sprint', string='Sprint', ondelete='set null')

    def write(self, vals):
        """Block project change if task is in a sprint (backup validation)."""
        if 'project_id' in vals:
            for task in self:
                if task.sprint_id and vals['project_id'] != task.sprint_id.project_id.id:
                    raise UserError(
                        f"Cannot change project while task is in a sprint. "
                        f"Remove the task from sprint '{task.sprint_id.name}' first."
                    )
        return super().write(vals)
    
    def action_unassign_from_sprint(self):
        """Remove task from sprint (set sprint_id to null)."""
        self.sprint_id = False