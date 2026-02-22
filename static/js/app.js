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
},15);
}

function runAudit(){

let text=document.getElementById("input").innerText;

fetch("/audit",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({data:text})
})
.then(res=>res.json())
.then(d=>{

animateScore(d.confidence);

document.getElementById("critical").innerText=d.issues.length+" CRITICAL";
document.getElementById("high").innerText="0 HIGH";
document.getElementById("medium").innerText="0 MEDIUM";
document.getElementById("low").innerText=d.issues.length==0?"1 LOW":"0 LOW";

let html="";

d.issues.forEach(i=>{
html+=`
<div class="issue" onclick="this.classList.toggle('open')">
🔥 ${i}
<div class="fix">Suggested fix: sanitize inputs / avoid string concat / use env vars.</div>
</div>`;
});

document.getElementById("issues").innerHTML=html;

});
}