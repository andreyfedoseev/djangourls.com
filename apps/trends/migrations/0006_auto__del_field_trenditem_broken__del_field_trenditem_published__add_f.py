# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'Mention', fields ['timestamp']
        db.create_index('trends_mention', ['timestamp'])

        # Deleting field 'TrendItem.broken'
        db.delete_column('trends_trenditem', 'broken')

        # Deleting field 'TrendItem.published'
        db.delete_column('trends_trenditem', 'published')

        # Adding field 'TrendItem.displayed'
        db.add_column('trends_trenditem', 'displayed',
                      self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, db_index=True, blank=True),
                      keep_default=False)

        # Adding index on 'TrendItem', fields ['url']
        db.create_index('trends_trenditem', ['url'])


        # Changing field 'TrendItem.timestamp'
        db.alter_column('trends_trenditem', 'timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))
        # Adding index on 'TrendItem', fields ['timestamp']
        db.create_index('trends_trenditem', ['timestamp'])

        # Adding index on 'TwitterMention', fields ['tweet_id']
        db.create_index('trends_twittermention', ['tweet_id'])


    def backwards(self, orm):
        # Removing index on 'TwitterMention', fields ['tweet_id']
        db.delete_index('trends_twittermention', ['tweet_id'])

        # Removing index on 'TrendItem', fields ['timestamp']
        db.delete_index('trends_trenditem', ['timestamp'])

        # Removing index on 'TrendItem', fields ['url']
        db.delete_index('trends_trenditem', ['url'])

        # Removing index on 'Mention', fields ['timestamp']
        db.delete_index('trends_mention', ['timestamp'])

        # Adding field 'TrendItem.broken'
        db.add_column('trends_trenditem', 'broken',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TrendItem.published'
        db.add_column('trends_trenditem', 'published',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'TrendItem.displayed'
        db.delete_column('trends_trenditem', 'displayed')


        # Changing field 'TrendItem.timestamp'
        db.alter_column('trends_trenditem', 'timestamp', self.gf('django.db.models.fields.DateTimeField')())

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
            'bad_words': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_tweet_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['trends']