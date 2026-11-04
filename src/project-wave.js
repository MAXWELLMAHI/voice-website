(()=>{
  'use strict';
  const section=document.getElementById('project-wave');if(!section)return;
  const stage=document.getElementById('voice-projects');
  const track=document.getElementById('wave-score-track');
  const container=document.getElementById('wave-score-container');
  const playhead=document.getElementById('wave-playhead');
  const playheadLabel=document.getElementById('playhead-label');
  const progressFill=document.getElementById('wave-progress-fill');
  const contact=document.getElementById('contact');

  // HUD elements
  const hudIndex=document.getElementById('hud-index');
  const hudKicker=document.getElementById('hud-kicker');
  const hudTitle=document.getElementById('hud-title');
  const hudSummary=document.getElementById('hud-summary');
  const hudWorkTags=document.getElementById('hud-work-tags');
  const hudOpenBtn=document.getElementById('hud-open-btn');

  // Drawer / Modal elements
  const drawer=document.getElementById('wave-project-drawer');
  const drawerClose=document.getElementById('drawer-close');
  const drawerIndex=document.getElementById('drawer-index');
  const drawerSubheading=document.getElementById('drawer-subheading');
  const drawerTitle=document.getElementById('drawer-title');
  const drawerSummary=document.getElementById('drawer-summary');
  const drawerWork=document.getElementById('drawer-work');
  const drawerGallery=document.getElementById('drawer-gallery');
  const drawerFullLink=document.getElementById('drawer-full-link');

  const rawData=document.getElementById('project-wave-data');
  const projects=rawData?JSON.parse(rawData.textContent):[];
  const stations=[...stage.querySelectorAll('.wave-project-station')];

  let currentIndex=0;
  let isHoverLocked=false;
  let hoverTimeout=null;

  const clamp=(val,min=0,max=1)=>Math.max(min,Math.min(max,val));

  function updateHUD(index){
    const p=projects[index];if(!p)return;
    const numStr=String(p.num || (projects.length - index)).padStart(2,'0');
    if(hudIndex)hudIndex.textContent=`${numStr} / ${String(projects.length).padStart(2,'0')}`;
    if(hudKicker)hudKicker.textContent=p.subheading;
    if(hudTitle)hudTitle.textContent=p.title;
    if(hudSummary)hudSummary.textContent=p.summary;
    if(hudWorkTags){
      hudWorkTags.innerHTML=p.work.split('·').map(w=>`<span class="hud-tag">${w.trim()}</span>`).join('');
    }
    if(playheadLabel)playheadLabel.textContent=`TRACK ${numStr}`;
  }

  function setActiveStation(index,fromHover=false){
    if(index<0||index>=stations.length)return;
    currentIndex=index;
    stations.forEach((st,i)=>{
      st.classList.toggle('is-active',i===index);
    });
    updateHUD(index);
    if(fromHover){
      isHoverLocked=true;
      clearTimeout(hoverTimeout);
      hoverTimeout=setTimeout(()=>{isHoverLocked=false;},1200);
    }
  }

  function openDrawer(index){
    const p=projects[index];if(!p||!drawer)return;
    setActiveStation(index);
    const numStr=String(p.num || (projects.length - index)).padStart(2,'0');
    if(drawerIndex)drawerIndex.textContent=numStr;
    if(drawerSubheading)drawerSubheading.textContent=p.subheading;
    if(drawerTitle)drawerTitle.textContent=p.title;
    if(drawerSummary)drawerSummary.textContent=p.summary;
    if(drawerWork)drawerWork.textContent=p.work;
    if(drawerFullLink)drawerFullLink.href=`/projects/${p.id}.html`;

    if(drawerGallery){
      drawerGallery.innerHTML='';
      if(p.images && p.images.some(Boolean)){
        p.images.forEach((img, j)=>{
          if(!img) return;
          const slot=document.createElement('div');
          slot.className='drawer-gallery-slot';
          slot.innerHTML=`<img src="/assets/${img}" alt="${p.title} — image ${j+1}" loading="lazy">`;
          drawerGallery.appendChild(slot);
        });
      } else {
        const pile=stations[index]?.querySelector('.station-card-pile');
        if(pile){
          [...pile.children].forEach(card=>{
            const slot=document.createElement('div');
            slot.className='drawer-gallery-slot';
            slot.innerHTML=card.innerHTML;
            drawerGallery.appendChild(slot);
          });
        }
      }
    }
    try{
      drawer.showModal();
    }catch(err){
      drawer.setAttribute('open','');
    }
    document.body.style.overflow='hidden';
  }

  function closeDrawer(){
    if(!drawer)return;
    try{
      drawer.close();
    }catch(err){
      drawer.removeAttribute('open');
    }
    document.body.style.overflow='';
  }

  if(drawerClose)drawerClose.addEventListener('click',closeDrawer);
  if(drawer){
    drawer.addEventListener('click',e=>{
      if(e.target===drawer)closeDrawer();
    });
  }
  if(hudOpenBtn){
    hudOpenBtn.addEventListener('click',()=>openDrawer(currentIndex));
  }

  // Station & Card Interactions
  stations.forEach((st,index)=>{
    // Hover: immediately reveal information & activate pile
    st.addEventListener('pointerenter',()=>{
      setActiveStation(index,true);
    });
    st.addEventListener('focus',()=>{
      setActiveStation(index,true);
    });

    // Click: open project story drawer
    st.addEventListener('click',e=>{
      if(e.target.closest('a'))return; // allow links if any
      openDrawer(index);
    });

    // Enter key opens drawer
    st.addEventListener('keydown',e=>{
      if(e.key==='Enter'||e.key===' '){
        e.preventDefault();
        openDrawer(index);
      }
    });
  });

  // Scroll Synchronization
  function onScroll(){
    const isMobile=innerWidth<701;
    const r=section.getBoundingClientRect();
    const active=r.top<innerHeight*0.85&&r.bottom>innerHeight*0.15;
    const contactRect=contact?.getBoundingClientRect();
    const contactActive=!!contactRect&&contactRect.top<innerHeight&&contactRect.bottom>0;

    document.body.classList.toggle('project-wave-active',active);
    document.body.classList.toggle('voice-contact-active',contactActive);
    window.__voiceProjectWaveActive=active||contactActive;

    if(!active)return;

    const scrollHeight=r.height-innerHeight;
    const progress=clamp(-r.top/Math.max(1,scrollHeight),0,1);

    if(progressFill){
      progressFill.style.width=`${(progress*100).toFixed(1)}%`;
    }

    if(!isMobile&&track&&container){
      // Horizontal translation along staff lines
      const maxTranslate=track.scrollWidth-container.clientWidth+innerWidth*0.35;
      const currentX=progress*maxTranslate;
      track.style.transform=`translateX(-${currentX}px)`;

      // Identify closest station to playhead
      if(!isHoverLocked&&playhead){
        const playheadX=playhead.getBoundingClientRect().left;
        let closest=0,minDist=Infinity;
        stations.forEach((st,i)=>{
          const stRect=st.getBoundingClientRect();
          const centerX=stRect.left+stRect.width*0.5;
          const dist=Math.abs(centerX-playheadX);
          if(dist<minDist){
            minDist=dist;
            closest=i;
          }
        });
        if(closest!==currentIndex){
          setActiveStation(closest);
        }
      }
    }
  }

  // Keyboard navigation
  addEventListener('keydown',e=>{
    if(drawer?.hasAttribute('open')||drawer?.open){
      if(e.key==='Escape')closeDrawer();
      return;
    }
    if(!window.__voiceProjectWaveActive)return;
    if(e.key==='ArrowRight'){
      setActiveStation(Math.min(projects.length-1,currentIndex+1),true);
    }else if(e.key==='ArrowLeft'){
      setActiveStation(Math.max(0,currentIndex-1),true);
    }
  });

  addEventListener('scroll',onScroll,{passive:true});
  addEventListener('resize',onScroll,{passive:true});

  // Initialize
  setActiveStation(0);
  onScroll();
})();
