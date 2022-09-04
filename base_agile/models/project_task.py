# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _


class Task(models.Model):
    _inherit = 'project.task'

    task_type = fields.Selection(selection=[
        ('epic', 'Epic'),
        ('user_story', 'User Story'),
        ('task', 'Task'),
        ('sub_task', 'Sub-Task'),
        ('bug', 'Bug'),
    ], tracking=True,
        help="""
    1-Epic: is a body of work that can be broken down into specific stories
    2- User Story:  is a small (actually, the smallest) piece of work that represents some value to an end user and can be delivered during a sprint.
    The main aim of this element is to put end users in the center of conversation and capture product functionality from their perspective. Thus, developers get a better understanding of what, for whom and why they’re building.
    3-Task: small steps to achieve the story 
    4-Sub Task: small steps to achieve the Task
    5-Bug: testing issue that raised from Q&A Team 
    """)
    task_priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], default='low', index=True, string="Task Priority", tracking=True)
    task_severity = fields.Selection([
        ('low', 'Low'),
        ('minor', 'Minor'),
        ('major', 'Major'),
        ('critical', 'Critical'),
    ], default='low', index=True, string="Task Severity", tracking=True)
    delegation_date = fields.Date(tracking=True)
    task_count = fields.Integer(string="Tasks", compute="_compute_task_type_count")
    bug_count = fields.Integer(string="Bugs", compute="_compute_task_type_count")

    # TODO:fields for story writing criteria
    story_role = fields.Char(
        string="As a",
        tracking=True,
        help="""
    Step 1: Think of the “Who”
    This is the first and, maybe, the most fundamental step. 
    Before writing a User Story you should actually know who the end users of your product are. 
    And more important - what needs they have, which you are trying to cover.
    
    Here are a few more tips from our own experience:
    1-It’s all about the use:. Not about developers. And even not about a Product Owner. Each Story should be valuable to some group of your end users.
    2-Don’t think of users only as external customers: It’s true that your Stories will be mostly about them. But it’s also true that you have to consider internal users such as admins, editors etc.
    3-Feel some empathy. Give your “user” a name: Think of his mobile habits, what issue your app is going to get resolved for him and how you’re going to make this path easier and faster. Remember some people who you know from the real life and who fit this portrait; feel how you relate to this target group.
        """
    )
    story_action = fields.Text(
        string="I want",
        tracking=True,
        help="""
    Step 2: Think of the “What”
    Now we have a few groups of end users. The next step we do is define what actions each user expects, 
    how he’s going to interact with the app.
    
    These are the main rules to remember when writing an action for a Kanban or Scrum User Story:
    1-One action per a Story: If you want to write something like “as a customer I want to browse items and add them to the cart” you’d better split it into 2 separate Stories.
    2-Describe an intention, not a feature: For example, instead of “I want to manage my profile” create a few Stories like “I want to be able to register”, “I want to upload my profile photo”, “I want to link my credit card to my profile” - each Story will have a different value.
    3-Keep it short: Users don’t care what library you will use to let them browse the list of items so leave all the tech details aside.
    4-Avoid describing UI: We’ve defined Stories as negotiable, remember? That's why all good User Story examples don't include any UI details. So don’t try to compose any special way to implement them (we’ll do this later).
        """
    )
    story_value = fields.Text(
        string="So that",
        tracking=True,
        help="""
    Step 3: Think of the “Why”
    Finally, the last piece of our User Stories template is dedicated to a value that users get after performing an action. It may seem like not a big deal but it’s often the most tricky part of User Story development.
    
    If you can’t answer what value this feature brings to end users and your product as well, then you’re doing something wrong.
    Examples:
    1-As a customer, I want to get notifications when there are new hot offers so that I never miss the best deals. 
    2-As a restaurant manager, I want to complement dish description in the menu with a photo so that it looks more attractive to the customers.
        """
    )
    story_acceptance_criteria = fields.Text(
        string="Acceptance criteria?",
        tracking=True,
        help="""
    An acceptance criteria is a set of conditions that are used to confirm when a Story is completed.
    Also, these conditions provide us with a deeper and better understanding since they include key info on how Stories perform. Let’s reuse one of the User Story examples from the beginning of the article:

    As a passenger, I want several available drivers to be displayed so that I can choose the most suitable option for me.

    What acceptance criteria can be applied to this Story?
    The app shows drivers that were online within last 20 minutes and don’t have an ongoing ride.
    The app shows only 5 drivers that are closest to the user.
    A user can browse profiles of these drivers, including their photos and rates.
        """
    )
    story_scenario = fields.Text('Scenario')

    def _compute_task_type_count(self):
        for rec in self:
            tasks = 0
            bugs = 0
            for line in rec.child_ids:
                if line.task_type in ['task', 'sub_task']:
                    tasks += 1
                elif line.task_type == 'bug':
                    bugs += 1
            rec.task_count = tasks
            rec.bug_count = bugs

    def action_open_tasks(self):
        return {
            'name': _('Tasks'),
            'type': 'ir.actions.act_window',
            'res_model': 'project.task',
            'view_mode': 'tree,form,search',
            'target': 'current',
            'domain': [('parent_id', '=', self.id), ('task_type', 'in', ['task', 'sub_task'])],
            'context': {
                'default_display_project_id': self.project_id.id,
                'default_project_id': self.project_id.id,
                'default_parent_id': self.id,
                'default_task_type': 'task'
            }
        }

    def action_open_bugs(self):
        return {
            'name': _('Bugs'),
            'type': 'ir.actions.act_window',
            'res_model': 'project.task',
            'view_mode': 'tree,form,search',
            'target': 'current',
            'domain': [('parent_id', '=', self.id), ('task_type', '=', 'bug')],
            'context': {
                'default_display_project_id': self.project_id.id,
                'default_project_id': self.project_id.id,
                'default_parent_id': self.id,
                'default_task_type': 'bug'
            }
        }
