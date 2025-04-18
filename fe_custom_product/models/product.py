from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = _('Product Template')
    

    fe_product_categ = fields.Selection([
        ('rideau', _('Rideaux')),
        ('linge_de_table', _('Linge de table')),
        ('mobilier', _('Mobilier')),
    ], string=_('FE Product Type'))
    
    fe_component_categ = fields.Selection([
        ('tissu', _('Tissu')),
        ('tringle', _('Tringle')),
        ('facon', _('Façon')),
        ('accessoire', _('Accessoire')),
        ('pose', _('Pose')),
    ], string=_('FE component category'))
    
    custom_product = fields.Boolean(
        string=_('Custom Product'),
        compute='_compute_component_product',
        store=True,
    )
    component_product = fields.Boolean(
        string=_('Component Product'),
        compute='_compute_component_product',
        store=True,
    )

    @api.depends('fe_product_type')
    def _compute_component_product(self):
        for record in self:
            record.component_product = record.fe_product_type == 'component_product'
            record.custom_product = record.fe_product_type == 'custom_product'

    fe_product_type = fields.Selection(
        string=_('FE type de produit'),
        selection=[
            ('normal_product', 'Normal Product'),
            ('custom_product', 'Custom Product'),
            ('component_product', 'Component Product'),
        ],
        default='normal_product',
    )

    laize = fields.Float(
        string=_('Laize'),
    )

