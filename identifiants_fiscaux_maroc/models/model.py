
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    rc = fields.Char(string='R.C.')
    tp = fields.Char(string='T.P.')
    iff = fields.Char(string='I.F.')
    cnss = fields.Char(string='C.N.S.S.')
    ice = fields.Char(string='I.C.E.')
    capital = fields.Char(string='Capital')
    cin = fields.Char(string='CIN')
    
    @api.constrains('ice')
    def _check_company_ice(self):
        for record in self:
            if record.country_code == 'MA' and record.ice and (len(record.ice) != 15 or not record.ice.isdigit()):
                raise ValidationError(_("ICE number should have exactly 15 digits."))



class ResCompany(models.Model):
    _inherit = 'res.company'

    rc = fields.Char(string='R.C.')
    tp = fields.Char(string='T.P.')
    iff = fields.Char(string='I.F.')
    cnss = fields.Char(string='C.N.S.S.')
    ice = fields.Char(string='I.C.E.')
    capital = fields.Char(string='Capital')

    
    @api.constrains('ice')
    def _check_company_ice(self):
        for record in self:
            if record.country_code == 'MA' and record.ice and (len(record.ice) != 15 or not record.ice.isdigit()):
                raise ValidationError(_("ICE number should have exactly 15 digits."))

