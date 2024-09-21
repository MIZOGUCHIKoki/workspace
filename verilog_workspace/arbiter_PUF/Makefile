COMP = iverilog
EXEC = vvp
SHOW_WAVE = gtkwave
TARGETS = 1bit_arbiter.v Arbiter_PUF.v decision.v selector.v TestBench.v

all: $(TARGETS)
	$(COMP) -o a.out $^
	$(EXEC) a.out
	$(SHOW_WAVE) wave.vcd

.PHONY: clean
clean:
	rm -rf a.out wave.vcd
