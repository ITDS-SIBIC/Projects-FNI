# -*- coding: utf-8 -*-
from odoo import models, fields

class Emprunt(models.Model):
    _name = 'emprunt'
    _inherit = 'convention'  # Inherit from the 'convention' model of the 'engagement' module
    _description = 'Emprunt'

    # Adding new fields or overriding existing fields
    loan_type = fields.Selection([
        ('short_term', 'Short Term'),
        ('long_term', 'Long Term'),
    ], string='Loan Type', required=True, default='short_term')

    # Example method to perform a specific action
    def action_mark_as_closed(self):
        self.write({'state': 'closed'})
