/** @odoo-module **/
/* global L */

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.OsmMap = publicWidget.Widget.extend({
    selector: '.s_osm_map',
    disabledInEditableMode: false,

    // OpenStreetMap tile layer URLs for different styles
    tileProviders: {
        standard: {
            url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 19,
        },
        grayscale: {
            url: 'https://tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png',
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 18,
        },
        dark: {
            url: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            maxZoom: 19,
        },
        watercolor: {
            url: 'https://tiles.stadiamaps.com/tiles/stamen_watercolor/{z}/{x}/{y}.jpg',
            attribution: '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
            maxZoom: 16,
        },
        toner: {
            url: 'https://tiles.stadiamaps.com/tiles/stamen_toner/{z}/{x}/{y}{r}.png',
            attribution: '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
            maxZoom: 18,
        },
    },

    /**
     * @override
     */
    async start() {
        await this._super(...arguments);

        // Check if Leaflet is loaded
        if (typeof L !== 'object') {
            console.error('Leaflet library not loaded');
            return;
        }

        this._renderMap();
        
        // In edit mode, watch for snippet updates
        if (this.editableMode) {
            this.$target.on('content_changed', () => {
                this._renderMap();
            });
        }
        
        // Listen for attribute changes to update map
        const observer = new MutationObserver(() => {
            this._renderMap();
        });
        observer.observe(this.el, {
            attributes: true,
            attributeFilter: ['data-map-lat', 'data-map-lng', 'data-map-style', 'data-map-zoom']
        });
    },

    /**
     * Render or update the map
     */
    _renderMap() {
        // Get GPS coordinates from data attributes
        const lat = parseFloat(this.el.dataset.mapLat) || 50.854975;
        const lng = parseFloat(this.el.dataset.mapLng) || 4.3753899;
        
        // Get zoom level from data attribute
        const zoom = parseInt(this.el.dataset.mapZoom) || 12;
        
        // Get map style from data attribute
        const mapStyle = this.el.dataset.mapStyle || 'standard';
        const tileProvider = this.tileProviders[mapStyle] || this.tileProviders.standard;

        // Get the map container
        const mapContainer = this.$('.map_container').get(0);
        
        // If map exists, just update center and zoom
        if (this.map) {
            this.map.setView([lat, lng], zoom);
            if (this.marker) {
                this.marker.setLatLng([lat, lng]);
            }
            return;
        }

        // Initialize the map
        this.map = L.map(mapContainer, {
            center: [lat, lng],
            zoom: zoom,
            scrollWheelZoom: false,
            zoomControl: true,
        });

        // Add tile layer
        L.tileLayer(tileProvider.url, {
            attribution: tileProvider.attribution,
            maxZoom: tileProvider.maxZoom,
        }).addTo(this.map);

        // Create marker based on pin style
        const markerOptions = {};
        if (this.el.dataset.pinStyle === 'custom') {
            const customIcon = L.icon({
                iconUrl: '/website_block_osm/static/src/img/marker-icon-custom.svg',
                iconSize: [25, 41],
                iconAnchor: [12, 41],
                popupAnchor: [1, -34],
                shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
                shadowSize: [41, 41],
            });
            markerOptions.icon = customIcon;
        }

        // Add marker
        const marker = L.marker([lat, lng], markerOptions).addTo(this.map);

        // Add popup with address if available
        if (this.el.dataset.pinAddress) {
            marker.bindPopup(this.el.dataset.pinAddress);
        }

        // Update map size on window resize
        window.addEventListener('resize', () => {
            if (this.map) {
                this.map.invalidateSize();
            }
        });

        // Force map to resize after a short delay (fixes rendering issues)
        setTimeout(() => {
            if (this.map) {
                this.map.invalidateSize();
            }
        }, 100);
    },

    /**
     * @override
     */
    destroy() {
        if (this.map) {
            this.map.remove();
            this.map = null;
        }
        this._super(...arguments);
    },
});

