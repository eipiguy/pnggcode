# Color Folders

- Colors are mapped to a color space (RGB/CHS).
- Colors are grouped to form a "directory" of colors called the "ColorTree"
  - Points in color space are grouped into nearest neighbor clusters recursively.
  - Groups are represented by a weighted average of the sub-colors in the group.
    - Number of times color appears in image = weight
- Image preview is presented based on state of color directories (collapsed/open).
  - Selection in image highlights corresponding colors in directory explorer.
  - Directory selection highlights corresponding points in image preview
  - Directories can be dragged and dropped to reorganize.
- Interface
  - File Menu
    - "Save ColorTree"
    - "Load ColorTree"
  - "Load Image" button
  - "Save Preview" button
  - Raw vs preview selection mode switch.
  - Image Preview
  - ColorTree display
