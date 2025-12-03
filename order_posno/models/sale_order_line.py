# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    _order = 'order_id, positionno, id'

    positionno = fields.Float(
        string='Position Nr.',
        required=True,
        default=10.0,
        digits=(8, 3),
        copy=False,
        help='Positionsnummer für diese Zeile (erlaubt Dezimalwerte für flexible Sortierung)'
    )

    @api.model_create_multi
    def create(self, vals_list):
        """Automatische Vergabe von Positionsnummern beim Erstellen"""
        # Hole die konfigurierte Standard-Schrittweite
        increment = float(self.env['ir.config_parameter'].sudo().get_param('order_posno.default_increment', 10.0))
        
        for vals in vals_list:
            if 'order_id' in vals and ('positionno' not in vals or vals.get('positionno') == 10.0):
                # Finde die höchste vorhandene Positionsnummer für diesen Auftrag
                order_id = vals['order_id']
                existing_lines = self.search([('order_id', '=', order_id)], order='positionno desc', limit=1)
                if existing_lines:
                    vals['positionno'] = existing_lines.positionno + increment
                else:
                    vals['positionno'] = increment
        return super(SaleOrderLine, self).create(vals_list)

    @api.constrains('positionno', 'order_id')
    def _check_positionno_positive(self):
        """Stelle sicher, dass die Positionsnummer positiv ist"""
        for line in self:
            if line.positionno <= 0:
                raise ValidationError('Die Positionsnummer muss größer als 0 sein!')

    def write(self, vals):
        """Bei Änderung der Sequence durch Drag & Drop, aktualisiere positionno"""
        # Speichere alte sequence-Werte vor dem Update
        old_sequences = {line.id: line.sequence for line in self} if 'sequence' in vals else {}
        
        result = super(SaleOrderLine, self).write(vals)
        
        # Wenn sequence geändert wurde (durch Drag & Drop), aktualisiere positionno
        if 'sequence' in vals and old_sequences:
            # Prüfe ob sich die Sequence tatsächlich geändert hat
            changed = any(self.browse(lid).sequence != old_seq for lid, old_seq in old_sequences.items())
            
            if changed:
                increment = float(self.env['ir.config_parameter'].sudo().get_param('order_posno.default_increment', 10.0))
                
                for order in self.mapped('order_id'):
                    # Hole alle Zeilen des Auftrags, sortiert nach sequence und id
                    lines = order.order_line.sorted(lambda l: (l.sequence, l.id))
                    
                    # Nummeriere basierend auf sequence neu
                    current_pos = increment
                    for line in lines:
                        if abs(line.positionno - current_pos) > 0.001:  # Float-Vergleich
                            # Verwende SQL UPDATE um Rekursion zu vermeiden
                            self.env.cr.execute(
                                "UPDATE sale_order_line SET positionno = %s WHERE id = %s",
                                (current_pos, line.id)
                            )
                        current_pos += increment
                    
                    # Invalidiere Cache
                    self.env['sale.order.line'].invalidate_model(['positionno'])
        
        return result

    def action_quick_renumber(self):
        """Schnelles Neunummerieren der ausgewählten Zeilen mit 10er-Schritten"""
        if not self:
            return
        
        orders = self.mapped('order_id')
        if len(orders) > 1:
            raise ValidationError('Alle ausgewählten Positionen müssen zum selben Auftrag gehören.')
        
        sorted_lines = self.sorted('positionno')
        current_number = 10.0
        for line in sorted_lines:
            line.positionno = current_number
            current_number += 10.0

    def action_move_to_front(self):
        """Verschiebt die ausgewählten Zeilen nach vorne"""
        if not self:
            return
        
        orders = self.mapped('order_id')
        if len(orders) > 1:
            raise ValidationError('Alle ausgewählten Positionen müssen zum selben Auftrag gehören.')
        
        order = orders[0]
        other_lines = order.order_line.filtered(lambda l: l.id not in self.ids)
        
        if other_lines:
            min_pos = min(other_lines.mapped('positionno'))
            sorted_lines = self.sorted('positionno')
            current_pos = min_pos - (len(sorted_lines) * 10.0)
            
            for line in sorted_lines:
                line.positionno = current_pos
                current_pos += 10.0

    def action_move_to_back(self):
        """Verschiebt die ausgewählten Zeilen nach hinten"""
        if not self:
            return
        
        orders = self.mapped('order_id')
        if len(orders) > 1:
            raise ValidationError('Alle ausgewählten Positionen müssen zum selben Auftrag gehören.')
        
        order = orders[0]
        other_lines = order.order_line.filtered(lambda l: l.id not in self.ids)
        
        if other_lines:
            max_pos = max(other_lines.mapped('positionno'))
            sorted_lines = self.sorted('positionno')
            current_pos = max_pos + 10.0
            
            for line in sorted_lines:
                line.positionno = current_pos
                current_pos += 10.0
