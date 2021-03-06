#!/usr/bin/env python2.7
import os
join = os.path.join

html = \
"""
<html>
<head>
<title>Latency</title>
<link rel="stylesheet" href="/static/css/v0.3/jschart.css"/>
</head>
<body>
<script src="/static/js/v0.3/d3.min.js" charset="utf-8"></script>
<script src="/static/js/v0.3/d3-queue.min.js" charset="utf-8"></script>
<script src="/static/js/v0.3/jschart.js" charset="utf-8"></script>
<script src="/static/js/v0.3/saveSvgAsPng.js" charset="utf-8"></script>
<div id='jschart_latency'>
  <script>
    create_graph(0, "xy", "jschart_latency", "Percentiles", "Time (s)", "Latency (s)",
        { plotfiles: [ "avg.log", "median.log", "p90.log",
                       "p99.log", "min.log", "max.log" ],
          sort_datasets: false, x_log_scale: false
        });
  </script>
</div>
<script>finish_page()</script>
</body>
</html>
"""

columns = ["samples", "min", "avg", "median", "p90", "p95", "p99", "max"]

def main(ctx):

  out_files = [open(join(ctx.DIR, "%s.log" % c), 'w') for c in columns]
  for i in range(len(columns)):
    out_files[i].write("#LABEL:%s\n" % columns[i])

  with open(join(ctx.DIR, 'hist.csv'), 'r') as csv:
    csv.readline()
    for line in csv:
      vs = line.split(', ')
      for i in range(len(columns)):
        out_files[i].write("%.4f %s\n" % (int(vs[0]) / 1000.0, vs[i+1].rstrip()))

  with open(join(ctx.DIR, 'results.html'), 'w') as fp:
    fp.write(html)

if __name__ == '__main__':
  import argparse
  p = argparse.ArgumentParser()
  arg = p.add_argument
  arg('DIR', help='results directory')
  main(p.parse_args())

