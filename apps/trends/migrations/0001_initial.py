# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'TrendItem'
        db.create_table('trends_trenditem', (
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=500)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('broken', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('trends', ['TrendItem'])

        # Adding model 'TwitterSearch'
        db.create_table('trends_twittersearch', (
            ('term', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_tweet_id', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('trends', ['TwitterSearch'])

        # Adding model 'DeliciousSearch'
        db.create_table('trends_delicioussearch', (
            ('last_fetched', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('trends', ['DeliciousSearch'])

        # Adding model 'DiigoSearch'
        db.create_table('trends_diigosearch', (
            ('last_fetched', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('trends', ['DiigoSearch'])

        # Adding model 'Mention'
        db.create_table('trends_mention', (
            ('trend', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trends.TrendItem'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('trends', ['Mention'])

        # Adding model 'TwitterMention'
        db.create_table('trends_twittermention', (
            ('tweet_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('mention_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['trends.Mention'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('trends', ['TwitterMention'])

        # Adding model 'DeliciousMention'
        db.create_table('trends_deliciousmention', (
            ('username', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('mention_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['trends.Mention'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('trends', ['DeliciousMention'])

        # Adding model 'DiigoMention'
        db.create_table('trends_diigomention', (
            ('username', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('mention_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['trends.Mention'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('trends', ['DiigoMention'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'TrendItem'
        db.delete_table('trends_trenditem')

        # Deleting model 'TwitterSearch'
        db.delete_table('trends_twittersearch')

        # Deleting model 'DeliciousSearch'
        db.delete_table('trends_delicioussearch')

        # Deleting model 'DiigoSearch'
        db.delete_table('trends_diigosearch')

        # Deleting model 'Mention'
        db.delete_table('trends_mention')

        # Deleting model 'TwitterMention'
        db.delete_table('trends_twittermention')

        # Deleting model 'DeliciousMention'
        db.delete_table('trends_deliciousmention')

        # Deleting model 'DiigoMention'
        db.delete_table('trends_diigomention')
    
    
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_tweet_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }
    
    complete_apps = ['trends']
