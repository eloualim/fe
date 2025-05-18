from odoo import models, fields, api, _


class FeAddSectionWizard(models.TransientModel):
    _name = 'fe.add.section.wizard'
    _description = _('Fe Add Section Wizard')
    

    piece = fields.Char(string=_('Point de vente'))

    windows_nbr = fields.Integer(
        string=_('Nombre de fenêtres'),
        default=1,
        required=True,
        help=_('Nombre de fenêtres à ajouter'),
    )

    rideau1 = fields.Many2one(
        string=_('Tissu1'),
        comodel_name='product.template',
        domain=[('fe_component_categ', '=', 'tissu')],
    )

    rideau2 = fields.Many2one(
        string=_('Tissu1'),
        comodel_name='product.template',
        domain=[('fe_component_categ', '=', 'tissu')],
    )

