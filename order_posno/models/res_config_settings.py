# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    posno_increment = fields.Float(
        string='Standard-Schrittweite für Positionsnummern',
        default=10.0,
        digits=(8, 3),
        help='Standard-Schrittweite für die automatische Nummerierung von Auftragspositionen (z.B. 1, 10, 100, 0.1, 20)'
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            posno_increment=float(params.get_param('order_posno.default_increment', 10.0))
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        params = self.env['ir.config_parameter'].sudo()
        params.set_param('order_posno.default_increment', self.posno_increment)
