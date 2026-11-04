(()=>{
  const note=document.querySelector('.voice-personal-note');
  const trigger=document.querySelector('.trg-note');
  const close=note?.querySelector('.note__close');
  if(!note||!trigger||!close)return;
  let wasOpen=false;
  const hero=document.getElementById('voice-hero');
  function sync(){
    const open=document.body.classList.contains('is-note-open');
    trigger.setAttribute('aria-expanded',String(open));
    note.setAttribute('aria-hidden',String(!open));
    if(open&&!wasOpen){
      hero?.contentWindow?.postMessage({voiceParent:true,active:false},location.origin);
      note.scrollTop=0;
      note.querySelector('.note__texts').scrollTop=0;
      close.focus({preventScroll:true});
    }else if(!open&&wasOpen){
      hero?.contentWindow?.postMessage({voiceParent:true,active:!!window.__voiceHeroActive},location.origin);
      trigger.focus({preventScroll:true});
    }
    wasOpen=open;
  }
  new MutationObserver(sync).observe(document.body,{attributes:true,attributeFilter:['class']});
  note.addEventListener('keydown',event=>{
    if(event.key!=='Tab')return;
    const elements=[...note.querySelectorAll('button,a[href],video[controls],[tabindex="0"]')];
    const first=elements[0],last=elements[elements.length-1];
    if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus();}
    else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}
  });
  sync();
})();
