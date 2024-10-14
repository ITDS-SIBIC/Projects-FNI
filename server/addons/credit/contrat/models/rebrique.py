# File: models/rebrique.py

from odoo import models, fields

class Rebrique(models.Model):
    _name = 'rebrique'
    _description = 'Rebrique'

    name = fields.Char(string='Name', required=True)
    montant_da = fields.Float(string='Montant DA')
    total_paiement = fields.Float(string='Total Paiement')
    solde_rubrique = fields.Float(string='Solde Rubrique')
