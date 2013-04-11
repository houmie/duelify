# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'duelify_app_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=35)),
        ))
        db.send_create_signal(u'duelify_app', ['Category'])

        # Adding model 'Ring'
        db.create_table(u'duelify_app_ring', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['duelify_app.Category'], null=True, blank=True)),
            ('topic', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('rule', self.gf('django.db.models.fields.CharField')(default='public', max_length=8)),
        ))
        db.send_create_signal(u'duelify_app', ['Ring'])

        # Adding M2M table for field red on 'Ring'
        db.create_table(u'duelify_app_ring_red', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ring', models.ForeignKey(orm[u'duelify_app.ring'], null=False)),
            ('user', models.ForeignKey(orm[u'duelify_app.user'], null=False))
        ))
        db.create_unique(u'duelify_app_ring_red', ['ring_id', 'user_id'])

        # Adding M2M table for field blue on 'Ring'
        db.create_table(u'duelify_app_ring_blue', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ring', models.ForeignKey(orm[u'duelify_app.ring'], null=False)),
            ('user', models.ForeignKey(orm[u'duelify_app.user'], null=False))
        ))
        db.create_unique(u'duelify_app_ring_blue', ['ring_id', 'user_id'])

        # Adding model 'Punch'
        db.create_table(u'duelify_app_punch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ring', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['duelify_app.Ring'])),
            ('speaker', self.gf('django.db.models.fields.related.ForeignKey')(related_name='speaker', to=orm['duelify_app.User'])),
            ('side', self.gf('django.db.models.fields.CharField')(default='blue', max_length=4)),
            ('discussion', self.gf('django.db.models.fields.TextField')()),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'duelify_app', ['Punch'])

        # Adding M2M table for field voters on 'Punch'
        db.create_table(u'duelify_app_punch_voters', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('punch', models.ForeignKey(orm[u'duelify_app.punch'], null=False)),
            ('user', models.ForeignKey(orm[u'duelify_app.user'], null=False))
        ))
        db.create_unique(u'duelify_app_punch_voters', ['punch_id', 'user_id'])

        # Adding model 'DuelInvitation'
        db.create_table(u'duelify_app_duelinvitation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['duelify_app.User'])),
            ('ring', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['duelify_app.Ring'])),
        ))
        db.send_create_signal(u'duelify_app', ['DuelInvitation'])

        # Adding model 'User'
        db.create_table(u'duelify_app_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=255, db_index=True)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('browser', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('score', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'duelify_app', ['User'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'duelify_app_category')

        # Deleting model 'Ring'
        db.delete_table(u'duelify_app_ring')

        # Removing M2M table for field red on 'Ring'
        db.delete_table('duelify_app_ring_red')

        # Removing M2M table for field blue on 'Ring'
        db.delete_table('duelify_app_ring_blue')

        # Deleting model 'Punch'
        db.delete_table(u'duelify_app_punch')

        # Removing M2M table for field voters on 'Punch'
        db.delete_table('duelify_app_punch_voters')

        # Deleting model 'DuelInvitation'
        db.delete_table(u'duelify_app_duelinvitation')

        # Deleting model 'User'
        db.delete_table(u'duelify_app_user')


    models = {
        u'duelify_app.category': {
            'Meta': {'object_name': 'Category'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'duelify_app.duelinvitation': {
            'Meta': {'object_name': 'DuelInvitation'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ring': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['duelify_app.Ring']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['duelify_app.User']"})
        },
        u'duelify_app.punch': {
            'Meta': {'object_name': 'Punch'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'discussion': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ring': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['duelify_app.Ring']"}),
            'side': ('django.db.models.fields.CharField', [], {'default': "'blue'", 'max_length': '4'}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'speaker'", 'to': u"orm['duelify_app.User']"}),
            'voters': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['duelify_app.User']", 'null': 'True', 'blank': 'True'})
        },
        u'duelify_app.ring': {
            'Meta': {'object_name': 'Ring'},
            'blue': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'blue_users'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['duelify_app.User']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['duelify_app.Category']", 'null': 'True', 'blank': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'red': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'red_users'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['duelify_app.User']"}),
            'rule': ('django.db.models.fields.CharField', [], {'default': "'public'", 'max_length': '8'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'duelify_app.user': {
            'Meta': {'object_name': 'User'},
            'browser': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'score': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['duelify_app']