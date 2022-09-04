# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _


class Project(models.Model):
    _inherit = 'project.project'

    is_scrum = fields.Boolean(string="Scrum Project OK")
