# EPUS
Note: This repo is based on [UEdgeSkyline](https://github.com/0penth3wind0w/UEdgeSkyline.git).

## Environment
We use conda to manage our environment and there are our install commands in the following list.

<pre><code>conda create --name skyline python=3.7
conda install rtree numpy openpyxl pandas -y
</code></pre>

If you missing something needed, just following the error messages to install them.
## Skyline  
All skyline method used are implemented in this folder.  
- `prunePSky`: The original concept of this skyline method. No sliding window version.  
- `slideBPSky`: It represented PRPO. It is likely to the brute force in [UEdgeSkyline](https://github.com/0penth3wind0w/UEdgeSkyline.git).
- `slideUPSky`: It represented EPUS. It is likely to the method he proposed in [UEdgeSkyline](https://github.com/0penth3wind0w/UEdgeSkyline.git).

## Data  
Data can be generated using generator.py in data folder.
Or, you can just unzzip the data.zip file. 
There are all use datasets in the experiment.

The format of data is as follows:  

	name, probability_1, location_1, probability_2, location_2, ...  
	
For a single data, the sum of probability will be equal to 1  .

## Experiment
Central exps of every parameter setting have their file and are hinted by their name. 

Distribute exps are the same as Central exps. 


## Test  
Use for experiment results.  
Before using these script. Make sure to create following csv file by using `generator.py` locate in `data/`.  

	10000_dim2_pos3_rad5_01000.csv  
	10000_dim2_pos4_rad5_01000.csv  
	10000_dim2_pos5_rad3_01000.csv  
	10000_dim2_pos5_rad4_01000.csv  
	10000_dim2_pos5_rad5_01000.csv  
	10000_dim2_pos5_rad6_01000.csv  
	10000_dim2_pos5_rad7_01000.csv  
	10000_dim2_pos5_rad8_01000.csv  
	10000_dim2_pos5_rad9_01000.csv  
	10000_dim2_pos5_rad10_01000.csv  
	10000_dim2_pos6_rad5_01000.csv  
	10000_dim2_pos7_rad5_01000.csv  
	10000_dim2_pos8_rad5_01000.csv  
	10000_dim2_pos9_rad5_01000.csv  
	10000_dim2_pos10_rad5_01000.csv  
	10000_dim3_pos5_rad5_01000.csv  
	10000_dim4_pos5_rad5_01000.csv  
	10000_dim5_pos5_rad5_01000.csv  
	10000_dim6_pos5_rad5_01000.csv  
	10000_dim7_pos5_rad5_01000.csv  
	10000_dim8_pos5_rad5_01000.csv  
	10000_dim9_pos5_rad5_01000.csv  
	10000_dim10_pos5_rad5_01000.csv  

## Unit test
Data related unit test are provided.  
Just simply run the .py file  

## Visualization  
2D and 3D data can be visualized.  
Just input an array to the visualize function and the result will appaer in a flash.  
