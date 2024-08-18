`timescale 1ns / 100ps

module top_tb;
    reg r_clk;
    reg [3:0] r_sw_n;
    wire w_led_blue;
    wire w_led_green;
    wire w_led_orange;
    wire w_led_red;

    initial begin
        r_clk <= 0;
    end

    always #(5) r_clk <= ~r_clk;

    // Create switch signal: 1=OFF, 0=ON
    initial fork
        r_sw_n = 4'b1111;
        #100 r_sw_n = 4'b1110;
        #200 r_sw_n = 4'b1101;
        #300 r_sw_n = 4'b1011;
        #400 r_sw_n = 4'b0111;
        #500 r_sw_n = 4'b1111;

        #600 r_sw_n = 4'b1110;
        #700 r_sw_n = 4'b1101;
        #800 r_sw_n = 4'b1011;
        #500 r_sw_n = 4'b0111;
        #1000 r_sw_n = 4'b1111;

				#1100 $finish();
    join

    // Instantiate top module
    top top_inst (
        .i_clk(r_clk),
        .i_sw_n(r_sw_n),
        .o_led_blue(w_led_blue),
        .o_led_green(w_led_green),
        .o_led_orange(w_led_orange),
        .o_led_red(w_led_red)
    );

    initial begin
        $dumpfile("wave.vcd");
        $dumpvars(0, top_inst);
    end

endmodule

