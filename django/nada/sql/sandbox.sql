insert into nada_mesh3d_fulltile(box)
select
st_translate(box::geometry, x::float * 2560, y::float * 2160, z::float * 50)
from generate_series(0, 10 - 1) as x,
generate_series(0, 10 - 1) as y,
generate_series(0, 2000 - 1) as z,
(
select ('MultiPoint(0 0 0, 2560 2160 50)')::geometry as box
)as foo;

----------------------------------------------------------------------------------------------------------------------
-- queries for validating the bin
----------------------------------------------------------------------------------------------------------------------
select id, GeometryType(box), Box3d(box) from nada_bin_table_default limit 10;
select * from nada_neuron_to_bin;

-- should only be in bin 1
insert into nada_neuron(name, cell_type, geometry, keypoint, experiment_id, layer_id) 
values(1000, 1, 'MULTIPOINT(0 0 0, 5 5 5)', 'POINT(2 2 2)', 1, 1) RETURNING "nada_neuron"."id";

-- should only be in bin 2
insert into nada_neuron(name, cell_type, geometry, keypoint, experiment_id, layer_id) 
values(1000, 1, 'MULTIPOINT(0 0 51, 0 0 60)', 'POINT(2559 2159 51)', 1, 1) RETURNING "nada_neuron"."id";

-- should be in bin 1 and 2
insert into nada_neuron(name, cell_type, geometry, keypoint, experiment_id, layer_id) 
values(1000, 1, 'MULTIPOINT(0 0 49, 27 5 51)', 'POINT(2 2 2)', 1, 1) RETURNING "nada_neuron"."id";

-- lands on a boundry
insert into nada_neuron(name, cell_type, geometry, keypoint, experiment_id, layer_id) 
values(1000, 1, 'MULTIPOINT(2560 2160 50, 2561 2161 51)', 'POINT(2 2 2)', 1, 1) RETURNING "nada_neuron"."id";

----------------------------------------------------------------------------------------------------------------------
-- queries for validating the partitions
----------------------------------------------------------------------------------------------------------------------

insert into nada_coordinateframe(name, description, x_start, x_stop, y_start, y_stop, z_start, z_stop, x_voxel_size, y_voxel_size, z_voxel_size, voxel_unit, time_step, time_step_unit)
values('test', 'test', 1, 1, 1, 0, 0, 0, 1, 1, 1, 'test', 1, 'test');

insert into nada_collection(name, description)
values('test', 'test');

insert into nada_experiment(name, description, num_hierarchy_levels, hierarchy_method, max_time_sample, collection_id, coord_frame_id) 
values('test', 'test', 1, 'na', 1, 1, 1);

insert into nada_layer(name, description, is_channel, base_resolution, default_time_step, datatype, experiment_id)
values('test', 'test', FALSE, 1, 1, 'test', 1);

delete from nada_neuron;
delete from nada_synapse;

insert into nada_neuron(name, cell_type, geometry, keypoint, experiment_id, layer_id) 
values(1000, 1, 'MULTIPOINT(0 0 0, 5 5 5)', 'POINT(2 2 2)', 1, 1) RETURNING "nada_neuron"."id";

INSERT INTO "nada_neuron" ("name", "experiment_id", "layer_id", "cell_type", "geometry", "keypoint") 
VALUES (55, 1, 1, 0, ST_GeomFromEWKB('\x0104000080010000000101000080000000000000f03f00000000000000400000000000000840'::bytea), ST_GeomFromEWKB('\x0101000080000000000000f03f00000000000000400000000000000840'::bytea)) RETURNING "nada_neuron"."id";

select * from neuron_insert(555, 1, 'MULTIPOINT(0 0 0, 5 5 5)', 'POINT(2 2 2)', 1, 1);

INSERT INTO "nada_synapse" ("name", "experiment_id", "layer_id", "neuron_id", "partner_neuron_id", "partner_synapse_id", "geometry", "keypoint", "polarity", "compartment") 
VALUES (44, 1, 1, NULL, NULL, NULL, 'MULTIPOINT(0 0 0, 5 5 5)', 'POINT(2 2 2)', 0, 0) RETURNING "nada_synapse"."id";


select * from neuron_insert_function(55, 1, 'MULTIPOINT(0 0 0, 5 5 5)', 'POINT(2 2 2)', 1, 1);
select * from synapse_insert_function(44, 'MULTIPOINT(0 0 0, 5 5 5)', 'POINT(2 2 2)', 0, 0, 1, 1, null, null, null);


-----------------------------------------------------------------------------------------
-- Function for creating bin tables of arbitrary dimensions
-----------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION
public.create_bin_table(
    x_size int,
    y_size int,
    z_size int,
    x_bins int,
    y_bins int,
    z_bins int
)
RETURNS VOID AS $$
BEGIN

    EXECUTE format('CREATE TABLE public.nada_bin3d_' || x_size || '_' || y_size || '_' || z_size || '() INHERITS (public.nada_bin3d_default)')
    USING x_size, y_size, z_size;

    EXECUTE format('
        INSERT INTO nada_bin3d_' || x_size || '_' || y_size || '_' || z_size || '(box)
        SELECT 
        ST_TRANSLATE(box::geometry, x::float * ' || x_size || ', y::float * ' || y_size || ', z::float * ' || z_size || ')
        FROM generate_series(0, ' || x_bins || ' - 1) as x,
        generate_series(0, ' || y_bins || ' - 1) as y,
        generate_series(0, ' || z_bins || ' - 1) as z,
        (
        SELECT (''MultiPoint(0 0 0, ' || (x_size - 1) || ' ' || (y_size - 1) || ' ' || (z_size - 1) || ')'')::geometry as box
        )AS foo;
    ')
    USING x_size, y_size, z_size, x_bins, y_bins, z_bins, x_size, y_size, z_size;

END;
$$
LANGUAGE plpgsql;

insert into public.nada_bin_table(x_size, y_size, z_size, x_bins, y_bins, z_bins) values (5, 5, 10, 2, 2, 2);

drop table nada_bin_table_dimension cascade;
create table nada_bin_table(
id int,
x_size int,
y_size int,
z_size int,
x_bins int,
y_bins int,
z_bins int
);

\dt