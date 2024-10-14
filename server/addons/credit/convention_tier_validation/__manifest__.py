# Copyright 2017 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Convention Tier Validation",
    "summary": "Extends the functionality of Convention/engagement Orders to "
    "support a tier validation process.",
    "version": "17.0.1.0.0",
    "category": "Engagement",
    "website": "https://github.com/OCA/purchase-workflow",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["engagement", "base_tier_validation"],
    "data": ["views/convention_view.xml"],
}
