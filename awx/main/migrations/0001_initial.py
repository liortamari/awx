# -*- coding: utf-8 -*-

# Copyright (c) 2016 Ansible, Inc.
# All Rights Reserved.

from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import django.db.models.deletion
from django.conf import settings
import taggit.managers
import awx.main.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityStream',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (
                    'operation',
                    models.CharField(
                        max_length=13,
                        choices=[
                            ('create', 'Entity Created'),
                            ('update', 'Entity Updated'),
                            ('delete', 'Entity Deleted'),
                            ('associate', 'Entity Associated with another Entity'),
                            ('disassociate', 'Entity was Disassociated with another Entity'),
                        ],
                    ),
                ),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('changes', models.TextField(blank=True)),
                ('object_relationship_type', models.TextField(blank=True)),
                ('object1', models.TextField()),
                ('object2', models.TextField()),
                (
                    'actor',
                    models.ForeignKey(related_name='activity_stream', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name='AdHocCommandEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=None, editable=False)),
                ('modified', models.DateTimeField(default=None, editable=False)),
                ('host_name', models.CharField(default='', max_length=1024, editable=False)),
                (
                    'event',
                    models.CharField(
                        max_length=100,
                        choices=[
                            ('runner_on_failed', 'Host Failed'),
                            ('runner_on_ok', 'Host OK'),
                            ('runner_on_unreachable', 'Host Unreachable'),
                            ('runner_on_skipped', 'Host Skipped'),
                        ],
                    ),
                ),
                ('event_data', awx.main.fields.JSONBlob(default=dict, blank=True)),
                ('failed', models.BooleanField(default=False, editable=False)),
                ('changed', models.BooleanField(default=False, editable=False)),
                ('counter', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('-pk',),
            },
        ),
        migrations.CreateModel(
            name='AuthToken',
            fields=[
                ('key', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('expires', models.DateTimeField(default=django.utils.timezone.now)),
                ('request_hash', models.CharField(default='', max_length=40, blank=True)),
                ('reason', models.CharField(default='', help_text='Reason the auth token was invalidated.', max_length=1024, blank=True)),
                ('user', models.ForeignKey(related_name='auth_tokens', on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Credential',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=None, editable=False)),
                ('modified', models.DateTimeField(default=None, editable=False)),
                ('description', models.TextField(default='', blank=True)),
                ('active', models.BooleanField(default=True, editable=False)),
                ('name', models.CharField(max_length=512)),
                (
                    'kind',
                    models.CharField(
                        default='ssh',
                        max_length=32,
                        choices=[
                            ('ssh', 'Machine'),
                            ('scm', 'Source Control'),
                            ('aws', 'Amazon Web Services'),
                            ('rax', 'Rackspace'),
                            ('vmware', 'VMware vCenter'),
                            ('gce', 'Google Compute Engine'),
                            ('azure', 'Microsoft Azure'),
                            ('openstack', 'OpenStack'),
                        ],
                    ),
                ),
                ('cloud', models.BooleanField(default=False, editable=False)),
                ('host', models.CharField(default='', help_text='The hostname or IP address to use.', max_length=1024, verbose_name='Host', blank=True)),
                ('username', models.CharField(default='', help_text='Username for this credential.', max_length=1024, verbose_name='Username', blank=True)),
                (
                    'password',
                    models.CharField(
                        default='',
                        help_text='Password for this credential (or "ASK" to prompt the user for machine credentials).',
                        max_length=1024,
                        verbose_name='Password',
                        blank=True,
                    ),
                ),
                (
                    'security_token',
                    models.CharField(default='', help_text='Security Token for this credential', max_length=1024, verbose_name='Security Token', blank=True),
                ),
                ('project', models.CharField(default='', help_text='The identifier for the project.', max_length=100, verbose_name='Project', blank=True)),
                (
                    'ssh_key_data',
                    models.TextField(
                        default='', help_text='RSA or DSA private key to be used instead of password.', verbose_name='SSH private key', blank=True
                    ),
                ),
                (
                    'ssh_key_unlock',
                    models.CharField(
                        default='',
                        help_text='Passphrase to unlock SSH private key if encrypted (or "ASK" to prompt the user for machine credentials).',
                        max_length=1024,
                        verbose_name='SSH key unlock',
                        blank=True,
                    ),
                ),
                (
                    'become_method',
                    models.CharField(
                        default='',
                        help_text='Privilege escalation method.',
                        max_length=32,
                        blank=True,
                        choices=[('', 'None'), ('sudo', 'Sudo'), ('su', 'Su'), ('pbrun', 'Pbrun'), ('pfexec', 'Pfexec')],
                    ),
                ),
                ('become_username', models.CharField(default='', help_text='Privilege escalation username.', max_length=1024, blank=True)),
                ('become_password', models.CharField(default='', help_text='Password for privilege escalation method.', max_length=1024, blank=True)),
                ('vault_password', models.CharField(default='', help_text='Vault password (or "ASK" to prompt the user).', max_length=1024, blank=True)),
                (
                    'created_by',
                    models.ForeignKey(
                        related_name="{u'class': 'credential', u'app_label': 'main'}(class)s_created+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        default=None,
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                (
                    'modified_by',
                    models.ForeignKey(
                        related_name="{u'class': 'credential', u'app_label': 'main'}(class)s_modified+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        default=None,
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                (
                    'tags',
                    taggit.managers.TaggableManager(
                        to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'
                    ),
                ),
            ],
            options={
                'ordering': ('kind', 'name'),
            },
        ),
        migrations.CreateModel(
            name='CustomInventoryScript',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=None, editable=False)),
                ('modified', models.DateTimeField(default=None, editable=False)),
                ('description', models.TextField(default='', blank=True)),
                ('active', models.BooleanField(default=True, editable=False)),
                ('name', models.CharField(max_length=512)),
                ('script', models.TextField(default='', help_text='Inventory script contents', blank=True)),
                (
                    'created_by',
                    models.ForeignKey(
                        related_name="{u'class': 'custominventoryscript', u'app_label': 'main'}(class)s_created+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        default=None,
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                (
                    'modified_by',
                    models.ForeignKey(
                        related_name="{u'class': 'custominventoryscript', u'app_label': 'main'}(class)s_modified+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        default=None,
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=None, editable=False)),
                ('modified', models.DateTimeField(default=None, editable=False)),
                ('description', models.TextField(default='', blank=True)),
                ('active', models.BooleanField(default=True, editable=False)),
                ('name', models.CharField(max_length=512)),
                ('variables', models.TextField(default='', help_text='Group variables in JSON or YAML format.', blank=True)),
                (
                    'total_hosts',
                    models.PositiveIntegerField(default=0, help_text='Total number of hosts directly or indirectly in this group.', editable=False),
                ),
                (
                    'has_active_failures',
                    models.BooleanField(default=False, help_text='Flag indicating whether this group has any hosts with active failures.', editable=False),
                ),
                (
                    'hosts_with_active_failures',
                    models.PositiveIntegerField(default=0, help_text='Number of hosts in this group with active failures.', editable=False),
                ),
                ('total_groups', models.PositiveIntegerField(default=0, help_text='Total number of child groups contained within this group.', editable=False)),
                (
                    'groups_with_active_failures',
                    models.PositiveIntegerField(default=0, help_text='Number of child groups within this group that have active failures.', editable=False),
                ),
                (
                    'has_inventory_sources',
                    models.BooleanField(
                        default=False, help_text='Flag indicating whether this group was created/updated from any external inventory sources.', editable=False
                    ),
                ),
                (
                    'created_by',
                    models.ForeignKey(
                        related_name="{u'class': 'group', u'app_label': 'main'}(class)s_created+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        default=None,
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=None, editable=False)),
                ('modified', models.DateTimeField(default=None, editable=False)),
                ('description', models.TextField(default='', blank=True)),
                ('active', models.BooleanField(default=True, editable=False)),
                ('name', models.CharField(max_length=512)),
                ('enabled', models.BooleanField(default=True, help_text='Is this host online and available for running jobs?')),
                ('instance_id', models.CharField(default='', max_length=100, blank=True)),
                ('variables', models.TextField(default='', help_text='Host variables in JSON or YAML format.', blank=True)),
                (
                    'has_active_failures',
                    models.BooleanField(default=False, help_text='Flag indicating whether the last job failed for this host.', editable=False),
                ),
                (
                    'has_inventory_sources',
                    models.BooleanField(
                        default=False, help_text='Flag indicating whether this host was created/updated from any external inventory sources.', editable=False
                    ),
                ),
                (
                    'created_by',
                    models.ForeignKey(
                        related_name="{u'class': 'host', u'app_label': 'main'}(class)s_created+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        default=None,
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
            ],
            options={
                'ordering': ('inventory', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(unique=True, max_length=40)),
                ('hostname', models.CharField(unique=True, max_length=250)),
                ('primary', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=None, editable=False)),
                ('modified', models.DateTimeField(default=None, editable=False)),
                ('description', models.TextField(default='', blank=True)),
                ('active', models.BooleanField(default=True, editable=False)),
                ('name', models.CharField(unique=True, max_length=512)),
                ('variables', models.TextField(default='', help_text='Inventory variables in JSON or YAML format.', blank=True)),
                (
                    'has_active_failures',
                    models.BooleanField(default=False, help_text='Flag indicating whether any hosts in this inventory have failed.', editable=False),
                ),
                ('total_hosts', models.PositiveIntegerField(default=0, help_text='Total number of hosts in this inventory.', editable=False)),
                (
                    'hosts_with_active_failures',
                    models.PositiveIntegerField(default=0, help_text='Number of hosts in this inventory with active failures.', editable=False),
                ),
                ('total_groups', models.PositiveIntegerField(default=0, help_text='Total number of groups in this inventory.', editable=False)),
                (
                    'groups_with_active_failures',
                    models.PositiveIntegerField(default=0, help_text='Number of groups in this inventory with active failures.', editable=False),
                ),
                (
                    'has_inventory_sources',
                    models.BooleanField(default=False, help_text='Flag indicating whether this inventory has any external inventory sources.', editable=False),
                ),
                (
                    'total_inventory_sources',
                    models.PositiveIntegerField(
                        default=0, help_text='Total number of external inventory sources configured within this inventory.', editable=False
                    ),
                ),
                (
                    'inventory_sources_with_failures',
                    models.PositiveIntegerField(default=0, help_text='Number of external inventory sources in this inventory with failures.', editable=False),
                ),
                (
                    'created_by',
                    models.ForeignKey(
                        related_name="{u'class': 'inventory', u'app_label': 'main'}(class)s_created+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        default=None,
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                (
                    'modified_by',
                    models.ForeignKey(
                        related_name="{u'class': 'inventory', u'app_label': 'main'}(class)s_modified+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        default=None,
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'inventories',
            },
        ),
        migrations.CreateModel(
            name='JobEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=None, editable=False)),
                ('modified', models.DateTimeField(default=None, editable=False)),
                (
                    'event',
                    models.CharField(
                        max_length=100,
                        choices=[
                            ('runner_on_failed', 'Host Failed'),
                            ('runner_on_ok', 'Host OK'),
                            ('runner_on_error', 'Host Failure'),
                            ('runner_on_skipped', 'Host Skipped'),
                            ('runner_on_unreachable', 'Host Unreachable'),
                            ('runner_on_no_hosts', 'No Hosts Remaining'),
                            ('runner_on_async_poll', 'Host Polling'),
                            ('runner_on_async_ok', 'Host Async OK'),
                            ('runner_on_async_failed', 'Host Async Failure'),
                            ('runner_on_file_diff', 'File Difference'),
                            ('playbook_on_start', 'Playbook Started'),
                            ('playbook_on_notify', 'Running Handlers'),
                            ('playbook_on_no_hosts_matched', 'No Hosts Matched'),
                            ('playbook_on_no_hosts_remaining', 'No Hosts Remaining'),
                            ('playbook_on_task_start', 'Task Started'),
                            ('playbook_on_vars_prompt', 'Variables Prompted'),
                            ('playbook_on_setup', 'Gathering Facts'),
                            ('playbook_on_import_for_host', 'internal: on Import for Host'),
                            ('playbook_on_not_import_for_host', 'internal: on Not Import for Host'),
                            ('playbook_on_play_start', 'Play Started'),
                            ('playbook_on_stats', 'Playbook Complete'),
                        ],
                    ),
                ),
                ('event_data', awx.main.fields.JSONBlob(default=dict, blank=True)),
                ('failed', models.BooleanField(default=False, editable=False)),
                ('changed', models.BooleanField(default=False, editable=False)),
                ('host_name', models.CharField(default='', max_length=1024, editable=False)),
                ('play', models.CharField(default='', max_length=1024, editable=False)),
                ('role', models.CharField(default='', max_length=1024, editable=False)),
                ('task', models.CharField(default='', max_length=1024, editable=False)),
                ('counter', models.PositiveIntegerField(default=0)),
                (
                    'host',
                    models.ForeignKey(
                        related_name='job_events_as_primary_host',
                        on_delete=django.db.models.deletion.SET_NULL,
                        default=None,
                        editable=False,
                        to='main.Host',
                        null=True,
                    ),
                ),
                ('hosts', models.ManyToManyField(related_name='job_events', editable=False, to='main.Host')),
                (
                    'parent',
                    models.ForeignKey(
                        related_name='children', on_delete=django.db.models.deletion.SET_NULL, default=None, editable=False, to='main.JobEvent', null=True
                    ),
                ),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='JobHostSummary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=None, editable=False)),
                ('modified', models.DateTimeField(default=None, editable=False)),
                ('host_name', models.CharField(default='', max_length=1024, editable=False)),
                ('changed', models.PositiveIntegerField(default=0, editable=False)),
                ('dark', models.PositiveIntegerField(default=0, editable=False)),
                ('failures', models.PositiveIntegerField(default=0, editable=False)),
                ('ok', models.PositiveIntegerField(default=0, editable=False)),
                ('processed', models.PositiveIntegerField(default=0, editable=False)),
                ('skipped', models.PositiveIntegerField(default=0, editable=False)),
                ('failed', models.BooleanField(default=False, editable=False)),
                (
                    'host',
                    models.ForeignKey(
                        related_name='job_host_summaries', on_delete=django.db.models.deletion.SET_NULL, default=None, editable=False, to='main.Host', null=True
                    ),
                ),
            ],
            options={
                'ordering': ('-pk',),
                'verbose_name_plural': 'job host summaries',
            },
        ),
        migrations.CreateModel(
            name='JobOrigin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('instance', models.ForeignKey(on_delete=models.CASCADE, to='main.Instance')),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=None, editable=False)),
                ('modified', models.DateTimeField(default=None, editable=False)),
                ('description', models.TextField(default='', blank=True)),
                ('active', models.BooleanField(default=True, editable=False)),
                ('name', models.CharField(unique=True, max_length=512)),
                ('admins', models.ManyToManyField(related_name='admin_of_organizations', to=settings.AUTH_USER_MODEL, blank=True)),
                (
                    'created_by',
                    models.ForeignKey(
                        related_name="{u'class': 'organization', u'app_label': 'main'}(class)s_created+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        default=None,
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                (
                    'modified_by',
                    models.ForeignKey(
                        related_name="{u'class': 'organization', u'app_label': 'main'}(class)s_modified+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        default=None,
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                (
                    'tags',
                    taggit.managers.TaggableManager(
                        to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'
                    ),
                ),
                ('users', models.ManyToManyField(related_name='organizations', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=None, editable=False)),
                ('modified', models.DateTimeField(default=None, editable=False)),
                ('description', models.TextField(default='', blank=True)),
                ('active', models.BooleanField(default=True, editable=False)),
                ('name', models.CharField(max_length=512)),
                (
                    'permission_type',
                    models.CharField(
                        max_length=64,
                        choices=[
                            ('read', 'Read Inventory'),
                            ('write', 'Edit Inventory'),
                            ('admin', 'Administrate Inventory'),
                            ('run', 'Deploy To Inventory'),
                            ('check', 'Deploy To Inventory (Dry Run)'),
                            ('scan', 'Scan an Inventory'),
                            ('create', 'Create a Job Template'),
                        ],
                    ),
                ),
                ('run_ad_hoc_commands', models.BooleanField(default=False, help_text='Execute Commands on the Inventory')),
                (
                    'created_by',
                    models.ForeignKey(
                        related_name="{u'class': 'permission', u'app_label': 'main'}(class)s_created+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        default=None,
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                ('inventory', models.ForeignKey(related_name='permissions', on_delete=django.db.models.deletion.SET_NULL, to='main.Inventory', null=True)),
                (
                    'modified_by',
                    models.ForeignKey(
                        related_name="{u'class': 'permission', u'app_label': 'main'}(class)s_modified+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        default=None,
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                (
                    'tags',
                    taggit.managers.TaggableManager(
                        to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=None, editable=False)),
                ('modified', models.DateTimeField(default=None, editable=False)),
                ('ldap_dn', models.CharField(default='', max_length=1024)),
                ('user', awx.main.fields.AutoOneToOneField(related_name='profile', editable=False, on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=None, editable=False)),
                ('modified', models.DateTimeField(default=None, editable=False)),
                ('description', models.TextField(default='', blank=True)),
                ('active', models.BooleanField(default=True, editable=False)),
                ('name', models.CharField(unique=True, max_length=512)),
                ('enabled', models.BooleanField(default=True)),
                ('dtstart', models.DateTimeField(default=None, null=True, editable=False)),
                ('dtend', models.DateTimeField(default=None, null=True, editable=False)),
                ('rrule', models.CharField(max_length=255)),
                ('next_run', models.DateTimeField(default=None, null=True, editable=False)),
                ('extra_data', models.JSONField(default=dict, null=True, blank=True)),
                (
                    'created_by',
                    models.ForeignKey(
                        related_name="{u'class': 'schedule', u'app_label': 'main'}(class)s_created+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        default=None,
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                (
                    'modified_by',
                    models.ForeignKey(
                        related_name="{u'class': 'schedule', u'app_label': 'main'}(class)s_modified+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        default=None,
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                (
                    'tags',
                    taggit.managers.TaggableManager(
                        to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'
                    ),
                ),
            ],
            options={
                'ordering': ['-next_run'],
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=None, editable=False)),
                ('modified', models.DateTimeField(default=None, editable=False)),
                ('description', models.TextField(default='', blank=True)),
                ('active', models.BooleanField(default=True, editable=False)),
                ('name', models.CharField(max_length=512)),
                (
                    'created_by',
                    models.ForeignKey(
                        related_name="{u'class': 'team', u'app_label': 'main'}(class)s_created+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        default=None,
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                (
                    'modified_by',
                    models.ForeignKey(
                        related_name="{u'class': 'team', u'app_label': 'main'}(class)s_modified+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        default=None,
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                ('organization', models.ForeignKey(related_name='teams', on_delete=django.db.models.deletion.SET_NULL, to='main.Organization', null=True)),
                (
                    'tags',
                    taggit.managers.TaggableManager(
                        to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'
                    ),
                ),
                ('users', models.ManyToManyField(related_name='teams', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'ordering': ('organization__name', 'name'),
            },
        ),
        migrations.CreateModel(
            name='UnifiedJob',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=None, editable=False)),
                ('modified', models.DateTimeField(default=None, editable=False)),
                ('description', models.TextField(default='', blank=True)),
                ('active', models.BooleanField(default=True, editable=False)),
                ('name', models.CharField(max_length=512)),
                ('old_pk', models.PositiveIntegerField(default=None, null=True, editable=False)),
                (
                    'launch_type',
                    models.CharField(
                        default='manual',
                        max_length=20,
                        editable=False,
                        choices=[
                            ('manual', 'Manual'),
                            ('relaunch', 'Relaunch'),
                            ('callback', 'Callback'),
                            ('scheduled', 'Scheduled'),
                            ('dependency', 'Dependency'),
                        ],
                    ),
                ),
                ('cancel_flag', models.BooleanField(blank=True, default=False, editable=False)),
                (
                    'status',
                    models.CharField(
                        default='new',
                        max_length=20,
                        editable=False,
                        choices=[
                            ('new', 'New'),
                            ('pending', 'Pending'),
                            ('waiting', 'Waiting'),
                            ('running', 'Running'),
                            ('successful', 'Successful'),
                            ('failed', 'Failed'),
                            ('error', 'Error'),
                            ('canceled', 'Canceled'),
                        ],
                    ),
                ),
                ('failed', models.BooleanField(default=False, editable=False)),
                ('started', models.DateTimeField(default=None, null=True, editable=False)),
                ('finished', models.DateTimeField(default=None, null=True, editable=False)),
                ('elapsed', models.DecimalField(editable=False, max_digits=12, decimal_places=3)),
                ('job_args', models.TextField(default='', editable=False, blank=True)),
                ('job_cwd', models.CharField(default='', max_length=1024, editable=False, blank=True)),
                ('job_env', models.JSONField(default=dict, editable=False, null=True, blank=True)),
                ('job_explanation', models.TextField(default='', editable=False, blank=True)),
                ('start_args', models.TextField(default='', editable=False, blank=True)),
                ('result_stdout_text', models.TextField(default='', editable=False, blank=True)),
                ('result_stdout_file', models.TextField(default='', editable=False, blank=True)),
                ('result_traceback', models.TextField(default='', editable=False, blank=True)),
                ('celery_task_id', models.CharField(default='', max_length=100, editable=False, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UnifiedJobTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=None, editable=False)),
                ('modified', models.DateTimeField(default=None, editable=False)),
                ('description', models.TextField(default='', blank=True)),
                ('active', models.BooleanField(default=True, editable=False)),
                ('name', models.CharField(max_length=512)),
                ('old_pk', models.PositiveIntegerField(default=None, null=True, editable=False)),
                ('last_job_failed', models.BooleanField(default=False, editable=False)),
                ('last_job_run', models.DateTimeField(default=None, null=True, editable=False)),
                ('has_schedules', models.BooleanField(default=False, editable=False)),
                ('next_job_run', models.DateTimeField(default=None, null=True, editable=False)),
                (
                    'status',
                    models.CharField(
                        default='ok',
                        max_length=32,
                        editable=False,
                        choices=[
                            ('new', 'New'),
                            ('pending', 'Pending'),
                            ('waiting', 'Waiting'),
                            ('running', 'Running'),
                            ('successful', 'Successful'),
                            ('failed', 'Failed'),
                            ('error', 'Error'),
                            ('canceled', 'Canceled'),
                            ('never updated', 'Never Updated'),
                            ('ok', 'OK'),
                            ('missing', 'Missing'),
                            ('none', 'No External Source'),
                            ('updating', 'Updating'),
                        ],
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='AdHocCommand',
            fields=[
                (
                    'unifiedjob_ptr',
                    models.OneToOneField(
                        parent_link=True,
                        auto_created=True,
                        primary_key=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        serialize=False,
                        to='main.UnifiedJob',
                    ),
                ),
                ('job_type', models.CharField(default='run', max_length=64, choices=[('run', 'Run'), ('check', 'Check')])),
                ('limit', models.CharField(default='', max_length=1024, blank=True)),
                ('module_name', models.CharField(default='', max_length=1024, blank=True)),
                ('module_args', models.TextField(default='', blank=True)),
                ('forks', models.PositiveIntegerField(default=0, blank=True)),
                (
                    'verbosity',
                    models.PositiveIntegerField(
                        default=0,
                        blank=True,
                        choices=[
                            (0, '0 (Normal)'),
                            (1, '1 (Verbose)'),
                            (2, '2 (More Verbose)'),
                            (3, '3 (Debug)'),
                            (4, '4 (Connection Debug)'),
                            (5, '5 (WinRM Debug)'),
                        ],
                    ),
                ),
                ('become_enabled', models.BooleanField(default=False)),
            ],
            bases=('main.unifiedjob',),
        ),
        migrations.CreateModel(
            name='InventorySource',
            fields=[
                (
                    'unifiedjobtemplate_ptr',
                    models.OneToOneField(
                        parent_link=True,
                        auto_created=True,
                        primary_key=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        serialize=False,
                        to='main.UnifiedJobTemplate',
                    ),
                ),
                (
                    'source',
                    models.CharField(
                        default='',
                        max_length=32,
                        blank=True,
                        choices=[
                            ('', 'Manual'),
                            ('file', 'Local File, Directory or Script'),
                            ('rax', 'Rackspace Cloud Servers'),
                            ('ec2', 'Amazon EC2'),
                            ('gce', 'Google Compute Engine'),
                            ('azure', 'Microsoft Azure'),
                            ('vmware', 'VMware vCenter'),
                            ('openstack', 'OpenStack'),
                            ('custom', 'Custom Script'),
                        ],
                    ),
                ),
                ('source_path', models.CharField(default='', max_length=1024, editable=False, blank=True)),
                ('source_vars', models.TextField(default='', help_text='Inventory source variables in YAML or JSON format.', blank=True)),
                ('source_regions', models.CharField(default='', max_length=1024, blank=True)),
                (
                    'instance_filters',
                    models.CharField(
                        default='',
                        help_text='Comma-separated list of filter expressions (EC2 only). Hosts are imported when ANY of the filters match.',
                        max_length=1024,
                        blank=True,
                    ),
                ),
                (
                    'group_by',
                    models.CharField(default='', help_text='Limit groups automatically created from inventory source (EC2 only).', max_length=1024, blank=True),
                ),
                ('overwrite', models.BooleanField(default=False, help_text='Overwrite local groups and hosts from remote inventory source.')),
                ('overwrite_vars', models.BooleanField(default=False, help_text='Overwrite local variables from remote inventory source.')),
                ('update_on_launch', models.BooleanField(default=False)),
                ('update_cache_timeout', models.PositiveIntegerField(default=0)),
            ],
            bases=('main.unifiedjobtemplate', models.Model),
        ),
        migrations.CreateModel(
            name='InventoryUpdate',
            fields=[
                (
                    'unifiedjob_ptr',
                    models.OneToOneField(
                        parent_link=True,
                        auto_created=True,
                        primary_key=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        serialize=False,
                        to='main.UnifiedJob',
                    ),
                ),
                (
                    'source',
                    models.CharField(
                        default='',
                        max_length=32,
                        blank=True,
                        choices=[
                            ('', 'Manual'),
                            ('file', 'Local File, Directory or Script'),
                            ('rax', 'Rackspace Cloud Servers'),
                            ('ec2', 'Amazon EC2'),
                            ('gce', 'Google Compute Engine'),
                            ('azure', 'Microsoft Azure'),
                            ('vmware', 'VMware vCenter'),
                            ('openstack', 'OpenStack'),
                            ('custom', 'Custom Script'),
                        ],
                    ),
                ),
                ('source_path', models.CharField(default='', max_length=1024, editable=False, blank=True)),
                ('source_vars', models.TextField(default='', help_text='Inventory source variables in YAML or JSON format.', blank=True)),
                ('source_regions', models.CharField(default='', max_length=1024, blank=True)),
                (
                    'instance_filters',
                    models.CharField(
                        default='',
                        help_text='Comma-separated list of filter expressions (EC2 only). Hosts are imported when ANY of the filters match.',
                        max_length=1024,
                        blank=True,
                    ),
                ),
                (
                    'group_by',
                    models.CharField(default='', help_text='Limit groups automatically created from inventory source (EC2 only).', max_length=1024, blank=True),
                ),
                ('overwrite', models.BooleanField(default=False, help_text='Overwrite local groups and hosts from remote inventory source.')),
                ('overwrite_vars', models.BooleanField(default=False, help_text='Overwrite local variables from remote inventory source.')),
                ('license_error', models.BooleanField(default=False, editable=False)),
            ],
            bases=('main.unifiedjob', models.Model),
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                (
                    'unifiedjob_ptr',
                    models.OneToOneField(
                        parent_link=True,
                        auto_created=True,
                        primary_key=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        serialize=False,
                        to='main.UnifiedJob',
                    ),
                ),
                ('job_type', models.CharField(default='run', max_length=64, choices=[('run', 'Run'), ('check', 'Check'), ('scan', 'Scan')])),
                ('playbook', models.CharField(default='', max_length=1024, blank=True)),
                ('forks', models.PositiveIntegerField(default=0, blank=True)),
                ('limit', models.CharField(default='', max_length=1024, blank=True)),
                (
                    'verbosity',
                    models.PositiveIntegerField(
                        default=0,
                        blank=True,
                        choices=[
                            (0, '0 (Normal)'),
                            (1, '1 (Verbose)'),
                            (2, '2 (More Verbose)'),
                            (3, '3 (Debug)'),
                            (4, '4 (Connection Debug)'),
                            (5, '5 (WinRM Debug)'),
                        ],
                    ),
                ),
                ('extra_vars', models.TextField(default='', blank=True)),
                ('job_tags', models.CharField(default='', max_length=1024, blank=True)),
                ('force_handlers', models.BooleanField(blank=True, default=False)),
                ('skip_tags', models.CharField(default='', max_length=1024, blank=True)),
                ('start_at_task', models.CharField(default='', max_length=1024, blank=True)),
                ('become_enabled', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('id',),
            },
            bases=('main.unifiedjob', models.Model),
        ),
        migrations.CreateModel(
            name='JobTemplate',
            fields=[
                (
                    'unifiedjobtemplate_ptr',
                    models.OneToOneField(
                        parent_link=True,
                        auto_created=True,
                        primary_key=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        serialize=False,
                        to='main.UnifiedJobTemplate',
                    ),
                ),
                ('job_type', models.CharField(default='run', max_length=64, choices=[('run', 'Run'), ('check', 'Check'), ('scan', 'Scan')])),
                ('playbook', models.CharField(default='', max_length=1024, blank=True)),
                ('forks', models.PositiveIntegerField(default=0, blank=True)),
                ('limit', models.CharField(default='', max_length=1024, blank=True)),
                (
                    'verbosity',
                    models.PositiveIntegerField(
                        default=0,
                        blank=True,
                        choices=[
                            (0, '0 (Normal)'),
                            (1, '1 (Verbose)'),
                            (2, '2 (More Verbose)'),
                            (3, '3 (Debug)'),
                            (4, '4 (Connection Debug)'),
                            (5, '5 (WinRM Debug)'),
                        ],
                    ),
                ),
                ('extra_vars', models.TextField(default='', blank=True)),
                ('job_tags', models.CharField(default='', max_length=1024, blank=True)),
                ('force_handlers', models.BooleanField(blank=True, default=False)),
                ('skip_tags', models.CharField(default='', max_length=1024, blank=True)),
                ('start_at_task', models.CharField(default='', max_length=1024, blank=True)),
                ('become_enabled', models.BooleanField(default=False)),
                ('host_config_key', models.CharField(default='', max_length=1024, blank=True)),
                ('ask_variables_on_launch', models.BooleanField(default=False)),
                ('survey_enabled', models.BooleanField(default=False)),
                ('survey_spec', models.JSONField(default=dict, blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=('main.unifiedjobtemplate', models.Model),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                (
                    'unifiedjobtemplate_ptr',
                    models.OneToOneField(
                        parent_link=True,
                        auto_created=True,
                        primary_key=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        serialize=False,
                        to='main.UnifiedJobTemplate',
                    ),
                ),
                (
                    'local_path',
                    models.CharField(
                        help_text='Local path (relative to PROJECTS_ROOT) containing playbooks and related files for this project.', max_length=1024, blank=True
                    ),
                ),
                (
                    'scm_type',
                    models.CharField(
                        default='',
                        max_length=8,
                        verbose_name='SCM Type',
                        blank=True,
                        choices=[('', 'Manual'), ('git', 'Git'), ('hg', 'Mercurial'), ('svn', 'Subversion')],
                    ),
                ),
                ('scm_url', models.CharField(default='', max_length=1024, verbose_name='SCM URL', blank=True)),
                (
                    'scm_branch',
                    models.CharField(
                        default='', help_text='Specific branch, tag or commit to checkout.', max_length=256, verbose_name='SCM Branch', blank=True
                    ),
                ),
                ('scm_clean', models.BooleanField(default=False)),
                ('scm_delete_on_update', models.BooleanField(default=False)),
                ('scm_delete_on_next_update', models.BooleanField(default=False, editable=False)),
                ('scm_update_on_launch', models.BooleanField(default=False)),
                ('scm_update_cache_timeout', models.PositiveIntegerField(default=0, blank=True)),
            ],
            options={
                'ordering': ('id',),
            },
            bases=('main.unifiedjobtemplate', models.Model),
        ),
        migrations.CreateModel(
            name='ProjectUpdate',
            fields=[
                (
                    'unifiedjob_ptr',
                    models.OneToOneField(
                        parent_link=True,
                        auto_created=True,
                        primary_key=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        serialize=False,
                        to='main.UnifiedJob',
                    ),
                ),
                (
                    'local_path',
                    models.CharField(
                        help_text='Local path (relative to PROJECTS_ROOT) containing playbooks and related files for this project.', max_length=1024, blank=True
                    ),
                ),
                (
                    'scm_type',
                    models.CharField(
                        default='',
                        max_length=8,
                        verbose_name='SCM Type',
                        blank=True,
                        choices=[('', 'Manual'), ('git', 'Git'), ('hg', 'Mercurial'), ('svn', 'Subversion')],
                    ),
                ),
                ('scm_url', models.CharField(default='', max_length=1024, verbose_name='SCM URL', blank=True)),
                (
                    'scm_branch',
                    models.CharField(
                        default='', help_text='Specific branch, tag or commit to checkout.', max_length=256, verbose_name='SCM Branch', blank=True
                    ),
                ),
                ('scm_clean', models.BooleanField(default=False)),
                ('scm_delete_on_update', models.BooleanField(default=False)),
            ],
            bases=('main.unifiedjob', models.Model),
        ),
        migrations.CreateModel(
            name='SystemJob',
            fields=[
                (
                    'unifiedjob_ptr',
                    models.OneToOneField(
                        parent_link=True,
                        auto_created=True,
                        primary_key=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        serialize=False,
                        to='main.UnifiedJob',
                    ),
                ),
                (
                    'job_type',
                    models.CharField(
                        default='',
                        max_length=32,
                        blank=True,
                        choices=[
                            ('cleanup_jobs', 'Remove jobs older than a certain number of days'),
                            ('cleanup_activitystream', 'Remove activity stream entries older than a certain number of days'),
                            ('cleanup_deleted', 'Purge previously deleted items from the database'),
                            ('cleanup_facts', 'Purge and/or reduce the granularity of system tracking data'),
                        ],
                    ),
                ),
                ('extra_vars', models.TextField(default='', blank=True)),
            ],
            options={
                'ordering': ('id',),
            },
            bases=('main.unifiedjob', models.Model),
        ),
        migrations.CreateModel(
            name='SystemJobTemplate',
            fields=[
                (
                    'unifiedjobtemplate_ptr',
                    models.OneToOneField(
                        parent_link=True,
                        auto_created=True,
                        primary_key=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        serialize=False,
                        to='main.UnifiedJobTemplate',
                    ),
                ),
                (
                    'job_type',
                    models.CharField(
                        default='',
                        max_length=32,
                        blank=True,
                        choices=[
                            ('cleanup_jobs', 'Remove jobs older than a certain number of days'),
                            ('cleanup_activitystream', 'Remove activity stream entries older than a certain number of days'),
                            ('cleanup_deleted', 'Purge previously deleted items from the database'),
                            ('cleanup_facts', 'Purge and/or reduce the granularity of system tracking data'),
                        ],
                    ),
                ),
            ],
            bases=('main.unifiedjobtemplate', models.Model),
        ),
        migrations.AddField(
            model_name='unifiedjobtemplate',
            name='created_by',
            field=models.ForeignKey(
                related_name="{u'class': 'unifiedjobtemplate', u'app_label': 'main'}(class)s_created+",
                on_delete=django.db.models.deletion.SET_NULL,
                default=None,
                editable=False,
                to=settings.AUTH_USER_MODEL,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='unifiedjobtemplate',
            name='current_job',
            field=models.ForeignKey(
                related_name='unifiedjobtemplate_as_current_job+',
                on_delete=django.db.models.deletion.SET_NULL,
                default=None,
                editable=False,
                to='main.UnifiedJob',
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='unifiedjobtemplate',
            name='last_job',
            field=models.ForeignKey(
                related_name='unifiedjobtemplate_as_last_job+',
                on_delete=django.db.models.deletion.SET_NULL,
                default=None,
                editable=False,
                to='main.UnifiedJob',
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='unifiedjobtemplate',
            name='modified_by',
            field=models.ForeignKey(
                related_name="{u'class': 'unifiedjobtemplate', u'app_label': 'main'}(class)s_modified+",
                on_delete=django.db.models.deletion.SET_NULL,
                default=None,
                editable=False,
                to=settings.AUTH_USER_MODEL,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='unifiedjobtemplate',
            name='next_schedule',
            field=models.ForeignKey(
                related_name='unifiedjobtemplate_as_next_schedule+',
                on_delete=django.db.models.deletion.SET_NULL,
                default=None,
                editable=False,
                to='main.Schedule',
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='unifiedjobtemplate',
            name='polymorphic_ctype',
            field=models.ForeignKey(
                related_name='polymorphic_main.unifiedjobtemplate_set+',
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                to='contenttypes.ContentType',
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='unifiedjobtemplate',
            name='tags',
            field=taggit.managers.TaggableManager(
                to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'
            ),
        ),
        migrations.AddField(
            model_name='unifiedjob',
            name='created_by',
            field=models.ForeignKey(
                related_name="{u'class': 'unifiedjob', u'app_label': 'main'}(class)s_created+",
                on_delete=django.db.models.deletion.SET_NULL,
                default=None,
                editable=False,
                to=settings.AUTH_USER_MODEL,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='unifiedjob',
            name='dependent_jobs',
            field=models.ManyToManyField(related_name='_unifiedjob_dependent_jobs_+', editable=False, to='main.UnifiedJob'),
        ),
        migrations.AddField(
            model_name='unifiedjob',
            name='modified_by',
            field=models.ForeignKey(
                related_name="{u'class': 'unifiedjob', u'app_label': 'main'}(class)s_modified+",
                on_delete=django.db.models.deletion.SET_NULL,
                default=None,
                editable=False,
                to=settings.AUTH_USER_MODEL,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='unifiedjob',
            name='polymorphic_ctype',
            field=models.ForeignKey(
                related_name='polymorphic_main.unifiedjob_set+',
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                to='contenttypes.ContentType',
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='unifiedjob',
            name='schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, editable=False, to='main.Schedule', null=True),
        ),
        migrations.AddField(
            model_name='unifiedjob',
            name='tags',
            field=taggit.managers.TaggableManager(
                to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'
            ),
        ),
        migrations.AddField(
            model_name='unifiedjob',
            name='unified_job_template',
            field=models.ForeignKey(
                related_name='unifiedjob_unified_jobs',
                on_delete=django.db.models.deletion.SET_NULL,
                default=None,
                editable=False,
                to='main.UnifiedJobTemplate',
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='schedule',
            name='unified_job_template',
            field=models.ForeignKey(related_name='schedules', on_delete=django.db.models.deletion.CASCADE, to='main.UnifiedJobTemplate'),
        ),
        migrations.AddField(
            model_name='permission',
            name='team',
            field=models.ForeignKey(related_name='permissions', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='main.Team', null=True),
        ),
        migrations.AddField(
            model_name='permission',
            name='user',
            field=models.ForeignKey(
                related_name='permissions', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True
            ),
        ),
        migrations.AddField(
            model_name='joborigin',
            name='unified_job',
            field=models.OneToOneField(related_name='job_origin', on_delete=django.db.models.deletion.CASCADE, to='main.UnifiedJob'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='organization',
            field=models.ForeignKey(
                related_name='inventories',
                on_delete=django.db.models.deletion.CASCADE,
                to='main.Organization',
                help_text='Organization containing this inventory.',
            ),
        ),
        migrations.AddField(
            model_name='inventory',
            name='tags',
            field=taggit.managers.TaggableManager(
                to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'
            ),
        ),
        migrations.AddField(
            model_name='host',
            name='inventory',
            field=models.ForeignKey(related_name='hosts', on_delete=django.db.models.deletion.CASCADE, to='main.Inventory'),
        ),
        migrations.AddField(
            model_name='host',
            name='last_job_host_summary',
            field=models.ForeignKey(
                related_name='hosts_as_last_job_summary+',
                on_delete=django.db.models.deletion.SET_NULL,
                default=None,
                blank=True,
                editable=False,
                to='main.JobHostSummary',
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='host',
            name='modified_by',
            field=models.ForeignKey(
                related_name="{u'class': 'host', u'app_label': 'main'}(class)s_modified+",
                on_delete=django.db.models.deletion.SET_NULL,
                default=None,
                editable=False,
                to=settings.AUTH_USER_MODEL,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='host',
            name='tags',
            field=taggit.managers.TaggableManager(
                to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'
            ),
        ),
        migrations.AddField(
            model_name='group',
            name='hosts',
            field=models.ManyToManyField(help_text='Hosts associated directly with this group.', related_name='groups', to='main.Host', blank=True),
        ),
        migrations.AddField(
            model_name='group',
            name='inventory',
            field=models.ForeignKey(related_name='groups', on_delete=django.db.models.deletion.CASCADE, to='main.Inventory'),
        ),
        migrations.AddField(
            model_name='group',
            name='modified_by',
            field=models.ForeignKey(
                related_name="{u'class': 'group', u'app_label': 'main'}(class)s_modified+",
                on_delete=django.db.models.deletion.SET_NULL,
                default=None,
                editable=False,
                to=settings.AUTH_USER_MODEL,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='group',
            name='parents',
            field=models.ManyToManyField(related_name='children', to='main.Group', blank=True),
        ),
        migrations.AddField(
            model_name='group',
            name='tags',
            field=taggit.managers.TaggableManager(
                to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'
            ),
        ),
        migrations.AddField(
            model_name='custominventoryscript',
            name='organization',
            field=models.ForeignKey(
                related_name='custom_inventory_scripts',
                on_delete=django.db.models.deletion.SET_NULL,
                to='main.Organization',
                help_text='Organization owning this inventory script',
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='custominventoryscript',
            name='tags',
            field=taggit.managers.TaggableManager(
                to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'
            ),
        ),
        migrations.AddField(
            model_name='credential',
            name='team',
            field=models.ForeignKey(
                related_name='credentials', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='main.Team', null=True
            ),
        ),
        migrations.AddField(
            model_name='credential',
            name='user',
            field=models.ForeignKey(
                related_name='credentials', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True
            ),
        ),
        migrations.AddField(
            model_name='adhoccommandevent',
            name='host',
            field=models.ForeignKey(
                related_name='ad_hoc_command_events', on_delete=django.db.models.deletion.SET_NULL, default=None, editable=False, to='main.Host', null=True
            ),
        ),
        migrations.AddField(
            model_name='activitystream',
            name='credential',
            field=models.ManyToManyField(to='main.Credential', blank=True),
        ),
        migrations.AddField(
            model_name='activitystream',
            name='custom_inventory_script',
            field=models.ManyToManyField(to='main.CustomInventoryScript', blank=True),
        ),
        migrations.AddField(
            model_name='activitystream',
            name='group',
            field=models.ManyToManyField(to='main.Group', blank=True),
        ),
        migrations.AddField(
            model_name='activitystream',
            name='host',
            field=models.ManyToManyField(to='main.Host', blank=True),
        ),
        migrations.AddField(
            model_name='activitystream',
            name='inventory',
            field=models.ManyToManyField(to='main.Inventory', blank=True),
        ),
        migrations.AddField(
            model_name='activitystream',
            name='organization',
            field=models.ManyToManyField(to='main.Organization', blank=True),
        ),
        migrations.AddField(
            model_name='activitystream',
            name='permission',
            field=models.ManyToManyField(to='main.Permission', blank=True),
        ),
        migrations.AddField(
            model_name='activitystream',
            name='schedule',
            field=models.ManyToManyField(to='main.Schedule', blank=True),
        ),
        migrations.AddField(
            model_name='activitystream',
            name='team',
            field=models.ManyToManyField(to='main.Team', blank=True),
        ),
        migrations.AddField(
            model_name='activitystream',
            name='unified_job',
            field=models.ManyToManyField(related_name='_activitystream_unified_job_+', to='main.UnifiedJob', blank=True),
        ),
        migrations.AddField(
            model_name='activitystream',
            name='unified_job_template',
            field=models.ManyToManyField(related_name='_activitystream_unified_job_template_+', to='main.UnifiedJobTemplate', blank=True),
        ),
        migrations.AddField(
            model_name='activitystream',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='unifiedjobtemplate',
            unique_together=set([('polymorphic_ctype', 'name')]),
        ),
        migrations.AddField(
            model_name='team',
            name='projects',
            field=models.ManyToManyField(related_name='teams', to='main.Project', blank=True),
        ),
        migrations.AddField(
            model_name='systemjob',
            name='system_job_template',
            field=models.ForeignKey(
                related_name='jobs', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='main.SystemJobTemplate', null=True
            ),
        ),
        migrations.AddField(
            model_name='projectupdate',
            name='credential',
            field=models.ForeignKey(
                related_name='projectupdates', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='main.Credential', null=True
            ),
        ),
        migrations.AddField(
            model_name='projectupdate',
            name='project',
            field=models.ForeignKey(related_name='project_updates', on_delete=django.db.models.deletion.CASCADE, editable=False, to='main.Project'),
        ),
        migrations.AddField(
            model_name='project',
            name='credential',
            field=models.ForeignKey(
                related_name='projects', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='main.Credential', null=True
            ),
        ),
        migrations.AddField(
            model_name='permission',
            name='project',
            field=models.ForeignKey(related_name='permissions', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='main.Project', null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='projects',
            field=models.ManyToManyField(related_name='organizations', to='main.Project', blank=True),
        ),
        migrations.AddField(
            model_name='jobtemplate',
            name='cloud_credential',
            field=models.ForeignKey(
                related_name='jobtemplates_as_cloud_credential+',
                on_delete=django.db.models.deletion.SET_NULL,
                default=None,
                blank=True,
                to='main.Credential',
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='jobtemplate',
            name='credential',
            field=models.ForeignKey(
                related_name='jobtemplates', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='main.Credential', null=True
            ),
        ),
        migrations.AddField(
            model_name='jobtemplate',
            name='inventory',
            field=models.ForeignKey(related_name='jobtemplates', on_delete=django.db.models.deletion.SET_NULL, to='main.Inventory', null=True),
        ),
        migrations.AddField(
            model_name='jobtemplate',
            name='project',
            field=models.ForeignKey(
                related_name='jobtemplates', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='main.Project', null=True
            ),
        ),
        migrations.AddField(
            model_name='jobhostsummary',
            name='job',
            field=models.ForeignKey(related_name='job_host_summaries', on_delete=django.db.models.deletion.CASCADE, editable=False, to='main.Job'),
        ),
        migrations.AddField(
            model_name='jobevent',
            name='job',
            field=models.ForeignKey(related_name='job_events', on_delete=django.db.models.deletion.CASCADE, editable=False, to='main.Job'),
        ),
        migrations.AddField(
            model_name='job',
            name='cloud_credential',
            field=models.ForeignKey(
                related_name='jobs_as_cloud_credential+',
                on_delete=django.db.models.deletion.SET_NULL,
                default=None,
                blank=True,
                to='main.Credential',
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='job',
            name='credential',
            field=models.ForeignKey(
                related_name='jobs', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='main.Credential', null=True
            ),
        ),
        migrations.AddField(
            model_name='job',
            name='hosts',
            field=models.ManyToManyField(related_name='jobs', editable=False, through='main.JobHostSummary', to='main.Host'),
        ),
        migrations.AddField(
            model_name='job',
            name='inventory',
            field=models.ForeignKey(related_name='jobs', on_delete=django.db.models.deletion.SET_NULL, to='main.Inventory', null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='job_template',
            field=models.ForeignKey(
                related_name='jobs', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='main.JobTemplate', null=True
            ),
        ),
        migrations.AddField(
            model_name='job',
            name='project',
            field=models.ForeignKey(related_name='jobs', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='main.Project', null=True),
        ),
        migrations.AddField(
            model_name='inventoryupdate',
            name='credential',
            field=models.ForeignKey(
                related_name='inventoryupdates', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='main.Credential', null=True
            ),
        ),
        migrations.AddField(
            model_name='inventoryupdate',
            name='inventory_source',
            field=models.ForeignKey(related_name='inventory_updates', on_delete=django.db.models.deletion.CASCADE, editable=False, to='main.InventorySource'),
        ),
        migrations.AddField(
            model_name='inventoryupdate',
            name='source_script',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='main.CustomInventoryScript', null=True),
        ),
        migrations.AddField(
            model_name='inventorysource',
            name='credential',
            field=models.ForeignKey(
                related_name='inventorysources', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='main.Credential', null=True
            ),
        ),
        migrations.AddField(
            model_name='inventorysource',
            name='group',
            field=awx.main.fields.AutoOneToOneField(
                related_name='inventory_source', on_delete=django.db.models.deletion.SET_NULL, null=True, default=None, editable=False, to='main.Group'
            ),
        ),
        migrations.AddField(
            model_name='inventorysource',
            name='inventory',
            field=models.ForeignKey(
                related_name='inventory_sources', on_delete=django.db.models.deletion.SET_NULL, default=None, editable=False, to='main.Inventory', null=True
            ),
        ),
        migrations.AddField(
            model_name='inventorysource',
            name='source_script',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='main.CustomInventoryScript', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='inventory',
            unique_together=set([('name', 'organization')]),
        ),
        migrations.AddField(
            model_name='host',
            name='inventory_sources',
            field=models.ManyToManyField(
                help_text='Inventory source(s) that created or modified this host.', related_name='hosts', editable=False, to='main.InventorySource'
            ),
        ),
        migrations.AddField(
            model_name='host',
            name='last_job',
            field=models.ForeignKey(
                related_name='hosts_as_last_job+', on_delete=django.db.models.deletion.SET_NULL, default=None, editable=False, to='main.Job', null=True
            ),
        ),
        migrations.AddField(
            model_name='group',
            name='inventory_sources',
            field=models.ManyToManyField(
                help_text='Inventory source(s) that created or modified this group.', related_name='groups', editable=False, to='main.InventorySource'
            ),
        ),
        migrations.AlterUniqueTogether(
            name='custominventoryscript',
            unique_together=set([('name', 'organization')]),
        ),
        migrations.AlterUniqueTogether(
            name='credential',
            unique_together=set([('user', 'team', 'kind', 'name')]),
        ),
        migrations.AddField(
            model_name='adhoccommandevent',
            name='ad_hoc_command',
            field=models.ForeignKey(related_name='ad_hoc_command_events', on_delete=django.db.models.deletion.CASCADE, editable=False, to='main.AdHocCommand'),
        ),
        migrations.AddField(
            model_name='adhoccommand',
            name='credential',
            field=models.ForeignKey(
                related_name='ad_hoc_commands', on_delete=django.db.models.deletion.SET_NULL, default=None, to='main.Credential', null=True
            ),
        ),
        migrations.AddField(
            model_name='adhoccommand',
            name='hosts',
            field=models.ManyToManyField(related_name='ad_hoc_commands', editable=False, through='main.AdHocCommandEvent', to='main.Host'),
        ),
        migrations.AddField(
            model_name='adhoccommand',
            name='inventory',
            field=models.ForeignKey(related_name='ad_hoc_commands', on_delete=django.db.models.deletion.SET_NULL, to='main.Inventory', null=True),
        ),
        migrations.AddField(
            model_name='activitystream',
            name='ad_hoc_command',
            field=models.ManyToManyField(to='main.AdHocCommand', blank=True),
        ),
        migrations.AddField(
            model_name='activitystream',
            name='inventory_source',
            field=models.ManyToManyField(to='main.InventorySource', blank=True),
        ),
        migrations.AddField(
            model_name='activitystream',
            name='inventory_update',
            field=models.ManyToManyField(to='main.InventoryUpdate', blank=True),
        ),
        migrations.AddField(
            model_name='activitystream',
            name='job',
            field=models.ManyToManyField(to='main.Job', blank=True),
        ),
        migrations.AddField(
            model_name='activitystream',
            name='job_template',
            field=models.ManyToManyField(to='main.JobTemplate', blank=True),
        ),
        migrations.AddField(
            model_name='activitystream',
            name='project',
            field=models.ManyToManyField(to='main.Project', blank=True),
        ),
        migrations.AddField(
            model_name='activitystream',
            name='project_update',
            field=models.ManyToManyField(to='main.ProjectUpdate', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='team',
            unique_together=set([('organization', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='jobhostsummary',
            unique_together=set([('job', 'host_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='host',
            unique_together=set([('name', 'inventory')]),
        ),
        migrations.AlterUniqueTogether(
            name='group',
            unique_together=set([('name', 'inventory')]),
        ),
        migrations.AlterUniqueTogether(
            name='adhoccommandevent',
            unique_together=set([('ad_hoc_command', 'host_name')]),
        ),
    ]
