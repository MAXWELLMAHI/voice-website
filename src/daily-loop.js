(()=>{
  'use strict';
  const section=document.getElementById('daily-loop');
  if(!section)return;
  const stage=document.getElementById('clockwork-runner');
  const stops=JSON.parse(document.getElementById('daily-loop-data').textContent);
  const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $=id=>document.getElementById(id);
  const dom={time:$('loop-time'),location:$('loop-location'),nextDay:$('loop-next-day'),message:$('loop-message'),note:$('loop-caption-note'),announcer:$('loop-announcer'),index:$('loop-stop-index'),dial:$('loop-dial'),hour:$('loop-hour-hand'),minute:$('loop-minute-hand'),orbit:$('loop-runner-orbit'),upright:$('loop-runner-upright'),facing:$('loop-runner-facing'),body:$('loop-runner-body'),frontLeg:$('loop-front-leg'),backLeg:$('loop-back-leg'),frontArm:$('loop-front-arm'),backArm:$('loop-back-arm'),route:$('loop-orbit-progress'),wash:section.querySelector('.loop-night-wash'),glow:section.querySelector('.loop-dawn-glow')};
  const buttons=[...section.querySelectorAll('[data-loop-stop]')],markers=[...section.querySelectorAll('[data-route-stop]')],props=[...section.querySelectorAll('[data-scene-stop]')],numbers=[...section.querySelectorAll('[data-dial-number]')];
  const motion={progress:0};
  let gsap,scrollTrigger,timeline,activeIndex=-1,lastMinute=-1,lastProgress=0,lastMotion=0,energy=0,frame=0,active=false,initialized=false,resizeTimer;
  const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
  const formatTime=value=>{const minute=Math.floor(value)%1440,hour=Math.floor(minute/60);return `${hour%12||12}:${String(minute%60).padStart(2,'0')} ${hour<12?'AM':'PM'}`;};
  function setActivity(index,atEnd=false){
    const changed=index!==activeIndex;
    if(!changed&&stage.dataset.complete===String(atEnd))return;
    activeIndex=index;
    const stop=stops[index];
    dom.message.textContent=atEnd?'Tomorrow, we do it all again.':stop.message;
    dom.note.textContent=atEnd?'One day ends where the next begins.':stop.caption;
    dom.location.textContent=atEnd?'Home':stop.location;
    dom.index.textContent=String(index+1).padStart(2,'0');
    if(!reduced&&gsap)gsap.fromTo([dom.message,dom.note],{y:9,opacity:0},{y:0,opacity:1,duration:.36,stagger:.045,ease:'power2.out',overwrite:true});
    buttons.forEach((button,i)=>button.setAttribute('aria-current',String(i===index)));
    markers.forEach((marker,i)=>marker.classList.toggle('is-active',i===index));
    props.forEach((prop,i)=>{prop.classList.toggle('is-active',i===index);prop.classList.toggle('is-near',Math.abs(i-index)===1);});
    dom.announcer.textContent=`${formatTime(stop.start)}. ${stop.label}. ${stop.caption}`;
    stage.dataset.activity=stop.id;stage.dataset.stop=String(index+1);stage.dataset.complete=String(atEnd);
  }
  function render(value){
    const p=clamp(value),position=p*stops.length,index=Math.min(stops.length-1,Math.floor(position)),local=p===1?1:position-index,stop=stops[index];
    const minute=stop.start+(stop.end-stop.start)*local,degree=360*p;
    const atEnd=p>=.9998;
    setActivity(index,atEnd);
    if(Math.floor(minute)!==lastMinute){
      lastMinute=Math.floor(minute);dom.time.textContent=formatTime(minute);dom.time.dateTime=`${String(Math.floor(minute/60)%24).padStart(2,'0')}:${String(Math.floor(minute)%60).padStart(2,'0')}`;
      dom.nextDay.hidden=minute<1440;stage.dataset.time=formatTime(minute);
    }
    dom.dial.setAttribute('transform',`rotate(${degree})`);
    // The clock face makes one turn. Hands keep the real relationship to its
    // moving numerals, including the midnight boundary and the eight-hour sleep.
    dom.hour.setAttribute('transform',`rotate(${minute*.5+degree})`);
    dom.minute.setAttribute('transform',`rotate(${minute*6+degree})`);
    numbers.forEach(number=>{const x=number.getAttribute('x'),y=number.getAttribute('y');number.setAttribute('transform',`rotate(${-degree} ${x} ${y})`);});
    dom.orbit.setAttribute('transform',`rotate(${degree})`);
    dom.upright.setAttribute('transform',`rotate(${-degree})`);
    dom.facing.setAttribute('transform',`scale(${Math.cos(degree*Math.PI/180)<0?-1:1},1)`);
    dom.route.style.strokeDashoffset=String(1-p);
    const night=clamp((minute-1080)/360)*(1-clamp((minute-1860)/120));
    dom.wash.style.opacity=String(night*.8);dom.glow.style.opacity=String(clamp((minute-1860)/120)*.85);
    stage.dataset.progress=p.toFixed(5);stage.dataset.rotation=degree.toFixed(2);stage.dataset.hourRotation=(minute*.5+degree).toFixed(2);stage.dataset.minuteRotation=(minute*6+degree).toFixed(2);
    if(Math.abs(p-lastProgress)>.000002){lastMotion=performance.now();energy=clamp(energy+Math.abs(p-lastProgress)*200);}
    lastProgress=p;
    if(!reduced&&!frame)frame=requestAnimationFrame(animateRunner);
  }
  function animateRunner(now){
    frame=0;
    const running=now-lastMotion<110,resting=stops[activeIndex]?.id==='sleep'&&!running;
    energy+=(running?1-energy:-energy)*.18;
    const stride=lastProgress*Math.PI*2*stops.length*3,wave=Math.sin(stride),opposite=Math.sin(stride+Math.PI),amount=reduced?0:energy;
    dom.frontLeg.setAttribute('transform',`translate(4,-26) rotate(${wave*36*amount})`);
    dom.backLeg.setAttribute('transform',`translate(-3,-27) rotate(${opposite*36*amount})`);
    dom.frontArm.setAttribute('transform',`translate(6,-48) rotate(${opposite*31*amount})`);
    dom.backArm.setAttribute('transform',`translate(-2,-48) rotate(${wave*31*amount})`);
    const bob=-Math.abs(Math.sin(stride*2))*2.5*amount;
    dom.body.setAttribute('transform',resting?'translate(-22,-3) rotate(78 0 -24)':`translate(0,${bob}) rotate(${amount*5} 0 -28)`);
    stage.dataset.running=String(running&&amount>.05);
    if(energy>.002&&active&&!document.hidden)frame=requestAnimationFrame(animateRunner);
  }
  function updateActive(){
    const rect=section.getBoundingClientRect();
    active=rect.top<=innerHeight*.25&&rect.bottom>=innerHeight*.75;
    document.body.classList.toggle('daily-loop-active',active);stage.dataset.active=String(active);
    stage.dataset.nativeProgress=nativeProgress().toFixed(5);stage.dataset.scrollY=String(Math.round(scrollY));stage.dataset.scrollTarget=String(Math.round(window.__voiceLenis?.targetScroll??scrollY));
    if(active&&!reduced&&!frame)frame=requestAnimationFrame(animateRunner);
  }
  function nativeProgress(){
    const rect=section.getBoundingClientRect();return clamp(-rect.top/Math.max(1,rect.height-innerHeight));
  }
  function jump(progress){
    const top=section.getBoundingClientRect().top+scrollY+clamp(progress)*(section.offsetHeight-innerHeight);
    stage.dataset.jumpProgress=String(progress);stage.dataset.jumpTop=String(Math.round(top));
    // A selected moment is an exact seek. ScrollTrigger supplies the visual
    // easing, so native smooth scrolling cannot fight the site's own scroller.
    if(window.__voiceLenis)window.__voiceLenis.scrollTo(top,{immediate:true});
    else window.scrollTo({top,behavior:'instant'});
  }
  buttons.forEach((button,index)=>button.addEventListener('click',()=>jump(index/stops.length+.00005)));
  section.querySelector('.loop-skip').addEventListener('click',event=>{
    const next=document.getElementById('mumbai-alley');if(!next)return;
    event.preventDefault();const top=next.getBoundingClientRect().top+scrollY;
    if(window.__voiceLenis&&!reduced)window.__voiceLenis.scrollTo(top,{duration:1});else window.scrollTo({top,behavior:reduced?'instant':'smooth'});
  });
  function setupAnimation(){
    if(initialized)return;
    initialized=true;
    const animation=window.__voiceAnimation;
    if(!reduced&&animation){
      gsap=animation.gsap;scrollTrigger=animation.ScrollTrigger;
      timeline=gsap.timeline({scrollTrigger:{trigger:section,start:'top top',end:'bottom bottom',scrub:.35,invalidateOnRefresh:true,onToggle:updateActive,onRefresh:updateActive}});
      timeline.to(motion,{progress:1,duration:1,ease:'none',onUpdate:()=>render(motion.progress)});
      stage.dataset.engine='gsap-scrolltrigger';scrollTrigger.refresh();
    }else{
      stage.dataset.engine=reduced?'reduced-motion':'native-scroll';
      const update=()=>{if(!reduced)render(nativeProgress());updateActive();};
      addEventListener('scroll',update,{passive:true});addEventListener('resize',update,{passive:true});update();
    }
    render(reduced?0:nativeProgress());updateActive();stage.dataset.ready='true';
  }
  const start=performance.now();
  function awaitAnimation(){
    if(window.__voiceAnimation||reduced||performance.now()-start>4500){document.fonts.ready.then(setupAnimation);return;}
    requestAnimationFrame(awaitAnimation);
  }
  addEventListener('scroll',updateActive,{passive:true});
  addEventListener('resize',()=>{clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>{scrollTrigger?.refresh();updateActive();},180);},{passive:true});
  addEventListener('pagehide',()=>{timeline?.scrollTrigger?.kill();timeline?.kill();if(frame)cancelAnimationFrame(frame);});
  addEventListener('pageshow',event=>{if(event.persisted)location.reload();});
  render(0);awaitAnimation();
})();
