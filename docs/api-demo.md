---
layout: default
---

# NDA API demo readme


This document describes how to demo the abilities of the NDA API using the dummy data on the demo site. 

## Demo site:
To find REST parameter documentation for all NDA API endpoints, visit this page:
[`http://api-nda.us-east-1.elasticbeanstalk.com/docs/`](http://api-nda.us-east-1.elasticbeanstalk.com/docs/)

## Example values:
This section describes the ranges of example values used to populate the demo site. 

| Parameter name  | Example values|
|---|---|
| collection  |  collection1 |
| experiment  | experiment1  |
| layer  |layer1 (for neurons), layer2 (for synapses) |
|  id (for neurons or synapses) |  0-500 (for neurons), 0-1000 (for synapses) |
| start_time, stop_time  |  0-100 |
| resolution  |  0 (value is ignored for now) |
| neuron keypoint’s x-coordinate  |  0-500 (assigned to be same as neuron’s ID) |
|  neuron keypoint’s y or z-coordinate | 0-2000 (randomized)   |
|synapse keypoint’s x-coordinate | 0-1000 (assigned to be same as synapse ID) |
|synapse keypoint’s y or z-coordinate | 0-2000 (randomized) |
{: .table .table-striped}

## API Examples you can try:
This sections gives specific examples of API URLs you can try on the demo site, using dummy data in both the request parameters and the responses.

### Note: 
Current dummy demo server provides verbose HTML responses for debugging purposes.
You many wish to append “?format=json” to each request. We can also configure the server to return json format by default, if preferred.

For example:

[`http://api-nda.us-east-1.elasticbeanstalk.com/is_synapse/collection1/experiment1/layer2/34?format=json`](http://api-nda.us-east-1.elasticbeanstalk.com/is_synapse/collection1/experiment1/layer2/34?format=json)

```json
=> { "result": true }   // returns bare-bones json
```

### S1: is_synapse
[`http://api-nda.us-east-1.elasticbeanstalk.com/is_synapse/collection1/experiment1/layer2/34`](http://api-nda.us-east-1.elasticbeanstalk.com/is_synapse/collection1/experiment1/layer2/34)

```json
=> { "result": true }
```

[`http://api-nda.us-east-1.elasticbeanstalk.com/is_synapse/collection1/experiment1/layer1/34`](http://api-nda.us-east-1.elasticbeanstalk.com/is_synapse/collection1/experiment1/layer1/34)

```json
=> { "result": false }  // references a neuron, not a synapse
```

[`http://api-nda.us-east-1.elasticbeanstalk.com/is_synapse/collection1/experiment1/layer2/9999`](http://api-nda.us-east-1.elasticbeanstalk.com/is_synapse/collection1/experiment1/layer2/9999)

```json
=> HTTP 400: Not found error
```

### S2: synapse_ids
[`http://api-nda.us-east-1.elasticbeanstalk.com/synapse_ids/collection1/experiment1/layer2/0/0,50/0,2000/0,2000`](http://api-nda.us-east-1.elasticbeanstalk.com/synapse_ids/collection1/experiment1/layer2/0/0,50/0,2000/0,2000)

```json
=> { "ids": [0, ..., 50] }
```

### S3: synapse_keypoint
[`http://api-nda.us-east-1.elasticbeanstalk.com/synapse_keypoint/collection1/experiment1/layer2/0/33`](http://api-nda.us-east-1.elasticbeanstalk.com/synapse_keypoint/collection1/experiment1/layer2/0/33)

```json
=> { "keypoint":  [ 33.0, 1137.0, 1802.0] }
```

### S4: synapse_parent
[`http://api-nda.us-east-1.elasticbeanstalk.com/synapse_parent/collection1/experiment1/layer2/47`](http://api-nda.us-east-1.elasticbeanstalk.com/synapse_parent/collection1/experiment1/layer2/47)

```json
=> { "parent_neurons": { "452": 2, "206": 1 } }
```

### S5: is_neuron
[`http://api-nda.us-east-1.elasticbeanstalk.com/is_neuron/collection1/experiment1/layer1/34`](http://api-nda.us-east-1.elasticbeanstalk.com/is_neuron/collection1/experiment1/layer1/34)

```json
=> { "result": true }
```

[`http://api-nda.us-east-1.elasticbeanstalk.com/is_neuron/collection1/experiment1/layer2/34`](http://api-nda.us-east-1.elasticbeanstalk.com/is_neuron/collection1/experiment1/layer2/34)

```json
=> { "result": false }   // references a synapse, not a neuron
```

[`http://api-nda.us-east-1.elasticbeanstalk.com/is_neuron/collection1/experiment1/layer1/9999`](http://api-nda.us-east-1.elasticbeanstalk.com/is_neuron/collection1/experiment1/layer1/9999)

```json
=> HTTP 400: Not found error
```

### S6: neuron_ids
[`http://api-nda.us-east-1.elasticbeanstalk.com/neuron_ids/collection1/experiment1/layer1/0/0,50/0,2000/0,2000`](http://api-nda.us-east-1.elasticbeanstalk.com/neuron_ids/collection1/experiment1/layer1/0/0,50/0,2000/0,2000)

```json
=> { "ids": [0, ...50] }
```

### S7: neuron_keypoint
[`http://api-nda.us-east-1.elasticbeanstalk.com/neuron_keypoint/collection1/experiment1/layer1/0/33`](http://api-nda.us-east-1.elasticbeanstalk.com/neuron_keypoint/collection1/experiment1/layer1/0/33)

```json
=> { "keypoint":  [ 33.0, 387.0, 1190.0 ] }
```

### S8: neuron_children
[`http://api-nda.us-east-1.elasticbeanstalk.com/neuron_children/collection1/experiment1/layer1/0/0,50/0,2000/0,2000/37`](http://api-nda.us-east-1.elasticbeanstalk.com/neuron_children/collection1/experiment1/layer1/0/0,50/0,2000/0,2000/37)

```json
=> { "child_synapses": { "96": 2, "541": 1 } }
```

### S9: voxel_list
[`http://api-nda.us-east-1.elasticbeanstalk.com/voxel_list/collection1/experiment1/layer1/0/0,50/0,2000/0,2000/23`](http://api-nda.us-east-1.elasticbeanstalk.com/voxel_list/collection1/experiment1/layer1/0/0,50/0,2000/0,2000/23)

```json
=> { "x": [ 62.0,14.0… ], "y": [ 1192.0,1036.0… ], "z": [ 1592.0,1602.0… ]}
```

### S10: synapse_compartment
[`http://api-nda.us-east-1.elasticbeanstalk.com/synapse_compartment/collection1/experiment1/layer2/55`](http://api-nda.us-east-1.elasticbeanstalk.com/synapse_compartment/collection1/experiment1/layer2/55)

```json
=> { "compartment": "soma" }
```

### S11: neuron_celltype
[`http://api-nda.us-east-1.elasticbeanstalk.com/neuron_celltype/collection1/experiment1/layer1/66`](http://api-nda.us-east-1.elasticbeanstalk.com/neuron_celltype/collection1/experiment1/layer1/66)

```json
=> { "cell_type": "excitatory" }
```

### S12: neuron_stimulus
[`http://api-nda.us-east-1.elasticbeanstalk.com/neuron_stimulus/collection1/experiment1/layer1/73/0,25`](http://api-nda.us-east-1.elasticbeanstalk.com/neuron_stimulus/collection1/experiment1/layer1/73/0,25)

```json
=>  { "stimulus": [ [ 0, 3 ],  [ 1, 8 ], … ] }
```
(note: S12 API signature is subject to change soon)

### S13: neuron_activity
[`http://api-nda.us-east-1.elasticbeanstalk.com/neuron_activity/collection1/experiment1/layer1/36/0,25`](http://api-nda.us-east-1.elasticbeanstalk.com/neuron_activity/collection1/experiment1/layer1/36/0,25)

```json
=>  { "activity": [[ 0, 0.858960732532459 ], [ 1, 0.0411693150537612 ], … ] }
```
