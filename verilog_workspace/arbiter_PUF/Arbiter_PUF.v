module Arbiter_PUF(
    input CLK,
    input [15:0] SW,
    output [3:0] LD
);

    reg [31:0] counter;         // クロックカウント用レジスタ
    wire [3:0] response;         // レスポンス信号
    reg update_response;        // レスポンス更新フラグ
//    reg test_led = 0;

    // クロックカウント
    always @(posedge CLK) begin
        if (counter >= 32'd50000000 - 1) begin // 50MHzクロックで1秒カウント
            counter <= 0;
            update_response <= 1; // 1秒ごとにレスポンスを更新
//            test_led <= ~test_led;
        end else begin
            counter <= counter + 1;
            update_response <= 0;
        end
    end

    // bit_arbiter モジュールのインスタンス化とレスポンスの更新
    bit_arbiter inst1 (
        .SW(SW[3:0]),
        .response(response[0])
    );
    bit_arbiter inst2 (
        .SW(SW[7:4]),
        .response(response[1])
    );
    bit_arbiter inst3 (
        .SW(SW[11:8]),
        .response(response[2])
    );
    bit_arbiter inst4 (
        .SW(SW[15:12]),
        .response(response[3])
    );

    assign LD = response;
//    assign LED = test_led;
endmodule