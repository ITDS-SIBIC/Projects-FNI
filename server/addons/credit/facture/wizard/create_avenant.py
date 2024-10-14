# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from markupsafe import Markup
from odoo import api, fields, models, _
from odoo.tools.mail import is_html_empty


class CreateAvenantWizard(models.TransientModel):
    _name = 'create.avenant.wizard'
    _description = u'Création avenant'

    contrat_id = fields.Many2one('contrat', string='Contrat initial', readonly=True)
    partner_id = fields.Many2one(related='contrat_id.partner_id', string='Client')
    date_avenant = fields.Date('Date')
    objet = fields.Char('Objet')
    user_id = fields.Many2one('res.users', string='Responsable', default=lambda self: self.env.user)

    def action_appliquer(self):
        # dupliquer
        avenant = self.contrat_id.copy()
        # archiver
        self.contrat_id.action_archiver()

        # modifier les champs de l'avenant
        avenant.objet_contrat = self.objet
        avenant.user_id = self.user_id.id
        avenant.date = self.date_avenant
        avenant.type_contrat = 'avenant'
        avenant.state = 'draft'
        avenant.parent_id = self.contrat_id.id
        if self.contrat_id.num_avenant:
            avenant.num_avenant = str(int(self.contrat_id.num_avenant) + 1)
        else:
            avenant.num_avenant = '1'
        avenant.name += '/' + avenant.num_avenant

        return {
            'name': _(u'Nouvel avenant'),
            'type': 'ir.actions.act_window',
            'res_model': 'contrat',
            'view_mode': 'form',
            'view_id': self.env.ref('contrat.contrat_form_view').id,
            'target': 'current',
            'res_id': avenant.id,
        }