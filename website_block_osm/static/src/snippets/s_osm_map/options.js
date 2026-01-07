/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import options from "@web_editor/js/editor/snippets.options";

options.registry.OsmMap = options.Class.extend({

    //--------------------------------------------------------------------------
    // Options
    //--------------------------------------------------------------------------

    /**
     * Use company address coordinates
     * @see this.selectClass for parameters
     */
    async useCompanyAddress(previewMode, widgetValue, params) {
        // Get company data - using a simple geocoding for Brussels as fallback
        // In real implementation, this would fetch from company settings
        const companyLat = 50.8503;
        const companyLng = 4.3517;
        const companyAddress = 'Grand Place, Brussels';
        
        this.$target[0].dataset.mapLat = companyLat;
        this.$target[0].dataset.mapLng = companyLng;
        this.$target[0].dataset.pinAddress = companyAddress;
        
        // Trigger map update
        this.trigger_up('snippet_option_update', {
            onSuccess: () => {
                // Reload the map widget
                const mapWidget = this.$target[0];
                if (mapWidget) {
                    $(mapWidget).trigger('content_changed');
                }
            }
        });
    },

    /**
     * Show or hide the description overlay
     * @see this.selectClass for parameters
     */
    async showDescription(previewMode, widgetValue, params) {
        const descriptionEl = this.$target[0].querySelector('.description');
        if (widgetValue && !descriptionEl) {
            this.$target.append($(`
                <div class="description">
                    <font>${_t('Besuchen Sie uns:')}</font>
                    <span>${_t('Unser Büro befindet sich im Nordosten von Brüssel. TEL (555) 432 2365')}</span>
                </div>`)
            );
        } else if (!widgetValue && descriptionEl) {
            descriptionEl.remove();
        }
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @override
     */
    _computeWidgetState(methodName, params) {
        if (methodName === 'showDescription') {
            return this.$target[0].querySelector('.description') ? 'true' : '';
        }
        return this._super(...arguments);
    },

    /**
     * @override
     */
    async updateUI() {
        await this._super(...arguments);
        // Trigger map re-render when any option changes
        this.$target.trigger('content_changed');
    },
});

