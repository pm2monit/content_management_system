from odoo import http
from odoo.http import request
import werkzeug.wrappers
import json
from datetime import datetime, date

class DateTimeEncoder(json.JSONEncoder):
    """Custom encoder for datetime/date objects"""
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)


class ContentAPIController(http.Controller):
    """Content Management System API Controller"""

    @http.route('/api/cms/content', type='http', auth='public', methods=['GET'], csrf=False)
    def get_contents(self, **kwargs):
        """Get all published content or filter by parameters"""
        domain = [('state', '=', 'published')]
        
        # Handle query parameters for filtering
        if kwargs.get('category_id'):
            domain.append(('category_id', '=', int(kwargs.get('category_id'))))
        
        if kwargs.get('content_type_id'):
            domain.append(('content_type_id', '=', int(kwargs.get('content_type_id'))))
        
        if kwargs.get('tag_ids'):
            domain.append(('tag_ids', 'in', [int(kwargs.get('tag_ids'))]))
        
        # Pagination
        limit = int(kwargs.get('limit', 10))
        offset = int(kwargs.get('offset', 0))
        
        # Get content records
        contents = request.env['cms.content'].sudo().search(domain, limit=limit, offset=offset)
        
        result = []
        for content in contents:
            result.append({
                'id': content.id,
                'name': content.name,
                'content': content.content,
                'url_slug': content.url_slug,
                'category_id': content.category_id.id if content.category_id else False,
                'category_name': content.category_id.name if content.category_id else False,
                'content_type': content.content_type_id.name if content.content_type_id else False,
                'date_published': content.date_published,
                'tags': [{'id': tag.id, 'name': tag.name} for tag in content.tag_ids],
                'author': content.author_id.name if content.author_id else False,
            })
        
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With',
        }
        
        return werkzeug.wrappers.Response(
            json.dumps({'count': len(result), 'data': result}, cls=DateTimeEncoder), 
            headers=headers, 
            status=200
        )
    
    @http.route('/api/cms/content/<int:content_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_content(self, content_id, **kwargs):
        """Get content by ID"""
        content = request.env['cms.content'].sudo().browse(content_id)
        
        if not content.exists() or content.state != 'published':
            headers = {'Content-Type': 'application/json'}
            return werkzeug.wrappers.Response(json.dumps({'error': 'Content not found'}), 
                                             headers=headers, status=404)
        
        result = {
            'id': content.id,
            'name': content.name,
            'content': content.content,
            'url_slug': content.url_slug,
            'category_id': content.category_id.id if content.category_id else False,
            'category_name': content.category_id.name if content.category_id else False,
            'content_type': content.content_type_id.name if content.content_type_id else False,
            'date_published': content.date_published.isoformat() if content.date_published else False,
            'tags': [{'id': tag.id, 'name': tag.name} for tag in content.tag_ids],
            'author': content.author_id.name if content.author_id else False,
        }
        
        headers = {'Content-Type': 'application/json'}
        return werkzeug.wrappers.Response(json.dumps(result), headers=headers, status=200)
    
    @http.route('/api/cms/categories', type='http', auth='public', methods=['GET'], csrf=False)
    def get_categories(self, **kwargs):
        """Get all categories"""
        categories = request.env['cms.category'].sudo().search([])
        
        result = []
        for category in categories:
            result.append({
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'parent_id': category.parent_id.id if category.parent_id else False,
            })
        
        headers = {'Content-Type': 'application/json'}
        return werkzeug.wrappers.Response(
            json.dumps(result, cls=DateTimeEncoder),
            headers=headers,
            status=200
        )
    
    @http.route('/api/cms/tags', type='http', auth='public', methods=['GET'], csrf=False)
    def get_tags(self, **kwargs):
        """Get all tags"""
        tags = request.env['cms.tag'].sudo().search([])
        
        result = []
        for tag in tags:
            result.append({
                'id': tag.id,
                'name': tag.name,
                'color': tag.color,
            })
        
        headers = {'Content-Type': 'application/json'}
        return werkzeug.wrappers.Response(
            json.dumps(result, cls=DateTimeEncoder),
            headers=headers,
            status=200
        )
    
    @http.route('/api/cms/content/slug/<string:url_slug>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_content_by_slug(self, url_slug, **kwargs):
        """Get content by URL slug"""
        content = request.env['cms.content'].sudo().search([
            ('url_slug', '=', url_slug),
            ('state', '=', 'published')
        ], limit=1)
        
        if not content:
            headers = {'Content-Type': 'application/json'}
            return werkzeug.wrappers.Response(
                json.dumps({'error': 'Content not found'}),
                headers=headers,
                status=404
            )
        
        result = {
            'id': content.id,
            'name': content.name,
            'content': content.content,
            'url_slug': content.url_slug,
            'category_id': content.category_id.id if content.category_id else False,
            'category_name': content.category_id.name if content.category_id else False,
            'content_type': content.content_type_id.name if content.content_type_id else False,
            'date_published': content.date_published,
            'tags': [{'id': tag.id, 'name': tag.name} for tag in content.tag_ids],
            'author': content.author_id.name if content.author_id else False,
        }
        
        headers = {'Content-Type': 'application/json'}
        return werkzeug.wrappers.Response(
            json.dumps(result, cls=DateTimeEncoder),
            headers=headers,
            status=200
        )