/** @odoo-module **/

import { registry } from '@web/core/registry';
import { Component, xml } from "@odoo/owl";

class CMSDashboard extends Component {
    static template = xml`
        <div class="o_cms_dashboard">
            <h1>CMS Dashboard</h1>
            <p>Welcome to the CMS Dashboard!</p>
        </div>`;
}

// Registry entry point - nama cms_dashboard harus sama dengan yang direferensikan di XML
registry.category("actions").add("cms_dashboard", CMSDashboard);