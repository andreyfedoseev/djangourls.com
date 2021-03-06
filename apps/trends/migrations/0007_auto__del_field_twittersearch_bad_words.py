# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'TwitterSearch.bad_words'
        db.delete_column('trends_twittersearch', 'bad_words')


    def backwards(self, orm):
        # Adding field 'TwitterSearch.bad_words'
        db.add_column('trends_twittersearch', 'bad_words',
                      self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True),
                      keep_default=False)


    models = {
        'trends.mention': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'Mention'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'trend': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['trends.TrendItem']"})
        },
        'trends.trenditem': {
            'Meta': {'object_name': 'TrendItem'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'displayed': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500', 'db_index': 'True'})
        },
        'trends.twittermention': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'TwitterMention', '_ormbases': ['trends.Mention']},
            'mention_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['trends.Mention']", 'unique': 'True', 'primary_key': 'True'}),
            'tweet_id': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'})
        },
        'trends.twittersearch': {
            'Meta': {'object_name': 'TwitterSearch'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_tweet_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['trends']