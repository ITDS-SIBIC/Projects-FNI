from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import UserError


class Pret(models.Model):
    _name = 'pret'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = u'Pret'

    @api.depends('duree_annee')
    def _duree_mois(self):
        for rec in self:
            rec.duree_mois = rec.duree_annee * 12

    name = fields.Char(u'Numéro', required=True, default='New')
    objet_contrat = fields.Char(u'Objet du prêt', tracking=True, required=True)
    date = fields.Date('Date signature')
    commission_gestion = fields.Float('Commission de Gestion')
    taux_interet = fields.Float('Taux d\'Intérêt')
    penalite = fields.Float('Pénalité')
    montant = fields.Float(string='Montant')
    #
    duree_credit = fields.Integer(string="Durée de Crédit (mois)")
    date_limite = fields.Date(string="Date Limite")
    duree_differee_mois = fields.Integer(string="Durée Différée (mois)")
    taux_interets_intercalaires = fields.Float(string="Taux Intérêts Intercalaires")
    #
    partner_id = fields.Many2one('res.partner', string='Client', required=False)

    conv_id = fields.Many2one(
        'convention',
        string='Convention',
        required=True,

    )

    @api.onchange('conv_id')
    def onchange_convention(self):
        for rec in self:
            if rec.conv_id:
                rec.partner_id = rec.conv_id.partner_id.id
            else:
                rec.partner_id = None

    user_id = fields.Many2one('res.users', string='Responsable', default=lambda self: self.env.user)
    state = fields.Selection([
        ('draft', 'En saisie'),
        ('in_progress', 'Vérifié'),
        ('done', 'Validé'),
        ('closed', 'Clôturé'),
    ], default='draft', string="State")


    def action_verifier(self):
        self.write({'state': 'in_progress'})

    def action_valider(self):
        self.write({'state': 'done'})  # Change 'Validé' to 'done'

    def action_cloturer(self):
        self.write({'state': 'closed'})


    description = fields.Text('Description')

    # Référence
    Co_contractants = fields.Char('Co-contractants')

    # Montants
    montant_dz = fields.Monetary('Montant')
    com = fields.Char(string='COM')
    currency_id = fields.Many2one('res.currency', string='Devise', default=lambda self: self.env.company.currency_id)

    # Commission de Gestion
    commission_gestion = fields.Monetary('Commission de Gestion', currency_field='currency_id')



    # Rubriques
    rebrique_ids = fields.Many2many('rebrique', string='Rubriques')
    total_montant_da = fields.Float(string='Total Montant DA', compute='_compute_total_montant_da', store=True)

    @api.depends('rebrique_ids.montant_da')
    def _compute_total_montant_da(self):
        for record in self:
            record.total_montant_da = sum(record.rebrique_ids.mapped('montant_da'))

            # Vérifier si la somme dépasse le montant de la convention
            if record.total_montant_da > record.conv_id.montant:
                raise UserError(
                    _('Vous ne pouvez pas ajouter d\'autres rubriques car la somme des Montant DA dépasse le montant de la convention.'))

    @api.constrains('rebrique_ids')
    def _check_rebrique_montant(self):
        for record in self:
            # Calculez la somme des montant_da des rubriques existantes
            total_montant_da = sum(record.rebrique_ids.mapped('montant_da'))

            # Vérifiez si la somme dépasse le montant de la convention
            if total_montant_da > record.conv_id.montant:
                raise UserError(
                    _('La somme des Montant DA des rubriques ne doit pas dépasser le montant de la convention.'))
    # Documents
    nom_doc_cnt = fields.Char('Nom de document')
    fichier_piece_jointe_doc_cnt = fields.Binary(string='Document Pièce Jointe')
    doc_cnt_piece = fields.Char(string='Nom du Fichier')

    # Avenant
    type_contrat = fields.Selection([('pret', 'Pret'), ('avenant', 'Avenant')], string='Type', default='pret')
    num_avenant = fields.Char('Numéro avenant', readonly=True)
    parent_id = fields.Many2one('pret', string='Pret origine', readonly=True)
    objet_avenant = fields.Char(u'Objet de l\'avenant', tracking=True)
    dpp1 = fields.Selection([
        ('PM', 'PM'),
        ('cni', 'CNI'),
        ('cim', 'CIM'),
        ('cpe', 'CPE'),
        ('autre', 'Autre')
    ], string='Décision pouvoir publique 01')
    ref_DPP1 = fields.Char('Référence DPP1')
    ref_dpp1_date = fields.Date('Date DPP1')

    dpp2 = fields.Selection([
        ('PM', 'PM'),
        ('cni', 'CNI'),
        ('cim', 'CIM'),
        ('cpe', 'CPE'),
        ('autre', 'Autre')
    ], string='Décision pouvoir publique 02')
    ref_DPP2 = fields.Char('Référence DPP2')
    ref_dpp2_date = fields.Date('Date DPP2')

    dpp3 = fields.Selection([
        ('PM', 'PM'),
        ('cni', 'CNI'),
        ('cim', 'CIM'),
        ('cpe', 'CPE'),
        ('autre', 'Autre')
    ], string='Décision pouvoir publique 03')
    ref_DPP3 = fields.Char('Référence DPP3')
    ref_dpp3_date = fields.Date('Date DPP3')

    dpp4 = fields.Selection([
        ('PM', 'PM'),
        ('cni', 'CNI'),
        ('cim', 'CIM'),
        ('cpe', 'CPE'),
        ('autre', 'Autre')
    ], string='Décision pouvoir publique 04')
    ref_DPP4 = fields.Char('Référence DPP4')
    ref_dpp4_date = fields.Date('Date DPP4')

    # Champs pour Décision Tutelle
    dt1 = fields.Selection([
        ('PM', 'PM'),
        ('cni', 'CNI'),
        ('cim', 'CIM'),
        ('cpe', 'CPE'),
        ('autre', 'Autre')
    ], string='Décision Tutelle 01')
    ref_DT1 = fields.Char('Référence DT1')
    ref_dt1_date = fields.Date('Date DT1')

    dt2 = fields.Selection([
        ('PM', 'PM'),
        ('cni', 'CNI'),
        ('cim', 'CIM'),
        ('cpe', 'CPE'),
        ('autre', 'Autre')
    ], string='Décision Tutelle 02')
    ref_DT2 = fields.Char('Référence DT2')
    ref_dt2_date = fields.Date('Date DT2')

    dt3 = fields.Selection([
        ('PM', 'PM'),
        ('cni', 'CNI'),
        ('cim', 'CIM'),
        ('cpe', 'CPE'),
        ('autre', 'Autre')
    ], string='Décision Tutelle 03')
    ref_DT3 = fields.Char('Référence DT3')
    ref_dt3_date = fields.Date('Date DT3')

    dt4 = fields.Selection([
        ('PM', 'PM'),
        ('cni', 'CNI'),
        ('cim', 'CIM'),
        ('cpe', 'CPE'),
        ('autre', 'Autre')
    ], string='Décision Tutelle 04')
    ref_DT4 = fields.Char('Référence DT4')
    ref_dt4_date = fields.Date('Date DT4')
    dt1 = fields.Selection([
        ('PM', 'PM'),
        ('cni', 'CNI'),
        ('cim', 'CIM'),
        ('cpe', 'CPE'),
        ('autre', 'Autre')
    ], string='Décision Tutelle 01')
    dt1_date = fields.Date('Date Décision Tutelle 01')

    dt2 = fields.Selection([
        ('PM', 'PM'),
        ('cni', 'CNI'),
        ('cim', 'CIM'),
        ('cpe', 'CPE'),
        ('autre', 'Autre')
    ], string='Décision Tutelle 02')
    dt2_date = fields.Date('Date Décision Tutelle 02')

    dt3 = fields.Selection([
        ('PM', 'PM'),
        ('cni', 'CNI'),
        ('cim', 'CIM'),
        ('cpe', 'CPE'),
        ('autre', 'Autre')
    ], string='Décision Tutelle 03')
    dt3_date = fields.Date('Date Décision Tutelle 03')

    dt4 = fields.Selection([
        ('PM', 'PM'),
        ('cni', 'CNI'),
        ('cim', 'CIM'),
        ('cpe', 'CPE'),
        ('autre', 'Autre')
    ], string='Décision Tutelle 04')
    dt4_date = fields.Date('Date Décision Tutelle 04')

    # Nouveaux Champs
    source_financement = fields.Selection([
        ('resources_fni', 'Resources FNI'),
        ('trésor', 'Sur resources du trésor'),
        ('bailleur_etranger', 'Bailleur de fond étranger')
    ], string='Source de Financement' )

    objet_financement = fields.Selection([
        ('pret_investissement', 'Prêt d\'Investissement'),
        ('participation_capital', 'Participation au capital social'),
        ('credit_exploitation', 'Crédit d\'Exploitation'),
        ('financement_refinancement', 'Financement d\'Investissement Refinancement')
    ], string='Objet de Financement')
    secteur_activite = fields.Selection([
        ('Hydrolique', 'Hydrolique'),
        ('industrie mechanique', 'industrie mechanique'),
        ('energie', 'energie'),

    ], string='Secteur d\'Activité')

    wilaya = fields.Char(string='Wilaya' )
    periode_remb_interets = fields.Date(string="Période de remboursement des intérêts intercalaires")
    periode_remb_principal = fields.Date(string="Période de remboursement du principal")
    dates_fixes_remb_interets = fields.Date(string="Dates fixes de remboursement des intérêts intercalaires",
                                            )
    service_gestionnaire = fields.Selection([
        ('credit_DR_alger', 'Département Crédit - DR Alger'),
        ('direction_gestion_financement', 'Direction Gestion des Financements pour Compte'),
        ('departement_financement_compte', 'Département Financement pour Compte'),
        ('direction_regionale_alger', 'Direction Régionale d\'Alger'),
        ('direction_regionale_annaba', 'Direction Régionale Annaba'),
        ('direction_regionale_constantine', 'Direction Régionale Constantine'),
        ('direction_regionale_oran', 'Direction Régionale d\'Oran'),
        ('service_gestion_1', 'Service Gestion 1'),
        ('service_gestion_2', 'Service de Gestion 02'),
        ('service_credit_dr_alger', 'Service Crédit DR Alger')
    ], string="Service Gestionnaire")

    gestionnaire_pret = fields.Selection([
        ('administrateur', 'Administrateur')
    ], string="Gestionnaire du Prêt")

    service_suivi = fields.Selection([
        ('credit_DR_alger', 'Département Crédit - DR Alger'),
        ('direction_gestion_financement', 'Direction Gestion des Financements pour Compte'),
        ('departement_financement_compte', 'Département Financement pour Compte'),
        ('direction_regionale_alger', 'Direction Régionale d\'Alger'),
        ('direction_regionale_annaba', 'Direction Régionale Annaba'),
        ('direction_regionale_constantine', 'Direction Régionale Constantine'),
        ('direction_regionale_oran', 'Direction Régionale d\'Oran'),
        ('service_gestion_1', 'Service Gestion 1'),
        ('service_gestion_2', 'Service de Gestion 02'),
        ('service_credit_dr_alger', 'Service Crédit DR Alger')
    ], string="Service Suivi (Siège)")

    res_suivi_pret = fields.Char(string="Res. Suivi du Prêt (Siège)")

    date_debut_differe = fields.Date(string="Date Début du Différé")
    date_fin_differe = fields.Date(string="Date Fin du Différé")
    total_mobilisation_fonds = fields.Float(string="Total Mobilisation de Fonds DGT", readonly=True)
    montant_utilisations = fields.Float(string="Montant des Utilisations", readonly=True)
    total_appel_fonds = fields.Float(string="Total Appel de Fonds DFC", readonly=True)
    montant_non_utilise = fields.Float(string="Montant Non Utilisé", readonly=True)
    encours = fields.Float(string="Encours", readonly=True)

    # New fields for Engagements et Paiements
    total_engagements = fields.Float(string="Total Engagements", readonly=True)
    solde_engagements = fields.Float(string="Solde Engagements", readonly=True)
    total_paiements = fields.Float(string="Total Paiements", readonly=True)
    solde_paiements = fields.Float(string="Solde Paiements", readonly=True)
    observations = fields.Text(string="Observations")
    compte_comptable = fields.Char(string="N° de Compte Comptable")
    designation_compte_comptable = fields.Char(string="Désignation Compte Comptable")
    interets_intercalaires_capitalises = fields.Boolean(string="Intérêts Intercalaires Capitalisés")
    interets_intercalaires_pris_en_charge_par_tresor = fields.Boolean(
        string="Intérêts Intercalaires Pris en Charge par le Trésor")
    commission_prise_en_charge_par_tresor = fields.Boolean(
        string="Commission Prise en Charge par le Trésor (pendant la période différée)")
    commission_prise_en_charge_par_entreprise = fields.Boolean(
        string="Commission Prise en Charge par l'Entreprise (pendant la période différée)")
    # ajoute

    avenant_ids = fields.One2many('avenant.pret', 'pret_id', string='Avenants Associés')

    def action_add_avenant(self):
        """Ouvre le formulaire pour ajouter un nouvel avenant."""
        return {
            'name': 'Ajouter Avenant',
            'type': 'ir.actions.act_window',
            'res_model': 'avenant.pret',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_pret_id': self.id,  # Passer l'ID du prêt actuel
            }
        }

    def action_go_to_avenant(self):
        """Redirige vers le formulaire d'avenant pour le prêt actuel."""
        if self.state != 'done':
            raise UserError("Le prêt doit être dans l'état 'Validé' pour accéder à l'avenant.")

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'avenant.pret',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_pret_id': self.id,  # Passer l'ID du prêt actuel
            }
        }


    #@api.model
    #def create(self, vals):
       # if vals.get('type_contrat') == 'pret':
            #vals['name'] = self.env['ir.sequence'].get('pret.engagement')
        #return super(Pret, self).create(vals)


    @api.model

    @api.onchange('conv_id')
    def onchange_conv_id(self):
        if self.conv_id:
            self.partner_id = self.conv_id.partner_id.id
            self.commission_gestion = self.conv_id.commission_gestion
            self.penalite = self.conv_id.penalite
            self.taux_interet = self.conv_id.taux_interet
            self.montant = self.conv_id.montant
            self.currency_id = self.conv_id.currency_id
            #####
            self.duree_credit = self.conv_id.duree_annee # Assuming these fields are available on the convention model
            self.date_limite = self.conv_id.extensions_differee_date_limite
            self.duree_differee_mois = self.conv_id. duree_mois
            self.taux_interets_intercalaires = self.conv_id.taux_commission_intercalaire

            #####

    #def create_avenant(self):
        #return {
            #'name': _('Create Avenant'),
            #'type': 'ir.actions.act_window',
            #'res_model': 'create.avenant.pret.wizard',
            #'view_mode': 'form',
            #'target': 'new',
            #'context': {
               # 'default_pret_id': self.id,
                #'default_date_avenant': fields.Date.today(),
            #}
        #}
    def create_avenant(self):
        return {
            'name': _('Create Avenant'),
            'type': 'ir.actions.act_window',
            'res_model': 'create.avenant.pret.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_pret_id': self.id,
                'default_date_avenant': fields.Date.today(),
            }
        }

def update_from_avenant(self, avenant):
    """Update fields of the loan based on the amendment's information."""
    if avenant.state in ['valide', 'enreg']:
        fields_to_update = {
            'montant': avenant.montant,
            'taux_interet': avenant.taux_interet,
            'penalite': avenant.penalite,
            'commission_gestion': avenant.commission_gestion,
            # Add other fields that need to be updated
        }

        for field, value in fields_to_update.items():
            if value is not None:
                setattr(self, field, value)



def showavenants(self):
    """This method is called when the Show Avenants button is clicked."""
    self.ensure_one()  # Ensures that we are working with a single record
    return {
        'type': 'ir.actions.act_window',
        'name': 'Avenants de Prêt',
        'res_model': 'avenant.pret',
        'view_mode': 'tree,form',
        'domain': [('pret_id', '=', self.id)],  # Filter Avenants by the current Loan
        'context': {
            'default_pret_id': self.id,  # Optional: Pre-fill the pret_id field in Avenant form
        },
    }