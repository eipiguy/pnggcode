---
author: eipiguy
project: pnggcode
title: png to gcode
tags: [png, art, gcode, plot]
date: 2023-07-12
---

## png to gcode

This is a way of processing png images into a "cell shaded" style, and then creating the gcode needed to plot the result with a 2d pen plotter.

I'm starting with images that are already close to being "cell shaded", but need cleaning. I also want to create a corresponding svg file to match the gcode that's being sent out.

## Influences

- A
- B

## Goals

Start with [big concepts](#summary) and [break them down](#influences) into [progressively smaller bits](#distinctions) until you have [things that seem manageable](#goals).

This is an evolving list. It will change based on obstacles and requirements that arise, and will grow and shrink as tasks are completed, added, and learning makes bigger tasks easier.

- [ ] Main thing to do
  - [ ] There are always parts to it
  - [ ] More than one thing makes a list
- [ ] Make a follow up task

> Tasks age like milk, not like wine. Only plan what is necessary. "Pie in the sky" ideas go in separate documents.

### Constraints?

## Method

[How does it work?](#goals) [What depends on what?](#constraints) What gets done in what order? Change this as necessary.

```mermaid
flowchart LR
  A[Sharp Corner Box] -->|Arrow Text| B(Rounded Box);
  B --> C{Decision Diamond};
  C -->|Option 1| D[Result 1];
  C -->|Option 2| E[Result 2];
```

## Testing

How do we run [tests](#testing)? How do we interpret failures and file an item? Where do we track bugs?

1. Where is the main test file?
2. Test names reflect what failed and why
3. More details available in a [log somewhere](#records)

### Records

A table of the "health records" of the project's components

|Date         |Metric 1 | Metric 2  |
|-            |-        |-          |
|2023-07-08   |Purple   |85%        |
|2023-07-15   |Blue     |85%        |
|-            |-        |-          |
