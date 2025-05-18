from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # Champs relatifs aux catégories de produits
    fe_product_categ = fields.Selection( 
        string=_('FE Product Category'),
        related='product_id.fe_product_categ',
    )
    
    fe_product_type = fields.Selection(
        string=_('FE type de produit'),
        related='product_id.fe_product_type',
    )

    # Champs pour les rideaux
    largeur_rideau = fields.Float(
        string=_('Largeur rideau en (m)'),
    )

    hauteur_rideau = fields.Float(
        string=_('Hauteur rideau en (m)'),
        default=2.8,
    )

    ourlet_rideau = fields.Float(
        string=_('Ourlet rideau en (m)'),
    )

    # Champs pour le linge de table
    longueur_linge = fields.Float(
        string=_('Longueur en (cm)'),
    )

    largeur_linge = fields.Float(
        string=_('Largeur en (cm)'),
    )
    
    @api.constrains('longueur_linge', 'largeur_linge')
    def _check_length_greater_than_width(self):
        for record in self:
            if record.longueur_linge < record.largeur_linge:
                raise ValidationError(_("La longueur doit être supérieure à la largeur."))
    
    optim_forced = fields.Boolean(
        string=_('Optimisation forcée'),
        help=_('Forcer l\'optimisation de la consommation de tissu'),
    )

    chute_nappe = fields.Float(
        string=_('Chute en (cm)'),
    )

    ourlet_nappe = fields.Float(
        string=_('Ourlet en (cm)'),
    )

    # Champs pour le mobilier
    longueur_meuble = fields.Float(
        string=_('Longueur meuble en (cm)'),
    )

    largeur_meuble = fields.Float(
        string=_('Largeur meuble en (cm)'),
    )

    # Champs relatifs aux composants
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

    # Configuration des rideaux
    simple_paire = fields.Selection([
            ('simple', _('Simple')),
            ('paire', _('Paire')),
            ('overlap', _('Paire Overlap')),
        ],
        string=_('Simple ou paire'),
        default='paire',
    )

    # Champs calculés pour les rideaux
    panel_nbr = fields.Integer(
        string='Nombre de panneaux',
        help='Nombre de panneaux nécessaires',
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
    usr_panel_nbr = fields.Float(
        string='Nombre de panneaux utilisateur',
        help='Nombre de panneaux nécessaires',
    )

    usr_largeur_tissu = fields.Float(
        string='Ampleur rideau',
        help='Ampleur du rideau',
        compute='_compute_panel_nbr',
    )

    usr_ampleur_rideau = fields.Float(
        string='Ampleur rideau',
        help='Ampleur du rideau',
        compute='_compute_panel_nbr',
    )

    longueur_coupe = fields.Float(
        string='Longueur coupe',
        compute='_compute_panel_nbr',
    )
    
    largeur_coupe = fields.Float(
        string='Largeur coupe',
        compute='_compute_panel_nbr',
    )


    longueur_corrig = fields.Float(
        string='Longueur corrigée',
    )

    largeur_corrig = fields.Float(
        string='Largeur corrigée',
    )

    custom_price_used = fields.Boolean(string='Prix personnalisé utilisé', default=False)
    stored_custom_price = fields.Float(string='Prix personnalisé stocké')
    
    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _compute_price_unit(self):
        for line in self:
            # Sauvegarde du prix personnalisé
            if line.custom_price_used:
                stored_price = line.price_unit
            
            # Appel de la méthode d'origine
            super(SaleOrderLine, line)._compute_price_unit()
            
            # Restauration du prix personnalisé
            if line.custom_price_used:
                line.price_unit = line.stored_custom_price


    def action_open_order_line_form(self):
        """Ouvre le formulaire de modification de la ligne de commande et enregistre le devis."""
        self.ensure_one()
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('Edit Sale Order Line'),
            'res_model': 'sale.order.line',
            'view_mode': 'form',
            'views': [(self.env.ref('fe_custom_product.view_sale_order_line_form_custom').id, 'form')],
            'res_id': self.id,
            'target': 'new',
            'context': {
                'ignore_readonly_fields': True,
                'force_edit': True
            }
        }

    @api.depends('tissu_id', 'facon_id', 'tringle_id', 'pose_id', 'simple_paire','largeur_rideau', 'hauteur_rideau')
    def _compute_name(self):
        """Calcule le nom de la ligne de commande selon le type de produit."""
        for line in self:

            if line.fe_product_categ == 'rideau':
                elements = []
                
                # Ajouter chaque élément à la liste seulement s'il existe
                if line.simple_paire:
                    elements.append(line.simple_paire)
                if line.tissu_id and line.tissu_id.name:
                    elements.append(line.tissu_id.name)
                if line.facon_id and line.facon_id.name:
                    elements.append(line.facon_id.name)
                if line.tringle_id and line.tringle_id.name:
                    elements.append(line.tringle_id.name)
                if line.pose_id and line.pose_id.name:
                    elements.append(line.pose_id.name)
                    
                # Ajouter les dimensions si elles existent
                dimensions = []
                if line.largeur_rideau and line.hauteur_rideau:
                    dimensions.append(f"{line.largeur_rideau:.2f}x{line.hauteur_rideau:.2f}m")
                elif line.largeur_rideau:
                    dimensions.append(f"{line.largeur_rideau:.2f}m de large")
                elif line.hauteur_rideau:
                    dimensions.append(f"{line.hauteur_rideau:.2f}m de haut")
                    
                if dimensions:
                    elements.extend(dimensions)
                    
                # Composer le nom final
                if elements:
                    line.name = (_('Rideaux ') + ', '.join(elements))
                else:
                    line.name = _('Rideaux')








            elif line.fe_product_categ == 'linge_de_table':
                line.name = _('{}, {}, {}x{}cm, {}').format(
                    line.product_id.name or _('N/A'),
                    line.tissu_id.name or _('N/A'),
                    line.longueur_linge or 0,
                    line.largeur_linge or 0,
                    line.facon_id.name or "",
                )
            elif line.fe_product_categ == 'mobilier':
                line.name = _('Mobilier - Tringle: {}').format(
                    line.tringle_id.name or _('N/A')
                )
            else:
                # Utilisation de la méthode originale
                super(SaleOrderLine, line)._compute_name()

    @api.onchange('tissu_id', 'facon_id', 'tringle_id', 'pose_id', 'simple_paire','largeur_rideau', 'hauteur_rideau','usr_panel_nbr','optim_forced','longueur_linge','largeur_linge','chute_nappe','ourlet_nappe','longueur_corrig','largeur_corrig')
    @api.depends('tissu_id', 'facon_id', 'tringle_id', 'pose_id', 'simple_paire','largeur_rideau', 'hauteur_rideau','usr_panel_nbr','optim_forced','longueur_linge','largeur_linge','chute_nappe','ourlet_nappe','longueur_corrig','largeur_corrig')
    def _compute_panel_nbr(self):
        """Calcule le nombre de panneaux et l'ampleur pour les rideaux."""
        for line in self:
            if line.laize != 0:
                nbr_panneaux = (line.largeur_rideau * 1.8) / line.laize 
                line.panel_nbr = round(nbr_panneaux)
                # Calculer la largeur totale du tissu
                line.largeur_tissu = line.panel_nbr * line.laize
                line.usr_largeur_tissu = line.usr_panel_nbr * line.laize
                if line.largeur_rideau != 0 :
                    line.ampleur_rideau = line.largeur_tissu / line.largeur_rideau
                    line.usr_ampleur_rideau = line.usr_largeur_tissu / line.largeur_rideau
                else:
                    line.ampleur_rideau = 0
                    line.usr_ampleur_rideau = 0
                # Mise à jour du prix selon le type de produit
            else:
                
                line.panel_nbr = 0
                line.largeur_tissu = 0
                line.ampleur_rideau = 0
                line.usr_largeur_tissu = 0
                line.usr_ampleur_rideau = 0
            line.longueur_coupe = self.longueur_linge + 2*self.ourlet_nappe + 2 + 2*self.chute_nappe
            line.largeur_coupe = self.largeur_linge + 2*self.ourlet_nappe + 2 + 2*self.chute_nappe
            line._update_price_based_on_category()

    def _update_price_based_on_category(self):
        """Met à jour le prix selon la catégorie de produit."""
        for line in self:
            # Vérifier si la catégorie de produit est définie
            if line.fe_product_categ == 'rideau':
                line.price_unit = self._calculate_total_price('rideau')
            elif line.fe_product_categ == 'linge_de_table':
                line.price_unit = self._calculate_total_price('linge_de_table')
            elif line.fe_product_categ == 'mobilier':
                line.price_unit = self._calculate_total_price('mobilier')

            self.custom_price_used = True
            self.stored_custom_price = line.price_unit


    def _calculate_total_price(self, category_type):
        """
        Calcule le prix total pour une catégorie de produit spécifique.
        Structure unifiée pour tous les types de produits.
        """
        self.ensure_one()
        
        # Initialiser les composants du prix
        prix_tissu = 0
        prix_facon = 0
        prix_tringle = 0
        prix_pose = 0
        prix_autres = 0
        
        # Calculer les différents composants selon la catégorie
        if category_type == 'rideau':
            # Consommation de tissu pour les rideaux
            conso_tissu = self.calculate_conso_tissu('rideau')
            prix_tissu = conso_tissu * self.tissu_id.list_price if self.tissu_id else 0
            
            # Prix de la façon (confection)
            prix_facon = self.calculate_price_facon('rideau')
            
            # Prix de la tringle
            prix_tringle = self.tringle_id.list_price * self.largeur_rideau if self.tringle_id else 0
            
            # Prix de la pose
            prix_pose = self.pose_id.list_price if self.pose_id else 0
            
        elif category_type == 'linge_de_table':
            # Consommation de tissu pour le linge de table
            conso_tissu = self.calculate_conso_tissu('linge_de_table')
            prix_tissu = conso_tissu * self.tissu_id.list_price if self.tissu_id else 0
            
            # Prix de la façon (confection)
            prix_facon = self.calculate_price_facon('linge_de_table')
            
        elif category_type == 'mobilier':
            # Prix de base pour le mobilier
            base_price = self.tringle_id.list_price or 0
            prix_autres = base_price * (self.largeur_meuble / 100) * 1.5 + 100
        

        prix_total = prix_tissu + prix_facon + prix_tringle + prix_pose + prix_autres
        return prix_total

    def calculate_conso_tissu(self, category_type):
        """
        Calcule la consommation de tissu selon le type de produit.
        Méthode unifiée pour tous les types de produits.
        """
        self.ensure_one()
        
        if category_type == 'rideau':
            # Calcul pour les rideaux
            panel_nbr = self.usr_panel_nbr or self.panel_nbr
            # Consommation en m² : nombre de panneaux * (hauteur + marge pour ourlets)
            conso = panel_nbr * (self.hauteur_rideau + 0.3)
            return conso
            
        elif category_type == 'linge_de_table':
            # Calcul pour le linge de table
            # Dimensions réelles avec ourlets et chutes
            longueur_conso = self.longueur_corrig or self.longueur_coupe
            largeur_conso = self.largeur_corrig or self.longueur_coupe
            
            # Vérifier si le linge peut être fait avec la laize disponible
            laize_cm = self.laize * 100  # Conversion de la laize en cm
            if longueur_conso <= laize_cm:
                # Si la largeur du linge tient dans la laize, on utilise juste la longueur
                if self.optim_forced:
                    conso = (longueur_conso * largeur_conso) / (laize_cm * 100)
                else:
                    conso = largeur_conso / 100
            else:
                # Si le linge est plus large que la laize, on calcule combien de laizes sont nécessaires
                if self.laize == 0:
                    nb_laizes = 0
                else:
                    nb_laizes = largeur_conso / laize_cm


                if laize_cm and largeur_conso % laize_cm != 0:
                    nb_laizes = int(nb_laizes) + 1
                else:
                    nb_laizes = 0
                conso = (longueur_conso * nb_laizes) / 100  # Conversion en mètres
                
            return conso
            
        # Pour les autres catégories, retourner 0
        return 0

    def calculate_price_facon(self, category_type):
        """
        Calcule le prix de façon (confection) selon le type de produit.
        Méthode unifiée pour tous les types de produits.
        """
        self.ensure_one()
        
        if not self.facon_id:
            return 0
            
        if category_type == 'rideau':
            # Pour les rideaux, le prix dépend de la largeur
            prix_facon = self.largeur_rideau * self.facon_id.list_price
            return prix_facon
            
        elif category_type == 'linge_de_table':
            # Pour le linge de table, on peut calculer le prix basé sur le périmètre
            perimetre = self.calculate_perimetre_couture(category_type)
            prix_facon = self.facon_id.list_price * perimetre
            # On pourrait ajuster le prix en fonction du périmètre
            # prix_facon = perimetre * coefficient * self.facon_id.list_price
            return prix_facon
            
        # Pour les autres catégories, retourner 0
        return 0

    def calculate_perimetre_couture(self, category_type=None):
        """
        Calcule le périmètre à coudre selon le type de produit.
        Méthode unifiée pour tous les types de produits.
        """
        self.ensure_one()
        
        if not category_type:
            category_type = self.fe_product_categ
            
        if category_type == 'linge_de_table':
            # Calcul des dimensions réelles avec ourlets et chutes
            longueur_coupe = self.longueur_linge +  2*self.chute_nappe
            largeur_coupe = self.largeur_linge +  2*self.chute_nappe
            
            # Calcul du périmètre (2 fois la somme de la longueur et de la largeur)
            perimetre = 2 * (longueur_coupe + largeur_coupe)
            return perimetre / 100  # Conversion en mètres
            
        elif category_type == 'rideau':
            # Pour les rideaux, le périmètre est calculé différemment
            # On considère généralement les côtés et le bas (pas le haut qui est fixé à la tringle)
            perimetre = 2 * self.hauteur_rideau + self.largeur_rideau
            return perimetre
            
        # Pour les autres catégories, retourner 0
        return 0