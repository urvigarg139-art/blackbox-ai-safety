let chart;

function loadExample(){

code.value=
`// SQL Injection
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

document.getElementById("status").innerText="Analyzing...";

setTimeout(()=>{

fetch("/scan",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({code:code.value})
})
.then(r=>r.json())
.then(d=>{

status.innerText="Complete";

critical.innerText=d.critical;
high.innerText=d.high;
medium.innerText=d.medium;
low.innerText=d.low;

if(chart) chart.destroy();

chart=new Chart(chart,{
type:"doughnut",
data:{
labels:["Critical","High","Medium","Low"],
datasets:[{
data:[d.critical,d.high,d.medium,d.low],
backgroundColor:["#ff3b3b","#ff9b21","#ffd93b","#3bff8f"]
}]
},
options:{plugins:{legend:{display:false}}}
});

let html="";
d.issues.forEach(i=>{
html+=`<div class="issue">${i}</div>`;
});

issues.innerHTML=html;

});

},1200);
}