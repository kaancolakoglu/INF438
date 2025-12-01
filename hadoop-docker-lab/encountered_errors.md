# Errors

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

Problem:

- ResourceManager container crash loop (exit code 255)

Error:

```
java.net.UnknownHostException: Invalid host name: local host is: (unknown); destination host is: "resourcemanager":8032
```

Root Cause:

- Typo in `hadoop.env`: `SSnappyCodec` instead of `SnappyCodec`

Solution:

- Fixed `YARN_CONF_mapred_map_output_compress_codec=org.apache.hadoop.io.compress.SnappyCodec`

Problem:

- MapReduce streaming jobs fail with "command not found" (exit code 127)

Error:

```
PipeMapRed.waitOutputThreads(): subprocess failed with code 127
```

Root Cause:

- Python not installed in nodemanager container (bde2020 images are Java-only)

Solution:

- Created `Dockerfile.nodemanager` to install Python 3
- Updated `docker-compose.yml` to build custom nodemanager image

Problem:

- Reducer2 crashes with exit code 1

Error:

```
PipeMapRed.waitOutputThreads(): subprocess failed with code 1
```

Root Cause:

- CSV header row not filtered (starts with `"tripduration"` not `tripduration`)
- Reducer fails on `int("tripduration")`

Solution:

- Updated header check in all mappers: `line.startswith('"tripduration') or line.startswith('tripduration')`
