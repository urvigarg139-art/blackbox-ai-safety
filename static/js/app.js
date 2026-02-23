function scan(){

fetch("/audit",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({data:input.value})
})
.then(r=>r.json())
.then(d=>{
score.innerHTML="Risk: "+d.score;
issues.innerHTML=d.issues.join("<br>");

fetch("/history")
.then(r=>r.json())
.then(h=>{
let html="";
h.forEach(x=>html+=`Score ${x[0]} at ${x[1]}<br>`);
history.innerHTML=html;
});
});
}