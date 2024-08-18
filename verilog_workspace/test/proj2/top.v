module top(
	input i_clk,
	output o_timer_1r0sec
);
	
	//1.0sec timer
	timer timer_1r0sec_inst(
		.i_clk(i_clk),
		.o_timer(o_timer_1r0sec)
	);

endmodule
