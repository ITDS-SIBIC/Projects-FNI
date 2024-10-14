from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import UserError


class Contrat(models.Model):
    _name = 'contrat'
    _inherit     = ['mail.thread', 'mail.activity.mixin']
    _description = u'Contrat'

    @api.depends('duree_annee')
    def _duree_mois(self):
        for rec in self:
            rec.duree_mois = rec.duree_annee * 12

    name = fields.Char(u'Numéro', required=True, readonly=True, default='New')
    objet_contrat = fields.Char(u'Objet du contrat', tracking=True, required=True)
    date = fields.Date('Date signature')
    num_mobilisation = fields.Integer('N° Mobilisation')
    partner_id = fields.Many2one('res.partner', string='Client', required=True)
    conv_id = fields.Many2one('convention', string='Convention', required=True)
    user_id = fields.Many2one('res.users', string='Responsable', default=lambda self: self.env.user)
    state = fields.Selection([('draft', 'Nouveau'),
                              ('in_progress', 'En cours'),
                              ('done', u'Terminé'),
                              ('archived', u'Archivé'),
                              ('cancel', u'Annulé'),
                              ], string=u'Etat', default='draft')

    description = fields.Text('Description')

    # Référence
    Co_contractants = fields.Char('Co-contractants')

    # Montants
    montant_dz = fields.Monetary('Montant')
    currency_id = fields.Many2one('res.currency', string='Devise', default=lambda self: self.env.company.currency_id)
    currency_2_id = fields.Many2one('res.currency', string='Devise', default=lambda self: self.env.company.currency_id)
    montant_devise = fields.Monetary('Montant Devise')
    taux_devise = fields.Float('Taut Devise')
    part_FNI = fields.Float('Part FNI (%)')
    part_client = fields.Float('Part Client (%)')
    Contre_valeur = fields.Float('Contre-valeur DA')
    montant_global_DA_HT = fields.Float('Montant global DA HT')
    montant_TVA = fields.Float('Montant TVA')
    montant_global_DA_TTC = fields.Float('Montant global DA TTC')

    # Domiciliation Bancaire
    banque = fields.Char('Banque')
    num_compte_Dinars = fields.Char('N° compte Dinars')
    agence = fields.Char('Agence')
    fichier_piece_jointe_domiciliations_etranger = fields.Binary(string='Engagement des domiciliations pour les fournisseurs à l’étranger ')
    domiciliations_etranger_piece = fields.Char(string='Nom du Fichier')

    # Rubriques
    rubrique = fields.Char('Rubrique')
    montantDA_rub = fields.Float('Montant DA')
    total_paiement = fields.Float('Total paiement')
    solde_rubrique = fields.Float('Solde rubrique')

    # Documents
    nom_doc_cnt = fields.Char('Nom de document')
    fichier_piece_jointe_doc_cnt = fields.Binary(string='Document Pièce Jointe')
    doc_cnt_piece = fields.Char(string='Nom du Fichier')

    # Avenant
    #type_contrat = fields.Selection([('contrat', 'Contrat'), ('avenant', 'Avenant')], string='Type', default='contrat')
    num_avenant = fields.Char('Numéro avenant', readonly=True)
    parent_id = fields.Many2one('contrat', string='Contrat origine', readonly=True)
    objet_avenant = fields.Char(u'Objet de l\'avenant', tracking=True)

    def action_activate(self):
        # self.date_signature = fields.Date.today()
        self.state = 'in_progress'

    @api.model
    def create(self, vals):
        if vals.get('type_contrat') == 'contrat':
            vals['name'] = self.env['ir.sequence'].get('contrat.engagement')

        return super(Contrat, self).create(vals)


    @api.onchange('conv_id')
    def onchange_convention(self):
        for rec in self:
            if rec.conv_id:
                rec.partner_id = rec.conv_id.partner_id.id
            else:
                rec.partner_id = None

    def create_avenant(self):
        return {
            'name': _(u'Création avenant'),
            'type': 'ir.actions.act_window',
            'res_model': 'create.avenant.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('contrat.create_avenant_form').id,
            'target': 'new',
            'context': {
                'default_contrat_id': self.id,
                'default_date_avenant': fields.Date.today()}
        }

    def action_archiver(self):
        self.state = 'archived'
