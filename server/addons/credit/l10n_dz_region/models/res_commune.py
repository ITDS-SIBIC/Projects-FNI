# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2016  - Osis - www.osis-dz.net

from odoo import fields, models, api
from odoo.osv import expression


class ResCommune(models.Model):
    _name = 'res.commune'
    _description = 'Commune'
    _order = 'name,id'

    name = fields.Char(string='Commune', size=64, required=True)
    code = fields.Char(string='Code commune', size=2, help='Le code de la commune sur deux positions', required=True)
    state_id = fields.Many2one('res.country.state', string='Wilaya', required=True)
    wcode = fields.Char(related='state_id.code', readonly=True)

    # @api.model
    # def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
    #     args = args or []
    #     if self.env.context.get('state_id'):
    #         args = expression.AND([args, [('state_id', '=', self.env.context.get('state_id'))]])
    #
    #     if operator == 'ilike' and not (name or '').strip():
    #         first_domain = []
    #         domain = []
    #     else:
    #         first_domain = [('wcode', '=ilike', name)]
    #         domain = [('name', operator, name)]
    #
    #     first_com_ids = self._search(expression.AND([first_domain, args]), limit=limit, access_rights_uid=name_get_uid) if first_domain else []
    #     com_ids = first_com_ids + [commune_id for commune_id in self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid) if not commune_id in first_com_ids]
    #     return models.lazy_name_get(self.browse(com_ids).with_user(name_get_uid))
    #
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "{} ({})".format(record.name, record.state_id.code)))
        return result


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _algeria(self):
        return self.env.ref('base.dz').id

    def _alger(self):
        return self.env.ref('l10n_dz_region.16').id

    commune_id = fields.Many2one('res.commune', string='Commune', domain="[('state_id', '=?', state_id)]")
    state_id = fields.Many2one("res.country.state", string='Wilaya', ondelete='restrict', default=_alger, domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Pays', ondelete='restrict', default=_algeria)

    @api.onchange('commune_id')
    def commune_id_change(self):
        for partner in self:
            partner.state_id = partner.commune_id.state_id.id
            partner.city = partner.commune_id.name
            partner.country_id = partner.commune_id.state_id.country_id.id
