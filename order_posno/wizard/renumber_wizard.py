# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class RenumberWizard(models.TransientModel):
    _name = 'order.posno.renumber.wizard'
    _description = 'Positionen neu nummerieren'

    action_type = fields.Selection([
        ('renumber', 'Neu nummerieren (von ausgewählten Positionen)'),
        ('renumber_all', 'Alle Positionen des Auftrags neu nummerieren'),
        ('move_front', 'Ausgewählte nach vorne verschieben'),
        ('move_back', 'Ausgewählte nach hinten verschieben'),
    ], string='Aktion', required=True, default='renumber')

    start_number = fields.Float(
        string='Start-Nummer',
        default=10.0,
        digits=(8, 3),
        help='Startwert für die Neunummerierung'
    )

    increment = fields.Float(
        string='Schrittweite',
        digits=(8, 3),
        help='Inkrement zwischen den Positionen'
    )
    
    avoid_duplicates = fields.Boolean(
        string='Duplikate automatisch verschieben',
        default=True,
        help='Verschiebt automatisch Positionen nach hinten, die eine bereits vergebene Nummer bekommen würden'
    )

    @api.model
    def default_get(self, fields_list):
        """Setze Standard-Schrittweite aus Konfiguration"""
        res = super(RenumberWizard, self).default_get(fields_list)
        if 'increment' in fields_list:
            increment = self.env['ir.config_parameter'].sudo().get_param('order_posno.default_increment', '10.0')
            res['increment'] = float(increment)
        return res

    def action_apply(self):
        """Führt die ausgewählte Aktion aus"""
        self.ensure_one()
        
        # Hole die ausgewählten Zeilen aus dem Kontext
        active_ids = self.env.context.get('active_ids', [])
        if not active_ids:
            raise UserError(_('Bitte wählen Sie mindestens eine Position aus.'))
        
        lines = self.env['sale.order.line'].browse(active_ids)
        
        # Prüfe ob alle Zeilen zum selben Auftrag gehören
        orders = lines.mapped('order_id')
        if len(orders) > 1:
            raise UserError(_('Alle ausgewählten Positionen müssen zum selben Auftrag gehören.'))
        
        order = orders[0]
        
        if self.action_type == 'renumber':
            self._renumber_lines(lines, order)
        elif self.action_type == 'renumber_all':
            self._renumber_all_lines(order)
        elif self.action_type == 'move_front':
            self._move_to_front(lines, order)
        elif self.action_type == 'move_back':
            self._move_to_back(lines, order)
        
        return {'type': 'ir.actions.act_window_close'}

    def _renumber_lines(self, lines, order):
        """Nummeriert die ausgewählten Zeilen neu und verschiebt Duplikate"""
        # Sortiere nach aktueller Positionsnummer
        sorted_lines = lines.sorted('positionno')
        
        if self.avoid_duplicates:
            # Hole alle anderen Zeilen des Auftrags
            other_lines = order.order_line.filtered(lambda l: l.id not in lines.ids)
            used_numbers = set(other_lines.mapped('positionno'))
            
            # Neue Nummern zuweisen
            new_assignments = {}
            current_number = self.start_number
            
            for line in sorted_lines:
                # Finde nächste freie Nummer
                while current_number in used_numbers:
                    current_number += self.increment
                
                new_assignments[line.id] = current_number
                used_numbers.add(current_number)
                current_number += self.increment
            
            # Wende Nummern an
            for line in sorted_lines:
                line.positionno = new_assignments[line.id]
        else:
            # Einfache Neunummerierung ohne Duplikat-Check
            current_number = self.start_number
            for line in sorted_lines:
                line.positionno = current_number
                current_number += self.increment

    def _renumber_all_lines(self, order):
        """Nummeriert alle Zeilen des Auftrags neu"""
        all_lines = order.order_line.sorted('positionno')
        
        current_number = self.start_number
        for line in all_lines:
            line.positionno = current_number
            current_number += self.increment

    def _move_to_front(self, lines, order):
        """Verschiebt die Zeilen nach vorne"""
        # Hole alle Zeilen des Auftrags außer den ausgewählten
        other_lines = order.order_line.filtered(lambda l: l.id not in lines.ids)
        
        if not other_lines:
            # Nur die ausgewählten Zeilen vorhanden
            self._renumber_lines(lines, order)
            return
        
        # Finde die kleinste Positionsnummer der anderen Zeilen
        min_pos = min(other_lines.mapped('positionno'))
        
        # Berechne neue Positionen für die zu verschiebenden Zeilen
        sorted_lines = lines.sorted('positionno')
        
        # Starte vor der kleinsten Position
        current_pos = min_pos - (len(sorted_lines) * self.increment)
        
        for line in sorted_lines:
            line.positionno = current_pos
            current_pos += self.increment

    def _move_to_back(self, lines, order):
        """Verschiebt die Zeilen nach hinten"""
        # Hole alle Zeilen des Auftrags außer den ausgewählten
        other_lines = order.order_line.filtered(lambda l: l.id not in lines.ids)
        
        if not other_lines:
            # Nur die ausgewählten Zeilen vorhanden
            self._renumber_lines(lines, order)
            return
        
        # Finde die größte Positionsnummer der anderen Zeilen
        max_pos = max(other_lines.mapped('positionno'))
        
        # Berechne neue Positionen für die zu verschiebenden Zeilen
        sorted_lines = lines.sorted('positionno')
        
        # Starte nach der größten Position
        current_pos = max_pos + self.increment
        
        for line in sorted_lines:
            line.positionno = current_pos
            current_pos += self.increment
