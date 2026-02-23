function loadExample(){
document.getElementById("input").innerText=
`query = "SELECT * FROM users WHERE id=" + user
eval(query)
password = "123456"
print("<script>alert('hack')</script>")`;
}

function animateScore(target){
let current=0;
let el=document.getElementById("scoreVal");

let interval=setInterval(()=>{
if(current>=target){
clearInterval(interval);
return;
}
current++;
el.innerText=current;
},10);
}

function runAudit(){

document.getElementById("issues").innerHTML="🤖 AI analyzing...";
document.getElementById("progressFill").style.width="100%";

let text=document.getElementById("input").innerText;

fetch("/audit",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({data:text})
})
.then(res=>res.json())
.then(d=>{

animateScore(d.score);

document.getElementById("critical").innerText=d.issues.length+" 🔴 CRITICAL";
document.getElementById("high").innerText="0 🟠 HIGH";
document.getElementById("medium").innerText="0 🟡 MEDIUM";
document.getElementById("low").innerText=d.issues.length==0?"1 🟢 LOW":"0 🟢 LOW";

let html="";

d.issues.forEach(i=>{
html+=`
<div class="issue" onclick="this.classList.toggle('open')">
🔥 ${i}
<div class="fix">
Suggested fix: sanitize inputs, avoid eval, remove hardcoded secrets.
<button onclick="navigator.clipboard.writeText('sanitize inputs, avoid eval, remove hardcoded secrets')">
Copy Fix
</button>
</div>
</div>`;
});

document.getElementById("issues").innerHTML=html;

setTimeout(()=>{document.getElementById("progressFill").style.width="0%"},1000);

fetch("/history")
.then(r=>r.json())
.then(h=>{
let historyHtml="<h3>Previous Scans</h3>";
h.forEach(s=>{
historyHtml+=`<div class="issue">Score: ${s.score}</div>`;
});
document.getElementById("history").innerHTML=historyHtml;
});

});
}