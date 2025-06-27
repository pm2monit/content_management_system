from odoo import models, fields, api

class CmsCategory(models.Model):
    _name = 'cms.category'
    _description = 'CMS Category'
    _parent_name = 'parent_id'
    _parent_store = True
    _rec_name = 'name'
    
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    parent_id = fields.Many2one('cms.category', string='Parent Category', ondelete='restrict', index=True)
    parent_path = fields.Char(index=True)
    child_ids = fields.One2many('cms.category', 'parent_id', string='Child Categories')
    
    active = fields.Boolean(string='Active', default=True)