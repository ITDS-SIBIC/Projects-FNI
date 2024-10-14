# Copyright 2017 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class Convention(models.Model):
    _name = "convention"
    _inherit = ["convention", "tier.validation"]
    _state_from = ["signed"]
    _state_to = ["valide", "enreg", "done"]

    _tier_validation_manual_config = False
