-----------------------------------------------------------------------------------------
-- Partition trigger for Experiments table
-----------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION
public.create_partitions()
RETURNS TRIGGER AS
$BODY$
BEGIN

EXECUTE 'CREATE TABLE public.nada_neuron_' || LASTVAL() || ' (CHECK ( experiment_id = ' || LASTVAL() || ')) INHERITS (public.nada_neuron)';
EXECUTE 'CREATE INDEX neurons_layer_id_' || LASTVAL() || ' on public.nada_neuron_' || LASTVAL() || ' USING btree(layer_id)';
EXECUTE 'CREATE INDEX neurons_experiment_id_' || LASTVAL() || ' on public.nada_neuron_' || LASTVAL() || ' USING btree(experiment_id)';
EXECUTE 'CREATE INDEX neurons_geom_' || LASTVAL() || ' on public.nada_neuron_' || LASTVAL() || ' USING gist(geometry gist_geometry_ops_nd)';
EXECUTE 'CREATE INDEX neurons_keypoint_' || LASTVAL() || ' on public.nada_neuron_' || LASTVAL() || ' USING gist(keypoint gist_geometry_ops_nd)';

EXECUTE 'DROP SEQUENCE IF EXISTS public.nada_neuron_to_mesh_' || LASTVAL() || '_id_seq';
EXECUTE 'CREATE SEQUENCE public.nada_neuron_to_mesh_' || LASTVAL() || '_id_seq';
EXECUTE 'CREATE TABLE public.nada_neuron_to_mesh_' || LASTVAL() || ' (CHECK ( experiment_id = ' || LASTVAL() || ')) INHERITS (public.nada_neuron_to_mesh)';
EXECUTE 'ALTER TABLE public.nada_neuron_to_mesh_' || LASTVAL() || ' ALTER COLUMN id SET DEFAULT NEXTVAL(' || quote_literal('nada_neuron_to_mesh_' || LASTVAL() || '_id_seq') || ')';
EXECUTE 'CREATE INDEX nada_neuron_to_mesh_' || LASTVAL() || '_id on public.nada_neuron_to_mesh_' || LASTVAL() || ' USING btree(id)';
EXECUTE 'CREATE INDEX nada_neuron_to_mesh_' || LASTVAL() || '_neuron_id on public.nada_neuron_to_mesh_' || LASTVAL() || ' USING btree(neuron_id)';
EXECUTE 'CREATE INDEX nada_neuron_to_mesh_' || LASTVAL() || '_fulltile_id on public.nada_neuron_to_mesh_' || LASTVAL() || ' USING btree(mesh3d_fulltile_id)';

EXECUTE 'CREATE TABLE public.nada_synapse_' || LASTVAL() || ' (CHECK ( experiment_id = ' || LASTVAL() || ')) INHERITS (public.nada_synapse)';
EXECUTE 'CREATE INDEX synapses_layer_id_' || LASTVAL() || ' on public.nada_synapse_' || LASTVAL() || ' USING btree(layer_id)';
EXECUTE 'CREATE INDEX synapses_partner_neuron_id_' || LASTVAL() || ' on public.nada_synapse_' || LASTVAL() || ' USING btree(partner_neuron_id)';
EXECUTE 'CREATE INDEX synapses_experiment_id_' || LASTVAL() || ' on public.nada_synapse_' || LASTVAL() || ' USING btree(experiment_id)';
EXECUTE 'CREATE INDEX synapses_neuron_id_' || LASTVAL() || ' on public.nada_synapse_' || LASTVAL() || ' USING btree(neuron_id)';
EXECUTE 'CREATE INDEX synapses_geometry_' || LASTVAL() || ' on public.nada_synapse_' || LASTVAL() || ' USING gist(geometry gist_geometry_ops_nd)';
EXECUTE 'CREATE INDEX synapses_keypoint_' || LASTVAL() || ' on public.nada_synapse_' || LASTVAL() || ' USING gist(keypoint gist_geometry_ops_nd)';

RETURN NULL;
END;
$BODY$
LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS add_experiment_trigger ON public.nada_experiment;
CREATE TRIGGER add_experiment_trigger
AFTER INSERT ON public.nada_experiment
FOR EACH ROW EXECUTE PROCEDURE public.create_partitions();

-----------------------------------------------------------------------------------------
-- Partition trigger for neurons table
-----------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION neurons_partition_function()
RETURNS TRIGGER AS $$
BEGIN
    EXECUTE format('INSERT INTO nada_neuron_' || NEW.experiment_id 
    || ' (name, cell_type, geometry, keypoint, experiment_id, layer_id) ' 
    || ' SELECT $1, $2, $3, $4, $5, $6 ' )
    USING NEW.name, NEW.cell_type, NEW.geometry::text, NEW.keypoint::text, NEW.experiment_id, NEW.layer_id; 

    EXECUTE format('INSERT INTO nada_neuron_to_mesh_'|| NEW.experiment_id
    || ' (neuron_id, experiment_id, mesh3d_fulltile_id) '
    || ' SELECT $1, '
    || ' $2, '
    || ' nada_mesh3d_fulltile.id '
    || ' FROM nada_mesh3d_fulltile WHERE $3 &&& nada_mesh3d_fulltile.box;')
    USING NEW.id, NEW.experiment_id, NEW.geometry::text; 
    
    RETURN NULL;
