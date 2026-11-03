(() => {
  const $ = (id) => document.getElementById(id);
  const csvInput = $('csvFile');
  const dropZone = $('dropZone');
  const schemaBody = $('schemaBody');
  const dataPreview = $('dataPreview');
  const qualityTitle = $('qualityTitle');
  const qualityDetails = $('qualityDetails');
  const continueSourceButton = $('continueSourceButton');
  const sourceStepStatus = $('sourceStepStatus');
  const sourceActions = document.querySelector('.source-actions');
  let csvFile = null;
  let profile = null;
  let mappings = [];
  let signedIn = null;
  fetch('/api/auth/me').then(r=>r.json()).then(d=>{signedIn=!!d.authenticated;}).catch(()=>{signedIn=null;});
  const defaultSchema = [
    {name:'student_id',type:'string',required:true},
    {name:'full_name',type:'string',required:true},
    {name:'email',type:'string',required:true},
    {name:'payment_status',type:'boolean',required:true},
  ];
  const types = ['string','integer','decimal','boolean','date_iso'];
  const esc = (text) => String(text).replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const getSchema = () => [...schemaBody.querySelectorAll('tr')].map((row) => ({
    name:row.querySelector('[data-name]').value.trim(),type:row.querySelector('[data-type]').value,
    required:row.querySelector('[data-required]').checked,
  }));
  function renderSchema(fields=defaultSchema) {
    schemaBody.replaceChildren();
    fields.forEach((field) => {
      const row = document.createElement('tr');
      row.innerHTML = `<td><input data-name aria-label="Target field name" type="text" maxlength="80" value="${esc(field.name)}"></td><td><select data-type aria-label="Field type">${types.map(t=>`<option ${t===field.type?'selected':''}>${t}</option>`).join('')}</select></td><td><input data-required aria-label="Required field" type="checkbox" ${field.required?'checked':''}></td><td><button class="remove-field" aria-label="Remove field" type="button">×</button></td>`;
      row.querySelector('.remove-field').addEventListener('click', () => { row.remove(); renderMappings(); });
      row.querySelectorAll('input,select').forEach((el) => el.addEventListener('change', renderMappings));
      schemaBody.append(row);
    });
    renderMappings();
  }
  function showError(id, message) { const el=$(id); el.textContent=message; el.hidden=false; }
  function clearError(id) { $(id).hidden=true; $(id).textContent=''; }
  function updateProgress(step) { document.querySelectorAll('.progress-list li').forEach((li,i)=>li.classList.toggle('active',i===step)); }
  function renderFileOverview(body) {
    const preview=Array.isArray(body.preview)?body.preview:[];
    const headers=Array.isArray(body.headers)?body.headers:[];
    if (!dataPreview) return;
    if (!preview.length || !headers.length) {
      dataPreview.innerHTML='<p class="preview-empty">No preview rows are available for this file.</p>';
    } else {
      const visibleHeaders=headers.slice(0,4);
      dataPreview.innerHTML=`<div class="table-scroll"><table class="preview-table"><thead><tr>${visibleHeaders.map(h=>`<th scope="col">${esc(h)}</th>`).join('')}</tr></thead><tbody>${preview.slice(0,4).map(row=>`<tr>${visibleHeaders.map(h=>`<td>${esc(row[h]??'')}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
    }
    const blankCount=(body.columns||[]).reduce((total,column)=>total+Number(column.empty_count||0),0);
    $('qualityIcon').classList.add('is-ready');
    $('qualityIcon').textContent='✓';
    qualityTitle.textContent=blankCount ? 'Profile ready with blanks' : 'No critical issues found';
    qualityDetails.textContent=`${body.row_count} rows profiled · ${blankCount} blank values · ${headers.length} columns`;
    sourceStepStatus.textContent=`Step 1 of 4 — ${$('fileName').textContent}`;
    if (continueSourceButton) continueSourceButton.disabled=false;
  }
  async function loadFile(file) {
    clearError('profileError'); clearError('mappingError'); $('resultSummary').hidden=true;
    if (!file || (!file.name.toLowerCase().endsWith('.csv') && file.type !== 'text/csv')) { showError('profileError','Choose a file with the .csv extension.'); return; }
    if (file.size > 5*1024*1024) { showError('profileError','File exceeds the 5 MB limit.'); return; }
    csvFile=file; $('fileName').textContent=file.name;
    const form=new FormData(); form.append('file',file);
    try {
      const response=await fetch('/api/profile',{method:'POST',body:form});
      const body=await response.json(); if(!response.ok) throw new Error(body.detail||'Could not read this CSV.');
      profile=body; $('profileSummary').hidden=false;
      const preview=Array.isArray(body.preview)?body.preview:[];
      const previewTable=preview.length?`<div class="table-scroll"><table class="preview-table"><caption>First ${preview.length} of ${body.row_count} rows</caption><thead><tr>${body.headers.map(h=>`<th scope="col">${esc(h)}</th>`).join('')}</tr></thead><tbody>${preview.map(row=>`<tr>${body.headers.map(h=>`<td>${esc(row[h]??'')}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`:'';
      $('profileSummary').innerHTML=`<strong>${body.row_count} data rows</strong> · ${body.headers.length} columns<div class="summary-columns">${body.columns.map(c=>`<span>${esc(c.name)} <small>${c.empty_count} blank</small></span>`).join('')}</div>${previewTable}<p class="hint">Up to 3 sample values per column (shown locally): ${body.columns.map(c=>`${esc(c.name)}: ${c.samples.map(v=>`“${esc(v)}”`).join(', ')}`).join(' · ')}</p>`;
       sourceActions?.classList.add('has-file'); renderFileOverview(body); renderMappings(); $('processButton').disabled=false; $('approveMappings').checked=false;
    } catch(error) { csvFile=null; profile=null; sourceActions?.classList.remove('has-file'); $('fileName').textContent='No file selected'; showError('profileError',error.message); }
  }
  function renderMappings(values=mappings) {
    mappings=values;
    const container=$('mappingTable'); container.replaceChildren();
    const schema=getSchema();
    if(!profile || !schema.length){container.innerHTML='<p class="empty-state">Load a CSV and target fields to begin mapping.</p>';return;}
    schema.forEach((field) => {
      const prior=mappings.find(m=>m.target_field===field.name) || {source_column:null,operation:'identity'};
      const row=document.createElement('div');row.className='mapping-item';
      const label=document.createElement('span');label.className='mapping-target';label.textContent=field.name+(field.required?' *':'');
      const source=document.createElement('select');source.setAttribute('aria-label',`Source column for ${field.name}`);
      source.innerHTML='<option value="">— Unmapped —</option>'+profile.headers.map(h=>`<option value="${esc(h)}" ${h===prior.source_column?'selected':''}>${esc(h)}</option>`).join('');
      const operation=document.createElement('select');operation.className='mapping-op';operation.setAttribute('aria-label',`Transformation for ${field.name}`);
      const ops=['identity','trim','collapse_whitespace','lowercase','uppercase'];operation.innerHTML=ops.map(op=>`<option value="${op}" ${op===prior.operation?'selected':''}>${op.replaceAll('_',' ')}</option>`).join('');
      const persist=()=>{mappings=mappings.filter(m=>m.target_field!==field.name);mappings.push({source_column:source.value||null,target_field:field.name,operation:operation.value,needs_review:true});$('approveMappings').checked=false;};
      source.addEventListener('change',persist);operation.addEventListener('change',persist);
      row.append(label,source,operation);container.append(row);
    });
    $('processButton').disabled=!csvFile;
  }
  dropZone.addEventListener('click',()=>csvInput.click());
  dropZone.addEventListener('keydown',(event)=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();csvInput.click();}});
  csvInput.addEventListener('change',()=>loadFile(csvInput.files[0]));
  ['dragenter','dragover'].forEach(name=>dropZone.addEventListener(name,e=>{e.preventDefault();dropZone.classList.add('dragover');}));
  ['dragleave','drop'].forEach(name=>dropZone.addEventListener(name,e=>{e.preventDefault();dropZone.classList.remove('dragover');}));
  dropZone.addEventListener('drop',e=>loadFile(e.dataTransfer.files[0]));
  $('exampleButton').addEventListener('click',async()=>{try{const [csv,schema]=await Promise.all([fetch('/examples/registrations.csv'),fetch('/examples/registrations_schema.json')]);if(!csv.ok||!schema.ok)throw new Error('Example files could not be loaded.');const fields=await schema.json();renderSchema(fields);const blob=await csv.blob();loadFile(new File([blob],'registrations.csv',{type:'text/csv'}));}catch(error){showError('profileError',error.message);}});
  $('addField').addEventListener('click',()=>{const current=getSchema();current.push({name:`field_${current.length+1}`,type:'string',required:false});renderSchema(current);});
  $('schemaPreset').addEventListener('change',()=>renderSchema($('schemaPreset').value==='example'?defaultSchema:[]));
  async function requestMappings(mode) {
    clearError('mappingError'); if(!csvFile){showError('mappingError','Choose a CSV first.');return;}
    const form=new FormData();form.append('file',csvFile);form.append('schema_data',JSON.stringify(getSchema()));form.append('mode',mode);form.append('include_samples',String($('sampleConsent').checked));
    try{const response=await fetch('/api/suggest-mappings',{method:'POST',body:form});const body=await response.json();if(!response.ok)throw new Error(body.detail||'Mapping suggestion failed.');mappings=body.mappings;renderMappings(mappings);$('approveMappings').checked=false;updateProgress(2);}catch(error){showError('mappingError',error.message);}
  }
  $('localSuggest').addEventListener('click',()=>requestMappings('local'));
  $('metaSuggest').addEventListener('click',()=>requestMappings('meta'));
  $('approveMappings').addEventListener('change',()=>{if($('approveMappings').checked)updateProgress(2);});
  $('processButton').addEventListener('click',async()=>{
    clearError('processError');$('resultSummary').hidden=true;
    if(!csvFile){showError('processError','Choose a CSV before processing.');return;}
    if(!$('approveMappings').checked){showError('processError','Review your mappings and confirm approval before processing.');return;}
    const schema=getSchema();const names=schema.map(f=>f.name);
    if(!schema.length||schema.some(f=>!f.name)||new Set(names).size!==names.length){showError('processError','Target fields must have non-empty, unique names.');return;}
    const selected=mappings.filter(m=>names.includes(m.target_field));
    if(selected.length!==schema.length){showError('processError','Run local suggestions or choose a source for every target field.');return;}
    if(selected.some(m=>!m.source_column&&schema.find(f=>f.name===m.target_field)?.required)){showError('processError','Map every required field before processing.');return;}
    const form=new FormData();form.append('file',csvFile);form.append('schema_data',JSON.stringify(schema));form.append('mappings_json',JSON.stringify(selected));
    const button=$('processButton');button.disabled=true;button.firstChild.textContent='Processing… ';
    try{const response=await fetch('/api/process',{method:'POST',body:form});if(!response.ok){const data=await response.json();throw new Error(data.detail||'Processing failed.');}const blob=await response.blob();download(blob,'importguard-export.zip');const accepted=response.headers.get('X-Accepted-Rows');const rejected=response.headers.get('X-Rejected-Rows');const exportId=response.headers.get('X-Export-Id');const summary=$('resultSummary');summary.innerHTML=`<strong>${accepted}</strong> accepted · <strong>${rejected}</strong> rejected<br><span>Every input row is accounted for. ZIP package downloaded.${exportId?` Saved to <a href="/dashboard">history</a>.${signedIn===false?' <a href="/signup">Create a free account</a> to keep it.':''}`:''}</span>`;summary.hidden=false;updateProgress(3);}catch(error){showError('processError',error.message);}finally{button.disabled=false;button.firstChild.textContent='Validate & download package ';}
  });
  function download(blob,name){const url=URL.createObjectURL(blob);const link=document.createElement('a');link.href=url;link.download=name;document.body.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);}
  $('recipeFile').addEventListener('change',()=>{$('replayButton').disabled=!$('recipeFile').files.length;});
  $('replayButton').addEventListener('click',()=>{
    const source=document.createElement('input');source.type='file';source.accept='.csv,text/csv';source.addEventListener('change',async()=>{const file=source.files[0];if(!file)return;const form=new FormData();form.append('file',file);form.append('recipe_file',$('recipeFile').files[0]);$('replayButton').disabled=true;
      try{const response=await fetch('/api/replay',{method:'POST',body:form});if(!response.ok){const data=await response.json();throw new Error(data.detail||'Recipe replay failed.');}download(await response.blob(),'importguard-replay.zip');$('replayMessage').className='message success';$('replayMessage').textContent=`Replay complete: ${response.headers.get('X-Accepted-Rows')} accepted, ${response.headers.get('X-Rejected-Rows')} rejected. No model request was made.`;$('replayMessage').hidden=false;}catch(error){$('replayMessage').className='message error';$('replayMessage').textContent=error.message;$('replayMessage').hidden=false;}finally{$('replayButton').disabled=false;}
    });source.click();
  });
  $('resetButton').addEventListener('click',()=>{csvFile=null;profile=null;mappings=[];csvInput.value='';sourceActions?.classList.remove('has-file');$('fileName').textContent='No file selected';$('qualityIcon').classList.remove('is-ready');$('qualityIcon').textContent='·';qualityTitle.textContent='Waiting for a file';qualityDetails.textContent='Your file profile and row checks will appear here.';$('profileSummary').hidden=true;$('approveMappings').checked=false;$('resultSummary').hidden=true;['profileError','mappingError','processError'].forEach(clearError);renderSchema(defaultSchema);updateProgress(0);});
  continueSourceButton?.addEventListener('click',()=>{updateProgress(1);$('schema-heading').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'start'});});
  dataPreview && (dataPreview.innerHTML='<p class="preview-empty">Upload a CSV to preview its first rows.</p>');
  if (continueSourceButton) continueSourceButton.disabled=true;
  renderSchema(defaultSchema);
})();
