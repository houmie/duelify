# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'User.score'
        db.add_column(u'duelify_app_user', 'score',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'User.score'
        db.delete_column(u'duelify_app_user', 'score')


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
            'speaker': ('django.db.models.fields.CharField', [], {'default': "'red'", 'max_length': '4'}),
            'voters': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['duelify_app.User']", 'null': 'True', 'blank': 'True'})
        },
        u'duelify_app.ring': {
            'Meta': {'object_name': 'Ring'},
            'blue': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'blue_user'", 'null': 'True', 'to': u"orm['duelify_app.User']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['duelify_app.Category']", 'null': 'True', 'blank': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'red': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'red_user'", 'null': 'True', 'to': u"orm['duelify_app.User']"}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'duelify_app.user': {
            'Meta': {'object_name': 'User'},
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'score': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['duelify_app']