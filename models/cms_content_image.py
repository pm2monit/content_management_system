from odoo import models, fields, api

class CmsContentImage(models.Model):
    _name = 'cms.content.image'
    _description = 'CMS Content Image Gallery'
    _order = 'sequence'
    
    name = fields.Char(string='Title')
    content_id = fields.Many2one('cms.content', string='Content', ondelete='cascade', required=True)
    image = fields.Binary(string='Image', attachment=True, required=True)
    image_filename = fields.Char(string='Image Filename')
    description = fields.Text(string='Description')
    sequence = fields.Integer(string='Sequence', default=10)
    is_published = fields.Boolean(string='Published', default=True)
    
    # URL untuk akses gambar
    full_url = fields.Char(string='Full URL', compute='_compute_urls', store=False)
    
    @api.depends('image')
    def _compute_urls(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for record in self:
            if record.id:
                record.full_url = f"{base_url}/web/image/cms.content.image/{record.id}/image"
            else:
                record.full_url = False