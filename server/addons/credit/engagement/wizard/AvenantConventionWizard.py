from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AvenantConventionWizard(models.TransientModel):
    _name = 'avenant.convention.wizard'
    _description = 'Wizard to update convention fields'

    convention_id = fields.Many2one('convention', string='Convention', required=True)
    objet = fields.Char(string='Objet du crédit', required=True)
    commission_gestion = fields.Float(string='Commission de Gestion', required=True)
    taux_interet = fields.Float(string='Taux d\'Intérêt', required=True)
    penalite = fields.Float(string='Pénalité', required=True)
    montant = fields.Float(string='Montant', required=True)
    # Add more fields as necessary...

    def action_update_convention(self):
        """Update the convention record with the wizard's values."""
        self.ensure_one()
        if self.convention_id.state != 'validee':
            raise UserError(_('La convention doit être validée pour effectuer des modifications.'))

        self.convention_id.write({
            'objet': self.objet,
            'commission_gestion': self.commission_gestion,
            'taux_interet': self.taux_interet,
            'penalite': self.penalite,
            'montant': self.montant,
            # Update other fields as necessary
        })
        return {'type': 'ir.actions.act_window_close'}

    def actionavenant(self):
        """Open the avenant wizard to create a new avenant for the convention."""
        self.ensure_one()  # Ensure this method is called on a single record
        if self.state != 'validee':
            raise UserError(_('Vous ne pouvez pas créer un avenant tant que la convention n\'est pas validée.'))

        return {
            'name': _('Créer Avenant'),
            'type': 'ir.actions.act_window',
            'res_model': 'avenant.convention.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_convention_id': self.id,
                'default_objet_avenant': self.objet,  # Pass default values to the wizard
                'default_montant': self.montant,
                # Add any other necessary fields...
            },
        }
