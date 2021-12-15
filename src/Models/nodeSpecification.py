class NodeSpecification():
    minCPU = 4
    maxCPU = 8
    minRAM = 2
    maxRAM = 32
    OS = "linux"
    Spot = "lowpriority"
    excludedSeries = ['A', 'Av2']