from odoo import models, fields, api


class Convention(models.Model):
    _inherit = 'convention'

    @api.depends('mobilisation_ids')
    def _nbr_mobilisation(self):
        for rec in self:
            rec.nbr_mobilisation = len(rec.mobilisation_ids)

    mobilisation_ids = fields.One2many('contrat', 'conv_id', string='Contrats')
    nbr_mobilisation = fields.Integer(compute=_nbr_mobilisation, string='Nombre de mobilisations')
