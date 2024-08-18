module timer #(
	parameter TIME = 20'd1000000,
	parameter WIDTH = 20
)(
	input i_clk,
	output o_timer
);
	reg [WIDTH-1:0] r_cnt = {WIDTH{1'b0}};
	reg r_timer = 1'b0;
	
	always @(posedge i_clk) begin
		if (r_cnt == TIME - 1) begin
			r_timer <= 1'b1;
			r_cnt <= {WIDTH{1'b0}};
		end else begin
			r_timer <= 1'b0;
			r_cnt <= r_cnt + {{(WIDTH-1){1'b0}}, 1'b1};// 00...01
		end
	end
	assign o_timer = r_timer;
endmodule
