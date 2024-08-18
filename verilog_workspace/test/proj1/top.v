module top (
    input i_clk,
    input [3:0] i_sw_n,
    output o_led_blue,
    output o_led_green,
    output o_led_orange,
    output o_led_red
);
		
		wire w_sw0_n_edge;
		reg r_sw0_n_d1;
		reg r_sw0_n_d2;
		reg r_sw0_n_toggle;
		
		initial begin
			r_sw0_n_d1 <= 0;
			r_sw0_n_d2 <= 0;
			r_sw0_n_toggle <= 0;
		end

		// reproduce the delay-line
		always @(posedge i_clk) begin
			r_sw0_n_d1 <= i_sw_n[0];
			r_sw0_n_d2 <= r_sw0_n_d1;
			r_sw0_n_toggle <= (w_sw0_n_edge) ? ~r_sw0_n_toggle : r_sw0_n_toggle;
		end
		assign r_sw0_n_edge = ~r_sw0_n_d1 & r_sw0_n_d2;

    assign o_led_blue = r_sw0_n_toggle;
    assign o_led_green = ~i_sw_n[1];
    assign o_led_orange = ~i_sw_n[2];
    assign o_led_red = ~i_sw_n[3];

endmodule
