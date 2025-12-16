(function (){
    "use strict";

    // =========================
    // 日本祝日・休業日判定
    // =========================
    function isJapaneseHoliday(date) {
        var holidays = [
            '2025-12-27',
            '2025-12-28',
            '2025-12-29',
            '2025-12-30',
            '2025-12-31',
            '2026-01-01',
            '2026-01-02',
            '2026-01-03',
            '2026-01-04',
            '2026-01-12',
            '2026-02-11',
            '2026-02-23',
            '2026-03-20',
            '2026-04-29',
            '2026-05-03',
            '2026-05-04',
            '2026-05-05',
            '2026-05-06',
            '2026-07-20',
            '2026-08-11',
            '2026-09-21',
            '2026-09-22',
            '2026-09-23'

        ];

        var y = date.getFullYear();
        var m = ('0' + (date.getMonth() + 1)).slice(-2);
        var d = ('0' + date.getDate()).slice(-2);

        return holidays.indexOf(y + '-' + m + '-' + d) !== -1;
    }

    // 「希望日」が変更された時に実行
    collaboflow.events.on('request.input.fid117.change',function(data){

        if (data.parts.fid117.value != "" && data.parts.fid117.value != null) {

            // 当日日付
            var kanoubi = new Date();
            var dayOfWeek = kanoubi.getDay();

            // 最短受付可能日（5営業日以降）
            switch (dayOfWeek) {
                case 0:
                case 1:
                case 2:
                case 3:
                case 4:
                    kanoubi.setDate(kanoubi.getDate() + 8);
                    break;
                case 5:
                    kanoubi.setDate(kanoubi.getDate() + 10);
                    break;
                case 6:
                    kanoubi.setDate(kanoubi.getDate() + 9);
                    break;
            }

            kanoubi = new Date(
                kanoubi.getFullYear(),
                kanoubi.getMonth(),
                kanoubi.getDate()
            );

            // 希望日
            var kiboubi = new Date(data.parts.fid117.value);

            // =========================
            // ① 周末チェック（新增）
            // =========================
            var selectedDay = kiboubi.getDay();
            if (selectedDay === 0 || selectedDay === 6) {
                window.alert('土日を希望日として選択することはできません。');
                data.parts.fid117.value = "";
                data.parts.fid117.focus();
                return false;
            }

            // =========================
            // ② 祝日・休業日チェック
            // =========================
            if (isJapaneseHoliday(kiboubi)) {
                window.alert('祝日・休業日は対応不可日のため、別の日付を選択してください。');
                data.parts.fid117.value = "";
                data.parts.fid117.focus();
                return false;
            }

            // =========================
            // ③ 最短日チェック
            // =========================
            if (kiboubi < kanoubi) {
                window.alert(
                    'ＰＣ初期化の要望受付は、土日祝日および当社「日曜定休者」で定められている休日を除く５営業日以降としています。\n' +
                    '緊急の場合は、「その他特記事項」に理由を記入の上、日本情報産業様またはＩＴ推進部へご連絡ください。'
                );
                data.parts.fid117.value = "";
                data.parts.fid117.focus();
                return false;
            }
        }

        return true;
    });

})();
