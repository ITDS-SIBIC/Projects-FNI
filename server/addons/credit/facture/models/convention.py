from odoo import models, fields, api

class Convention(models.Model):
    _inherit = 'convention'

    facture_ids = fields.One2many('facture', 'conv_id', string='Factures')
    nbr_facture = fields.Integer(compute='_compute_nbr_facture', string='Nombre de factures')

    @api.depends('facture_ids')
    def _compute_nbr_facture(self):
        for rec in self:
            rec.nbr_facture = len(rec.facture_ids)