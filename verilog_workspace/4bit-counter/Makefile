COMP = iverilog
EXEC = vvp
SHOW_WAVE = gtkwave
TARGETS = counter.v counter_test.v

all: $(TARGETS)
	$(COMP) -o a.out $^
	$(EXEC) a.out
	$(SHOW_WAVE) wave.vcd
