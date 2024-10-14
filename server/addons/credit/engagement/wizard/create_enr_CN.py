from odoo import api, fields, models, _
from odoo.tools.mail import is_html_empty


class CreateAvenant2Wizard(models.TransientModel):
    _name = 'create.avenantc2.wizard'
    _description = 'Enregistrement'

    convention_id = fields.Many2one('convention', string='Convention initial', readonly=True)
    partner_id = fields.Many2one(related='convention_id.partner_id', string='Client')
    date_enregistrement = fields.Date('Date')
    objet = fields.Char('Objet')
    user_id = fields.Many2one('res.users', string='Responsable', default=lambda self: self.env.user)
    num_enregistrement = fields.Char('Numéro d\'enregistrement')

    def action_appliquer(self):
        # Update the convention with the new information

        return {
            'name': _(u'Nouvel avenant'),
            'type': 'ir.actions.act_window',
            'res_model': 'convention',
            'view_mode': 'form',
            'view_id': self.env.ref('engagement.convention_form_view').id,
            'target': 'current',
            'res_id': self.convention_id.id,
        }