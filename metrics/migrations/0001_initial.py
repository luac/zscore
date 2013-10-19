# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MetricsProfile'
        db.create_table('metrics_metricsprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal('metrics', ['MetricsProfile'])

        # Adding M2M table for field metrics on 'MetricsProfile'
        db.create_table('metrics_metricsprofile_metrics', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('metricsprofile', models.ForeignKey(orm['metrics.metricsprofile'], null=False)),
            ('metricscategory', models.ForeignKey(orm['metrics.metricscategory'], null=False))
        ))
        db.create_unique('metrics_metricsprofile_metrics', ['metricsprofile_id', 'metricscategory_id'])

        # Adding model 'MetricsCategory'
        db.create_table('metrics_metricscategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('metrictype', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('minLabel', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('maxLabel', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('metricMax', self.gf('django.db.models.fields.SmallIntegerField')(default=7)),
        ))
        db.send_create_signal('metrics', ['MetricsCategory'])

        # Adding unique constraint on 'MetricsCategory', fields ['creator', 'name']
        db.create_unique('metrics_metricscategory', ['creator_id', 'name'])

        # Adding model 'MetricsInstance'
        db.create_table('metrics_metricsinstance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('metrics', ['MetricsInstance'])

        # Adding model 'SingleMetricsInstance'
        db.create_table('metrics_singlemetricsinstance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metrics.MetricsCategory'])),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metrics.MetricsInstance'])),
            ('value', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('metrics', ['SingleMetricsInstance'])


    def backwards(self, orm):
        # Removing unique constraint on 'MetricsCategory', fields ['creator', 'name']
        db.delete_unique('metrics_metricscategory', ['creator_id', 'name'])

        # Deleting model 'MetricsProfile'
        db.delete_table('metrics_metricsprofile')

        # Removing M2M table for field metrics on 'MetricsProfile'
        db.delete_table('metrics_metricsprofile_metrics')

        # Deleting model 'MetricsCategory'
        db.delete_table('metrics_metricscategory')

        # Deleting model 'MetricsInstance'
        db.delete_table('metrics_metricsinstance')

        # Deleting model 'SingleMetricsInstance'
        db.delete_table('metrics_singlemetricsinstance')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'metrics.metricscategory': {
            'Meta': {'unique_together': "(('creator', 'name'),)", 'object_name': 'MetricsCategory'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maxLabel': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'metricMax': ('django.db.models.fields.SmallIntegerField', [], {'default': '7'}),
            'metrictype': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'minLabel': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'metrics.metricsinstance': {
            'Meta': {'object_name': 'MetricsInstance'},
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'values': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['metrics.MetricsCategory']", 'through': "orm['metrics.SingleMetricsInstance']", 'symmetrical': 'False'})
        },
        'metrics.metricsprofile': {
            'Meta': {'object_name': 'MetricsProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metrics': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['metrics.MetricsCategory']", 'symmetrical': 'False', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'metrics.singlemetricsinstance': {
            'Meta': {'object_name': 'SingleMetricsInstance'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['metrics.MetricsCategory']"}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['metrics.MetricsInstance']"}),
            'value': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['metrics']