module selector(
	input challenge,
	input [0:1] i_line ,
	output [0:1] o_line
);
	
	assign o_line[0] = challenge ? i_line[0] i_line[1];
	assign o_line[1] = challenge ? i_line[1] i_line[0];

endmodule
