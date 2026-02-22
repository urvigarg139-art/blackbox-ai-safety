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

function setSeverity(score){
let s=document.querySelector(".score");
s.classList.remove("low","medium","high","critical");

if(score==0) s.classList.add("low");
else if(score<40) s.classList.add("medium");
else if(score<70) s.classList.add("high");
else s.classList.add("critical");
}

function runAudit(){

let text=document.getElementById("input").innerText;

// fake scan animation
document.getElementById("progressFill").style.width="100%";

fetch("/audit",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({data:text})
})
.then(res=>res.json())
.then(d=>{

animateScore(d.confidence);
setSeverity(d.confidence);

document.getElementById("critical").innerText=d.issues.length+" 🔴 CRITICAL";
document.getElementById("high").innerText="0 🟠 HIGH";
document.getElementById("medium").innerText="0 🟡 MEDIUM";
document.getElementById("low").innerText=d.issues.length==0?"1 🟢 LOW":"0 🟢 LOW";

let html="";

d.issues.forEach(i=>{
html+=`
<div class="issue" onclick="this.classList.toggle('open')">
🔥 ${i}
<div class="fix">Suggested fix: sanitize inputs, avoid eval, remove hardcoded secrets.</div>
</div>`;
});

document.getElementById("issues").innerHTML=html;

// reset progress
setTimeout(()=>{document.getElementById("progressFill").style.width="0%"},1000);

});
}