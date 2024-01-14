<template>
    <div class="card">
        <div class="header">
            <h1 class="title">小六壬</h1>
        </div>
        <div class="content">
            <div v-if="!result">
                <button class="btn" @click="loadData">起卦</button>
                <div class="tips">一事一卦，多测不灵。</div>
            </div>
            <div class="info" v-else>
                <span class="date" v-if="date">{{ date }}</span>
                <span class="status" :class="{ 'unlucky': resultIndex % 2 }" v-if="result">{{ result }}</span>
            </div>
            <div v-if="guaCi">
                <div class="verse" v-for="(item, i) in guaCi.split('；')" :key="i">{{ item }}{{ i === 0 ? '；' : '。' }}</div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { DayList, GuaCi, MonthList, ResultList, TimeList } from '../lunar.modal';
declare const chrome: any;

export default defineComponent({
    name: 'Popup',
    setup() {
        const date = ref('');
        const result = ref('');
        const resultIndex = ref(0);
        const guaCi = ref('');
        function loadData() {
            const currentDate: Date = new Date();

            const year: number = currentDate.getFullYear();
            let month: number | string = currentDate.getMonth() + 1; // 月份是从 0 开始的
            let day: number | string = currentDate.getDate();
            const hour: number = currentDate.getHours();

            // 确保月份和日期始终有两位数字
            month = month < 10 ? '0' + month : month;
            day = day < 10 ? '0' + day : day;

            const formattedDate: string = `${month}-${day}`;
            chrome.runtime.sendMessage({ action: 'fetchData', data: year }, (response: any) => {
                if (response?.data) {
                    const lunarData = JSON.parse(decodeURIComponent(escape(atob(response.data.content))))[formattedDate];
                    const timeIndex = getTime(hour);
                    date.value = `${lunarData.month}${lunarData.day} ${TimeList[timeIndex]}`;
                    const monthIndex = MonthList.indexOf(lunarData.month);
                    const dayIndex = DayList.indexOf(lunarData.day);
                    const sum = monthIndex + dayIndex + timeIndex;
                    const index = getResult(sum);
                    resultIndex.value = index;
                    result.value = ResultList[index];
                    guaCi.value = GuaCi[index];
                }
            });
        }
        // 获取当前时辰
        function getTime(hour: number) {
            let index = Math.floor((hour + 1) / 2);
            if (index > 11) {
                index = 0;
            }
            return index;
        }

        function getResult(sum: number) {
            const index = sum % 6;
            return index;
        }
        return { date, result, resultIndex, guaCi, loadData };
    }
});
</script>

<style lang="scss">
.card {
    width: 350px;
    background: #fff;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    margin: 20px auto;

    .header {
        background-color: #5D93E1;
        padding: 15px;

        .title {
            margin: 0;
            color: #fff;
            font-size: 24px;
            white-space: nowrap;
        }
    }

    .content {
        padding: 20px;
        text-align: center;

        .btn {
            background-color: #42b983;
            border: none;
            border-radius: 4px;
            color: #fff;
            cursor: pointer;
            padding: 10px 100px;
            font-size: 18px;
            white-space: nowrap;

            &:hover {
                background-color: darken(#42b983, 10%);
            }
        }

        .tips {
            color: #999;
            font-size: 18px;
            margin-top: 15px;
        }

        .info {
            margin: 15px 0 10px;

            .date {
                display: block;
                color: #333;
                font-size: 27px;
                margin-bottom: 5px;
            }

            .status {
                display: block;
                color: #f00;
                font-size: 27px;
                font-weight: 900;
                margin-bottom: 5px;

                &.unlucky {
                    color: #333;
                }
            }
        }

        .verse {
            background-color: #f2f2f2;
            border-left: 5px solid #42b983;
            padding: 10px;
            margin-top: 15px;
            font-style: italic;
            font-size: 22px;
        }
    }
}
</style>