END;
$$
LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS insert_neurons_trigger ON public.nada_neuron_view;
CREATE TRIGGER insert_neurons_trigger
    INSTEAD OF INSERT ON nada_neuron_view
    FOR EACH ROW EXECUTE PROCEDURE neurons_partition_function();

DROP TRIGGER IF EXISTS insert_neuron_mesh_trigger ON public.nada_neuron;
CREATE TRIGGER insert_neuron_mesh_trigger
AFTER INSERT ON public.nada_neuron
FOR EACH ROW EXECUTE PROCEDURE public.insert_neuron_mesh();

-----------------------------------------------------------------------------------------
-- Partition triggers for Synapses
-----------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION synapses_partition_function()
RETURNS TRIGGER AS $$
BEGIN
    EXECUTE format('INSERT INTO nada_synapse_' || NEW.experiment_id 
    || ' (name, geometry, keypoint, polarity, compartment, experiment_id, layer_id, neuron_id, partner_neuron_id, partner_synapse_id) ' 
    || ' SELECT $1, $2, $3, $4, $5, $6, $7, $8, $9, $10' )
    using NEW.name, NEW.geometry::text, NEW.keypoint::text, NEW.polarity, NEW.compartment, NEW.experiment_id, NEW.layer_id, NEW.neuron_id, NEW.partner_neuron_id, NEW.partner_synapse_id; 
    RETURN NULL;
END;
$$
LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS insert_synapses_trigger ON public.nada_synapse;
CREATE TRIGGER insert_synapses_trigger
    BEFORE INSERT ON nada_synapse
    FOR EACH ROW EXECUTE PROCEDURE synapses_partition_function();

-----------------------------------------------------------------------------------------
-- Functions to insert Neurons and Synapses via Django
-----------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION neuron_insert_function(
    name bigint, 
    cell_type integer, 
    geometry geometry, 
    keypoint geometry, 
    experiment_id integer, 
    layer_id integer
)
RETURNS SETOF nada_neuron AS $$
BEGIN
    EXECUTE format('INSERT INTO nada_neuron_' || experiment_id 
    || ' (name, cell_type, geometry, keypoint, experiment_id, layer_id) ' 
    || ' SELECT $1, $2, $3, $4, $5, $6 ' )
    USING name, cell_type, geometry::text, keypoint::text, experiment_id, layer_id; 
    
    EXECUTE format('INSERT INTO nada_neuron_to_mesh_'|| experiment_id
    || ' (neuron_id, experiment_id, mesh3d_fulltile_id) '
    || ' SELECT $1, '
    || ' $2, '
    || ' nada_mesh3d_fulltile.id '
    || ' FROM nada_mesh3d_fulltile WHERE $3 &&& nada_mesh3d_fulltile.box;')
    USING CURRVAL('nada_neuron_id_seq'::regclass), experiment_id, geometry::text; 
    
    RETURN QUERY
        EXECUTE format('SELECT * FROM nada_neuron_' || experiment_id || ' WHERE id = ' || CURRVAL('nada_neuron_id_seq'::regclass));
    RETURN;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION synapse_insert_function(
name bigint, 
geometry geometry, 
keypoint geometry, 
polarity integer, 
compartment double precision, 
experiment_id integer, 
layer_id integer, 
neuron_id integer, 
partner_neuron_id integer, 
partner_synapse_id integer
)
RETURNS SETOF nada_synapse AS $$
BEGIN
    EXECUTE format('INSERT INTO nada_synapse_' || experiment_id 
    || ' (name, geometry, keypoint, polarity, compartment, experiment_id, layer_id, neuron_id, partner_neuron_id, partner_synapse_id) ' 
    || ' SELECT $1, $2, $3, $4, $5, $6, $7, $8, $9, $10' )
    using name, geometry::text, keypoint::text, polarity, compartment, experiment_id, layer_id, neuron_id, partner_neuron_id, partner_synapse_id;
    
    EXECUTE format('INSERT INTO nada_neuron_to_mesh_'|| experiment_id
    || ' (neuron_id, experiment_id, mesh3d_fulltile_id) '
    || ' SELECT $1, '
    || ' $2, '
    || ' nada_mesh3d_fulltile.id '
    || ' FROM nada_mesh3d_fulltile WHERE $3 &&& nada_mesh3d_fulltile.box;')
    USING CURRVAL('nada_synapse_id_seq'::regclass), experiment_id, geometry::text; 
    
    RETURN QUERY
        EXECUTE format('SELECT * FROM nada_synapse_' || experiment_id || ' WHERE id = ' || CURRVAL('nada_synapse_id_seq'::regclass));
    RETURN;
END;
$$
LANGUAGE plpgsql;