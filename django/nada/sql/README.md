# Useful Links
* http://www.postgis.us/downloads/postgis20_cheatsheet.html
* http://postgis.net/docs/manual-1.3/ch05.html
* Write data in (EWKB, HEXEWKT, EWKT) https://pypi.python.org/pypi/PPyGIS
* Shapefiles https://pypi.python.org/pypi/pyshp

# Partitioning
Partitioning is accomplished by creating a master table that each partition will inherit.  This is a standard technique for postgres so I won't go into full detail (see https://www.postgresql.org/docs/9.1/static/ddl-partitioning.html for more.)

The creation of each parition table happens in an insert trigger on the nada_experiment table (add_experiment_trigger).  This will run the function create_partitions which executes a set of dynamic ddl statements, most of which postpend the experiment id to the name of the created object.

Included in these statements are the inherted tables for nada_neuron and nada_synapse along with the table that joins neurons to the bin table.  Indexes for each table are created here as well.

The inherited tables for nada_neuron and nada_synpase are originally declared in the django model file.  We are able to do this because postgres doesn't require any additonal declarations for a master table, but it is important to note that there is no automated process for syncronizing the declarations in the django model and the dynamic ddl statements in create_partitions so this needs to be managed carefully.

For select statements, postgres will automatically route to the appropriate partition table by reading the experiment_id.  For other statements however, a trigger needs to override them and run a function to get the desired behavior.  This has some side effects and incompatibilities with Django.  Django's consistency relies on the database returning newly created rows after they've been created, but the partitioning results in only null being returned.  This is because postgres does not have an INSTEAD OF trigger to create a proper replacement effect.  Instead we use a BEFORE trigger and replace the new data with null after it has been inserted into the partition table (see https://github.com/WyssMICrONS/MIDAS-MICrONS/blob/master/django/nada/sql/partition.sql#L107).

# Bin Tables
To provide optimization beyond what is possible with GIS indexes we also have a bin table that is joined to each neurons partition (see nada_bin_table_default).  This reduces the amount of GIS data that needs to be scanned for a query.  Using the tables below to demonstrate, if we are given a cube (0 0 0, 3 3 3) and asked to provide all neuron_ids that are present in that cube, we should first compare it to the geoms in the bin table, finding that bin_id 1 is fully contained in this cube and bin_id 2 intersects it.  Because bin_id 1 is fully contained we can conclude that the geom in neuron_id 1 at least intersects the provided cube (but may not be fully contained itself).  Becauase neuron_id 2 is not fully contained we will need to evaluate it's geom data, but considering the amount of data that didn't need to be evaluated for neuron 1 the performane savings may be significant.  For this to work the size of the bins will need to be carefully chosen, taking into consideration the density and distribution of neuron data along with the typical query parameters.  Because these may be highly variable I've considered an implementation where the bin tables can be created dynamically (see create_bin_table) simply by inserting some dimensions into a table.  This is not a complete implementation, only enough to demonstrate that this process could potentially be tuned by some automated method.

I would also consider an implementation where the geom dimensions in the bin table are not all uniform but created by a recursive process that has a particular target density of neuron intersections.

The correct time to add rows to the table joining neurons to bins is unclear at this time.  Currently I've included it in the neurons_partition_function so they are added as each row is inserted.

neuron_id 	| geom
--- | ---
1			| (1 1 1, 1 1 2, 1 2 2, 1 3 2, ...)
2			| (5 5 5, 5 6 6, 6 5 5, 5 6 7, ...)

bin_id	| geom
--- | ---
1		| (0 0 0, 2 2 2)
7		| (3 3 3, 5 5 5)

bin_id	| neuron_id
--- | ---
1		| 1
2		| 2

See https://github.com/WyssMICrONS/MIDAS-MICrONS/tree/master/django/nada/sql/microns_mesh.png for a visualization of this.

# Testing
See the sandbox.sql file for a series of statements that can be used to validate the schema and the intersection queries that make the bin tables work.
