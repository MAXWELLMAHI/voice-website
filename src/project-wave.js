(()=>{
  'use strict';
  const section=document.getElementById('project-wave');if(!section)return;
  const stage=document.getElementById('voice-projects'),timeline=document.getElementById('wave-timeline'),projects=JSON.parse(document.getElementById('project-wave-data').textContent);
  const rows=[...stage.querySelectorAll('.wave-project-row')],links=[...stage.querySelectorAll('.wave-project')],reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const info=document.getElementById('wave-info'),path=document.getElementById('wave-thread-path'),svg=path?.closest('svg'),fill=document.getElementById('wave-scroll-fill'),step=document.getElementById('wave-current-step'),contact=document.getElementById('contact');
  const eqBars=[...stage.querySelectorAll('.wave-sound-equalizer .eq-bar')];

  let width=innerWidth,artWidth=0,artHeight=0,opening=false,dim=null,spotlight=null,resizeTimer,infoIndex=-1;
  let isSectionActive=false,animId=null;

  const clamp=(value,a=0,b=1)=>Math.max(a,Math.min(b,value));

  // Initialize per-project wave physics state
  const state=projects.map((_,index)=>({
    index,
    targetHover:0,
    hoverAmount:0,
    targetMouseX:0,
    mouseX:0,
    targetMouseY:0.5,
    mouseY:0.5,
    energy:0,
    slices:[...links[index].children]
  }));

  // Global pointer tracking
  const mouse={x:-1000,y:-1000,vx:0,vy:0,lastX:0,lastY:0,lastT:performance.now()};
  addEventListener('pointermove',e=>{
    const now=performance.now(),dt=Math.max(1,now-mouse.lastT);
    mouse.vx=(e.clientX-mouse.lastX)/dt;
    mouse.vy=(e.clientY-mouse.lastY)/dt;
    mouse.x=e.clientX;
    mouse.y=e.clientY;
    mouse.lastX=e.clientX;
    mouse.lastY=e.clientY;
    mouse.lastT=now;

    // Distribute acoustic energy to cards near pointer
    const speed=Math.min(4,Math.hypot(mouse.vx,mouse.vy));
    rows.forEach((row,i)=>{
      const link=links[i];
      const r=link.getBoundingClientRect();
      const pad=45;
      if(mouse.x>=r.left-pad&&mouse.x<=r.right+pad&&mouse.y>=r.top-pad&&mouse.y<=r.bottom+pad){
        const nx=clamp((mouse.x-r.left)/r.width,0,1)*2-1; // -1 to 1
        const ny=clamp((mouse.y-r.top)/r.height,0,1);     // 0 to 1
        state[i].targetMouseX=nx;
        state[i].targetMouseY=ny;
        state[i].energy=Math.min(2.8,state[i].energy+speed*0.35);
      }
    });
  },{passive:true});

  function showInfo(index){
    if(opening)return;const project=projects[index];infoIndex=index;
    state[index].targetHover=1;
    document.getElementById('wave-info-index').textContent=String(index+1).padStart(2,'0')+' / PROJECT';
    document.getElementById('wave-info-title').textContent=project.title;
    document.getElementById('wave-info-subheading').textContent=project.subheading;
    document.getElementById('wave-info-summary').textContent=project.summary;
    document.getElementById('wave-info-work').textContent=project.work;
    info.classList.add('is-visible');info.setAttribute('aria-hidden','false');stage.dataset.hovered=project.id;
  }
  function hideInfo(){
    if(infoIndex>=0&&state[infoIndex]){state[infoIndex].targetHover=0;state[infoIndex].targetMouseX=0;state[infoIndex].targetMouseY=0.5;}
    infoIndex=-1;info.classList.remove('is-visible');info.setAttribute('aria-hidden','true');delete stage.dataset.hovered;
  }

  function measure(){
    width=innerWidth;const mobile=width<701;
    artWidth=Math.min(mobile?width-66:width*.44,660);artHeight=artWidth*2/3;
    rows.forEach((row,index)=>{
      const x=mobile?width*.5+Math.sin((index+1)*1.35)*12:width*.43+Math.sin((index+1)*1.35)*Math.min(width*.095,140);
      row.style.setProperty('--art-width',artWidth+'px');row.style.setProperty('--art-height',artHeight+'px');row.style.setProperty('--card-x',x+'px');
      if(mobile)row.style.height=Math.max(520,artHeight+315)+'px';
      else row.style.height=Math.max(innerHeight*.73,artHeight+200)+'px';
      const count=5,gap=mobile?8:11,band=(artHeight-gap*(count-1))/count;
      const columns=projects[index].images.length,columnGap=mobile?6:10,columnWidth=(artWidth-(columns-1)*columnGap)/columns;
      row.style.setProperty('--column-width',columnWidth+'px');row.style.setProperty('--column-step',(columnWidth+columnGap)+'px');
      state[index].slices.forEach((slice,i)=>{
        const top=i*(band+gap);slice.style.top=top+'px';slice.style.height=band+'px';slice.style.setProperty('--band-top',top+'px');slice.dataset.band=String(i+1);
      });
    });
  }

  // Baseline sound wave envelope amplitudes (audio frequency bell curve)
  const baseAmplitudes=[0.66, 0.85, 1.0, 0.88, 0.69];

  // Core sound wave animation & physics loop
  function render(timeMs){
    const t=timeMs*0.001; // seconds
    const mobile=width<701;
    const root=timeline.getBoundingClientRect();
    const originDot=stage.querySelector('.wave-origin-dot');
    const origin=originDot?originDot.getBoundingClientRect():{left:width*0.43,top:root.top+40,width:10,height:10};
    const points=[{x:origin.left+origin.width/2,y:origin.top-root.top+origin.height/2}];

    let current=-1,closest=Infinity;
    let totalEnergy=0;

    rows.forEach((row,index)=>{
      const st=state[index];
      // Smooth lerp physics
      st.hoverAmount+=(st.targetHover-st.hoverAmount)*0.14;
      st.mouseX+=(st.targetMouseX-st.mouseX)*0.16;
      st.mouseY+=(st.targetMouseY-st.mouseY)*0.16;
      st.energy*=0.94; // kinetic decay
      totalEnergy+=st.hoverAmount*2+st.energy;

      const rect=row.getBoundingClientRect();
      const distance=Math.abs(rect.top+artHeight*.5-innerHeight*.5);
      if(distance<closest){closest=distance;current=index;}

      const p=clamp((innerHeight*.5-rect.top)/Math.max(1,innerHeight+rect.height),-.5,.7);
      const scrollMotion=reduced?0:Math.sin(p*Math.PI)*12;
      links[index].style.marginLeft=scrollMotion+'px';

      const center=parseFloat(row.style.getPropertyValue('--card-x'))||width*.43;

      // Sound wave motion on the 5 slices
      st.slices.forEach((slice,i)=>{
        if(reduced){
          const phase=index*1.2+i*.9,shift=Math.sin(phase)*(mobile?10:32);
          const bandWidth=artWidth*baseAmplitudes[i],left=(artWidth-bandWidth)/2+shift;
          slice.style.left=left+'px';slice.style.width=bandWidth+'px';slice.style.setProperty('--band-left',left+'px');
          return;
        }

        // 1. Acoustic Carrier Wave (~0.75 Hz)
        const freq1=0.75;
        const phase1=2*Math.PI*freq1*t + index*1.3 + i*0.84;
        const wave1=Math.sin(phase1);

        // 2. Harmonic Overtone (~2.15 Hz)
        const freq2=2.15;
        const phase2=2*Math.PI*freq2*t + index*2.4 + i*1.48;
        const wave2=Math.sin(phase2)*0.36;

        // 3. Fast Acoustic Flutter (~4.6 Hz)
        const freq3=4.6;
        const phase3=2*Math.PI*freq3*t + i*2.1;
        const wave3=Math.sin(phase3)*0.12;

        const combinedWave=wave1+wave2+wave3; // range approx [-1.48, 1.48]

        // 4. Pointer acoustic disturbance (Gaussian impulse centered on cursor Y)
        const sliceCenterY=(i+0.5)/5;
        const distY=Math.abs(st.mouseY-sliceCenterY)*5;
        const mouseImpulse=Math.exp(-distY*distY*0.75)*st.mouseX*(st.hoverAmount*(mobile?20:34)+st.energy*(mobile?12:22));

        // 5. Kinetic ripple traveling downward
        const ripple=st.energy*Math.sin(10*t - i*1.15)*(mobile?6:11);

        // 6. Dynamic width pulsation (equalizer breathing)
        const ampPulse=Math.sin(phase1+Math.PI*0.5)*0.045 + Math.cos(phase2)*0.024 + st.hoverAmount*0.06*Math.sin(phase2*1.4);
        const bandWidth=artWidth*clamp(baseAmplitudes[i]+ampPulse,0.48,1.06);

        // 7. Lateral displacement
        const maxShift=mobile?12:32;
        const lateralShift=combinedWave*(maxShift*(0.65+st.hoverAmount*0.55)) + mouseImpulse + ripple + Math.sin(p*2+i*.3)*7;
        const baseCenter=(artWidth-bandWidth)/2;
        const left=baseCenter+lateralShift;

        // Apply slice positions and synchronized inner artwork offset
        slice.style.left=left+'px';
        slice.style.width=bandWidth+'px';
        slice.style.backgroundPosition=`${-left}px ${-parseFloat(slice.style.top)}px`;
        slice.style.setProperty('--band-left',left+'px');
      });

      points.push({x:center+scrollMotion,y:rect.top-root.top+44+artHeight*.5});
    });

    // Connecting thread with acoustic resonant wave
    if(path&&svg){
      points.push({x:width*.5,y:timeline.offsetHeight-75});
      let d=`M${points[0].x},${points[0].y}`;
      for(let i=1;i<points.length;i++){
        const a=points[i-1],b=points[i];
        const waveShift=reduced?0:Math.sin(t*3.2 + i*1.35)*7;
        const middleX=(a.x+b.x)/2 + waveShift;
        const middleY=(a.y+b.y)/2;
        d+=` C${middleX},${middleY} ${middleX},${middleY} ${b.x},${b.y}`;
      }
      svg.setAttribute('viewBox',`0 0 ${width} ${timeline.offsetHeight}`);
      path.setAttribute('d',d);
    }

    // Header Sound Wave Equalizer animation
    if(eqBars.length&&!reduced){
      eqBars.forEach((bar,idx)=>{
        const f=0.9+idx*0.28;
        const barWave=Math.abs(Math.sin(t*f*2.6 + idx*0.42));
        const boost=Math.min(0.35,totalEnergy*0.06);
        const scale=clamp(0.18 + barWave*(0.52+boost),0.12,1.0);
        bar.style.transform=`scaleY(${scale.toFixed(3)})`;
      });
    }

    // Scroll metrics & active state
    const sectionRect=section.getBoundingClientRect();
    const active=sectionRect.top<innerHeight*0.85&&sectionRect.bottom>innerHeight*0.15;
    isSectionActive=active;

    const contactRect=contact?.getBoundingClientRect();
    const contactActive=!!contactRect&&contactRect.top<innerHeight&&contactRect.bottom>0;
    document.body.classList.toggle('project-wave-active',active);
    document.body.classList.toggle('voice-contact-active',contactActive);
    window.__voiceProjectWaveActive=active||contactActive;

    const progress=clamp(-sectionRect.top/Math.max(1,sectionRect.height-innerHeight));
    if(fill)fill.style.transform=`scaleY(${progress})`;
    if(step)step.textContent=String(current+1).padStart(2,'0');

    stage.dataset.progress=progress.toFixed(4);
    stage.dataset.project=current>=0?projects[current].id:'engineering';
    stage.dataset.active=String(active);
    stage.dataset.slices=String(links.length*5);

    if(!active)hideInfo();
    else if(infoIndex>=0){
      const hovered=rows[infoIndex].getBoundingClientRect();
      if(hovered.bottom<0||hovered.top>innerHeight)hideInfo();
    }
  }

  // Animation frame loop
  function loop(timeMs){
    animId=requestAnimationFrame(loop);
    render(timeMs);
  }

  function resetOpening(){
    opening=false;dim?.remove();spotlight?.remove();dim=spotlight=null;document.body.classList.remove('wave-project-opening');
  }

  links.forEach((link,index)=>{
    link.addEventListener('pointerenter',()=>{showInfo(index);state[index].targetHover=1;link.classList.add('is-active');});
    link.addEventListener('pointerleave',()=>{hideInfo();state[index].targetHover=0;link.classList.remove('is-active');});
    link.addEventListener('focus',()=>{showInfo(index);state[index].targetHover=1;link.classList.add('is-active');});
    link.addEventListener('blur',()=>{hideInfo();state[index].targetHover=0;link.classList.remove('is-active');});

    link.addEventListener('click',event=>{
      if(event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey||reduced)return;
      event.preventDefault();if(opening)return;opening=true;hideInfo();stage.dataset.opening=projects[index].id;
      const rect=link.getBoundingClientRect();dim=document.createElement('div');dim.className='wave-transition-dim';dim.setAttribute('aria-hidden','true');document.body.appendChild(dim);
      spotlight=link.cloneNode(true);spotlight.removeAttribute('href');spotlight.removeAttribute('id');spotlight.setAttribute('aria-hidden','true');spotlight.setAttribute('tabindex','-1');spotlight.classList.add('wave-project-spotlight');spotlight.style.left=rect.left+'px';spotlight.style.top=rect.top+'px';spotlight.style.width=rect.width+'px';spotlight.style.height=rect.height+'px';spotlight.style.marginLeft='0';
      const computed=getComputedStyle(link);for(const variable of ['--art-width','--art-height','--column-width','--column-step'])spotlight.style.setProperty(variable,computed.getPropertyValue(variable));document.body.appendChild(spotlight);
      document.body.classList.add('wave-project-opening');requestAnimationFrame(()=>dim.classList.add('is-visible'));
      setTimeout(()=>location.assign(link.href),620);
    });
  });

  addEventListener('resize',()=>{clearTimeout(resizeTimer);resizeTimer=setTimeout(measure,100);},{passive:true});
  addEventListener('pagehide',resetOpening);
  addEventListener('pageshow',event=>{if(event.persisted){resetOpening();}});

  document.fonts.ready.then(()=>{
    measure();
    stage.dataset.ready='true';
    stage.dataset.orientation='vertical';
    // Start continuous sound wave animation
    if(!animId)animId=requestAnimationFrame(loop);
  });
})();
