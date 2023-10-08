# PNG to G-Code

This is a way of processing png images into a "cell shaded" style, and then creating the gcode needed to plot the result with a 2d pen plotter.

I'm starting with images that are already close to being "cell shaded", but need cleaning. I also want to create a corresponding svg file to match the gcode that's being sent out.

## Method

```mermaid
flowchart LR

input--->png
draw--->png

png--->analysis
subgraph analysis
  color--->grouping--->contours
end

analysis--->interface
subgraph interface
  subgraph panel
    pallette
    histograms
    cells
    fill
  end
  subgraph overlay
    heatmap
    grouping
    edges
  end
end

interface--->path_planning
subgraph path_planning
  layers--->segmentation--->periodicity--->next_nearest
end

path_planning--->translator--->gcode
translator--->svg
```
