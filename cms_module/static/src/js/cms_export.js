// This file contains JavaScript code for handling the export of content in JSON format.

odoo.define('content_management_system.cms_export', function (require) {
    "use strict";

    var ajax = require('web.ajax');

    function exportContent() {
        ajax.jsonRpc('/cms/export', 'call', {})
            .then(function (data) {
                var jsonContent = JSON.stringify(data);
                downloadJSON(jsonContent, 'cms_content_export.json');
            })
            .fail(function (error) {
                console.error('Export failed:', error);
            });
    }

    function downloadJSON(content, filename) {
        var blob = new Blob([content], { type: 'application/json' });
        var link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    // Expose the export function to the global scope
    window.exportCMSContent = exportContent;
});