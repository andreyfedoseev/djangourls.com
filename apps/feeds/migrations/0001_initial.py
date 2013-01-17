# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Feed'
        db.create_table('feeds_feed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=300)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('source_url', self.gf('django.db.models.fields.URLField')(max_length=300, null=True, blank=True)),
            ('harvested', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('harvested_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('feeds', ['Feed'])

        # Adding model 'FeedItem'
        db.create_table('feeds_feeditem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=500, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feeds.Feed'])),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=500, db_index=True)),
            ('published_on', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('feeds', ['FeedItem'])


    def backwards(self, orm):
        # Deleting model 'Feed'
        db.delete_table('feeds_feed')

        # Deleting model 'FeedItem'
        db.delete_table('feeds_feeditem')


    models = {
        'feeds.feed': {
            'Meta': {'object_name': 'Feed'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'harvested': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'harvested_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '300'})
        },
        'feeds.feeditem': {
            'Meta': {'ordering': "['-published_on', '-timestamp']", 'object_name': 'FeedItem'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feeds.Feed']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_index': 'True'}),
            'published_on': ('django.db.models.fields.DateTimeField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500', 'db_index': 'True'})
        }
    }

    complete_apps = ['feeds']