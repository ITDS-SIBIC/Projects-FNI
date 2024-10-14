from odoo import models, fields, api


class Convention(models.Model):
    _inherit = 'convention'

    @api.depends('contrat_ids')
    def _nbr_contrat(self):
        for rec in self:
            rec.nbr_contrat = len(rec.contrat_ids)

    contrat_ids = fields.One2many('contrat', 'conv_id', string='Contrats')
    nbr_contrat = fields.Integer(compute=_nbr_contrat, string='Nombre de contrats')
