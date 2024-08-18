module top(
	input i_clk,
	output o_timer_1r0sec,
	output o_timer_0r3sec,
	output o_timer_2r8sec
);
	
	//1.0sec timer
	timer #(
		.TIME (20'd1000000),
		.WIDTH(20)
	) timer_1r0sec_inst(
		.i_clk(i_clk),
		.o_timer(o_timer_1r0sec)
	);
	timer #(
		.TIME (19'd300000),
		.WIDTH(19)
	) timer_0r3sec_inst(
		.i_clk(i_clk),
		.o_timer(o_timer_0r3sec)
	);
	timer #(
		.TIME (22'd28000000),
		.WIDTH(22)
	) timer_2r8sec_inst(
		.i_clk(i_clk),
		.o_timer(o_timer_2r8sec)
	);

endmodule
