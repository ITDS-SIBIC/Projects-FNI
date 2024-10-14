from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import UserError


class Mobilisation(models.Model):
    _name = 'mobilisation'
    _inherit= ['mail.thread', 'mail.activity.mixin']
    _description = u'Mobilisation'

    @api.depends('duree_annee')
    def _duree_mois(self):
        for rec in self:
            rec.duree_mois = rec.duree_annee * 12

    name = fields.Char(u'Numéro', required=True, readonly=True, default='New')
    num_mobilisation = fields.Integer('N° Mobilisation')
    partner_id = fields.Many2one('res.partner', string='Client', required=True)
    contrat_id = fields.Many2one('contrat', string='Contrat', required=True)
    facture_id = fields.Many2one('facture',string='Facture',required=True)
    conv_id = fields.Many2one('convention', string='Convention',required=True)
    user_id = fields.Many2one('res.users', string='Responsable', default=lambda self: self.env.user)
    state = fields.Selection([('draft', 'Nouveau'),
                              ('in_progress', 'En cours'),
                              ('done', u'Terminé'),
                              ('archived', u'Archivé'),
                              ('cancel', u'Annulé'),
                              ], string=u'Etat', default='draft')

    montant_mobilisation = fields.Monetary('Montant')
    currency_id = fields.Many2one('res.currency', string='Devise', default=lambda self: self.env.company.currency_id)
    date_mobilisation = fields.Date('Date mobilisation')
    date_limite_utilisation = fields.Date('Date limite d\'utilisation')
    reste_mobiliser = fields.Monetary('Reste à mobiliser')

    def action_activate(self):
        # self.date_signature = fields.Date.today()
        self.state = 'in_progress'



    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].get('mobilisation.engagement')
        return super(Mobilisation, self).create(vals)


   # @api.onchange('conv_id')
   # def onchange_convention(self):
    #    for rec in self:
     #       if rec.conv_id:
      #          rec.partner_id = rec.conv_id.partner_id.id
       #     else:
        #        rec.partner_id = None




