const ResultList = ['大安', '留连', '速喜', '赤口', '小吉', '空亡'];
const TimeList = ['子时', '丑时', '寅时', '卯时', '辰时', '巳时', '午时', '未时', '申时', '酉时', '戌时', '亥时'];
const MonthList = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'];
const DayList = ['初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十', '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十', '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十'];
const GuaCi = ['大安事事昌，求财在坤方，失物去不远，宅舍保安康；行人身未动，病者主无妨，将军回田野，仔细兴推祥。', '留连事难成，求谋月未明，凡事只宜缓，去者未回程；失物南方见，急讨方称心，更须防口舌，人口且太平。', '速喜喜来临，求财向南行，失物申未午，逢人路上寻；官事有福德，病者无祸侵，田宅六畜吉，行人有喜音。', '赤口主口舌，官非切要防，失物急去寻，行人有惊慌；六畜多惊怪，病者出西方，更须防诅咒，恐怕染瘟疫。', '小吉最吉昌，路上好商量，阴人来报喜，失物在坤方；行人立便至，交易甚是强，凡是皆和合，病者辱上苍。', '空亡事不祥，阴人多乖张，求财无利益，行人有灾秧；失物寻不见，官事有刑伤，病人逢暗鬼，禳解保安康。'];

// 创建 ListWidget 实例
let widget = new ListWidget();

// 设置小组件背景为渐变色
let gradient = new LinearGradient();
gradient.colors = [new Color("#1D2671"), new Color("#C33764")];
gradient.locations = [0.0, 1.0];
widget.backgroundGradient = gradient;
widget.setPadding(16, 16, 16, 10); // 设置内边距

// 获取数据
await loadData();

async function loadData() {
    const currentDate = new Date();
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth() + 1;
    const day = currentDate.getDate();
    const hour = currentDate.getHours();

    // 格式化日期
    const formattedDate = `${month < 10 ? '0' : ''}${month}-${day < 10 ? '0' : ''}${day}`;

    // 构建请求 URL
    const url = `https://api.github.com/repos/AngusFan-GH/6ren/contents/lunar/data/${year}.json`;
    let req = new Request(url);
    let data = await req.loadJSON();

    // 处理数据
    if (data && data[formattedDate]) {
        const lunarData = data[formattedDate];
        const timeIndex = getTimeIndex(hour);
        const monthIndex = MonthList.indexOf(lunarData.month);
        const dayIndex = DayList.indexOf(lunarData.day);
        const sum = monthIndex + dayIndex + timeIndex;
        const index = sum % 6; // 根据和的余数得出结果索引

        // 添加日期和时辰
        const monthStr = lunarData.month; // 从数据中获取农历月份
        const dayStr = lunarData.day; // 从数据中获取农历日期
        let dateLine = widget.addText(`${monthStr}${dayStr} ${TimeList[timeIndex]}`);
        dateLine.textColor = new Color("#ffffff");
        dateLine.font = Font.boldSystemFont(14);
        widget.addSpacer(5);

        // 添加结果文本
        let resultLine = widget.addText(ResultList[index]);
        resultLine.textColor = index % 2 === 0 ? new Color("#FF0000") : new Color("#42b983");
        resultLine.font = Font.systemFont(22);
        resultLine.shadowColor = new Color("#000");
        resultLine.shadowRadius = 3;
        resultLine.shadowOffset = new Point(0, 1);
        widget.addSpacer(5);

        // 添加卦辞
        let guaCiLines = GuaCi[index].split('；').map(line => `${line}；`);
        guaCiLines.forEach((line, index) => {
            let guaCiLine = widget.addText(index === guaCiLines.length - 1 ? line.slice(0, -1) : line);
            guaCiLine.textColor = new Color("#ffffff");
            guaCiLine.font = Font.boldSystemFont(10);
            widget.addSpacer(3);
        });
    } else {
        let errorText = widget.addText("数据未找到");
        errorText.textColor = new Color("#ffffff");
        errorText.font = Font.systemFont(12);
    }
}

function getTimeIndex(hour) {
    let index = Math.floor((hour + 1) / 2);
    if (index > 11) {
        index = 0;
    }
    return index;
}

// 计算当前时间到下一个整点的时间差 
let currentDate = new Date();
let nextRefresh = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate(), currentDate.getHours() + 1); widget.refreshAfterDate = nextRefresh;



// 设置小组件并完成脚本
Script.setWidget(widget);
Script.complete();

// 预览小组件
widget.presentSmall();
