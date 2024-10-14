from odoo import models, fields, api, _

class CreateAvenantPretWizard(models.TransientModel):
    _name = 'create.avenant.wizard'  # Ensure this name matches exactly
    _description = 'Create Avenant Wizard'

    pret_id = fields.Many2one('pret', string='Prêt initial', readonly=True)
    partner_id = fields.Many2one(related='pret_id.partner_id', string='Client', readonly=True)
    date_avenant = fields.Date('Date', default=fields.Date.context_today)
    objet = fields.Char('Objet')
    user_id = fields.Many2one('res.users', string='Responsable', default=lambda self: self.env.user)

    @api.model
    def _register(self, cr):
        """Override to include any custom logic during model registration if necessary."""
        super(CreateAvenantWizard, self)._register(cr)

        # Custom logic could be placed here if needed
        # For instance, you could dynamically create records or setup configurations
        # Example: Ensure certain records exist in the database
        # self.env['some.model'].create({'name': 'Default Record'}
    def action_create_avenant(self):
        avenant = self.pret_id.copy()
        self.pret_id.action_archiver()

        avenant.update({
            'objet_avenant': self.objet,
            'user_id': self.user_id.id,
            'date': self.date_avenant,
            'type_contrat': 'avenant',
            'state': 'draft',
            'parent_id': self.pret_id.id,
        })

        if self.pret_id.num_avenant:
            avenant.num_avenant = str(int(self.pret_id.num_avenant) + 1)
        else:
            avenant.num_avenant = '1'

        avenant.name += '/' + avenant.num_avenant

        return {
            'name': _('Nouvel avenant'),
            'type': 'ir.actions.act_window',
            'res_model': 'pret',
            'view_mode': 'form',
            'res_id': avenant.id,
        }
