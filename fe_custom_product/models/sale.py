from odoo import models, fields, api, _

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    fe_product_categ = fields.Selection( 
        string=_('FE Product Category'),
        related='product_id.fe_product_categ',
    )
    

    fe_product_type = fields.Selection(
        string=_('FE type de produit'),
        related='product_id.fe_product_type',
    )

    largeur_rideau = fields.Float(
        string=_('Largeur rideau en (m)'),
    )

    hauteur_rideau = fields.Float(
        string=_('Hauteur rideau en (m)'),
        default=2.8,
    )

    longueur_table = fields.Float(
        string=_('Longueur table en (cm)'),
    )

    largeur_table = fields.Float(
        string=_('Largeur table en (cm)'),
    )

    longueur_linge = fields.Float(
        string=_('Longueur linge en (cm)'),
    )

    largeur_linge = fields.Float(
        string=_('Largeur linge en (cm)'),
    )

    chute_nappe = fields.Float(
        string=_('Chute nappe en (cm)'),
        default=25,
    )

    

    longueur_meuble = fields.Float(
        string=_('Hauteur linge en (cm)'),
    )

    largeur_meuble = fields.Float(
        string=_('Largeur linge en (cm)'),
    )

    laize = fields.Float(
        string=_('Laize'),
        related='tissu_id.laize',
    )

    tissu_id = fields.Many2one(
        comodel_name='product.product',
        string=_('Tissu'),
        domain=[('fe_component_categ', '=', 'tissu')],
    )

    tringle_id = fields.Many2one(
        comodel_name='product.template',
        string=_('Tringle'),
        domain=[('fe_component_categ', '=', 'tringle')],
    )
    
    pose_id = fields.Many2one(
        comodel_name='product.template',
        string=_('Pose'),
        domain=[('fe_component_categ', '=', 'pose')],
    )

    facon_id = fields.Many2one(
        comodel_name='product.template',
        string=_('Confection'),
        domain=[('fe_component_categ', '=', 'facon')],
    )

    rideau_style = fields.Selection([
            ('wave', _('Wave')),
            ('plis_plats', _('Plis plats')),
            ('plis_simples', _('Plis simples')),
            ('plis_americains', _('Plis américains')),
        ], 
        string=_('Style de rideau')
    )

    simple_paire = fields.Selection([
            ('simple', _('Simple')),
            ('paire', _('Paire')),
            ('overlap', _('Paire Overlap')),
        ],
        string=_('Simple ou paire'),
        default='paire',
    )

    def action_open_order_line_form(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Edit Sale Order Line'),
            'res_model': 'sale.order.line',
            'view_mode': 'form',
            'views': [(self.env.ref('fe_custom_product.view_sale_order_line_form_custom').id, 'form')],
            'res_id': self.id,
            'target': 'new',
        }

    @api.depends('tissu_id', 'rideau_style', 'tringle_id', 'pose_id', 'simple_paire','largeur_rideau', 'hauteur_rideau')
    def _compute_name(self):
        for line in self:
            if line.fe_product_categ == 'rideau':
                line.name = _('Rideaux {}, {}, {}, {}, {}, {}m x {}m').format(
                    line.simple_paire or _('N/A'),
                    line.tissu_id.name or _('N/A'),
                    line.rideau_style or _('N/A'),
                    line.tringle_id.name or _('N/A'),
                    line.pose_id.name or "",
                    line.largeur_rideau or 0,
                    line.hauteur_rideau or 0,
                ).upper()


            elif line.fe_product_categ == 'linge_de_table':
                line.name = _('Linge de table - Largeur: {}m, Hauteur: {}m').format(
                    line.largeur_rideau or 0,
                    line.hauteur_rideau or 0
                )
            elif line.fe_product_categ == 'mobilier':
                line.name = _('Mobilier - Tringle: {}').format(
                    line.tringle_id.name or _('N/A')
                )
            else:
                line.name = _('Produit non spécifié')


    panel_nbr = fields.Integer(
        string='Nombre de panneaux',
        help='Nombre de panneaux nécessaires',
        compute='_compute_panel_nbr',
    )

    usr_panel_nbr = fields.Integer(
        string='Nombre de panneaux utilisateur',
        help='Nombre de panneaux nécessaires',
    )

    usr_ampleur_rideau = fields.Float(
        string='Ampleur rideau',
        help='Ampleur du rideau',
        compute='_compute_panel_nbr',
    )

    largeur_tissu = fields.Float(
        string='Largeur tissu',
        help='Largeur du tissu',
        compute='_compute_panel_nbr',
    )    
    
    ampleur_rideau = fields.Float(
        string='Ampleur rideau',
        help='Ampleur du rideau',
        compute='_compute_panel_nbr',
    )


    @api.onchange('largeur_rideau','laize')
    @api.depends('largeur_rideau','laize')
    def _compute_panel_nbr(self):
        """Calcul du nombre de panneaux."""
        for line in self:
            if line.laize != 0:
                nbr_panneaux = (line.largeur_rideau * 1.8) / line.laize 
                line.panel_nbr = round(nbr_panneaux)
                line.usr_panel_nbr = round(nbr_panneaux)
                # Calculer la largeur totale du tissu
                line.largeur_tissu = line.panel_nbr * line.laize
                if line.largeur_rideau != 0:
                    line.ampleur_rideau = line.largeur_tissu / line.largeur_rideau
                    line.usr_ampleur_rideau = line.usr_panel_nbr * line.laize / line.largeur_rideau
                else:
                    line.ampleur_rideau = 0
                    line.usr_ampleur_rideau = 0
                if line.fe_product_categ == 'rideau':
                    line.price_unit = self._calculate_price_rideau()
                elif line.fe_product_categ == 'linge_de_table':
                    line.price_unit = self._calculate_price_linge_de_table()
                elif line.fe_product_categ == 'mobilier':
                    line.price_unit = self._calculate_price_mobilier()
            else:
                line.panel_nbr = 0
                line.largeur_tissu = 0
                line.ampleur_rideau = 0



    def _calculate_price_rideau(self):
        """Calcul du prix pour les rideaux."""
        for line in self:
            panel_nbr = line.usr_panel_nbr or line.panel_nbr
            prix_tissu = panel_nbr * (line.hauteur_rideau + 0.3) * line.tissu_id.list_price
            prix_tringle = line.tringle_id.list_price * line.largeur_rideau
            prix_pose = line.pose_id.list_price 
            prix_total = prix_tissu + prix_tringle + prix_pose
            return prix_total


        return self.laize * 10  # Exemple : prix basé sur la largeur

    def _calculate_price_linge_de_table(self):
        """Calcul du prix pour le linge de table."""
        return 50  # Exemple : prix fixe

    def _calculate_price_mobilier(self):
        """Calcul du prix pour le mobilier."""
        return self.laize * 20 + 100  # Exemple : formule spécifique