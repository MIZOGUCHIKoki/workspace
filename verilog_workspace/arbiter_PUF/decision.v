module decision(
    input wire [1:0] in,
    output wire response
);

    // 2入力 NANDゲートで動作するシンプルな例
    wire Q, Qn;
    
    // Q と Qn を互いに依存させているロジック
    assign Q = ~(in[0] & in[1]);
    assign Qn = ~(in[1] & Q);
    
    // Qn を response として出力
    assign response = Qn;

endmodule
