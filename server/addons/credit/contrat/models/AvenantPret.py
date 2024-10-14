from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AvenantPret(models.Model):
    _name = 'avenant.pret'
    _description = 'Avenant de Prêt'

    name = fields.Char(string='Numéro d\'Avenant', required=True, readonly=True, default='New')
    pret_id = fields.Many2one('pret', string='Prêt associé', required=True)
    objet_avenant = fields.Char(string='Objet de l\'avenant', required=True)
    date_avenant = fields.Date(string='Date de l\'avenant', default=fields.Date.today)
    montant = fields.Float(string='Montant', required=True)
    taux_interet = fields.Float(string='Taux d\'Intérêt', required=True)
    penalite = fields.Float(string='Pénalité')
    commission_gestion = fields.Float(string='Commission de Gestion')
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('signed', 'Signé'),
        ('valide', 'Validé'),
        ('enreg', 'Enregistré'),
        ('done', 'Terminé'),
    ], default='draft', string="État")

    @api.model
    def create(self, vals):
        """Override the create method to handle changes to the related loan."""
        avenant = super(AvenantPret, self).create(vals)

        # Update the associated loan (pret) with the new values
        if avenant.pret_id:
            avenant.pret_id.write({
                'montant': avenant.montant,
                'taux_interet': avenant.taux_interet,
                'penalite': avenant.penalite,
                'commission_gestion': avenant.commission_gestion,
                # You can add more fields here if needed
            })

        return avenant

    def action_signed(self):
        """Mark the amendment as signed."""
        self.write({'state': 'signed'})

    def action_validate(self):
        """Mark the amendment as validated and update the associated loan."""
        self.write({'state': 'valide'})

        # Update the associated loan fields as needed
        if self.pret_id:
            self.pret_id.update_from_avenant(self)  # Call the method to update loan fields

    def action_register(self):
        """Register the amendment."""
        self.write({'state': 'enreg'})

    def action_done(self):
        """Complete the amendment process."""
        self.write({'state': 'done'})

def action_show_avenants(self):
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