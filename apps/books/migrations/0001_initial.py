# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BookSearch'
        db.create_table('books_booksearch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('browse_node', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('associate_tag', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('books', ['BookSearch'])


    def backwards(self, orm):
        # Deleting model 'BookSearch'
        db.delete_table('books_booksearch')


    models = {
        'books.booksearch': {
            'Meta': {'object_name': 'BookSearch'},
            'associate_tag': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'browse_node': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['books']