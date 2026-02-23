let donut;

function loadExample(){
code.value=`// SQL Injection
query = "SELECT * FROM users WHERE id = " + user
db.execute(query)

// XSS
print("<script>alert('hack')</script>")

// Hardcoded secret
password="123456"

// Unsafe eval
eval(query)`
}

function scan(){

status.innerText="Analyzing...";
document.body.classList.add("scanning");

setTimeout(()=>{

fetch("/scan",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({code:code.value})
})
.then(r=>r.json())
.then(d=>{

document.body.classList.remove("scanning");
status.innerText="Complete";

critical.innerText=d.critical;
high.innerText=d.high;
medium.innerText=d.medium;
low.innerText=d.low;

const score=Math.max(0,100-(d.critical*30+d.high*15+d.medium*7));

document.getElementById("scoreText").innerText=score;

if(donut) donut.destroy();

donut=new Chart(chart,{
type:"doughnut",
data:{
datasets:[{
data:[score,100-score],
backgroundColor:["#ff4b4b","#111"],
borderWidth:0
}]
},
options:{
cutout:"80%",
plugins:{legend:{display:false}}
}
});

let html="";
d.issues.forEach(i=>{
html+=`
<div class="issue-card">
<div class="issue-title">${i}</div>
<div class="issue-meta">Detected vulnerability</div>
</div>`;
});

issues.innerHTML=html;

});

},1600);
}