from odoo import models, fields


class DecisionPouvoirPublic(models.Model):
    _name = 'decision.pouvoir.public'
    _description = 'Décisions Pouvoir Public'

    decision_type = fields.Selection([
        ('pm', 'PM'),
        ('cni', 'CNI'),
        ('cim', 'CIM'),
        ('cpe', 'CPE'),
        ('autre', 'Autre')
    ], string='Décision', required=True)

    reference = fields.Char(string='Référence')
    date = fields.Date(string='Date')
    convention_id = fields.Many2one('convention', string='Convention', inverse_name='decision_ids')
    # ... other fields...

    

    # Champ Many2one vers le modèle convention

    # Champ Many2one vers le modèle convention


