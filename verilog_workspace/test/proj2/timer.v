module timer (
	input i_clk,
	output o_timer
);
	reg [19:0] r_cnt = 20'd0;
	reg r_timer = 1'b0;
	
	always @(posedge i_clk) begin
		if (r_cnt == 20'd999999) begin
			r_timer <= 1'b1;
			r_cnt <= 20'd0;
		end else begin
			r_timer <= 1'b0;
			r_cnt <= r_cnt + 20'd1;
		end
	end
	assign o_timer = r_timer;
endmodule
