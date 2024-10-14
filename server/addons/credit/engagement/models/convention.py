from odoo import models, fields, api, _
from odoo.exceptions import UserError

from datetime import timedelta
from server.odoo.cli.scaffold import env


class Convention(models.Model):
    _name = 'convention'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = u'Convention'


    def action_convert_values(self):
        """Méthode pour convertir les valeurs par 0.10."""
        for record in self:
            record.commission_gestion *= 0.10
            record.taux_interet *= 0.10
            record.penalite *= 0.10

        # Optionnel : Message de confirmation
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Les valeurs ont été converties avec succès !',
                'type': 'rainbow_man',
            }
        }
    @api.depends('duree_annee')
    def _duree_mois(self):
        for rec in self:
            rec.duree_mois = rec.duree_annee * 12

    @api.depends('duree_utilisation', 'date_premiere_mobilisation')
    def _compute_date_limite_utilisation(self):
        for record in self:
            if record.duree_utilisation and record.date_premiere_mobilisation:
                duree = timedelta(days=record.duree_utilisation * 365)
                record.date_limite_utilisation = record.date_premiere_mobilisation + duree
            else:
                record.date_limite_utilisation = False



    name = fields.Char(u'Numéro', required=True, readonly=True, default='New')
    objet = fields.Char(u'Objet du crédit', tracking=True, required=True)
    num_accord = fields.Char('Accord du comité des engagements')
    user_id = fields.Many2one('res.users', string='Responsable', default=lambda self: self.env.user)
    num_enregistrement = fields.Char('Numéro enregistrement')
    date_enregistrement = fields.Date('Date d\'enregistrement')
    date_signature = fields.Date('Date signature', default=fields.Date.today())
    date_notification = fields.Date('Date notification')
    date_limite = fields.Date('Date limite')
    type_credit = fields.Selection([('investissement', 'Investissement'),], string=u'Type crédit', default='investissement')
    partner_id = fields.Many2one('res.partner', string='Client', required=True)

    state = fields.Selection([
        ('draft', 'En saisie'),
        ('in_progress', 'Vérifié'),
        ('done', 'Validé'),
        ('closed', 'Clôturé'),
        ('archived', 'Archivé'),  # Add the archived state
    ], default='draft', string="State")

    description = fields.Text('Description')

    # Conditions
    commission_gestion = fields.Float('Commission de Gestion', required=True)
    taux_interet = fields.Float('Taux d\'Intérêt', required=True)
    penalite = fields.Float('Pénalité', required=True)

    @api.onchange('commission_gestion')
    def _onchange_commission_gestion(self):
        if self.commission_gestion:
            self.commission_gestion *= 0.01

    @api.onchange('taux_interet')
    def _onchange_taux_interet(self):
        if self.taux_interet:
            self.taux_interet *= 0.01

    @api.onchange('penalite')
    def _onchange_penalite(self):
        if self.penalite:
            self.penalite *= 0.01

    montant = fields.Float(string='Montant')
    taux_commission_intercalaire = fields.Float('Taux Commission Intercalaire',
                                                compute='_compute_taux_commission_intercalaire', store=True)

    @api.depends('taux_interet', 'commission_gestion')
    def _compute_taux_commission_intercalaire(self):
        for record in self:
            record.taux_commission_intercalaire = record.taux_interet + record.commission_gestion

    @api.model
    def create(self, vals):
        # Convert values to percentages
        vals['commission_gestion'] = vals.get('commission_gestion', 0) * 0.01
        vals['taux_interet'] = vals.get('taux_interet', 0) * 0.01
        vals['penalite'] = vals.get('penalite', 0) * 0.01
        vals['name'] = self.env['ir.sequence'].next_by_code('itdev.engagement')
        return super(Convention, self).create(vals)

    def write(self, vals):
        if 'commission_gestion' in vals:
            vals['commission_gestion'] *= 0.01
        if 'taux_interet' in vals:
            vals['taux_interet'] *= 0.01
        if 'penalite' in vals:
            vals['penalite'] *= 0.01
        return super(Convention, self).write(vals)

    commission_gestion_10 = fields.Float('Commission de Gestion (10%)', compute='_compute_commission_gestion_10')

    def _compute_commission_gestion_10(self):
        self.commission_gestion_10 = self.commission_gestion * 0.10


    currency_id = fields.Many2one('res.currency', string='Devise', default=lambda self: self.env.company.currency_id)

    duree_annee = fields.Integer('Durée (année)',required=True)
    duree_mois = fields.Integer(compute=_duree_mois, string='Durée (mois)')

    date_premiere_mobilisation = fields.Date('Date première mobilisation')




    # avenant
    type_convention = fields.Selection([('convention', 'Convention'), ('avenant', 'Avenant')], string='Type', default='convention')
    num_avenantcn = fields.Char(u'Numéro avenant', readonly=True)
    parent_id = fields.Many2one('convention', string='Convention origine', readonly=True)
    objet_avenant = fields.Char(u'Objet de l\'avenant', tracking=True)
    date = fields.Date('Date')


    def action_add_decision(self):
        # Implémentez la logique pour ajouter une décision
        self.ensure_one()  # Assurez-vous que l'objet est unique
        # Ajoutez la logique ici, comme créer un enregistrement lié
    # décisions
    #pouvoir public
    dpp1 = fields.Selection([
        ('PM', 'PM'),
        ('cni', 'CNI'),
        ('cim', 'CIM'),
        ('cpe', 'CPE'),
        ('autre', 'Autre')
    ], string='Décision pouvoir publique 01')
    ref_DPP1 = fields.Char('Référence DPP1')
    ref_dpp1_date = fields.Date('Date ')

    dpp2 = fields.Selection([
        ('pm', 'PM'),
        ('cni', 'CNI'),
        ('cim', 'CIM'),
        ('cpe', 'CPE'),
        ('autre', 'Autre')
    ], string='Décision pouvoir publique 02')
    ref_DPP2 = fields.Char('Référence DPP2')
    ref_dpp2_date = fields.Date('Date ')

    dpp3 = fields.Selection([
        ('pm', 'PM'),
        ('cni', 'CNI'),
        ('cim', 'CIM'),
        ('cpe', 'CPE'),
        ('autre', 'Autre')
    ], string='Décision pouvoir publique 03')
    ref_DPP3 = fields.Char('Référence DPP3')
    ref_dpp3_date = fields.Date('Date ')

    dpp4 = fields.Selection([
        ('pm', 'PM'),
        ('cni', 'CNI'),
        ('cim', 'CIM'),
        ('cpe', 'CPE'),
        ('autre', 'Autre')
    ], string='Décision pouvoir publique 04')
    ref_DPP4 = fields.Char('Référence DPP4')
    ref_dpp4_date = fields.Date('Date ')
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

    state_action = fields.Selection([
        ('saisie', 'saisie'),
        ('inactive', 'Désactivé')
    ], string='Statut', default='saisie')
    nantissement_action = fields.Char('Nantissement d\'action ')
    nantissement_action_date = fields.Date('Date de nantissement d\'action')
    fichier_piece_jointe_nantissement_action = fields.Binary(string='Nantissement d\'action Pièce Jointe')
    nantissement_action_piece = fields.Char(string='Nom du Fichier')
    checkbox_field_action = fields.Boolean(string='Cocher si oui')

    state_equipement = fields.Selection([
        ('active', 'Activé'),
        ('inactive', 'Désactivé')
    ], string='Statut', default='active')
    nantissement_equipement = fields.Char('Nantissement d\'équipement ')
    nantissement_equipement_date = fields.Date('Date d\'enregistrement de publication')
    fichier_piece_jointe_nantissement_equipement = fields.Binary(string='Nantissement d\'équipement Pièce Jointe')
    nantissement_equipement_piece = fields.Char(string='Nom du Fichier')
    checkbox_field_equipement = fields.Boolean(string='Cocher si oui')

    state_specimen = fields.Selection([
        ('active', 'Activé'),
        ('inactive', 'Désactivé')
    ], string='Statut', default='active')
    specimen_signature = fields.Char('Spécimen de signature')
    specimen_signature_date = fields.Date('Date de spécimen de signature')
    fichier_piece_jointe_specimen_signature = fields.Binary(string='Specimen de signature Pièce Jointe')
    specimen_signature_piece = fields.Char(string='Nom du Fichier')
    checkbox_field_specimen = fields.Boolean(string='Cocher si oui')

    state_billet = fields.Selection([
        ('active', 'Activé'),
        ('inactive', 'Désactivé')
    ], string='Statut', default='active')
    billet_ordre_global = fields.Char('Billet à ordre global')
    billet_ordre_global_date = fields.Date('Date de Billet à ordre global')
    fichier_piece_jointe_billet_ordre_global = fields.Binary(string='Billet à ordre global Pièce Jointe')
    billet_ordre_global_piece = fields.Char(string='Nom du Fichier')
    checkbox_field_billet = fields.Boolean(string='Cocher si oui')

    state_chaine = fields.Selection([
        ('active', 'Activé'),
        ('inactive', 'Désactivé')
    ], string='Statut', default='active')
    chaine_billet_ordre = fields.Char('Chaine de billet à ordre après la période d\'utilisation')
    chaine_billet_ordre_date = fields.Date('Date de chaine de billet à ordre après la période d\'utilisation')
    fichier_piece_jointe_chaine_billet_ordre = fields.Binary(string='chaine de billet à ordre global Pièce Jointe')
    chaine_billet_ordre_piece = fields.Char(string='Nom du Fichier')
    checkbox_field_chaine = fields.Boolean(string='Cocher si oui')

    state_caution = fields.Selection([
        ('active', 'Activé'),
        ('inactive', 'Désactivé')
    ], string='Statut', default='active')
    caution_solidaire = fields.Char('Caution solidaire')
    caution_solidaire_date = fields.Date('Date de caution solidaire')
    fichier_piece_jointe_caution_solidaire = fields.Binary(string='caution solidaire Pièce Jointe')
    caution_solidaire_piece = fields.Char(string='Nom du Fichier')
    checkbox_field_caution = fields.Boolean(string='Cocher si oui')

    state_financiere = fields.Selection([
        ('active', 'Activé'),
        ('inactive', 'Désactivé')
    ], string='Statut', default='active')
    garantie_fianciere = fields.Selection([('fgar', 'FGAR'), ('cgci', 'CGCI')], string='Garantie financière')
    garantie_fianciere_date = fields.Date('Date de garantie financière')
    fichier_piece_jointe_garantie_fianciere = fields.Binary(string='Garantie financière Pièce Jointe')
    garantie_fianciere_piece = fields.Char(string='Nom du Fichier')
    checkbox_field_garantie_fianciere = fields.Boolean(string='Cocher si oui')

    state_assurance = fields.Selection([
        ('active', 'Activé'),
        ('inactive', 'Désactivé')
    ], string='Statut', default='active')
    assurance = fields.Char('Autre / Assurance et subrogation d\'assurance')
    assurance_date = fields.Date('Date d\'Assurance et subrogation d\'assurance / Autre')
    fichier_piece_jointe_assurancee = fields.Binary(string='Autre / Assurance et subrogation d\'assurance Pièce Jointe')
    assurance_piece = fields.Char(string='Nom du Fichier')
    checkbox_field_assurance = fields.Boolean(string='Cocher si oui')
    avenant_ids = fields.One2many('convention', 'parent_id', string='Avenants')
    # New checkbox fields
    interets_intercalaires_capitalises = fields.Boolean(string="Intérêts Intercalaires Capitalisés")
    interets_intercalaires_pris_en_charge_par_tresor = fields.Boolean(
        string="Intérêts Intercalaires Pris en Charge par le Trésor")
    commission_prise_en_charge_par_tresor = fields.Boolean(
        string="Commission Prise en Charge par le Trésor (pendant la période différée)")
    commission_prise_en_charge_par_entreprise = fields.Boolean(
        string="Commission Prise en Charge par l'Entreprise (pendant la période différée)")


    # NUMERO DE CONVENTION

    numero_convention = fields.Char(string="Numéro de Convention")
 # DATE LIMITE

    extensions_differee_date_limite = fields.Date(string="Extensions Différée Date Limite")
    def action_view_avenants(self):
        """ Open a window to view the list of avenants related to this convention. """
        self.ensure_one()  # Ensure that we are dealing with a single record
        return {
            'type': 'ir.actions.act_window',
            'name': 'Avenants',
            'view_mode': 'tree,form',
            'res_model': 'convention',
            'domain': [('parent_id', '=', self.id)],  # Filter avenants related to this convention
            'context': {'create': False},
        }

    def action_verifier(self):
        self.write({'state': 'in_progress'})

    def action_valider(self):
          # Change 'Validé' to 'done'
        for record in self:
            record.write({'state': 'done'})


    def action_cloturer(self):
        self.write({'state': 'closed'})
        return {
            'name': _('Enregistrement'),
            'type': 'ir.actions.act_window',
            'res_model': 'create.avenantc2.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('engagement.create_enr_form').id,
            'target': 'new',
            'context': {
                'default_convention_id': self.id,
                'default_date_avenant': fields.Date.today(),
                'default_name': 'Registration Number',
                'default_date': fields.Date.today()
            },
        }







    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].get('itdev.engagement')

        return super(Convention, self).create(vals)

    def create_avenantc(self):
        return {
            'name': _(u'Création avenant'),
            'type': 'ir.actions.act_window',
            'res_model': 'create.avenantc.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('engagement.create_avenantc_form').id,
            'target': 'new',
            'context': {
                'default_convention_id': self.id,
                'default_date_avenant': fields.Date.today()},
            'avenant_vals' : {

            'objet_avenant': 'Nouvel avenant',

            'montant': 0.0,
        }
        }

    @api.model
    def create_avenant(self, convention_id, avenant_vals):

        # Get the convention record
        convention = self.browse(convention_id)

        # Calculate the new montant value

        new_montant = convention.montant + avenant_vals['montant']

        # Update the avenant_vals dictionary with the new montant value

        avenant_vals['montant'] = new_montant

        # Create the avenant record

        avenant = self.create({

            'type_convention': 'avenant',

            'parent_id': convention_id,

            **avenant_vals

        })

        # Update the montant field of the convention record

        convention.montant = new_montant

        # Return the avenant record

        return avenant

    def action_show_tree(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Conventions',
            'view_mode': 'tree,form',
            'res_model': 'convention',
            'domain': [],
            'context': {'create': False},
        }

    def action_archiver(self):
        self.state = 'archived'
    def action_open_avenant_wizard(self):
        """Open the avenant wizard to update fields of the convention."""
        self.ensure_one()
        if self.state != 'done':
            raise UserError(_('Vous ne pouvez pas modifier cette convention tant qu\'elle n\'est pas validée.'))

        return {
            'name': _('Modifier la Convention'),
            'type': 'ir.actions.act_window',
            'res_model': 'avenant.convention.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_convention_id': self.id,
                'default_objet': self.objet,
                'default_commission_gestion': self.commission_gestion,
                'default_taux_interet': self.taux_interet,
                'default_penalite': self.penalite,
                'default_montant': self.montant,
                # Add other default fields here...
            },
        }

    def action_view_conventions(self):
        """ Open a window to view only the list of conventions. """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Conventions',
            'view_mode': 'tree,form',
            'res_model': 'convention',
            'domain': [('type_convention', '=', 'convention')],  # Filter to show only conventions
        }
