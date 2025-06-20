from odoo import http
from odoo.http import request

class ContentManagementPortal(http.Controller):

    @http.route('/cms/content', type='http', auth='public', methods=['GET'], csrf=False)
    def get_content(self, **kwargs):
        contents = request.env['cms.content'].search([])
        content_data = []
        for content in contents:
            content_data.append({
                'title': content.title,
                'excerpt': content.excerpt,
                'description': content.description,
                'category': content.category_id.name,
                'tags': [tag.name for tag in content.tag_ids],
                'image_feature': content.image_feature,
                'post_type': content.post_type,
                'meta_keywords': content.meta_keywords,
                'meta_description': content.meta_description,
            })
        return request.make_response(json.dumps(content_data), headers={'Content-Type': 'application/json'})

    @http.route('/cms/content/<int:content_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_single_content(self, content_id, **kwargs):
        content = request.env['cms.content'].browse(content_id)
        if not content.exists():
            return request.not_found()
        content_data = {
            'title': content.title,
            'excerpt': content.excerpt,
            'description': content.description,
            'category': content.category_id.name,
            'tags': [tag.name for tag in content.tag_ids],
            'image_feature': content.image_feature,
            'post_type': content.post_type,
            'meta_keywords': content.meta_keywords,
            'meta_description': content.meta_description,
        }
        return request.make_response(json.dumps(content_data), headers={'Content-Type': 'application/json'})