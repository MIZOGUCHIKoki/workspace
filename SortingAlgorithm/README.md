## Sorting Algorithms included in the dir
* `selectionSort.c`: Selection sort
* `insertSort.c`: Insert sort
* `heapSort.c`: Heap sort
* `quickSort.c`: Quick sort

## How to use?
If you want to execute `xxxSort.c`, set the sort to the target of `Makefile`, as follows.

```
TARGETS = xxxSort
```

Heap sort is required `heapOperation.c`, so set sub-object `heapOperation.o` to the `$SUB_OBJS` in `Makefile`, as follows.

```
SUB_OBJS = heapOperation.o
```

Set `dataSize` in `sort.h`, as follows if you want to change data size to sort.

```c
#define dataSize 1000
```
