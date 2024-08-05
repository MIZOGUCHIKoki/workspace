CC = gcc
CFLAGS = 
SUB_OBJS = heapOperation.o

OBJS = dataOperation.o binarySearch.o $(SUB_OBJS)
TARGETS = heapSort

all: $(TARGETS)
	@echo "----- EXCEC -----"
	./$(TARGETS)
	@echo "----- CLEAN -----"
	make clean

$(TARGETS): $(OBJS) $(TARGETS).o
	$(CC) $(CFLAGS) -o $@ $(TARGETS).o $(OBJS)
	
%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<


# -c means compile only, no link

# $^ means all the files on the right side of the colon (list of dependencies).
# $@ means the file on the left side of the colon (the target name).
# $< means the first item in the dependencies list.
# $? means all the dependencies that are newer than the target.

PHONY: clean excec
clean:
	rm -f $(OBJS) $(TARGETS).o $(TARGETS)
excec: $(TARGETS)
	./$(TARGETS)
	make clean
