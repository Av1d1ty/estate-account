from odoo import models, exceptions, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        if not journal:
            raise exceptions.UserError(
                ('Please define an accounting sales journal for the company %s (%s).')
                % (self.company_id.name, self.company_id.id))

        for prop in self:
            print('-----------------------')
            print(prop.buyer_id)
            print(prop.buyer_id.id)
            self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': prop.buyer_id.id,  # it's actually a recordset: res.partner(31,)
                'journal_id': journal.id,  # company comes from the journal
                'line_ids': [
                    Command.create({
                        'name': prop.name,
                        'quantity': 1,
                        'price_unit': prop.selling_price,
                    }),
                    Command.create({
                        'name': 'Administrative fees',
                        'quantity': 1,
                        'price_unit': prop.selling_price * 0.06 + 100,
                    }),
                ],
            })

        return super().action_sold()
