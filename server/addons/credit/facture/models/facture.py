from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import UserError


class Facture(models.Model):
    _name = 'facture'
    _inherit= ['mail.thread', 'mail.activity.mixin']
    _description = u'Facture'

    @api.depends('duree_annee')
    def _duree_mois(self):
        for rec in self:
            rec.duree_mois = rec.duree_annee * 12

    name = fields.Char(u'Numéro', required=True, readonly=True, default='New')
    date = fields.Date('Date')
    num_mobilisation = fields.Integer('N° Mobilisation')

    partner_id = fields.Many2one('res.partner', string='Client')
    conv_id = fields.Many2one('convention', string='Convention')
    user_id = fields.Many2one('res.users', string='Responsable', default=lambda self: self.env.user)
    state = fields.Selection([('draft', 'Nouveau'),
                              ('in_progress', 'Enregistrer'),
                              ], string=u'Etat', default='draft')
    contratavantid=fields.Many2one('contrat', string=u'Contrat')
    description = fields.Text('Description')


    # Montants
    montant_dz = fields.Float('Montant contrat')
    montant_ttc = fields.Float('Montant TTC')
    montant_client = fields.Float('Montant réglé par le client')

    part_FNI = fields.Float('Part FNI (%)')
    part_client = fields.Float('Part Client (%)')
    Contre_valeur = fields.Float('Contre-valeur DA')


    def action_activate(self):
        # self.date_signature = fields.Date.today()
        self.state = 'in_progress'

    @api.model
    def create(self, vals):
        #if vals['type_contrat'] == 'contrat':
        vals['name'] = self.env['ir.sequence'].get('facture.engagement')

        return super(Facture, self).create(vals)



    def action_archiver(self):
        self.state = 'archived'