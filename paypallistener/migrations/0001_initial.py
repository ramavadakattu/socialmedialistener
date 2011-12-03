
from south.db import db
from django.db import models
from paypallistener.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Entry'
        db.create_table('paypallistener_entry', (
            ('id', orm['paypallistener.Entry:id']),
            ('url', orm['paypallistener.Entry:url']),
            ('title', orm['paypallistener.Entry:title']),
            ('htmltitle', orm['paypallistener.Entry:htmltitle']),
            ('description', orm['paypallistener.Entry:description']),
            ('noofshares', orm['paypallistener.Entry:noofshares']),
            ('service', orm['paypallistener.Entry:service']),
            ('examined', orm['paypallistener.Entry:examined']),
            ('entry_pdate', orm['paypallistener.Entry:entry_pdate']),
            ('entry_pdatetime', orm['paypallistener.Entry:entry_pdatetime']),
            ('entry_createdon', orm['paypallistener.Entry:entry_createdon']),
            ('enty_updatedon', orm['paypallistener.Entry:enty_updatedon']),
            ('entrycreatedgmt', orm['paypallistener.Entry:entrycreatedgmt']),
        ))
        db.send_create_signal('paypallistener', ['Entry'])
        
        # Adding model 'Stats'
        db.create_table('paypallistener_stats', (
            ('id', orm['paypallistener.Stats:id']),
            ('whichcron', orm['paypallistener.Stats:whichcron']),
            ('createdon', orm['paypallistener.Stats:createdon']),
            ('updatedon', orm['paypallistener.Stats:updatedon']),
            ('totalentries', orm['paypallistener.Stats:totalentries']),
            ('totalsaved', orm['paypallistener.Stats:totalsaved']),
            ('howmanymoved', orm['paypallistener.Stats:howmanymoved']),
            ('howmanydeleted', orm['paypallistener.Stats:howmanydeleted']),
        ))
        db.send_create_signal('paypallistener', ['Stats'])
        
        # Adding model 'Xtag'
        db.create_table('paypallistener_xtag', (
            ('id', orm['paypallistener.Xtag:id']),
            ('name', orm['paypallistener.Xtag:name']),
            ('createdon', orm['paypallistener.Xtag:createdon']),
            ('updatedon', orm['paypallistener.Xtag:updatedon']),
        ))
        db.send_create_signal('paypallistener', ['Xtag'])
        
        # Adding model 'EntryUIDS'
        db.create_table('paypallistener_entryuids', (
            ('id', orm['paypallistener.EntryUIDS:id']),
            ('entry', orm['paypallistener.EntryUIDS:entry']),
            ('entryid', orm['paypallistener.EntryUIDS:entryid']),
        ))
        db.send_create_signal('paypallistener', ['EntryUIDS'])
        
        # Adding model 'NotEnglish'
        db.create_table('paypallistener_notenglish', (
            ('id', orm['paypallistener.NotEnglish:id']),
            ('text', orm['paypallistener.NotEnglish:text']),
            ('createdon', orm['paypallistener.NotEnglish:createdon']),
            ('updatedon', orm['paypallistener.NotEnglish:updatedon']),
        ))
        db.send_create_signal('paypallistener', ['NotEnglish'])
        
        # Adding model 'Weight'
        db.create_table('paypallistener_weight', (
            ('id', orm['paypallistener.Weight:id']),
            ('xtag', orm['paypallistener.Weight:xtag']),
            ('weight', orm['paypallistener.Weight:weight']),
            ('createdon', orm['paypallistener.Weight:createdon']),
            ('updatedon', orm['paypallistener.Weight:updatedon']),
        ))
        db.send_create_signal('paypallistener', ['Weight'])
        
        # Adding ManyToManyField 'Xtag.entries'
        db.create_table('paypallistener_xtag_entries', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('xtag', models.ForeignKey(orm.Xtag, null=False)),
            ('entry', models.ForeignKey(orm.Entry, null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Entry'
        db.delete_table('paypallistener_entry')
        
        # Deleting model 'Stats'
        db.delete_table('paypallistener_stats')
        
        # Deleting model 'Xtag'
        db.delete_table('paypallistener_xtag')
        
        # Deleting model 'EntryUIDS'
        db.delete_table('paypallistener_entryuids')
        
        # Deleting model 'NotEnglish'
        db.delete_table('paypallistener_notenglish')
        
        # Deleting model 'Weight'
        db.delete_table('paypallistener_weight')
        
        # Dropping ManyToManyField 'Xtag.entries'
        db.delete_table('paypallistener_xtag_entries')
        
    
    
    models = {
        'paypallistener.entry': {
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'entry_createdon': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'entry_pdate': ('django.db.models.fields.DateField', [], {}),
            'entry_pdatetime': ('django.db.models.fields.DateTimeField', [], {}),
            'entrycreatedgmt': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'enty_updatedon': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'examined': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'htmltitle': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '124', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'noofshares': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'service': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '1024'})
        },
        'paypallistener.entryuids': {
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['paypallistener.Entry']"}),
            'entryid': ('django.db.models.fields.CharField', [], {'max_length': '124', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
