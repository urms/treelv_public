# -*- coding: utf-8 -*-
{
    'name': 'Website OpenStreetMap Block',
    'category': 'TreElv Public',
    'version': '18.0.1.0',
    'summary': 'Add OpenStreetMap/Leaflet map blocks to website',
    'icon': 'static/description/icon.png',
    'description': """
        OpenStreetMap Block for Website
        ================================
        This module adds a new website block that displays an OpenStreetMap
        with Leaflet instead of Google Maps.
        
        Features:
        ---------
        * Drag & drop OpenStreetMap block
        * Customizable map styles
        * Zoom control
        * GPS position picker
        * Custom marker styles
        * Optional description overlay
    """,
    'depends': ['website'],
    'data': [
        'views/snippets/s_osm_map.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_block_osm/static/src/snippets/s_osm_map/000.scss',
            'website_block_osm/static/src/snippets/s_osm_map/000.js',
            'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
            'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
