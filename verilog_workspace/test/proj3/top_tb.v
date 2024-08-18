`timescale 100ns / 10ns

module top_tb();
	// define signal
	reg r_clk;
	wire w_timer_1r0sec;
	wire w_timer_0r3sec;
	wire w_timer_2r8sec;

	// 1MHz clock
	initial
		r_clk = 0;
	
	always #(5)
		r_clk <= ~r_clk;

	top top_inst(
		.i_clk(r_clk),
		.o_timer_1r0sec(w_timer_1r0sec),
		.o_timer_0r3sec(w_timer_0r3sec),
		.o_timer_2r8sec(w_timer_2r8sec)
		);
	
	initial
		#100000000 $finish();
	
	initial begin
		$dumpfile("wave.vcd");
		$dumpvars(0, top_inst);
	end

endmodule
