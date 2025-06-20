from odoo import models, fields, api

class CmsTag(models.Model):
    _name = 'cms.tag'
    _description = 'CMS Tag'
    
    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color Index')
    description = fields.Text(string='Description')