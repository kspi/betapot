#!/usr/bin/env python3
"""
Generates grid of previews.
"""
import betapot
import numpy
import pandas
import seaborn
import fractions
seaborn.set_style("ticks")

def minplot(x, y, **kwargs):
    seaborn.plt.plot(x, y, **kwargs)
    seaborn.plt.axis('off')

def main():
    scales = [2, 3]
    param = [round(100 / x) / 100 for x in reversed(scales)] + [1] + scales

    ass = []
    bss = []
    ix = []
    vs = []
    for a in param:
        for b in param:
            indices, vals = betapot.lookup_table(float(a), float(b), 256, 0, 255)
            ix += list(indices)
            vs += list(vals)
            ass += list(numpy.repeat(a, len(indices)))
            bss += list(numpy.repeat(b, len(indices)))
    df = pandas.DataFrame(numpy.c_[ix, vs, ass, bss],
                          columns=["indices", "vals", "A", "B"])

    # Initialize a grid of plots with an Axes for each walk
    grid = seaborn.FacetGrid(df, col="A", row="B", margin_titles=True)

    grid.map(minplot, "indices", "vals")
    grid.set(xlim=(-1, 256), ylim=(-1, 256))

    # Adjust the arrangement of the plots
    grid.fig.tight_layout(w_pad=1)

    seaborn.plt.savefig("grid.png", dpi=60)
    seaborn.plt.show(block=True)

if __name__ == "__main__":
    main()
