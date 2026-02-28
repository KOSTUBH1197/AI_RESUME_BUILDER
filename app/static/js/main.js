/* Main JS for small interactions */
function setProgress(percent){
  const bar=document.getElementById('progress-bar');
  const txt=document.getElementById('score-text');
  if(bar) bar.style.width=percent+'%';
  if(txt) txt.innerText='Score: '+percent+'%';
}

window.setProgress=setProgress;
