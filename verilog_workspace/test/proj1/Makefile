COMP = iverilog
EXEC = vvp
SHOW_WAVE = gtkwave
TARGETS = top_tb.v top.v

all: $(TARGETS)
	$(COMP) -o a.out $^
	$(EXEC) a.out
	$(SHOW_WAVE) wave.vcd

.PHONY: clean
clean:
	rm -rf a.out wave.vcd
