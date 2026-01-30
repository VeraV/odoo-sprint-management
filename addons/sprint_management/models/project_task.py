from odoo import models, fields, api
from odoo.exceptions import UserError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    sprint_id = fields.Many2one('project.sprint', string='Sprint', ondelete='set null')

    #@api.onchange('project_id')
    #def _onchange_project_id_sprint_warning(self):
    #    """Warn immediately and revert when trying to change project on a task in a sprint."""
    #    if self._origin.id and self.sprint_id and self.project_id != self.sprint_id.project_id:
    #        sprint_name = self.sprint_id.name
    #        self.project_id = self.sprint_id.project_id  # Revert to original
    #        return {
    #            'warning': {
    #                'title': 'Cannot Change Project',
    #                'message': f'Remove the task from sprint "{sprint_name}" first before changing the project.'
    #            }
    #        }

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