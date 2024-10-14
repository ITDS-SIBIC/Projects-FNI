# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Avenant(models.Model):
    _name = 'avenant.pret'
    _description = 'Avenant (Amendment)'

    # Fields
    pret_id = fields.Many2one('pret', string='Loan Agreement', required=True)
    date_avenant = fields.Date(string='Date of Amendment', required=True)
    montant = fields.Float(string='Amount', required=True)
    taux_interet = fields.Float(string='Interest Rate', required=True)
    penalite = fields.Float(string='Penalty', required=True)
    commission_gestion = fields.Float(string='Management Commission', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('refused', 'Refused')
    ], string='State', default='draft')
    description = fields.Text(string='Description')

    # Constraints
    _sql_constraints = [
        ('unique_pret_id_date_avenant', 'unique(pret_id, date_avenant)', 'An avenant with the same date already exists for this loan agreement.')
    ]

    # Compute fields
    @api.depends('montant', 'taux_interet')
    def compute_interet(self):
        for avenant in self:
            avenant.interet = avenant.montant * avenant.taux_interet / 100

    interet = fields.Float(string='Interest', compute='compute_interet')

    # Onchange methods
    @api.onchange('pret_id')
    def onchange_pret_id(self):
        if self.pret_id:
            self.montant = self.pret_id.montant

    # Action methods
    def action_approve(self):
        self.state = 'approved'

    def action_refuse(self):
        self.state = 'refused'

    # Validation methods
    @api.constrains('date_avenant')
    def check_date_avenant(self):
        for avenant in self:
            if avenant.date_avenant < avenant.pret_id.date_pret:
                raise ValidationError('The date of amendment cannot be before the date of the loan agreement.')