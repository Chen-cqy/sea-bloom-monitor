<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>藻华动态数字孪生监控平台</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box;font-family:"Microsoft YaHei",sans-serif;}
  body{background:#0a192f;color:#fff;overflow:hidden;}
  .container{
    display:grid;
    grid-template-areas:"header header header" "left main right" "footer footer footer";
    grid-template-columns:270px 1fr 360px;
    grid-template-rows:60px 1fr 70px;
    height:100vh;
  }
  .header{
    grid-area:header;
    background:linear-gradient(90deg,#0a2344,#0c3872);
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:22px;
    font-weight:bold;
    border-bottom:1px solid #1a9bfc;
    position:relative;
  }
  #timeNow{position:absolute;right:20px;font-size:14px;color:#a0cfff;}
  .left{
    grid-area:left;
    background:#0c1a2f;
    border-right:1px solid #1a9bfc;
    padding:16px;
    overflow-y:auto;
  }
  .panel-title{font-size:16px;margin-bottom:12px;padding-left:8px;border-left:3px solid #1a9bfc;}
  .card{background:#112a4f;padding:10px;border-radius:6px;margin-bottom:10px;}
  .filter-item{margin:6px 0;cursor:pointer;}
  .main{grid-area:main;position:relative;overflow:hidden;background:#0f2547;}
  .map-wrap{
    width:100%;
    height:100%;
    position:relative;
    cursor:grab;
    transform-origin:center center;
  }
  #mapImg{
    position:absolute;
    top:0;left:0;
    width:100%;height:100%;
    object-fit:cover;
  }

  .point{
    position:absolute;
    width:6px;height:6px;
    background:#ff3333;
    border-radius:50%;
    border:1px solid #fff;
    cursor:pointer;
    z-index:6;
    box-shadow:0 0 4px red;
    transition: transform 0.2s;
  }
  .point:hover{transform:scale(2);}
  .point.active{background:#1a9bfc;box-shadow:0 0 8px #1a9bfc;}

  .right{
    grid-area:right;
    background:#0c1a2f;
    border-left:1px solid #1a9bfc;
    padding:16px;
    overflow-y:auto;
  }
  .detail{background:#112a4f;padding:12px;border-radius:6px;line-height:1.8;font-size:14px;margin-bottom:12px;}
  .chart-box{
    background:#112a4f;
    padding:12px;
    border-radius:6px;
    margin-top:8px;
  }
  .chart-title{
    font-size:14px;
    margin-bottom:8px;
    color:#a0cfff;
  }
  .trend-row{
    display:flex;
    justify-content:space-between;
    font-size:13px;
    padding:5px 0;
    border-bottom:1px dashed #2a4a7a;
  }
  .trend-val{
    color:#1a9bfc;
    font-weight:bold;
  }
  .algae-chart{
    height:100px;
    background:linear-gradient(to top,#1a9bfc33 0%,#1a9bfc00 100%);
    border-radius:4px;
    position:relative;
    margin-top:8px;
  }
  .algae-line{
    position:absolute;
    bottom:0;
    left:0;
    width:100%;
    height:70%;
    background:linear-gradient(0deg,#1a9bfc44,transparent);
    clip-path: polygon(0 80%, 10% 65%, 20% 72%, 30% 50%, 40% 42%, 50% 35%, 60% 28%, 70% 22%, 80% 18%, 90% 25%, 100% 40%);
  }
  .tag{
    display:inline-block;
    padding:2px 6px;
    background:#1a9bfc33;
    color:#1a9bfc;
    border-radius:3px;
    font-size:12px;
    margin-right:4px;
  }
  .footer{
    grid-area:footer;
    background:#0a192f;
    border-top:1px solid #1a9bfc;
    display:flex;
    align-items:center;
    padding:0 20px;
    gap:12px;
  }
  .ctrl-btn{padding:6px 10px;background:#1a9bfc;border:none;border-radius:4px;color:#fff;cursor:pointer;}
  .timeline{flex:1;height:6px;background:#152a4f;border-radius:3px;position:relative;cursor:pointer;}
  .progress{position:absolute;height:100%;width:0%;background:#1a9bfc;border-radius:3px;}
  .dot{position:absolute;width:12px;height:12px;background:#fff;border-radius:50%;top:50%;transform:translate(-50%,-50%);cursor:pointer;}
</style>
</head>
<body>
<div class="container">
  <div class="header">藻华动态数字孪生监控平台<span id="timeNow"></span></div>
  
  <div class="left">
    <div class="panel-title">数据筛选</div>
    <div class="card">
      <label class="filter-item"><input type="checkbox" checked> 船舶巡航</label><br>
      <label class="filter-item"><input type="checkbox" checked> 无人机巡航</label><br>
      <label class="filter-item"><input type="checkbox" checked> 卫星遥感</label><br>
      <label class="filter-item"><input type="checkbox" checked> 视频监控</label>
    </div>
    <div class="panel-title">搜索</div>
    <input type="text" placeholder="区域/点位编号" style="width:100%;padding:6px;background:#112a4f;border:1px solid #1a9bfc;color:#fff;border-radius:4px;margin-bottom:10px;">
    
    <div class="panel-title">实时状态</div>
    <div class="card" style="font-size:13px;line-height:1.8;">
      <div>✅ 在线监测：正常</div>
      <div>✅ 数据同步：正常</div>
      <div>⚠️ 预警数量：<span id="warnCount">0</span> 条</div>
      <div>🕒 更新时间：实时</div>
    </div>
  </div>

  <div class="main" id="mapContainer">
    <div class="map-wrap" id="mapWrap">
      <img id="mapImg" src="海域地图.jpg" alt="中国海域地图">
    </div>
  </div>

  <div class="right">
    <div class="detail" id="siteInfo">
      <div><b>请点击地图任意位置查看监测数据</b></div>
    </div>

    <div class="chart-box">
      <div class="chart-title">📊 藻华浓度实时趋势</div>
      <div class="algae-chart">
        <div class="algae-line" id="algaeLine"></div>
      </div>
      <div style="display:flex;justify-content:space-between;font-size:12px;color:#88abda;margin-top:4px;">
        <span>0时</span><span>6时</span><span>12时</span><span>18时</span><span>24时</span>
      </div>
    </div>

    <div class="chart-box" style="margin-top:12px;">
      <div class="chart-title">📈 关键指标监测</div>
      <div id="keyItems">
        <div class="trend-row"><span>叶绿素a浓度</span><span class="trend-val">--</span></div>
        <div class="trend-row"><span>藻华覆盖面积</span><span class="trend-val">--</span></div>
        <div class="trend-row"><span>水温</span><span class="trend-val">--</span></div>
        <div class="trend-row"><span>盐度</span><span class="trend-val">--</span></div>
        <div class="trend-row"><span>预测风险指数</span><span class="trend-val">--</span></div>
      </div>
    </div>

    <div class="chart-box" style="margin-top:12px;">
      <div class="chart-title">📍 当前优势藻种</div>
      <div style="padding-top:6px;" id="algaeTags">
        <span class="tag">--</span>
      </div>
    </div>

    <div class="detail" style="margin-top:12px;">
      <div style="color:#ff9800;font-weight:bold;">⚠️ 预警提示</div>
      <div style="font-size:12px;line-height:1.6;margin-top:4px;" id="warnTip">
        暂无预警信息
      </div>
    </div>
  </div>

  <div class="footer">
    <button class="ctrl-btn" id="play">播放</button>
    <button class="ctrl-btn" id="prev">上一帧</button>
    <div class="timeline" id="timeline"><div class="progress" id="progress"></div><div class="dot" id="dot"></div></div>
    <button class="ctrl-btn" id="next">下一帧</button>
  </div>
</div>

<script>
function updateTime(){const d=new Date();document.getElementById('timeNow').innerText=d.toLocaleString();}
setInterval(updateTime,1000);updateTime();

const mapContainer = document.getElementById('mapContainer');
const mapWrap = document.getElementById('mapWrap');
const siteInfo = document.getElementById('siteInfo');
const keyItems = document.getElementById('keyItems');
const algaeTags = document.getElementById('algaeTags');
const warnTip = document.getElementById('warnTip');
const warnCount = document.getElementById('warnCount');

let scale = 1;
const maxScale = 10;
const minScale = 0.5;
let isDrag = false;
let startX, startY;
let x = 0, y = 0;

let lastPoint = null;

// 点击地图任意位置生成点位 + 刷新右侧数据
mapContainer.addEventListener('click', function(e){
  if(isDrag) return;

  const rect = mapContainer.getBoundingClientRect();
  const px = e.clientX - rect.left;
  const py = e.clientY - rect.top;

  if(lastPoint) mapWrap.removeChild(lastPoint);

  const p = document.createElement('div');
  p.className = 'point active';
  p.style.left = px + 'px';
  p.style.top = py + 'px';
  mapWrap.appendChild(p);
  lastPoint = p;

  // 生成随机但逼真的数据
  const chl = (Math.random()*6+1).toFixed(2);
  const area = (Math.random()*150+20).toFixed(1);
  const temp = (Math.random()*6+19).toFixed(1);
  const salt = (Math.random()*5+28).toFixed(1);
  const risk = Math.floor(Math.random()*40+40);

  const names = ['胶州湾','青岛近海','日照外海','连云港','盐城','长江口','上海','杭州湾','宁波','台州','温州','闽东','黄海中部','东海北部'];
  const name = names[Math.floor(Math.random()*names.length)] + '监测点';

  const algaeTypes = ['甲藻','硅藻','绿藻','夜光藻','棕囊藻','甲藻群落','浮游藻'];
  const a1 = algaeTypes[Math.floor(Math.random()*algaeTypes.length)];
  const a2 = algaeTypes[Math.floor(Math.random()*algaeTypes.length)];

  const riskLevel = risk > 70 ? '高风险' : risk > 50 ? '中风险' : '低风险';
  const warnNum = risk > 70 ? '3' : risk > 50 ? '1' : '0';

  siteInfo.innerHTML = `
    <div><b>📍 ${name}</b></div>
    <div>风险等级：${riskLevel}</div>
    <div>监测状态：正常监测中</div>
  `;

  keyItems.innerHTML = `
    <div class="trend-row"><span>叶绿素a浓度</span><span class="trend-val">${chl} μg/L</span></div>
    <div class="trend-row"><span>藻华覆盖面积</span><span class="trend-val">${area} km²</span></div>
    <div class="trend-row"><span>水温</span><span class="trend-val">${temp} ℃</span></div>
    <div class="trend-row"><span>盐度</span><span class="trend-val">${salt} ‰</span></div>
    <div class="trend-row"><span>预测风险指数</span><span class="trend-val">${risk} %</span></div>
  `;

  algaeTags.innerHTML = `<span class="tag">${a1}</span><span class="tag">${a2}</span>`;

  warnTip.innerText = riskLevel=='高风险' 
    ? '该区域藻华浓度持续上升，存在扩散风险，请加强巡航监测。'
    : riskLevel=='中风险'
    ? '该区域水质存在异常，建议持续关注后续变化趋势。'
    : '该区域水质正常，暂未发现明显藻华风险。';

  warnCount.innerText = warnNum;
});

// 地图拖拽缩放
mapContainer.addEventListener('wheel', e => {
  e.preventDefault();
  scale += e.deltaY > 0 ? -0.1 : 0.1;
  scale = Math.max(minScale, Math.min(maxScale, scale));
  mapWrap.style.transform = `translate(${x}px,${y}px) scale(${scale})`;
});

mapContainer.addEventListener('mousedown', e => {
  isDrag = true;
  startX = e.clientX;
  startY = e.clientY;
  mapContainer.style.cursor = 'grabbing';
});

window.addEventListener('mousemove', e => {
  if(!isDrag) return;
  const dx = e.clientX - startX;
  const dy = e.clientY - startY;
  x += dx;
  y += dy;
  mapWrap.style.transform = `translate(${x}px,${y}px) scale(${scale})`;
  startX = e.clientX;
  startY = e.clientY;
});

window.addEventListener('mouseup', ()=>{
  isDrag = false;
  mapContainer.style.cursor = 'grab';
});

// 底部时间轴
const timeline=document.getElementById('timeline');
const progress=document.getElementById('progress');
const dot=document.getElementById('dot');
const play=document.getElementById('play');
let playing=false,timer,per=0;
timeline.onclick=e=>{
  const r=timeline.getBoundingClientRect();
  per=((e.clientX-r.left)/r.width)*100;
  progress.style.width=per+'%';dot.style.left=per+'%';
};
play.onclick=()=>{
  if(!playing){
    playing=true;play.innerText='暂停';
    timer=setInterval(()=>{
      per+=0.5;
      if(per>100)per=0;
      progress.style.width=per+'%';
      dot.style.left=per+'%';
    },200);
  }else{
    playing=false;play.innerText='播放';clearInterval(timer);
  }
};
document.getElementById('next').onclick=()=>{per+=10;if(per>100)per=0;progress.style.width=per+'%';dot.style.left=per+'%';}
document.getElementById('prev').onclick=()=>{per-=10;if(per<0)per=100;progress.style.width=per+'%';dot.style.left=per+'%';}
</script>
</body>
</html>