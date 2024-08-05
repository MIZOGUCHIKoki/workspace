## Included sort algorithms
* `selectionSort.c`: selection sort
* `insertSort.c`: insert sort
* `heapSort.c`: heap sort

## How to use?
If you want to execute `xxxSort.c`, set the sort to the target of `Makefile`, as follows.

```
TARGETS = xxxSort
```

Heap sort is required `heapOperation.c`, so set sub-object `heapOperation.o` to the `$SUB_OBJS` in `Makefile`, as follows.

```
SUB_OBJS = heapOperation.o
```
