# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-03 22:23
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import nada.models.neurons
import nada.models.util
import nada.models.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, validators=[nada.models.validators.NameValidator()], verbose_name='Name of the Collection')),
                ('description', models.CharField(blank=True, max_length=4096)),
            ],
            bases=(nada.models.util.NameLookupMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CoordinateFrame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, validators=[nada.models.validators.NameValidator()], verbose_name='Name of the Coordinate reference frame')),
                ('description', models.CharField(blank=True, max_length=4096)),
                ('x_start', models.IntegerField()),
                ('x_stop', models.IntegerField()),
                ('y_start', models.IntegerField()),
                ('y_stop', models.IntegerField()),
                ('z_start', models.IntegerField()),
                ('z_stop', models.IntegerField()),
                ('x_voxel_size', models.FloatField()),
                ('y_voxel_size', models.FloatField()),
                ('z_voxel_size', models.FloatField()),
                ('voxel_unit', models.CharField(choices=[('nanometers', 'NANOMETERS'), ('micrometers', 'MICROMETERS'), ('millimeters', 'MILLIMETERS'), ('centimeters', 'CENTIMETERS')], max_length=100)),
                ('time_step', models.IntegerField()),
                ('time_step_unit', models.CharField(choices=[('nanoseconds', 'NANOSECONDS'), ('microseconds', 'MICROSECONDS'), ('milliseconds', 'MILLISECONDS'), ('seconds', 'SECONDS')], max_length=100)),
            ],
            bases=(nada.models.util.NameLookupMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, validators=[nada.models.validators.NameValidator()], verbose_name='Name of the Experiment')),
                ('description', models.CharField(blank=True, max_length=4096)),
                ('num_hierarchy_levels', models.IntegerField(default=0)),
                ('hierarchy_method', models.CharField(choices=[('near_iso', 'NEAR_ISO'), ('iso', 'ISO'), ('slice', 'SLICE')], max_length=100)),
                ('max_time_sample', models.IntegerField(default=0)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='experiments', to='nada.Collection')),
                ('coord_frame', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='coord', to='nada.CoordinateFrame')),
            ],
            bases=(nada.models.util.NameLookupMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Layer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, validators=[nada.models.validators.NameValidator()], verbose_name='Name of the Layer')),
                ('description', models.CharField(blank=True, max_length=4096)),
                ('is_channel', models.BooleanField()),
                ('base_resolution', models.IntegerField(default=0)),
                ('default_time_step', models.IntegerField(default=0)),
                ('datatype', models.CharField(choices=[('uint8', 'UINT8'), ('uint16', 'UINT16'), ('uint32', 'UINT32'), ('uint64', 'UINT64')], max_length=100)),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='layers', to='nada.Experiment')),
            ],
            bases=(nada.models.util.NameLookupMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Neuron',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.BigIntegerField(unique=True)),
                ('cell_type', models.IntegerField(choices=[('unknown', 0), ('red', 1), ('green', 2), ('blue', 3)], default=0)),
                ('geometry', django.contrib.gis.db.models.fields.MultiPointField(dim=3, spatial_index=False, srid=0)),
                ('keypoint', django.contrib.gis.db.models.fields.PointField(dim=3, spatial_index=False, srid=0)),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='neurons', to='nada.Experiment')),
                ('layer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='neurons', to='nada.Layer')),
            ],
            bases=(nada.models.util.NameLookupMixin, nada.models.neurons.CELIMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Synapse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.BigIntegerField(unique=True)),
                ('geometry', django.contrib.gis.db.models.fields.MultiPointField(dim=3, spatial_index=False, srid=0)),
                ('keypoint', django.contrib.gis.db.models.fields.PointField(dim=3, spatial_index=False, srid=0)),
                ('polarity', models.IntegerField(choices=[('unknown', 0), ('pre', 1), ('post', 2), ('bidirectional', 3)], default=0)),
                ('compartment', models.FloatField()),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='synapses', to='nada.Experiment')),
                ('layer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='synapses', to='nada.Layer')),
                ('neuron', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='synapses', to='nada.Neuron')),
                ('partner_neuron', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='partner_synapses', to='nada.Neuron')),
                ('partner_synapse', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='nada.Synapse')),
            ],
            bases=(nada.models.util.NameLookupMixin, nada.models.neurons.CELIMixin, models.Model),
        ),
        migrations.AlterUniqueTogether(
            name='layer',
            unique_together=set([('experiment', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='experiment',
            unique_together=set([('collection', 'name')]),
        ),
        migrations.RunSQL(
			str("CREATE OR REPLACE FUNCTION " +
			"public.create_partitions() " +
			"RETURNS TRIGGER AS " +
			"$BODY$ " +
			"BEGIN " +
			" " +
			"EXECUTE 'CREATE TABLE public.nada_neuron_' || LASTVAL() || ' (CHECK ( experiment_id = ' || LASTVAL() || ')) INHERITS (public.nada_neuron)'; " +
			"EXECUTE 'CREATE INDEX neurons_layer_id_' || LASTVAL() || ' on public.nada_neuron_' || LASTVAL() || ' USING btree(layer_id)'; " +
			"EXECUTE 'CREATE INDEX neurons_experiment_id_' || LASTVAL() || ' on public.nada_neuron_' || LASTVAL() || ' USING btree(experiment_id)'; " +
			"EXECUTE 'CREATE INDEX neurons_geom_' || LASTVAL() || ' on public.nada_neuron_' || LASTVAL() || ' USING gist(geometry gist_geometry_ops_nd)'; " +
			"EXECUTE 'CREATE INDEX neurons_keypoint_' || LASTVAL() || ' on public.nada_neuron_' || LASTVAL() || ' USING gist(keypoint gist_geometry_ops_nd)'; " +
			" " +
			"EXECUTE 'CREATE TABLE public.nada_synapse_' || LASTVAL() || ' (CHECK ( experiment_id = ' || LASTVAL() || ')) INHERITS (public.nada_synapse)'; " +
			"EXECUTE 'CREATE INDEX synapses_layer_id_' || LASTVAL() || ' on public.nada_synapse_' || LASTVAL() || ' USING btree(layer_id)'; " +
			"EXECUTE 'CREATE INDEX synapses_partner_neuron_id_' || LASTVAL() || ' on public.nada_synapse_' || LASTVAL() || ' USING btree(partner_neuron_id)'; " +
			"EXECUTE 'CREATE INDEX synapses_experiment_id_' || LASTVAL() || ' on public.nada_synapse_' || LASTVAL() || ' USING btree(experiment_id)'; " +
			"EXECUTE 'CREATE INDEX synapses_neuron_id_' || LASTVAL() || ' on public.nada_synapse_' || LASTVAL() || ' USING btree(neuron_id)'; " +
			"EXECUTE 'CREATE INDEX synapses_geometry_' || LASTVAL() || ' on public.nada_synapse_' || LASTVAL() || ' USING gist(geometry gist_geometry_ops_nd)'; " +
			"EXECUTE 'CREATE INDEX synapses_keypoint_' || LASTVAL() || ' on public.nada_synapse_' || LASTVAL() || ' USING gist(keypoint gist_geometry_ops_nd)'; " +
			" " +
			"RETURN NULL; " +
			"END; " +
			"$BODY$ " +
			"LANGUAGE plpgsql;"),
			"DROP FUNCTION IF EXISTS public.create_partitions();"
        ),
        migrations.RunSQL(
			str("DROP TRIGGER IF EXISTS add_experiment_trigger ON public.nada_experiment; " +
			"CREATE TRIGGER add_experiment_trigger " +
			"AFTER INSERT ON public.nada_experiment " +
			"FOR EACH ROW EXECUTE PROCEDURE public.create_partitions();"),
			"DROP TRIGGER IF EXISTS add_experiment_trigger ON public.nada_experiment;"
        ),
        migrations.RunSQL(
			str("CREATE OR REPLACE FUNCTION neurons_insert_function() " +
				"RETURNS TRIGGER AS $$ " +
				"BEGIN " +
				"	EXECUTE format('INSERT INTO nada_neuron_' || NEW.experiment_id " +
				"	|| ' (name, cell_type, geometry, keypoint, experiment_id, layer_id) ' " +
				"	|| ' SELECT $1, $2, $3, $4, $5, $6 ' ) " +
				"	using NEW.name, NEW.cell_type, NEW.geometry::text, NEW.keypoint::text, NEW.experiment_id, NEW.layer_id; " +
				"    RETURN NULL; " +
				"END; " +
				"$$ " +
				"LANGUAGE plpgsql;"),
				"DROP FUNCTION IF EXISTS public.neurons_insert_function();"
        ),
        migrations.RunSQL(
			str("DROP TRIGGER IF EXISTS insert_neurons_trigger ON public.nada_neuron; " +
			"CREATE TRIGGER insert_neurons_trigger " +
			"BEFORE INSERT ON nada_neuron " +
			"FOR EACH ROW EXECUTE PROCEDURE neurons_insert_function();"),
			"DROP TRIGGER IF EXISTS insert_neurons_trigger ON public.nada_neuron;"
        ),
        migrations.RunSQL(
			str("CREATE OR REPLACE FUNCTION synapses_insert_function() " +
				"RETURNS TRIGGER AS $$ " +
				"BEGIN " +
				"	EXECUTE format('INSERT INTO nada_synapse_' || NEW.experiment_id " +
				"	|| ' (name, geometry, keypoint, polarity, compartment, experiment_id, layer_id, neuron_id, partner_neuron_id, partner_synapse_id) ' " +
				"	|| ' SELECT $1, $2, $3, $4, $5, $6, $7, $8, $9, $10' ) " +
				"	using NEW.name, NEW.geometry::text, NEW.keypoint::text, NEW.polarity, NEW.compartment, NEW.experiment_id, NEW.layer_id, NEW.neuron_id, NEW.partner_neuron_id, NEW.partner_synapse_id; " +
				"    RETURN NULL; " +
				"END; " +
				"$$ " +
				"LANGUAGE plpgsql;"),
				"DROP FUNCTION IF EXISTS public.synapses_insert_function();"
        ),
        migrations.RunSQL(
			str("DROP TRIGGER IF EXISTS insert_synapses_trigger ON public.nada_synapse; " +
			"CREATE TRIGGER insert_synapses_trigger " +
			"BEFORE INSERT ON nada_synapse " +
			"FOR EACH ROW EXECUTE PROCEDURE synapses_insert_function();"),
			"DROP TRIGGER IF EXISTS insert_synapses_trigger ON public.nada_synapse;"
        ),
    ]
