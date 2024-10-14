# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from markupsafe import Markup
from odoo import api, fields, models, _
from odoo.tools.mail import is_html_empty


class CreateAvenantWizard(models.TransientModel):
    _name = 'create.avenantc.wizard'
    _description = u'Création avenant'

    convention_id = fields.Many2one('convention', string='Convention initial', readonly=True)
    partner_id = fields.Many2one(related='convention_id.partner_id', string='Client')
    date_avenant = fields.Date('Date')
    objet = fields.Char('Objet')
    user_id = fields.Many2one('res.users', string='Responsable', default=lambda self: self.env.user)

    def action_appliquer(self):
        # dupliquer
        avenant = self.convention_id.copy()
        # archiver
        self.convention_id.action_archiver()
        self.convention_id.write({})
        # modifier les champs de l'avenant0000
        avenant.objet_avenant = self.objet
        avenant.user_id = self.user_id.id
        avenant.date = self.date_avenant
        avenant.type_convention= 'avenant'
        avenant.state = 'draft'
        avenant.parent_id = self.convention_id.id
        if self.convention_id.num_avenantcn:
            avenant.num_avenantcn = str(int(self.convention_id.num_avenantcn) + 1)
        else:
            avenant.num_avenantcn = '1'
        avenant.name += '/' + avenant.num_avenantcn

        return {
            'name': _(u'Nouvel avenant'),
            'type': 'ir.actions.act_window',
            'res_model': 'convention',
            'view_mode': 'form',
           'view_id': self.env.ref('engagement.convention_form_view').id,
            'target': 'current',
            'res_id': avenant.id,
        }
