import numpy as np
import cv2

# 并查集节点
class Node:
    def __init__(self, parent, rank=0, size=1):
        self.parent = parent
        self.rank = rank
        self.size = size

    def __repr__(self):
        return '(parent=%s, rank=%s, size=%s)' % (self.parent, self.rank, self.size)

# 每个pixel作为并查集一个节点 
class ImageNode(Node):
    def __init__(self, parent, xy, values, rank=0, size=1):
        super(ImageNode, self).__init__(parent, rank=rank, size=size)
        self.xy = xy
        self.values = values
    
    def diff(self, image_node, phi=1):
        return phi * np.sum((self.xy - image_node.xy) ** 2) + np.sum((self.values - image_node.values) ** 2)

# 并查集的查找与合并操作 
class ImageUnion:
    def __init__(self, image):
        height = image.shape[0]
        width = image.shape[1]
        self.num_set = height * width
        self.nodes = []
        for y in range(height):
            for x in range(width):
                parent = y * width + x
                xy = np.array([x, y])
                values = image[y, x]
                self.nodes.append(ImageNode(parent, xy, values))
        
    def find(self, idx):
        parent = idx
        while self.nodes[parent].parent != parent:
            parent = self.nodes[parent].parent
        self.nodes[idx].parent = parent
        return parent

    def merge(self, idx1, idx2):
        self.num_set -= 1
        if self.nodes[idx1].rank < self.nodes[idx2].rank:
            self.nodes[idx1].parent = idx2
            self.nodes[idx2].size += self.nodes[idx1].size
            return idx2
        else:
            self.nodes[idx2].parent = idx1
            self.nodes[idx1].size += self.nodes[idx2].size

            if self.nodes[idx1].rank == self.nodes[idx2].rank:
                self.nodes[idx1].rank += 1
            return idx1

    def __len__(self):
        return self.num_set
        
    def __getitem__(self, idx):
        return self.nodes[idx]

# 稀疏图的初始化以及用并查集合并的操作
class ImageGraph:
    def __init__(self, image, min_percent=0.01, num_neighbor=8, K=10, phi=1):
        self.K = K
        self.min_percent = min_percent
        self.image = image
        self.union = ImageUnion(image)
        self.height = image.shape[0]
        self.width = image.shape[1]
        self.edges = []
        assert num_neighbor == 4 or num_neighbor == 8, "num_neighbor must be 4 or 8"
        self.init_edges(phi, num_neighbor)
        self.edges.sort(key=lambda x:x[2])
        self.thresholds = [self.threshold(K, 1) for i in range(len(self.union))]

    def get_id(self, x, y):
        return y * self.width + x

    def threshold(self, K, size):
        return K * 1.0 / size

    # 初始化边权值
    def init_edges(self, phi, num_neighbor=8):
        phi *= 3 * np.max(self.image) ** 2 / np.sum(np.array(self.image.shape) ** 2)
        for y in range(self.height):
            for x in range(self.width):
                if y < self.height - 1:
                    node1 = self.union[self.get_id(x, y)]
                    node2 = self.union[self.get_id(x, y+1)]
                    self.edges.append((self.get_id(x, y), self.get_id(x, y+1), node1.diff(node2, phi)))

                if x < self.width - 1:
                    node1 = self.union[self.get_id(x, y)]
                    node2 = self.union[self.get_id(x+1, y)]
                    self.edges.append((self.get_id(x, y), self.get_id(x+1, y), node1.diff(node2, phi)))

                if num_neighbor == 8 and x < self.width - 1 and y < self.height - 1:
                    node1 = self.union[self.get_id(x, y)]
                    node2 = self.union[self.get_id(x+1, y+1)]
                    self.edges.append((self.get_id(x, y), self.get_id(x+1, y+1), node1.diff(node2, phi)))

                if num_neighbor == 8 and x > 0 and y < self.height - 1:
                    node1 = self.union[self.get_id(x, y)]
                    node2 = self.union[self.get_id(x-1, y+1)]
                    self.edges.append((self.get_id(x, y), self.get_id(x-1, y+1), node1.diff(node2, phi)))
    
    # 利用并查集进行合并
    def cluster(self):
        for edge in self.edges:
            parent_a = self.union.find(edge[0])
            parent_b = self.union.find(edge[1])

            if parent_a != parent_b and edge[2] <= self.thresholds[parent_a] and edge[2] <= self.thresholds[parent_b]:
                parent = self.union.merge(parent_a, parent_b)
                self.thresholds[parent] = edge[2] + self.threshold(self.K, self.union[parent].size)

        min_size = self.height * self.width * self.min_percent

        for edge in self.edges:
            parent_a = self.union.find(edge[0])
            parent_b = self.union.find(edge[1])

            if parent_a != parent_b and (self.union[parent_a].size < min_size or self.union[parent_b].size < min_size):
                self.union.merge(parent_a, parent_b)

        return self.union

    def generate_mask(self, union):
        parent_nodes = []
        for i, node in enumerate(union):
            if node.parent == i:
                parent_nodes.append(i)
        # print(parent_nodes)
        segment = np.zeros((self.height, self.width))
        for y in range(self.height):
            for x in range(self.width):
                segment[y, x] = parent_nodes.index(union.find(self.get_id(x, y)))
        return segment

def segment(image, ksize=5, sigma=5, min_percent=0.01, num_neighbor=8, K=10, phi=1):
    image = cv2.GaussianBlur(src=image, ksize=(ksize, ksize), sigmaX=sigma, sigmaY=sigma)
    graph = ImageGraph(image, min_percent, num_neighbor, K, phi)
    union = graph.cluster()
    return graph.generate_mask(union)