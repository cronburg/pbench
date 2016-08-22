#!/usr/bin/env python2.7
import os
join = os.path.join

html = \
"""
<html>
<head>
<title>Latency</title>
<link rel="stylesheet" href="jschart/jschart.css"/>
</head>
<body>
<script src="https://d3js.org/d3.v3.min.js" charset="utf-8"></script>
<script src="https://d3js.org/d3-queue.v3.min.js" charset="utf-8"></script>
<script src="jschart/jschart.js" charset="utf-8"></script>
<script src="other.js/saveSvgAsPng.js" charset="utf-8"></script>
<div id='jschart_latency'>
  <script>
    var data_dir = "%s";
    create_graph(0, "xy", "jschart_latency", "Percentiles", "Time (ms)", "Latency (s)", { plotfiles: [data_dir + "/avg.log", data_dir + "/med.log", data_dir + "/p90.log", data_dir + "/p99.log"], sort_datasets: false, x_log_scale: false });
    create_graph(0, "xy", "jschart_latency", "Max", "Time (ms)", "Latency (s)", { plotfiles: [data_dir + "/max.log"], sort_datasets: false, x_log_scale: false });
    create_graph(0, "xy", "jschart_latency", "Min", "Time (ms)", "Latency (s)", { plotfiles: [data_dir + "/min.log"], sort_datasets: false, x_log_scale: false }); 
  </script>
</div>
<script>finish_page()</script>
</body>
</html>
"""

columns = ["samples", "min", "avg", "median", "p90", "p95", "p99", "max"]

def main(ctx):
  global html

  out_files = [open(join(ctx.DIR, "%s.log" % c), 'w') for c in columns]

  with open(join(ctx.DIR, 'hist.csv', 'r')) as csv:
    csv.readline()
    for line in csv:
      vs = csv.split(', ')
      for i in range(len(columns)):
        out_files[i].write("%d %s\n" % (vs[0], vs[i+1].rstrip()))
  
  html = html % ctx.DIR
  with open(join(ctx.DIR, 'index.html'), 'w') as fp:
    fp.write(html)

if __name__ == '__main__':
  import argparse
  p = argparse.ArgumentParser()
  arg = p.add_argument
  arg('DIR', help='results directory')
  main(p.parse_args())

