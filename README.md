# Image Segmentation via Union Set

“Efficient Graph-Based Image Segmentation”，IJCV 2004

## Algorithm

1. Blur the image.

2. Taking each pixel as the vertex, the connected edge of its 4-neighborhood or 8-neighborhood is edge, and the weight of each edge is the dissimilarity between the pixel and its 4-neighborhood or 8-neighborhood. Each edge is sorted according to its dissimilarity.

3. Traverse each edge from small to large. If the two vertices of the edge belong to different sets, and the self-dissimilarity threshold of the set to which the two vertices belong is larger than the dissimilarity of the edge, the two sets will be merged. The operations of searching and merging are accelerated by Union Set.

4. If the merging occurs, the self-dissimilarity threshold of the merged set will be updated. Because only the parent node is valid in the union query set, only the parent node's threshold needs to be updated. At this time, the threshold value will be equal to the weight of the current edge plus the new constant.

5. After traversing, each edge is traversed again from small to large. If any one of the two vertices of the edge belongs to a set with much few elements, the set of the two vertices will be merged.

## Experiments

`python3 test.py`
you can check the detail of parameters in this code.
