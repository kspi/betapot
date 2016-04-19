#!/usr/bin/env python3
"""
Generate and plot potentiometer curve lookup table using Beta CDF.

There are two parameters that determine the curve shape: A and B. If both are 1,
the curve is linear.  If <1, that part of the curve (bottom or top) becomes
steeper.  If >1 it becomes flatter.

Outputs comma separated values suitable for inclusion in a C array.
"""

import numpy
from scipy.stats import beta

def lookup_table(a, b, size, min, max):
    indices = numpy.arange(size)
    x = indices / (size - 1)
    y = beta.cdf(x, a, b)
    vals = numpy.round(y * (max - min) + min).astype(int)
    return indices, vals

def write_table(f, table):
    indices, vals = table
    for i, val in enumerate(vals):
        f.write(str(val))
        if i != len(vals) - 1:
            f.write(",")
        f.write("\n")

def plot_table(table):
    indices, vals = table
    try:
        import seaborn
    except ImportError:
        pass
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 1)
    ax.plot(indices, vals)
    ax.set_xlim(0, numpy.max(indices))
    ax.set_ylim(numpy.min(vals) - 1, numpy.max(vals) + 1)
    fig.canvas.set_window_title("betapot")
    plt.show(block=True)

def main():
    import sys
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("A", type=float, help="bottom flatness")
    parser.add_argument("B", type=float, help="top flatness")
    parser.add_argument("--no-plot", dest='plot', action='store_false', help="don't plot preview")
    parser.add_argument("--size", type=int, default=256, help="size of lookup table (default: 256)")
    parser.add_argument("--min", type=int, default=0, help="minimum output value (default: 0)")
    parser.add_argument("--max", type=int, default=255, help="maximum output value (default: 255)")
    parser.add_argument("--output", type=argparse.FileType('w'), default=sys.stdout, help="output file (default: stdout)")
    parser.set_defaults(plot=True)
    args = parser.parse_args()

    table = lookup_table(args.A, args.B, args.size, args.min, args.max)
    write_table(args.output, table)

    if args.plot:
        plot_table(table)

if __name__ == "__main__":
    main()
