`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2024/08/20 23:04:43
// Design Name: 
// Module Name: TestBench
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////

module TestBench;

    // Declare the signals
    reg CLK;
    reg [15:0] SW;
    wire [3:0] LD; // Output should be wire as it's driven by Arbiter_PUF
    reg LDL = 0;

    // Instantiate the Arbiter_PUF module
    
    // Generate a clock signal with a period of 10 ns (100 MHz)
    always begin
        #5 CLK = ~CLK; // Toggle clock every 5 ns
    end

    // Initialize signals and apply test stimuli
    initial begin
        // Initialize signals
        CLK = 0;
        SW = 16'b0000_0000_0000_0000; // Initial switch state

        // Apply test stimuli
        #10 SW = 16'b1111_0000_0000_0000; // Change switch state after 10 ns
        #10 SW = 16'b0000_1111_0000_0000; // Change switch state after another 10 ns
        #10 SW = 16'b0000_0000_1111_0000; // Change switch state after another 10 ns
        #10 SW = 16'b1111_1111_1111_1111; // Change switch state after another 10 ns

        // Add more stimulus as needed

        // Finish the simulation after sufficient time
        #100;
        $stop;
    end
            
        Arbiter_PUF uut(
        .CLK(CLK),
        .SW(SW),
        .LD(LD)
        );

    // Monitor outputs (optional)
    initial begin
        $monitor("At time %t, SW = %b, LD = %b", $time, SW, LD);
    end

endmodule
