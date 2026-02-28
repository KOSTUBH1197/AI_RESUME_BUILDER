async function analyzeATS(){
  const jd=document.getElementById('job').value;
  const resume=document.getElementById('resume').value;
  const resultDiv=document.getElementById('ats-result');
  resultDiv.innerText='Analyzing...';
  try{
    const resp=await axios.post('/api/analyze_ats', {job_description: jd, resume_text: resume});
    const data=resp.data;
    // Render results
    let html='';
    const score = data.score || (data.match_score||0);
    setProgress(Number(score));
    html += `<div class="card"><h4>Suggestions</h4><p>${(data.suggestions||'No suggestions')}</p></div>`;
    html += '<div class="card"><h4>Matched</h4><div>';
    (data.matched_keywords||[]).forEach(k=>{html+=`<span class="badge match">${k}</span>`});
    html += '</div><h4>Missing</h4><div>';
    (data.missing_keywords||[]).forEach(k=>{html+=`<span class="badge missing">${k}</span>`});
    html += '</div></div>';
    resultDiv.innerHTML=html;
  }catch(e){
    resultDiv.innerText='Error: '+(e.response?.data?.detail||e.message);
  }
}
