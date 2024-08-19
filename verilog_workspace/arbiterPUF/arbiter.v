module arbiter(
	input [1:0] i_line,
	output [1:0] response
);
	wire Q_int, Qn_int;
	
	assign #1 Q_int = ~(i_line[0] & Qn_int);
	assign #1 Qn_int = ~(i_line[1] & Q_int);
	assign response[0] = Q_int;
	assign response[1] = Qn_int;

endmodule
