`timescale 100ns / 10ps

module top_tb();
	reg CLK;

	initial
		CLK <= 1'b0;

	always #5
		CLK <= ~CLK;

	reg [3:0] challenge = 4'b1001;
	
	wire torig;
	
	wire [1:0] delay_line_1;
	wire [1:0] delay_line_2;
	wire [1:0] delay_line_3;
	wire [1:0] delay_line_4;

	selector selector_inst_1(
		.challenge(challenge[0]),
		.i_line[0](torig),
		.i_line[1](torig),
		.o_line(delay_line_1)
	);
	selector selector_inst_2(
		.challenge(challenge[0]),
		.i_line[0](torig),
		.i_line[1](torig),
		.o_line(delay_line_2)
	);
	selector selector_inst_3(
		.challenge(challenge[0]),
		.i_line[0](torig),
		.i_line[1](torig),
		.o_line(delay_line_3)
	);
	selector selector_inst_4(
		.challenge(challenge[0]),
		.i_line[0](torig),
		.i_line[1](torig),
		.o_line(delay_line_4)
	);

endmodule
