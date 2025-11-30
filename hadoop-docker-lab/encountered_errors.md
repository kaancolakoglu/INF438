# Resources

Problem:

- MapReduce job killed due to memory

Error:

```
Job failed with state KILLED due to: REDUCE capability required is more than the supported max container capability in the cluster. reduceResourceRequest: <memory:8192, vCores:1> maxContainerCapability:<memory:4096, vCores:4>
```

Solution:

- Reduced memory requirements by adding parameters: `-Dmapreduce.map.memory.mb=2048 -Dmapreduce.reduce.memory.mb=2048`

Problem:

- Python scripts not executable in Hadoop Streaming

Error:

```
Caused by: java.io.IOException: Cannot run program "/tmp/mapper.py": error=2, No such file or directory
```

Solution: 

- Used `-file` option to distribute scripts: `-file /tmp/mapper.py -file /tmp/reducer.py`
- Used just filename in mapper/reducer: `-mapper mapper.py -reducer reducer.py`

Problem:

- f-strings not supported

Error:

```
SyntaxError: invalid syntax
PipeMapRed.waitOutputThreads(): subprocess failed with code 1
```

Solution:

- Replaced f-strings with .format() because containers have Python 3.5