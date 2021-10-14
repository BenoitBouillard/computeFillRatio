adjoining = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def compute_max_square(tiles):
    def is_square(x, y, m):
        for dx in range(m):
            for dy in range(m):
                uid = (x + dx, y + dy)
                if uid not in tiles:
                    return False
        return True

    max_square = 0
    for (x, y) in tiles:
        while is_square(x, y, max_square + 1):
            max_square += 1
    return max_square


def compute_zones(tiles):
    tiles = set(tiles)
    clusters = []
    while True:
        if len(tiles) == 0:
            break

        cluster = {tiles.pop()}
        boundary = cluster.copy()

        while True:
            new_c = set()
            for tile in boundary:
                x, y = tile
                for dx, dy in adjoining:
                    if (x + dx, y + dy) in tiles:
                        new_c.add((x + dx, y + dy))
            if new_c:
                cluster |= new_c
                boundary = new_c
                tiles -= new_c
            else:
                break
        clusters.append(cluster)

    clusters.sort(key=len, reverse=True)
    return clusters


def compute_cluster(tiles):
    cluster_tiles = set()
    for (x, y) in tiles:
        for dx, dy in adjoining:
            if (x + dx, y + dy) not in tiles:
                break
        else:
            cluster_tiles.add((x, y))

    if len(cluster_tiles) == 0:
        return 0
    zones = compute_zones(cluster_tiles)
    return max([len(c) for c in zones])


def compute_clusters(tiles):
    if isinstance(list(tiles)[0], str):
        tiles = set([tuple([int(i) for i in t.split('_')]) for t in tiles])
    tiles_d = {}
    for (x, y) in tiles:
        if x not in tiles_d:
            tiles_d[x] = set()
        tiles_d[x].add(y)
    cluster_tiles = set()
    for (x, y) in tiles:
        for dx, dy in adjoining:
            if x + dx not in tiles_d:
                break
            if y + dy not in tiles_d[x + dx]:
                break
        else:
            cluster_tiles.add((x, y))
    return compute_zones(cluster_tiles)


def compute_max_cluster(tiles):
    zones = compute_clusters(tiles)
    return zones[0]


def expand_cluster(cluster, limit):
    expansion = set(cluster)
    frontier = set(cluster)
    for n in range(limit):
        new_frontier = set()
        for x, y in frontier:
            for dx, dy in adjoining:
                if (x + dx, y + dy) not in expansion:
                    new_frontier.add((x + dx, y + dy))
                    expansion.add((x + dx, y + dy))
        frontier = new_frontier
    return expansion

