# Hadoop MapReduce - Average Followers by Popularity

## Objective

To calculate the **average number of followers** for each **popularity score (0–100)** using Hadoop MapReduce. This includes data preprocessing, custom mapper and reducer scripts, HDFS job execution, and result interpretation.

---

## Dataset Details

- **Filename:** `artists.csv`
- **Records:** ~1.1 million
- **Used Fields:**
  - `followers` — Number of followers (float)
  - `popularity` — Popularity score (0–100, integer)

---

## Environment Setup

### 1. Verify Hadoop Installation
```bash
hadoop version
```
Expected output: version information like `Hadoop 3.x.x`

### 2. Start Hadoop Services
```bash
start-dfs.sh
start-yarn.sh
```

### 3. Check Running Services
```bash
jps
```
Expected output includes:
- `NameNode`
- `DataNode`
- `SecondaryNameNode`
- `ResourceManager`
- `NodeManager`

### 4. Access Web UIs
- NameNode: http://localhost:9870
- ResourceManager: http://localhost:8088

---

## Project Files

```
.
├── artists.csv
├── mapper.py
├── reducer.py
├── popularity_avg_output.txt
├── README.md
└── evidence/
    ├── hadoop_version.png
    ├── jps_running.png
    ├── namenode_ui.png
    ├── resourcemanager_ui.png
    └── job_result_output.png
```

---

## Mapper Script (mapper.py)

```python
import sys
import csv

reader = csv.reader(sys.stdin)
try:
    header = next(reader)
except StopIteration:
    sys.exit(0)

for row in reader:
    print("DEBUG row:", row, file=sys.stderr)
    try:
        if len(row) < 5:
            continue

        followers_raw = row[1].strip()
        popularity_raw = row[4].strip()

        if followers_raw.lower() == "null" or popularity_raw.lower() == "null":
            continue
        if not followers_raw or not popularity_raw:
            continue

        followers = float(followers_raw)
        popularity = int(float(popularity_raw))

        print(f"{popularity}\t{followers}")

    except (ValueError, IndexError) as e:
        print(f"DEBUG error: {e}", file=sys.stderr)
        continue
```

---

## Reducer Script (reducer.py)

```python
import sys

current_popularity = None
total_followers = 0.0
count = 0

for line in sys.stdin:
    try:
        popularity, followers = line.strip().split('\t')
        popularity = int(popularity)
        followers = float(followers)

        if current_popularity == popularity:
            total_followers += followers
            count += 1
        else:
            if current_popularity is not None:
                avg = total_followers / count
                print(f"{current_popularity}\t{avg:.2f}")
            current_popularity = popularity
            total_followers = followers
            count = 1
    except:
        continue

if current_popularity is not None and count > 0:
    avg = total_followers / count
    print(f"{current_popularity}\t{avg:.2f}")

```

---

## How to Run the Project

### Step 1: Navigate to project directory
```bash
cd ~/hadoop-mapreduce
```

### Step 2: Upload dataset to HDFS
```bash
hdfs dfs -mkdir -p /user/hadoop/input
hdfs dfs -put artists.csv /user/hadoop/input/
```

### Step 3: Make scripts executable
```bash
chmod +x mapper.py reducer.py
```

### Step 4: Remove previous output (if exists)
```bash
hdfs dfs -rm -r /user/hadoop/output/artists_popularity_avg
```

### ⚙️ Step 5: Run the MapReduce job
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -input /user/hadoop/input/artists.csv \
  -output /user/hadoop/output/artists_popularity_avg \
  -mapper mapper.py \
  -reducer reducer.py \
  -file mapper.py \
  -file reducer.py
```

### Step 6: View results
```bash
hdfs dfs -cat /user/hadoop/output/artists_popularity_avg/part-00000
```

### Step 7: Save output locally
```bash
hdfs dfs -cat /user/hadoop/output/artists_popularity_avg/part-00000 > popularity_avg_output.txt
```

---

## Sample Output

```
0	2.14
1	8.93
2	37.56
...
100	8432.88
```

---

## Data Cleaning Notes
- Skips rows with empty, `"null"`, or missing `followers` or `popularity`
- Parses `followers` as `float` and `popularity` as `int`
- Ignores invalid or corrupt lines using `try-except`

---

## Interpretation Summary

- Artists with higher popularity scores tend to have more followers.
- Outliers (low popularity but high followers) may indicate legacy artists or niche genres.
- This model can be extended to include genre filtering, standard deviation analysis, or visualization.

---

## Execution Evidence

Include these screenshots in the submission under `/evidence`:

- `hadoop_version.png` — Hadoop version output
- `jps_running.png` — Daemons running
- `namenode_ui.png` — Web UI of HDFS
- `resourcemanager_ui.png` — Web UI of YARN
- `job_result_output.png` — Final result or terminal output

---