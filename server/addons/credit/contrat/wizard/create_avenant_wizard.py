from odoo import models, fields, api, _


class CreateAvenantWizard(models.TransientModel):
    _name = 'create.avenant.pret.wizard'
    _description = 'Create Avenant for Pret'

    pret_id = fields.Many2one('pret', string='Prêt', required=True)
    objet_avenant = fields.Char('Objet de l\'avenant', required=True)
    date_avenant = fields.Date('Date de l\'avenant', default=fields.Date.today())
    montant = fields.Float('Montant', required=True)
    taux_interet = fields.Float('Taux d\'Intérêt')
    penalite = fields.Float('Pénalité')

    def action_create_avenant(self):
        """Creates an Avenant from the wizard input."""
        avenant_vals = {
            'name': self.env['ir.sequence'].next_by_code('pret.engagement'),
            'objet_contrat': self.objet_avenant,
            'date': self.date_avenant,
            'montant': self.montant,
            'taux_interet': self.taux_interet,
            'penalite': self.penalite,
            'type_contrat': 'avenant',
            'parent_id': self.pret_id.id,
        }

        # Create the new Avenant
        self.env['pret'].create(avenant_vals)

        return {
            'type': 'ir.actions.act_window_close',
        }
