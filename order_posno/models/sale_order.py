# -*- coding: utf-8 -*-
from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_view_order_lines(self):
        """Öffnet die Positionen-Ansicht für diesen Auftrag"""
        self.ensure_one()
        
        return {
            'name': 'Positionen',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.line',
            'view_mode': 'list,form',
            'domain': [('order_id', '=', self.id)],
            'context': {
                'default_order_id': self.id,
                'search_default_order_id': self.id,
            },
        }

    def action_renumber_positions(self):
        """Nummeriert alle Positionen basierend auf der aktuellen Reihenfolge neu"""
        self.ensure_one()
        increment = float(self.env['ir.config_parameter'].sudo().get_param('order_posno.default_increment', 10.0))
        
        # Hole alle Zeilen sortiert nach sequence und id
        lines = self.order_line.sorted(lambda l: (l.sequence, l.id))
        
        # Nummeriere neu
        current_pos = increment
        for line in lines:
            # Verwende SQL UPDATE um Rekursion zu vermeiden
            self.env.cr.execute(
                "UPDATE sale_order_line SET positionno = %s WHERE id = %s",
                (current_pos, line.id)
            )
            current_pos += increment
        
        # Invalidiere Cache
        self.env['sale.order.line'].invalidate_model(['positionno'])
        
        return True
