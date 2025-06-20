from odoo import models, fields, api

class CmsContentType(models.Model):
    _name = 'cms.content.type'
    _description = 'CMS Content Type'
    
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)