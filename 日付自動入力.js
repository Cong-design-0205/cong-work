(function() {

    kintone.events.on([
        'app.record.create.change.貸与希望日',
        'app.record.edit.change.貸与希望日'
    ], function(event) {

        var record = event.record;

        // 取得 借与希望日
        var hopeDateStr = record['貸与希望日'].value;
        if (!hopeDateStr) {
            record['日付_0'].value = '';
            return event;
        }

        var hopeDate = new Date(hopeDateStr);

        /*
            ---- 计算“上周五” ----
            星期数 getDay()：日=0, 一=1, ... 五=5, 六=6
            所以：
              希望日的星期（0~6）
              要往回退到上周五 → 固定为退  (day + 2) 天
              例如：
                周一(1) → 退 3 天 → 周五
                周三(3) → 退 5 天 → 周五
                周五(5) → 退 7 天 → 上周五
                周日(0) → 退 2 天 → 周五
        */

        var day = hopeDate.getDay();  
        var diff = day + 2;           // 永远退回到上周五

        var shipDate = new Date(hopeDate);
        shipDate.setDate(hopeDate.getDate() - diff);

        // 格式化
        var yyyy = shipDate.getFullYear();
        var mm = ('0' + (shipDate.getMonth() + 1)).slice(-2);
        var dd = ('0' + shipDate.getDate()).slice(-2);

        // 写入 発送予定日（日付_0）
        record['日付_0'].value = `${yyyy}-${mm}-${dd}`;

        return event;
    });

})();

