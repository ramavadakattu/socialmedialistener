
from south.db import db
from django.db import models
from paypallistener.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'EntryUIDS.createdon'
        db.add_column('paypallistener_entryuids', 'createdon', orm['paypallistener.entryuids:createdon'])
        
        # Adding field 'EntryUIDS.updatedon'
        db.add_column('paypallistener_entryuids', 'updatedon', orm['paypallistener.entryuids:updatedon'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'EntryUIDS.createdon'
        db.delete_column('paypallistener_entryuids', 'createdon')
        
        # Deleting field 'EntryUIDS.updatedon'
        db.delete_column('paypallistener_entryuids', 'updatedon')
        
    
    
    models = {
        'paypallistener.entry': {
            'deliciouscount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'entry_createdon': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'entry_pdate': ('django.db.models.fields.DateField', [], {}),
            'entry_pdatetime': ('django.db.models.fields.DateTimeField', [], {}),
            'entrycreatedgmt': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'enty_updatedon': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'examined': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'facebookcount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'htmltitle': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '124', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'noofshares': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'readercount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'service': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'twittercount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '1024'})
        },
        'paypallistener.entryuids': {
            'createdon': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['paypallistener.Entry']"}),
            'entryid': ('django.db.models.fields.CharField', [], {'max_length': '124', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updatedon': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'paypallistener.notenglish': {
            'createdon': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'updatedon': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'paypallistener.stats': {
            'createdon': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'howmanydeleted': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'howmanymoved': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'totalentries': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'totalsaved': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'updatedon': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'whichcron': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'})
        },
        'paypallistener.weight': {
            'createdon': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updatedon': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'weight': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'xtag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['paypallistener.Xtag']"})
        },
        'paypallistener.xtag': {
            'createdon': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'entries': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['paypallistener.Entry']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'updatedon': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['paypallistener']
