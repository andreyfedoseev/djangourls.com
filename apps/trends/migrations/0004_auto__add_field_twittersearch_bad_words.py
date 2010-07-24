# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'TwitterSearch.bad_words'
        db.add_column('trends_twittersearch', 'bad_words', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Deleting field 'TwitterSearch.bad_words'
        db.delete_column('trends_twittersearch', 'bad_words')
    
    
    models = {
        'trends.deliciousmention': {
            'Meta': {'object_name': 'DeliciousMention', '_ormbases': ['trends.Mention']},
            'mention_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['trends.Mention']", 'unique': 'True', 'primary_key': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'trends.delicioussearch': {
            'Meta': {'object_name': 'DeliciousSearch'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_fetched': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'trends.diigomention': {
            'Meta': {'object_name': 'DiigoMention', '_ormbases': ['trends.Mention']},
            'mention_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['trends.Mention']", 'unique': 'True', 'primary_key': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'trends.diigosearch': {
            'Meta': {'object_name': 'DiigoSearch'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_fetched': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'trends.mention': {
            'Meta': {'object_name': 'Mention'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'trend': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['trends.TrendItem']"})
        },
        'trends.trenditem': {
            'Meta': {'object_name': 'TrendItem'},
            'broken': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500'})
        },
        'trends.twittermention': {
            'Meta': {'object_name': 'TwitterMention', '_ormbases': ['trends.Mention']},
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
