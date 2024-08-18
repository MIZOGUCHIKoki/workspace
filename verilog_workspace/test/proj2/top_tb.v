`timescale 100ns / 10ns

module top_tb();
	// define signal
	reg r_clk;
	wire w_timer_1r0sec;

	// 1MHz clock
	initial
		r_clk = 0;
	
	always #(5)
		r_clk <= ~r_clk;

	top top_inst(
		.i_clk(r_clk),
		.o_timer_1r0sec(w_timer_1r0sec)
		);
	
	initial
		#100000000 $finish();
	
	initial begin
		$dumpfile("wave.vcd");
		$dumpvars(0, top_inst);
	end

endmodule
