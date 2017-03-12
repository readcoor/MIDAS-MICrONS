-----------------------------------------------------------------------------------------
-- Remove function and trigger for creating bin tables of arbitrary dimensions
-----------------------------------------------------------------------------------------

DROP FUNCTION IF EXISTS public.create_bin_table() CASCADE;

DROP TRIGGER IF EXISTS bin_insert_trigger ON public.nada_bin_table;

-----------------------------------------------------------------------------------------
-- Remove partition trigger and function for Experiments table
-----------------------------------------------------------------------------------------

DROP FUNCTION IF EXISTS public.create_partitions() CASCADE;

DROP TRIGGER IF EXISTS add_experiment_trigger ON public.nada_experiment;

-----------------------------------------------------------------------------------------
-- Remove partition triggers and function for neurons table
-----------------------------------------------------------------------------------------

DROP FUNCTION IF EXISTS public.neurons_partition_function() CASCADE;

DROP TRIGGER IF EXISTS insert_neurons_trigger ON public.nada_neuron;
-- insert neurons mesh trigger

-----------------------------------------------------------------------------------------
-- Remove partition trigger and function for Synapses
-----------------------------------------------------------------------------------------

DROP FUNCTION IF EXISTS public.synapses_partition_function() CASCADE;

DROP TRIGGER IF EXISTS insert_synapses_trigger ON public.nada_synapse;

-----------------------------------------------------------------------------------------
-- Remove functions to insert Neurons and Synapses via Django
-----------------------------------------------------------------------------------------

DROP FUNCTION IF EXISTS neuron_insert_function(bigint,integer,geometry,geometry,integer,integer) CASCADE;

DROP FUNCTION IF EXISTS synapse_insert_function(bigint,geometry,geometry,integer,double precision,integer,integer,integer,integer,integer) CASCADE;