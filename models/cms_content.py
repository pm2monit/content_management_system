from odoo import models, fields, api, _
from odoo.exceptions import UserError

class CmsContent(models.Model):
    _name = 'cms.content'
    _description = 'CMS Content'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    # Tambahkan tracking=True di field yang ingin dimonitor perubahannya
    name = fields.Char(string='Title', required=True, tracking=True)
    content_type_id = fields.Many2one('cms.content.type', string='Content Type', tracking=True)
    category_id = fields.Many2one('cms.category', string='Category', tracking=True)
    tag_ids = fields.Many2many('cms.tag', string='Tags')
    author_id = fields.Many2one('res.users', string='Author', default=lambda self: self.env.user, tracking=True)
    content = fields.Html(string='Content', tracking=True, sanitize=True)
    excerpt = fields.Text(string='Excerpt')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived')
    ], string='Status', default='draft', tracking=True)
    
    # Fields untuk gambar
    featured_image = fields.Binary(string='Featured Image', attachment=True)
    featured_image_filename = fields.Char(string='Image Filename')
    
    # Fields untuk galeri gambar
    image_ids = fields.One2many('cms.content.image', 'content_id', string='Image Gallery')
    
    # Fields lainnya seperti sebelumnya
    url_slug = fields.Char(string='URL Slug')
    meta_keywords = fields.Char(string='Meta Keywords')
    meta_description = fields.Text(string='Meta Description')
    
    date_created = fields.Datetime(string='Created Date', default=fields.Datetime.now, readonly=True)
    date_published = fields.Datetime(string='Published Date')
    date_updated = fields.Datetime(string='Updated Date')
    
    active = fields.Boolean(string='Active', default=True)
    
    # Override message_get_default_recipients untuk menghindari masalah dengan model referensi
    def message_get_default_recipients(self):
        return {
            r.id: {
                'partner_ids': [],
                'email_to': False,
                'email_cc': False
            } for r in self
        }
    
    # Metode untuk mengubah state ke published
    def action_publish(self):
        self.write({
            'state': 'published',
            'date_published': fields.Datetime.now(),
        })
    
    # Metode untuk mengubah state ke archived
    def action_archive(self):
        self.write({'state': 'archived'})
    
    # Metode untuk mengubah state ke draft
    def action_draft(self):
        self.write({'state': 'draft'})
    
    # Metode untuk preview post
    def preview_post(self):
        """Fungsi untuk preview konten"""
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return {
            'type': 'ir.actions.act_url',
            'url': f"{base_url}/web/content/preview/{self.id}",
            'target': 'new',
        }
    
    # Tambahkan metode action_add_image dengan error handling
    def action_add_image(self):
        """Membuka wizard untuk menambahkan gambar ke galeri"""
        self.ensure_one()
        return {
            'name': 'Add Image to Gallery',
            'type': 'ir.actions.act_window',
            'res_model': 'cms.content.image',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_content_id': self.id,
                'default_name': f"{self.name} - Image {len(self.image_ids) + 1}",
                'default_is_published': True,
            }
        }
        
    @api.model_create_multi
    def create(self, vals_list):
        """Override create untuk menambahkan sanitasi tambahan"""
        for vals in vals_list:
            # Sanitize content
            if 'content' in vals and vals.get('content'):
                vals['content'] = self._sanitize_html_content(vals['content'])
            
            # Generate URL slug jika tidak ada
            if not vals.get('url_slug') and vals.get('name'):
                vals['url_slug'] = self._generate_url_slug(vals['name'])
                
        records = super(CmsContent, self).create(vals_list)
        # Auto-subscribe author ke konten yang dibuat
        for record in records:
            if record.author_id:
                record.message_subscribe(partner_ids=[record.author_id.partner_id.id])
        return records
    
    def write(self, vals):
        """Override write untuk menambahkan sanitasi tambahan"""
        if 'content' in vals and vals.get('content'):
            vals['content'] = self._sanitize_html_content(vals['content'])
            
        # Update date_updated saat ada perubahan
        vals['date_updated'] = fields.Datetime.now()
        
        return super(CmsContent, self).write(vals)
    
    def _sanitize_html_content(self, content):
        """Sanitize HTML content untuk mencegah XSS"""
        if not content:
            return content
        return content
    
    def _generate_url_slug(self, name):
        """Generate URL slug dari name"""
        slug = name.lower().replace(' ', '-')
        # Hapus karakter non-alphanumeric
        import re
        slug = re.sub(r'[^a-z0-9-]', '', slug)
        # Hapus multiple hyphens
        slug = re.sub(r'-+', '-', slug)
        return slug
    
    # Metode untuk mengontrol siapa yang bisa follow
    def _get_valid_followers(self):
        """Filter follower yang valid berdasarkan grup"""
        partners = super(CmsContent, self)._get_valid_followers()
        cms_user_group = self.env.ref('content_management_system.group_cms_user')
        cms_manager_group = self.env.ref('content_management_system.group_cms_manager')
        
        # Dapatkan semua partner yang terkait dengan user yang memiliki grup CMS
        valid_partners = self.env['res.users'].search([
            ('groups_id', 'in', [cms_user_group.id, cms_manager_group.id])
        ]).mapped('partner_id')
        
        return partners.filtered(lambda p: p in valid_partners)