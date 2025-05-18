from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = _('Product Template')
    

    fe_product_categ = fields.Selection([
        ('rideau', _('Rideaux')),
        ('linge_de_table', _('Linge de table')),
        ('linge_de_lit', _('Linge de lit')),
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

    fe_confection_config_line_ids = fields.One2many(
        string=_('FE config confection line'),
        comodel_name='fe.confection.line',
        inverse_name='product_id',
    )


class FeConfectionType(models.Model):
    _name = 'fe.confection.type'
    _description = _('Fe Confection Type')
    
    name = fields.Char(
        string=_('Name'),
        required=True,
    )


class FeConfectionLine(models.Model):
    _name = 'fe.confection.line'
    _description = _('Fe Confection Line')

    _sql_constraints = [
        ('unique_product_confection_type', 'UNIQUE(product_id, confection_type_id)', 
         _('Ce type de confection existe déjà pour ce produit!'))
    ]
        
    name = fields.Char(
        string=_('Name'),
    )

    confection_type_id = fields.Many2one(
        string=_('Confection_type_id'),
        comodel_name='fe.confection.type',
    )

    conso_tissu = fields.Float(
        string=_('Consommation tissu'),
        required=True,
    )
    
    conso_facon = fields.Float(
        string=_('Consommation façon'),
        required=True,
    )

    product_id = fields.Many2one(
        string=_('Product'),
        comodel_name='product.template',
    )


    