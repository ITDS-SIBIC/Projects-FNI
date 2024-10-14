from odoo import  fields, api, models, modules
from datetime import datetime
from odoo.exceptions import UserError


class Client(models.Model):
    _inherit = 'res.partner'

    numero = fields.Char(u'Numéro client', readonly=True)
    client = fields.Boolean('est un client')
    type_client = fields.Selection([('tier', 'Tier'), ('partiel', 'Partiel'), ('total', 'Total')], string=u'Type crédit', default='tier')
    nif = fields.Char('NIF', copy=False)
    nis = fields.Char('NIS', copy=False)


    @api.model
    def create(self, vals):
        vals['numero'] = self.env['ir.sequence'].get('client.engagement')
        return super(Client, self).create(vals)
