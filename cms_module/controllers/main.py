from odoo import http
from odoo.http import request

class ContentManagementSystem(http.Controller):

    @http.route('/cms/content', type='http', auth='user', methods=['GET', 'POST'], csrf=False)
    def edit_content(self, **kwargs):
        if request.httprequest.method == 'POST':
            # Logic to create or update content
            # Extract data from kwargs and save to the database
            pass
        # Logic to render the edit form
        return request.render('content_management_system.edit_content_template')

    @http.route('/cms/export', type='http', auth='public', methods=['GET'], csrf=False)
    def export_content(self):
        # Logic to fetch content and export it in JSON format
        content_data = []  # Fetch content data from the database
        return request.make_response(
            json.dumps(content_data),
            headers={'Content-Type': 'application/json'}
        )