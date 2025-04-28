# -*- coding: utf-8 -*-
{
    'name': "Identifiants fiscaux maroc",

    'summary': """
    
        Ce module Odoo permet d'ajouter six nouveaux champs importants dans la fiche client : 
        1. RC (Registre de Commerce) 
        2. TP : Taxe profesionnelle 
        3. IF (Identifiant Fiscale) 
        4. CNSS : Numéro d'immaticulation CNSS
        5. ICE (Identifiant Commun de l'Entreprise)
        6. CAPITAL de la société

        Ces champs facilitent la gestion et le suivi des informations légales et fiscales des entreprises clientes dans le système Odoo. Ce module est essentiel pour les entreprises nécessitant un suivi précis de leurs clients dans le respect des obligations légales.

    
    """,

    'description': """
       Ajout des champs RC, TP, IF, CNSS, ICE et CAPITAL dans la fiche société ainsi que les fiches clients & fournisseurs .

    """,

    'author': 'D-Business Consulting',
    'company': 'D-Business Consulting',
    'maintainer': 'D-Business Consulting',
    'website': 'https://d-business-consulting.ma',
    'category': 'Sales,Purchases,Accounting,Extra Tools',
    'version': '17.0.2.0.0',

    'depends': ['base'],

    'data': [
        'views/view.xml'
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
