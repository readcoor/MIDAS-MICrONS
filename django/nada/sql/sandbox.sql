----------------------------------------------------------------------------------------------------------------------
-- queries for validating the partitions
----------------------------------------------------------------------------------------------------------------------
-- Insert rows to satisfy FKs
insert into nada_coordinateframe(name, description, x_start, x_stop, y_start, y_stop, z_start, z_stop, x_voxel_size, y_voxel_size, z_voxel_size, voxel_unit, time_step, time_step_unit)
values('test', 'test', 1, 1, 1, 0, 0, 0, 1, 1, 1, 'test', 1, 'test');

insert into nada_collection(name, description)
values('test', 'test');

insert into nada_experiment(name, description, num_hierarchy_levels, hierarchy_method, max_time_sample, collection_id, coord_frame_id)
values('test', 'test', 1, 'na', 1, 1, 1);

insert into nada_layer(name, description, is_channel, base_resolution, default_time_step, datatype, experiment_id)
values('test', 'test', FALSE, 1, 1, 'test', 1);

----------------------------------------------------------------------------------------------------------------------
-- queries for validating the bin
----------------------------------------------------------------------------------------------------------------------
-- Simple query to manually inspect the geometries
select id, GeometryType(box), Box3d(box) from nada_bin_table_default limit 10;

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

-- Check the results
select * from nada_neuron_to_bin;
/*
 id | bin_table_id | experiment_id | neuron_id
----+--------------+---------------+-----------
  1 |            1 |             1 |         1
  2 |            2 |             1 |         3
  3 |            1 |             1 |         5
  4 |            2 |             1 |         5
  5 |          112 |             1 |         7
(5 rows)
*/
