# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'DiigoSearch'
        db.delete_table('trends_diigosearch')

        # Deleting model 'DeliciousMention'
        db.delete_table('trends_deliciousmention')

        # Deleting model 'DeliciousSearch'
        db.delete_table('trends_delicioussearch')

        # Deleting model 'DiigoMention'
        db.delete_table('trends_diigomention')


    def backwards(self, orm):
        # Adding model 'DiigoSearch'
        db.create_table('trends_diigosearch', (
            ('last_fetched', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('trends', ['DiigoSearch'])

        # Adding model 'DeliciousMention'
        db.create_table('trends_deliciousmention', (
            ('username', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('mention_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['trends.Mention'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('trends', ['DeliciousMention'])

        # Adding model 'DeliciousSearch'
        db.create_table('trends_delicioussearch', (
            ('last_fetched', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('trends', ['DeliciousSearch'])

        # Adding model 'DiigoMention'
        db.create_table('trends_diigomention', (
            ('username', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('mention_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['trends.Mention'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('trends', ['DiigoMention'])


    models = {
        'trends.mention': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'Mention'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'trend': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['trends.TrendItem']"})
        },
        'trends.trenditem': {
            'Meta': {'object_name': 'TrendItem'},
            'broken': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500'})
        },
        'trends.twittermention': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'TwitterMention', '_ormbases': ['trends.Mention']},
            'mention_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['trends.Mention']", 'unique': 'True', 'primary_key': 'True'}),
            'tweet_id': ('django.db.models.fields.BigIntegerField', [], {})
        },
        'trends.twittersearch': {
            'Meta': {'object_name': 'TwitterSearch'},
            'bad_words': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_tweet_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['trends']