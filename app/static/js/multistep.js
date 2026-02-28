let currentStep=1;
function showStep(n){
  document.querySelectorAll('.step').forEach(s=>s.style.display='none');
  const el=document.querySelector('.step[data-step="'+n+'"]');
  if(el) el.style.display='block';
}
function nextStep(){currentStep++;showStep(currentStep)}
function prevStep(){currentStep--;if(currentStep<1)currentStep=1;showStep(currentStep)}

async function submitResume(){
  const form=document.getElementById('resume-form');
  const fd=new FormData(form);
  const payload={
    header:{name:fd.get('name'), title:fd.get('title'), email:fd.get('email'), phone:fd.get('phone')},
    summary:fd.get('summary')||'',
    experience:(fd.get('experience')||'').split('\n'),
    education:(fd.get('education')||'').split('\n'),
    projects:(fd.get('projects')||'').split('\n'),
    skills:[]
  };
  const resDiv=document.getElementById('resume-result');
  resDiv.innerText='Generating...';
  try{
    const resp=await axios.post('/api/generate_resume', payload);
    resDiv.innerText=JSON.stringify(resp.data, null, 2);
  }catch(e){resDiv.innerText='Error: '+(e.response?.data?.detail||e.message)}
}

window.nextStep=nextStep;window.prevStep=prevStep;window.submitResume=submitResume;showStep(1);
