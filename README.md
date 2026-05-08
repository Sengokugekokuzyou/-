<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
<title>戦国武将育成伝</title>
<style>:root{--ink:#1a1208;--paper:#f5efe0;--paper-d:#e8dcc8;--gold:#c8941a;--gold-l:#e8b830;--red:#8b1a1a;--red-l:#c0392b;--border:rgba(26,18,8,.2);--aw:#7b2ff7;--aw-l:#b06bff;--army-bg:#0d1117;--morale-hi:#4fc3f7;--morale-lo:#ef5350}*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}body{font-family:'Shippori Mincho B1','Noto Serif JP',serif;background:var(--ink);color:var(--ink);min-height:100dvh;display:flex;justify-content:center;align-items:flex-start;overflow-x:hidden}#app{width:100%;max-width:480px;min-height:100dvh;background:var(--paper);position:relative;overflow:hidden}#app::before{content:'';position:fixed;inset:0;max-width:480px;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)' opacity='.04'/%3E%3C/svg%3E");pointer-events:none;z-index:1000;opacity:.5}@keyframes fadeIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}@keyframes slideIn{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:translateX(0)}}@keyframes glowPulse{0%,100%{box-shadow:0 0 12px rgba(200,148,26,.3)}50%{box-shadow:0 0 28px rgba(200,148,26,.7)}}@keyframes awakenP{0%,100%{box-shadow:0 4px 20px rgba(123,47,247,.4)}50%{box-shadow:0 4px 36px rgba(123,47,247,.8)}}@keyframes cardPop{from{transform:scale(.8);opacity:0}to{transform:scale(1);opacity:1}}@keyframes icSpin{0%{transform:rotate(-20deg) scale(.5);opacity:0}60%{transform:rotate(10deg) scale(1.2);opacity:1}100%{transform:rotate(0) scale(1)}}@keyframes bossGlow{0%,100%{box-shadow:0 0 0 rgba(200,148,26,0)}50%{box-shadow:0 0 16px rgba(200,148,26,.3)}}@keyframes routFlash{0%,100%{opacity:1}50%{opacity:.3}}@keyframes soldierDie{from{opacity:1;transform:scale(1) translateY(0)}to{opacity:0;transform:scale(0) translateY(8px)}}@keyframes moraleShake{0%,100%{transform:translateX(0)}20%,60%{transform:translateX(-3px)}40%,80%{transform:translateX(3px)}}@keyframes routBanner{0%{transform:scale(0) rotate(-10deg);opacity:0}60%{transform:scale(1.1) rotate(2deg);opacity:1}100%{transform:scale(1) rotate(0deg);opacity:1}}@keyframes personalityBadge{from{transform:scale(0) rotate(-15deg);opacity:0}to{transform:scale(1) rotate(0deg);opacity:1}}@keyframes retreatLeft{0%{transform:translateX(0);opacity:1}100%{transform:translateX(-30px);opacity:0}}@keyframes retreatRight{0%{transform:translateX(0);opacity:1}100%{transform:translateX(30px);opacity:0}}@keyframes chargeRight{0%{transform:translateX(-8px);opacity:0}100%{transform:translateX(0);opacity:1}}@keyframes chargeLeft{0%{transform:translateX(8px);opacity:0}100%{transform:translateX(0);opacity:1}}@keyframes clash{0%,100%{transform:translateX(0)}30%{transform:translateX(2px)}60%{transform:translateX(-2px)}}@keyframes shake{0%,100%{transform:translateX(0) rotate(0)}25%{transform:translateX(-3px) rotate(-3deg)}75%{transform:translateX(3px) rotate(3deg)}}@keyframes screenFlash{0%{opacity:0}20%{opacity:.35}100%{opacity:0}}@keyframes logSlide{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}@keyframes timeFlip{0%{transform:rotateX(90deg);opacity:0}100%{transform:rotateX(0);opacity:1}}@keyframes reversal{0%{transform:scale(1)}30%{transform:scale(1.08)}60%{transform:scale(.96)}100%{transform:scale(1)}}@keyframes awakenFlare{0%{box-shadow:0 0 0 rgba(123,47,247,0)}50%{box-shadow:0 0 40px rgba(123,47,247,.8)}100%{box-shadow:0 0 0 rgba(123,47,247,0)}}.screen{display:none;flex-direction:column;min-height:100dvh;animation:fadeIn .4s ease}.screen.active{display:flex}.pb{padding-bottom:calc(20px + env(safe-area-inset-bottom,0px))}.hdr{padding:20px 20px 12px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:12px;background:linear-gradient(180deg,var(--paper-d),var(--paper))}.hbk{width:36px;height:36px;border:1px solid var(--border);background:none;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:18px;color:var(--ink);border-radius:4px}.hbk:active{background:var(--paper-d)}.htitle{font-size:18px;font-weight:700;letter-spacing:.1em;flex:1}.btn-p{background:var(--ink);color:var(--gold);border:1px solid var(--gold);padding:14px 32px;font-family:inherit;font-size:15px;font-weight:700;letter-spacing:.2em;cursor:pointer;border-radius:2px;width:100%;position:relative;overflow:hidden}.btn-p::after{content:'';position:absolute;inset:0;background:linear-gradient(135deg,transparent 40%,rgba(200,148,26,.15) 100%)}.btn-p:active{transform:scale(.98)}.btn-s{background:transparent;color:var(--ink);border:1px solid var(--border);padding:12px 24px;font-family:inherit;font-size:14px;letter-spacing:.15em;cursor:pointer;border-radius:2px;width:100%}.btn-s:active{background:var(--paper-d)}.btn-g{background:linear-gradient(135deg,var(--gold),var(--gold-l));color:var(--ink);border:none;padding:14px 32px;font-family:inherit;font-size:15px;font-weight:700;letter-spacing:.2em;cursor:pointer;border-radius:2px;width:100%;box-shadow:0 4px 16px rgba(200,148,26,.3)}.btn-g:active{transform:scale(.98);box-shadow:none}.btn-aw{background:linear-gradient(135deg,var(--aw),var(--aw-l));color:#fff;border:none;padding:14px 32px;font-family:inherit;font-size:15px;font-weight:700;letter-spacing:.2em;cursor:pointer;border-radius:2px;width:100%;animation:awakenP 2s ease-in-out infinite}.btn-aw:active{transform:scale(.98)}#screen-title{background:var(--ink);color:var(--paper);justify-content:center;align-items:center;gap:32px;position:relative}.t-bg{position:absolute;inset:0;display:flex;justify-content:center;align-items:center;opacity:.04;font-size:320px;line-height:1;user-select:none}.t-kamon{width:80px;height:80px;border:2px solid var(--gold);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:36px;color:var(--gold);animation:glowPulse 3s ease-in-out infinite}.t-main{font-size:38px;font-weight:900;letter-spacing:.12em;text-align:center;color:var(--paper);text-shadow:0 2px 20px rgba(200,148,26,.4);writing-mode:vertical-rl;line-height:1.1}.t-sub{font-size:13px;letter-spacing:.3em;color:var(--gold);text-align:center}.t-div{width:60px;height:1px;background:linear-gradient(90deg,transparent,var(--gold),transparent)}.gsec{padding:16px 20px;border-bottom:1px solid var(--border)}.glbl{font-size:11px;letter-spacing:.3em;color:var(--gold);margin-bottom:10px}.bgrid{display:grid;grid-template-columns:1fr 1fr;gap:10px}.bcard{border:1px solid var(--border);border-radius:6px;padding:12px 12px 10px;cursor:pointer;background:var(--paper);position:relative;overflow:hidden;transition:transform .15s,box-shadow .15s}.bcard:active{transform:scale(.97)}.bcard.sel{border-color:var(--gold);box-shadow:inset 0 0 0 1px var(--gold),0 0 12px rgba(200,148,26,.2)}.bnm{font-size:16px;font-weight:700;letter-spacing:.1em;margin-bottom:3px;margin-top:2px}.bdsc{font-size:10px;color:rgba(26,18,8,.52);letter-spacing:.03em;line-height:1.55}.bst{display:flex;gap:5px;margin-top:7px;flex-wrap:wrap}.spip{font-size:10px;font-weight:700;padding:2px 6px;border-radius:3px;letter-spacing:.05em;border:1px solid var(--border);display:inline-flex;align-items:center;gap:3px}.spip-ss{background:rgba(255,107,53,.15);color:#e65100;border-color:rgba(255,107,53,.45)}.spip-s{background:rgba(200,148,26,.14);color:var(--gold);border-color:rgba(200,148,26,.4)}.spip-a{background:rgba(79,195,247,.12);color:#0277bd;border-color:rgba(79,195,247,.4)}.spip-b{background:rgba(76,175,80,.12);color:#2e7d32;border-color:rgba(76,175,80,.4)}.spip-c{background:rgba(26,18,8,.06);color:rgba(26,18,8,.55);border-color:var(--border)}.spip-d{background:rgba(141,110,99,.1);color:#6d4c41;border-color:rgba(141,110,99,.3)}.btrait{font-size:9px;letter-spacing:.05em;padding:2px 7px;border-radius:10px;border:1px solid currentColor;margin-top:6px;display:inline-block;font-weight:700}.affinity-row{margin:0 20px 12px;padding:10px 14px;border:1px solid var(--border);border-radius:4px;background:var(--paper);display:flex;align-items:center;gap:10px;font-size:11px;letter-spacing:.08em;animation:fadeIn .3s ease}.affinity-ic{font-size:18px;flex-shrink:0}.affinity-label{opacity:.5;font-size:10px;letter-spacing:.2em;margin-bottom:2px}.affinity-text{font-size:12px;font-weight:700}.aff-great{color:#e65100}.aff-good{color:var(--gold)}.aff-normal{color:rgba(26,18,8,.5)}.aff-bad{color:#78909c}.rc{margin:20px;border:1px solid var(--border);border-radius:4px;overflow:hidden}.rch{background:var(--ink);color:var(--paper);padding:16px 20px;text-align:center}.wnm{font-size:28px;font-weight:900;letter-spacing:.15em;color:var(--gold-l)}.wep{font-size:11px;letter-spacing:.25em;opacity:.6;margin-top:4px}.sgrid{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--border)}.scell{background:var(--paper);padding:14px 16px}.snm{font-size:10px;letter-spacing:.2em;color:rgba(26,18,8,.5);margin-bottom:4px}.sv{font-size:22px;font-weight:700}.sbar{height:3px;background:var(--paper-d);border-radius:2px;margin-top:6px;overflow:hidden}.sbf{height:100%;background:linear-gradient(90deg,var(--gold),var(--gold-l));border-radius:2px;transition:width 1s cubic-bezier(.22,1,.36,1);width:0}.skd{margin:0 20px 8px;padding:12px 16px;border:1px solid rgba(200,148,26,.4);border-radius:4px;background:linear-gradient(135deg,#fdf6e3,var(--paper));display:flex;align-items:center;gap:12px}.skd.mut{border-color:rgba(123,47,247,.5);background:linear-gradient(135deg,#f0eaff,var(--paper))}.skic{font-size:22px}.sknm{font-size:14px;font-weight:700;letter-spacing:.1em}.skef{font-size:11px;color:rgba(26,18,8,.55);letter-spacing:.05em;margin-top:2px}#screen-home{background:var(--paper)}.hpanel{background:var(--ink);color:var(--paper);padding:28px 20px;text-align:center;position:relative;overflow:hidden}.hpanel::before{content:'◎';position:absolute;font-size:200px;opacity:.03;top:50%;left:50%;transform:translate(-50%,-50%)}.hpanel.mut{background:linear-gradient(135deg,#0e0a1f 0%,#1a1208 60%,#0d0d1a 100%)}.hpanel.mut::after{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 50% 0%,rgba(123,47,247,.15) 0%,transparent 70%);pointer-events:none}.hwnm{font-size:30px;font-weight:900;letter-spacing:.15em;color:var(--gold-l);margin-bottom:4px}.hwep{font-size:11px;letter-spacing:.25em;opacity:.45;margin-bottom:8px}.skb{display:inline-block;border:1px solid rgba(200,148,26,.5);color:var(--gold);font-size:10px;letter-spacing:.2em;padding:3px 10px;border-radius:2px;margin-bottom:12px}.skb.p-ino{border-color:rgba(200,50,50,.5);color:#ff8a80}.skb.p-chi{border-color:rgba(50,100,200,.5);color:#82b1ff}.skb.p-mou{border-color:rgba(150,50,200,.5);color:#ce93d8}.skb.p-oku{border-color:rgba(100,150,100,.5);color:#a5d6a7}.skb.p-tou{border-color:rgba(200,148,26,.5);color:var(--gold-l)}.skb.mut{border-color:rgba(123,47,247,.6);color:var(--aw-l);background:rgba(123,47,247,.1)}.gr2{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px}.gl2{font-size:10px;letter-spacing:.3em;color:var(--gold)}.gv2{font-size:12px;color:var(--gold-l)}.gt2{height:3px;background:rgba(255,255,255,.1);border-radius:2px;margin-bottom:10px;overflow:hidden}.gf2{height:100%;background:linear-gradient(90deg,var(--gold),var(--gold-l));border-radius:2px;transition:width .8s cubic-bezier(.22,1,.36,1)}.ll{font-size:10px;letter-spacing:.3em;color:rgba(245,239,224,.45)}.lv{font-size:12px;color:rgba(245,239,224,.6)}.lt{height:3px;background:rgba(255,255,255,.08);border-radius:2px;margin-bottom:16px;overflow:hidden}.lf{height:100%;background:linear-gradient(90deg,#4a9e4a,#a8e048);border-radius:2px;transition:width .8s cubic-bezier(.22,1,.36,1)}.lf.danger{background:linear-gradient(90deg,#8b1a1a,#e85a2a)}.hage{display:flex;justify-content:center;gap:24px}.hai{text-align:center}.hail{font-size:9px;letter-spacing:.3em;opacity:.4;margin-bottom:4px}.haiv{font-size:20px;font-weight:700}.hmenu{padding:20px;display:flex;flex-direction:column;gap:10px}.mi{display:flex;align-items:center;gap:14px;padding:16px;border:1px solid var(--border);border-radius:4px;background:var(--paper);cursor:pointer;text-align:left}.mi:active{background:var(--paper-d)}.mi.boss{border-color:var(--gold);background:linear-gradient(135deg,#fdf6e3,var(--paper));animation:bossGlow 2s ease-in-out infinite}.miic{width:40px;height:40px;background:var(--ink);border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0}.mit{font-size:15px;font-weight:700;letter-spacing:.08em;margin-bottom:2px}.mid{font-size:11px;color:rgba(26,18,8,.45);letter-spacing:.05em}.mia{margin-left:auto;font-size:16px;opacity:.3}.tchoices{padding:16px 20px;display:flex;flex-direction:column;gap:10px}.tc{border:1px solid var(--border);border-radius:4px;padding:16px;cursor:pointer;background:var(--paper)}.tc:active{transform:scale(.99);background:var(--paper-d)}.tct{font-size:15px;font-weight:700;letter-spacing:.08em;margin-bottom:6px}.tcd{font-size:12px;color:rgba(26,18,8,.55);letter-spacing:.05em;line-height:1.6}.tefx{display:flex;gap:6px;margin-top:8px;flex-wrap:wrap}.etag{font-size:10px;padding:2px 8px;border-radius:2px;letter-spacing:.05em;font-weight:700}.eup{background:rgba(76,175,80,.15);border:1px solid rgba(76,175,80,.4);color:#2e7d32}.edn{background:rgba(244,67,54,.1);border:1px solid rgba(244,67,54,.3);color:#c62828}.erd{background:rgba(200,148,26,.12);border:1px solid rgba(200,148,26,.35);color:var(--gold)}.tarea{padding:20px;text-align:center}.tyr{font-size:32px;font-weight:900;letter-spacing:.1em;color:var(--gold)}.tyrl{font-size:10px;letter-spacing:.3em;color:rgba(26,18,8,.45);margin-bottom:20px}.tlog{max-height:260px;overflow-y:auto;border:1px solid var(--border);border-radius:4px;padding:12px;text-align:left;background:#faf6ee}.titem{font-size:13px;padding:6px 0;border-bottom:1px solid var(--border);letter-spacing:.05em;opacity:0;animation:slideIn .4s forwards}.titem:last-child{border-bottom:none}.tstats{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:16px}.tsi{border:1px solid var(--border);border-radius:4px;padding:10px 8px;text-align:center;background:var(--paper)}.tsin{font-size:9px;letter-spacing:.15em;color:rgba(26,18,8,.45);margin-bottom:4px}.tsiv{font-size:18px;font-weight:700}.tsid{font-size:10px;color:var(--gold);font-weight:700}.tsid.neg{color:var(--red-l)}#screen-battle{background:var(--army-bg);color:var(--paper);flex-direction:column;min-height:100dvh;position:relative;overflow:hidden}.time-bar{display:flex;align-items:center;justify-content:space-between;padding:10px 16px 6px;background:rgba(0,0,0,.5);border-bottom:1px solid rgba(245,239,224,.06)}.time-display{font-size:15px;font-weight:700;letter-spacing:.2em;color:var(--gold-l);animation:timeFlip .4s ease}.time-month{font-size:11px;color:rgba(245,239,224,.5);letter-spacing:.15em}.battle-title-row{font-size:12px;letter-spacing:.2em;color:rgba(245,239,224,.6)}.battlefield{position:relative;background:linear-gradient(180deg,#0a0d12 0%,#0d1520 40%,#111820 100%);border-bottom:1px solid rgba(245,239,224,.06);overflow:hidden;flex-shrink:0}.bf-bg{position:absolute;inset:0;background:radial-gradient(ellipse 80% 40% at 50% 50%,rgba(200,148,26,.04) 0%,transparent 70%),repeating-linear-gradient(0deg,transparent,transparent 30px,rgba(255,255,255,.01) 30px,rgba(255,255,255,.01) 31px);pointer-events:none}.bf-flash{position:absolute;inset:0;pointer-events:none;z-index:10;opacity:0}.army-zone{padding:8px 12px 4px;position:relative}.army-zone.enemy{border-bottom:1px solid rgba(200,50,50,.12)}.army-zone.ally{border-top:1px solid rgba(79,195,247,.1)}.general-row{display:flex;align-items:center;gap:8px;margin-bottom:5px}.general-name{font-size:11px;font-weight:700;letter-spacing:.15em}.general-name.enemy{color:#ff8a80}.general-name.ally{color:var(--morale-hi)}.personality-inline{font-size:9px;letter-spacing:.1em;opacity:.7;padding:1px 6px;border-radius:10px;border:1px solid currentColor}.soldier-grid{display:flex;flex-wrap:wrap;gap:1px;min-height:36px;align-content:flex-start;position:relative}.sol{font-size:11px;line-height:1;display:inline-block;transition:opacity .2s;will-change:transform,opacity}.sol.dying{animation:soldierDie .35s ease forwards}.sol.retreating-l{animation:retreatLeft .5s ease forwards}.sol.retreating-r{animation:retreatRight .5s ease forwards}.sol.charging-r{animation:chargeRight .3s ease}.sol.charging-l{animation:chargeLeft .3s ease}.sol.clashing{animation:clash .4s ease}.sol.shaking{animation:shake .3s ease}.army-info-row{display:flex;justify-content:space-between;align-items:center;margin-top:3px}.army-hp-label{font-size:9px;letter-spacing:.25em;opacity:.45}.army-hp-val{font-size:13px;font-weight:700;letter-spacing:.05em;transition:color .3s}.army-hp-val.critical{color:var(--morale-lo) !important;animation:shake .3s ease}.clash-line{height:2px;margin:0 16px;background:linear-gradient(90deg,transparent,rgba(200,148,26,.15),rgba(200,50,50,.15),transparent);position:relative;flex-shrink:0}.clash-line::before{content:'⚔';position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);font-size:12px;opacity:.5}.morale-bars{padding:6px 12px 4px;display:grid;grid-template-columns:1fr 1fr;gap:10px;background:rgba(0,0,0,.2)}.morale-label-row{display:flex;justify-content:space-between;align-items:center;margin-bottom:3px}.morale-lbl{font-size:9px;letter-spacing:.3em;opacity:.5}.morale-num{font-size:11px;font-weight:700;letter-spacing:.05em}.morale-track{height:4px;background:rgba(255,255,255,.08);border-radius:2px;overflow:hidden}.morale-fill{height:100%;border-radius:2px;transition:width .5s cubic-bezier(.22,1,.36,1),background .5s}.morale-status-row{grid-column:1/-1;font-size:9px;letter-spacing:.2em;text-align:center;min-height:14px;margin-top:2px}.battle-log-area{flex:1;overflow-y:auto;padding:8px 14px;display:flex;flex-direction:column;gap:0;min-height:0;scroll-behavior:smooth}.blog-entry{display:flex;align-items:flex-start;gap:8px;padding:6px 0;border-bottom:1px solid rgba(245,239,224,.04);opacity:0;animation:logSlide .35s ease forwards}.blog-entry.flash-red{background:rgba(200,50,50,.08);border-radius:4px}.blog-entry.flash-gold{background:rgba(200,148,26,.08);border-radius:4px}.blog-ic{width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;flex-shrink:0;margin-top:1px}.blog-ic.ally-ic{background:rgba(79,195,247,.1);border:1px solid rgba(79,195,247,.25)}.blog-ic.enemy-ic{background:rgba(200,50,50,.12);border:1px solid rgba(200,50,50,.3)}.blog-ic.neutral{background:rgba(200,148,26,.1);border:1px solid rgba(200,148,26,.25)}.blog-ic.rout-ic{background:rgba(239,83,80,.15);border:1px solid rgba(239,83,80,.4)}.blog-ic.drama-ic{background:rgba(255,215,0,.15);border:1px solid rgba(255,215,0,.4)}.blog-text{font-size:12px;line-height:1.6;letter-spacing:.04em;flex:1}.blog-text.bold{font-weight:700}.blog-text.rout-text{color:#ff8a80;font-weight:700}.blog-text.gold-text{color:var(--gold-l);font-weight:700}.blog-sub{font-size:10px;opacity:.4;letter-spacing:.05em;margin-top:1px}.rout-overlay{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;z-index:200;pointer-events:none;background:rgba(0,0,0,.3);animation:fadeIn .3s ease}.rout-banner-big{text-align:center;animation:routBanner .6s cubic-bezier(.22,1,.36,1) forwards}.rout-kanji{font-size:48px;font-weight:900;letter-spacing:.3em;display:block;margin-bottom:4px}.rout-kanji.win-text{color:var(--gold-l);text-shadow:0 0 40px rgba(232,184,48,.7)}.rout-kanji.lose-text{color:#ff8a80;text-shadow:0 0 40px rgba(200,50,50,.7)}.rout-sub-text{font-size:12px;letter-spacing:.3em;opacity:.7}.reversal-overlay{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;z-index:250;pointer-events:none}.reversal-text{font-size:28px;font-weight:900;letter-spacing:.25em;color:var(--gold-l);text-shadow:0 0 30px rgba(232,184,48,.8);animation:routBanner .5s cubic-bezier(.22,1,.36,1) forwards,reversal 1.2s .5s ease}.battle-footer{position:sticky;bottom:0;z-index:50;background:rgba(13,17,23,.97);border-top:1px solid rgba(245,239,224,.06)}.battle-bottom{padding:10px 14px 0}.gauge-row{display:flex;justify-content:space-between;align-items:center;margin-bottom:4px}.gauge-lbl{font-size:9px;letter-spacing:.35em;color:rgba(245,239,224,.4)}.gauge-val{font-size:12px;font-weight:700;color:var(--gold-l)}.gauge-track{height:3px;background:rgba(245,239,224,.08);border-radius:2px;overflow:hidden;margin-bottom:8px}.gauge-fill{height:100%;background:linear-gradient(90deg,var(--gold),var(--gold-l));border-radius:2px;width:0;transition:width 1.2s cubic-bezier(.22,1,.36,1)}.battle-ctrl{display:flex;gap:10px;padding:8px 14px 16px}.bskip{background:transparent;color:rgba(245,239,224,.4);border:1px solid rgba(245,239,224,.12);padding:10px 16px;font-family:inherit;font-size:12px;letter-spacing:.2em;cursor:pointer;border-radius:2px;flex:1}.bnxt{background:linear-gradient(135deg,var(--gold),var(--gold-l));color:var(--ink);border:none;padding:10px 16px;font-family:inherit;font-size:13px;font-weight:700;letter-spacing:.15em;cursor:pointer;border-radius:2px;flex:2;opacity:0;transition:opacity .4s,transform .2s;pointer-events:none}.bnxt.rdy{opacity:1;pointer-events:all}.bnxt:active{transform:scale(.97)}.blog-final{text-align:center;padding:16px 0 8px;opacity:0;animation:logSlide .5s .1s ease forwards}.blog-final-badge{display:inline-block;border:1px solid var(--gold);color:var(--gold);font-size:12px;letter-spacing:.3em;padding:6px 18px;margin-bottom:8px;font-weight:700}.blog-final-text{font-size:15px;font-weight:700;letter-spacing:.12em;color:var(--gold-l)}.personality-badge{display:inline-flex;align-items:center;gap:5px;padding:3px 10px;border-radius:12px;font-size:10px;letter-spacing:.15em;font-weight:700;margin-bottom:8px;animation:personalityBadge .6s cubic-bezier(.22,1,.36,1) forwards}.p-ino{background:rgba(200,50,50,.2);border:1px solid rgba(200,50,50,.5);color:#ff8a80}.p-chi{background:rgba(50,100,200,.2);border:1px solid rgba(50,100,200,.5);color:#82b1ff}.p-mou{background:rgba(150,50,200,.2);border:1px solid rgba(150,50,200,.5);color:#ce93d8}.p-oku{background:rgba(100,150,100,.2);border:1px solid rgba(100,150,100,.5);color:#a5d6a7}.p-tou{background:rgba(200,148,26,.2);border:1px solid rgba(200,148,26,.5);color:var(--gold-l)}.hlist{flex:1;overflow-y:auto;padding:12px 20px;display:flex;flex-direction:column;gap:12px}.hcard{border:1px solid var(--border);border-radius:4px;overflow:hidden}.hch{background:var(--ink);color:var(--paper);padding:10px 14px;display:flex;justify-content:space-between;align-items:center}.hcn{font-size:14px;font-weight:700;letter-spacing:.1em}.hbadge{font-size:10px;padding:2px 8px;border-radius:2px;letter-spacing:.1em;font-weight:700}.bw{background:var(--gold);color:var(--ink)}.bd{background:#4a6a8a;color:var(--paper)}.bl{background:var(--red);color:var(--paper)}.hcb{padding:10px 14px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px}.hst{text-align:center}.hsl{font-size:9px;letter-spacing:.15em;color:rgba(26,18,8,.45);margin-bottom:2px}.hsv{font-size:14px;font-weight:700}#screen-death{background:var(--ink);color:var(--paper);overflow-y:auto}.dh{padding:40px 20px 24px;text-align:center;border-bottom:1px solid rgba(245,239,224,.1)}.dic{font-size:48px;display:block;margin-bottom:16px}.dt{font-size:28px;font-weight:900;letter-spacing:.2em;margin-bottom:6px}.dwnm{font-size:22px;font-weight:700;color:var(--gold-l);letter-spacing:.15em;margin-bottom:4px}.dwep{font-size:11px;letter-spacing:.25em;opacity:.4}.dage{font-size:14px;color:var(--gold);letter-spacing:.2em;margin-top:12px}.rdsp{text-align:center;padding:28px 20px;border-bottom:1px solid rgba(245,239,224,.08)}.rl{font-size:10px;letter-spacing:.4em;color:rgba(245,239,224,.4);margin-bottom:8px}.rv{font-size:72px;font-weight:900;line-height:1}.rss{color:#ff6b35;text-shadow:0 0 32px rgba(255,107,53,.6)}.rs{color:var(--gold-l);text-shadow:0 0 24px rgba(232,184,48,.5)}.ra{color:#4fc3f7;text-shadow:0 0 20px rgba(79,195,247,.4)}.rb{color:#aed581}.rc2{color:rgba(245,239,224,.5)}.rcmt{font-size:14px;letter-spacing:.1em;opacity:.6;margin-top:10px}.dsum{padding:20px;display:flex;flex-direction:column;gap:8px}.dsi{display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid rgba(245,239,224,.08);font-size:13px;letter-spacing:.05em}.dsl{opacity:.45}.dsv{font-weight:700;color:var(--gold-l)}.dact{padding:16px 20px 32px;display:flex;flex-direction:column;gap:10px}#screen-status{overflow-y:auto}.ov{position:fixed;inset:0;background:rgba(0,0,0,.85);z-index:9000;display:flex;align-items:center;justify-content:center;padding:32px 20px;animation:fadeIn .4s ease}.ov.awbg{background:rgba(10,5,25,.92)}.ovc{border-radius:8px;padding:32px 24px;text-align:center;width:100%;max-width:360px;color:var(--paper);animation:cardPop .5s cubic-bezier(.22,1,.36,1)}.ovc.rare{background:var(--ink);border:1px solid var(--gold);box-shadow:0 0 60px rgba(200,148,26,.3)}.ovc.aw{background:linear-gradient(135deg,#0e0a1f,#1a0a30);border:1px solid var(--aw);box-shadow:0 0 60px rgba(123,47,247,.5)}.ovic{font-size:52px;display:block;margin-bottom:16px;animation:icSpin 1.5s ease-in-out}.ovic.aw{animation:none;filter:drop-shadow(0 0 12px rgba(123,47,247,.8))}.ovtag{font-size:11px;letter-spacing:.5em;color:var(--gold);margin-bottom:8px}.ovtag.aw{color:var(--aw-l)}.ovnm{font-size:24px;font-weight:900;letter-spacing:.15em;margin-bottom:12px}.ovnm.aw{color:var(--aw-l);text-shadow:0 0 20px rgba(176,107,255,.6)}.ovdsc{font-size:14px;opacity:.65;letter-spacing:.05em;line-height:1.7;margin-bottom:24px}</style>
</head>
<body>
<div id="app">

<!-- ===================== TITLE ===================== -->
<div id="screen-title" class="screen active">
  <div class="t-bg">将</div>
  <div class="t-kamon">⚔</div>
  <div style="display:flex;flex-direction:column;align-items:center;gap:16px">
    <div class="t-main">戦国武将<br>育成伝</div>
    <div class="t-div"></div>
    <div class="t-sub">SENGOKU IKUSEI DEN</div>
  </div>
  <div style="padding:0 40px;width:100%;display:flex;flex-direction:column;gap:10px">
    <button class="btn-p" onclick="goScreen('screen-gacha')">▶ 新たな血統を引く</button>
    <button class="btn-s" style="color:rgba(245,239,224,.5);border-color:rgba(245,239,224,.15)" onclick="goScreen('screen-history')">戦歴を見る</button>
  </div>
</div>

<!-- ===================== GACHA ===================== -->
<div id="screen-gacha" class="screen">
  <div class="hdr"><button class="hbk" onclick="goScreen('screen-title')">←</button><div class="htitle">血統を選ぶ</div></div>
  <div class="gsec"><div class="glbl">父の血統</div><div class="bgrid" id="fg"></div></div>
  <div class="gsec"><div class="glbl">母の血統</div><div class="bgrid" id="mg"></div></div>
  <div id="affinity-row" style="display:none" class="affinity-row">
    <span class="affinity-ic" id="aff-ic">⚔</span>
    <div>
      <div class="affinity-label">血統の相性</div>
      <div class="affinity-text" id="aff-text">—</div>
    </div>
    <div style="margin-left:auto;font-size:10px;opacity:.5;letter-spacing:.05em" id="aff-bonus">—</div>
  </div>
  <div style="padding:8px 20px 24px;display:flex;flex-direction:column;gap:10px" class="pb">
    <div id="sinfo" style="text-align:center;font-size:12px;letter-spacing:.1em;color:rgba(26,18,8,.45);min-height:20px"></div>
    <button class="btn-g" onclick="doGacha()" id="gbtn" disabled style="opacity:.4">武将を誕生させる</button>
  </div>
</div>

<!-- ===================== BORN ====================== -->
<div id="screen-born" class="screen">
  <div class="hdr"><div class="htitle" style="text-align:center">武将誕生</div></div>
  <div class="rc"><div class="rch"><div class="wnm" id="bnm">—</div><div class="wep" id="bep">—</div></div><div class="sgrid" id="bstats"></div></div>
  <div id="bskill"></div>
  <div id="bpersonality" style="padding:0 20px 8px;text-align:center"></div>
  <div style="padding:8px 20px;font-size:12px;letter-spacing:.05em;color:rgba(26,18,8,.5);text-align:center" id="bheri"></div>
  <div style="padding:8px 20px 24px;display:flex;flex-direction:column;gap:10px" class="pb">
    <button class="btn-g" onclick="goScreen('screen-home')">育成を始める →</button>
    <button class="btn-s" onclick="goScreen('screen-gacha')">もう一度引き直す</button>
  </div>
</div>

<!-- ===================== HOME ====================== -->
<div id="screen-home" class="screen">
  <div class="hpanel" id="hpanel">
    <div class="hwnm" id="hnm">—</div>
    <div class="hwep" id="hep">—</div>
    <div id="hskill"></div>
    <div class="gr2"><span class="gl2">名声</span><span class="gv2" id="hrep">0</span></div>
    <div class="gt2"><div class="gf2" id="hrepf" style="width:0"></div></div>
    <div class="gr2"><span class="ll">余命</span><span class="lv" id="hlife">—</span></div>
    <div class="lt"><div class="lf" id="hlifef" style="width:100%"></div></div>
    <div class="hage">
      <div class="hai"><div class="hail">年齢</div><div class="haiv" id="hage">15</div></div>
      <div class="hai"><div class="hail">出陣</div><div class="haiv" id="hbtl">0</div></div>
      <div class="hai"><div class="hail">功績</div><div class="haiv" id="hmer">0</div></div>
    </div>
  </div>
  <div class="hmenu" id="hmenu">
    <div class="mi" onclick="showTrChoices()"><div class="miic">⚒</div><div><div class="mit">鍛錬する</div><div class="mid">能力を磨き、次の出陣に備える</div></div><div class="mia">›</div></div>
    <div class="mi" onclick="startBattle()"><div class="miic">⚔</div><div><div class="mit">出陣する</div><div class="mid">軍勢を率い、合戦に参加する</div></div><div class="mia">›</div></div>
    <div class="mi" onclick="goScreen('screen-history')"><div class="miic">📜</div><div><div class="mit">戦歴を見る</div><div class="mid">これまでの合戦を振り返る</div></div><div class="mia">›</div></div>
    <div class="mi" onclick="viewStatus()"><div class="miic">🎴</div><div><div class="mit">武将詳細</div><div class="mid">現在のステータスを確認する</div></div><div class="mia">›</div></div>
  </div>
</div>

<!-- ================ TRAINING CHOICE ================ -->
<div id="screen-training-choice" class="screen">
  <div class="hdr"><button class="hbk" onclick="goScreen('screen-home')">←</button><div class="htitle">鍛錬を選ぶ</div></div>
  <div style="padding:16px 20px 8px;font-size:12px;letter-spacing:.08em;color:rgba(26,18,8,.5);text-align:center" id="tchdr"></div>
  <div class="tchoices" id="tcarea"></div>
</div>

<!-- =================== TRAINING ==================== -->
<div id="screen-training" class="screen">
  <div class="hdr"><button class="hbk" onclick="goScreen('screen-home')">←</button><div class="htitle">鍛錬</div></div>
  <div class="tarea">
    <div class="tyr" id="tyr">天正元年</div>
    <div class="tyrl">鍛錬の記録</div>
    <div class="tlog" id="tlog"></div>
    <div class="tstats" id="tstats"></div>
  </div>
  <div style="padding:16px 20px 24px" class="pb">
    <button class="btn-g" id="tdbtn" onclick="finishTr()" style="display:none">鍛錬を終える</button>
  </div>
</div>

<!-- ==================== BATTLE ===================== -->
<div id="screen-battle" class="screen">

  <div class="time-bar">
    <div>
      <div class="time-display" id="b-time-display">—</div>
      <div class="time-month" id="b-time-month">—</div>
    </div>
    <div class="battle-title-row" id="b-title-row">—</div>
  </div>

  <div class="battlefield" id="battlefield">
    <div class="bf-bg"></div>
    <div class="bf-flash" id="bf-flash"></div>

    <div class="army-zone enemy">
      <div class="general-row">
        <span class="general-name enemy" id="enemy-general">敵大将</span>
        <span class="personality-inline" style="color:#ff8a80;border-color:#ff8a80">⚔ 敵軍</span>
      </div>
      <div class="soldier-grid" id="enemy-grid"></div>
      <div class="army-info-row">
        <span class="army-hp-label">残兵</span>
        <span class="army-hp-val" id="enemy-hp-val" style="color:#ff8a80">—</span>
      </div>
    </div>

    <div class="clash-line"></div>

    <div class="army-zone ally">
      <div class="soldier-grid" id="ally-grid"></div>
      <div class="army-info-row">
        <span class="army-hp-label">残兵</span>
        <span class="army-hp-val" id="ally-hp-val" style="color:var(--morale-hi)">—</span>
      </div>
      <div class="general-row" style="margin-top:5px;margin-bottom:0">
        <span class="general-name ally" id="ally-general">—</span>
        <span id="ally-personality-badge"></span>
      </div>
    </div>

    <div class="rout-overlay" id="rout-overlay" style="display:none"></div>
  </div>

  <div class="morale-bars">
    <div class="morale-col">
      <div class="morale-label-row">
        <span class="morale-lbl">味方士気</span>
        <span class="morale-num" id="ally-morale-num" style="color:var(--morale-hi)">100</span>
      </div>
      <div class="morale-track"><div class="morale-fill" id="ally-morale-fill" style="width:100%;background:var(--morale-hi)"></div></div>
    </div>
    <div class="morale-col">
      <div class="morale-label-row">
        <span class="morale-lbl">敵士気</span>
        <span class="morale-num" id="enemy-morale-num" style="color:var(--morale-hi)">100</span>
      </div>
      <div class="morale-track"><div class="morale-fill" id="enemy-morale-fill" style="width:100%;background:var(--morale-hi)"></div></div>
    </div>
    <div class="morale-status-row" id="morale-status-row"></div>
  </div>

  <div class="battle-log-area" id="battle-log-area"></div>

  <!-- [FIX-J] battle-bottom + battle-ctrl を .battle-footer でラップし sticky 固定 -->
  <div class="battle-footer">
    <div class="battle-bottom">
      <div class="gauge-row"><span class="gauge-lbl">名声</span><span class="gauge-val" id="b-rep">0</span></div>
      <div class="gauge-track"><div class="gauge-fill" id="b-rep-fill"></div></div>
      <div class="gauge-row"><span class="gauge-lbl">功績</span><span class="gauge-val" id="b-mer">0</span></div>
      <div class="gauge-track"><div class="gauge-fill" id="b-mer-fill"></div></div>
    </div>
    <div class="battle-ctrl">
      <button class="bskip" onclick="skipBattle()">スキップ</button>
      <button class="bnxt" id="b-next-btn" onclick="afterBattle()">次へ →</button>
    </div>
  </div>

</div>

<!-- =================== HISTORY ==================== -->
<div id="screen-history" class="screen">
  <div class="hdr"><button class="hbk" onclick="goBack()">←</button><div class="htitle">戦歴</div></div>
  <div class="hlist" id="hlist"></div>
</div>

<!-- ==================== STATUS ==================== -->
<div id="screen-status" class="screen">
  <div class="hdr"><button class="hbk" onclick="goScreen('screen-home')">←</button><div class="htitle">武将詳細</div></div>
  <div id="scontent" style="padding:0 0 24px"></div>
</div>

<!-- ===================== DEATH ==================== -->
<div id="screen-death" class="screen">
  <div class="dh"><span class="dic">⚰</span><div class="dt">辞世</div><div class="dwnm" id="dnm">—</div><div class="dwep" id="dep">—</div><div class="dage" id="dage">—</div></div>
  <div class="rdsp"><div class="rl">総合評価</div><div class="rv" id="drank">—</div><div class="rcmt" id="drcmt">—</div></div>
  <div class="dsum" id="dsum"></div>
  <div class="dact pb">
    <button class="btn-aw" onclick="doInherit()">子の代へ — 世代継承</button>
    <button class="btn-p" onclick="goScreen('screen-gacha')">新たな血統を引く</button>
    <button class="btn-s" onclick="goScreen('screen-title')">タイトルへ戻る</button>
  </div>
</div>

</div><!-- /#app -->
<script>const f   = Math.floor;
const rnd = Math.random;
const rn  = n => f(rnd() * n);
const cl  = (v, lo, hi) => Math.min(Math.max(v, lo), hi);
const $el = id => document.getElementById(id);
const pick = a => a[rn(a.length)];
const shortName = w => w.name.split(' ')[1] || w.name;
const STAT_KEYS = [
  ['bu','武勇'],['ch','知略'],['se','政治'],['to','統率'],
];
const BLOODLINES = [
  {
  id:'oda', name:'織田', s:{bu:62,ch:75,se:98,to:65},
  desc:'革新の血。天下布武の気概と鉄砲の才を宿す。',
  trait:{ id:'kakushin', label:'革新', color:'#e65100',
  desc:'鍛錬効果+15%・勝利時名声+10%',
  apply:(w,ctx)=>{ if(ctx==='train') return {mul:1.15}; if(ctx==='rep_win') return {rm:1.1}; return {}; }},
  },
  {
  id:'take', name:'武田', s:{bu:98,ch:58,se:65,to:88},
  desc:'甲斐の虎。山岳戦に無敵の武の血脈。',
  trait:{ id:'fuurinkazan', label:'風林火山', color:'#c62828',
  desc:'戦闘時 武力+5・統率+5',
  apply:(w,ctx)=>{ if(ctx==='battle') return {buBonus:5,toBonus:5}; return {}; }},
  },
  {
  id:'toku', name:'徳川', s:{bu:62,ch:88,se:90,to:72},
  desc:'東国の雄。忍耐と磐石の地盤を持つ血。',
  trait:{ id:'nintai', label:'忍耐', color:'#1565c0',
  desc:'敗北時ペナルティ50%軽減',
  apply:(w,ctx)=>{ if(ctx==='loss_pen') return {reduce:.5}; return {}; }},
  },
  {
  id:'uesi', name:'上杉', s:{bu:76,ch:60,se:65,to:90},
  desc:'義の将。毘沙門天の加護と絶対の規律。',
  trait:{ id:'gi', label:'義の将', color:'#4a148c',
  desc:'統率+8・士気崩壊しにくい',
  apply:(w,ctx)=>{ if(ctx==='battle') return {toBonus:8,moraleFloor:15}; return {}; }},
  },
  {
  id:'shim', name:'島津', s:{bu:92,ch:45,se:50,to:78},
  desc:'鬼島津。捨て奸戦法で無敵を誇る武の極致。',
  trait:{ id:'sutegama', label:'捨て奸', color:'#b71c1c',
  desc:'劣勢時 武力+12',
  apply:(w,ctx)=>{ if(ctx==='battle_underdog') return {buBonus:12}; return {}; }},
  },
  {
  id:'date', name:'伊達', s:{bu:78,ch:74,se:64,to:76},
  desc:'独眼竜。華やかな武と先進的な知を兼ね備える。',
  trait:{ id:'dokuganryu', label:'独眼竜', color:'#f57f17',
  desc:'勝利時 名声+15%',
  apply:(w,ctx)=>{ if(ctx==='rep_win') return {rm:1.15}; return {}; }},
  },
  {
  id:'hojo', name:'北条', s:{bu:56,ch:76,se:90,to:72},
  desc:'関東の覇者。難攻不落の城と治世の才。',
  trait:{ id:'sougamae', label:'総構え', color:'#37474f',
  desc:'政治+8・統率+5',
  apply:(w,ctx)=>{ if(ctx==='battle') return {toBonus:5}; if(ctx==='train') return {seBonus:8}; return {}; }},
  },
  {
  id:'mou', name:'毛利', s:{bu:50,ch:88,se:74,to:56},
  desc:'謀将の血。水軍を率いた智謀の系譜。',
  trait:{ id:'mouri_ryaku', label:'権謀術数', color:'#2e7d32',
  desc:'知略+8・奇策成功率+15%',
  apply:(w,ctx)=>{ if(ctx==='battle') return {chBonus:8}; if(ctx==='gamble') return {bonusRate:.15}; return {}; }},
  },
  {
  id:'san', name:'真田', s:{bu:70,ch:85,se:56,to:64},
  desc:'表裏比興の策士。六文銭が示す死生観。',
  trait:{ id:'hyourihi', label:'表裏比興', color:'#e65100',
  desc:'奇策+大・スキル発動+10%',
  apply:(w,ctx)=>{ if(ctx==='gamble') return {bonusRate:.20}; if(ctx==='skill_rate') return {bonus:.10}; return {}; }},
  },
  {
  id:'cho', name:'長宗我部', s:{bu:75,ch:56,se:50,to:80},
  desc:'一領具足の精兵。土佐を統一した元親の血。',
  trait:{ id:'ichiryou', label:'一領具足', color:'#00695c',
  desc:'兵数+10%',
  apply:(w,ctx)=>{ if(ctx==='army_size') return {bonus:.10}; return {}; }},
  },
  {
  id:'naga', name:'長尾', s:{bu:78,ch:60,se:54,to:82},
  desc:'越後の龍。上杉謙信の出自たる武人の血。',
  trait:{ id:'echigo_ryu', label:'越後龍', color:'#1565c0',
  desc:'武力+6・統率+6',
  apply:(w,ctx)=>{ if(ctx==='battle') return {buBonus:6,toBonus:6}; return {}; }},
  },
  {
  id:'hosa', name:'細川', s:{bu:48,ch:80,se:84,to:50},
  desc:'文化と権力の仲介者。京都文化を体現する知。',
  trait:{ id:'kanrei', label:'管領', color:'#6a1b9a',
  desc:'政治+10・名声獲得+5%',
  apply:(w,ctx)=>{ if(ctx==='rep_win') return {rm:1.05}; if(ctx==='train') return {seBonus:10}; return {}; }},
  },
  {
  id:'otom', name:'大友', s:{bu:52,ch:68,se:76,to:58},
  desc:'南蛮貿易で栄えた九州の雄。鉄砲の先駆者。',
  trait:{ id:'nanban', label:'南蛮交易', color:'#bf360c',
  desc:'名声+20（初陣）・政治+6',
  apply:(w,ctx)=>{ if(ctx==='first_battle') return {repBonus:20}; if(ctx==='train') return {seBonus:6}; return {}; }},
  },
  {
  id:'ash', name:'芦名', s:{bu:56,ch:66,se:60,to:56},
  desc:'会津の豪族。東北に覇を唱えた悲運の家。',
  trait:{ id:'aidu', label:'会津魂', color:'#4e342e',
  desc:'敗北後 名声減少なし',
  apply:(w,ctx)=>{ if(ctx==='loss_pen') return {noRepLoss:true}; return {}; }},
  },
  {
  id:'azai', name:'浅井', s:{bu:68,ch:54,se:50,to:66},
  desc:'北近江の義将。義を通した悲劇の家系。',
  trait:{ id:'giretsu', label:'義烈', color:'#c62828',
  desc:'連敗中 武力+8',
  apply:(w,ctx)=>{ if(ctx==='battle_streak_loss') return {buBonus:8}; return {}; }},
  },
  {
  id:'asak', name:'朝倉', s:{bu:52,ch:68,se:70,to:50},
  desc:'越前の名門。文化と伝統を重んじる保守の血。',
  trait:{ id:'dento', label:'名門の矜持', color:'#5d4037',
  desc:'鍛錬 知略+政治 優遇',
  apply:(w,ctx)=>{ if(ctx==='train') return {chBonus:4,seBonus:4}; return {}; }},
  },
  {
  id:'ima', name:'今川', s:{bu:44,ch:76,se:80,to:48},
  desc:'海道一の弓取り。法と文化の高い家格。',
  trait:{ id:'imagawa_kana', label:'仮名目録', color:'#0277bd',
  desc:'政治+12',
  apply:(w,ctx)=>{ if(ctx==='train') return {seBonus:12}; return {}; }},
  },
  {
  id:'kita', name:'北畠', s:{bu:58,ch:65,se:62,to:58},
  desc:'伊勢の神官武将。公武を兼ねた特異な血脈。',
  trait:{ id:'kuge', label:'公武兼帯', color:'#558b2f',
  desc:'全ステ均等成長+2',
  apply:(w,ctx)=>{ if(ctx==='train') return {allBonus:2}; return {}; }},
  },
  {
  id:'ryuz', name:'龍造寺', s:{bu:76,ch:46,se:44,to:66},
  desc:'肥前の熊。力で九州を制した猛将の血。',
  trait:{ id:'higo_kuma', label:'肥前の熊', color:'#37474f',
  desc:'武力+10（ただし知略-5）',
  apply:(w,ctx)=>{ if(ctx==='battle') return {buBonus:10,chPenalty:-5}; return {}; }},
  },
  {
  id:'ron', name:'流浪', s:{bu:62,ch:62,se:62,to:62},
  desc:'主を持たぬ者。しかし無限の可能性を宿す。',
  trait:{ id:'mugen', label:'無限の可能性', color:'#b06bff',
  desc:'全ステ成長+8%・覚醒確率2倍',
  apply:(w,ctx)=>{ if(ctx==='train') return {mul:1.08}; if(ctx==='awaken') return {rate:2}; return {}; }},
  },
];
const AFFINITY_TABLE = {
  'oda_take':  { level:'great', label:'宿命の好敵手', bonus:'全ステ+4',      ic:'⚡', statBonus:{bu:4,ch:4,se:4,to:4} },
  'oda_toku':  { level:'great', label:'天下覇業の同志', bonus:'政治+6・名声+15',ic:'👑', statBonus:{se:6}, repBonus:15 },
  'take_uesi': { level:'great', label:'信玄・謙信の血', bonus:'武力+6・統率+6', ic:'⚔', statBonus:{bu:6,to:6} },
  'shim_ryuz': { level:'good',  label:'九州の双雄',    bonus:'武力+5',        ic:'🔥', statBonus:{bu:5} },
  'san_uesi':  { level:'good',  label:'義の継承',      bonus:'統率+5・知略+3', ic:'🌸', statBonus:{to:5,ch:3} },
  'date_hojo': { level:'good',  label:'関東の覇者',    bonus:'政治+5・統率+4', ic:'🏯', statBonus:{se:5,to:4} },
  'mou_hosa':  { level:'good',  label:'文と謀の融合',   bonus:'知略+6・政治+4', ic:'🧠', statBonus:{ch:6,se:4} },
  'oda_asak':  { level:'bad',   label:'金ヶ崎の因縁',  bonus:'—（成長-5%）',  ic:'💀', statBonus:{}, malus:true },
  'oda_azai':  { level:'bad',   label:'浅井の遺恨',    bonus:'—（成長-5%）',  ic:'💀', statBonus:{}, malus:true },
  'take_ima':  { level:'good',  label:'駿河侵攻の血',   bonus:'知略+4・政治+4', ic:'📜', statBonus:{ch:4,se:4} },
  'cho_shim':  { level:'good',  label:'西の豪傑',      bonus:'武力+6',        ic:'⚔', statBonus:{bu:6} },
  'ron_ron':   { level:'great', label:'流浪同士の絆',   bonus:'全ステ+6・覚醒率+',ic:'✦', statBonus:{bu:6,ch:6,se:6,to:6} },
  'naga_uesi': { level:'great', label:'越後の系譜',     bonus:'統率+8',        ic:'🏯', statBonus:{to:8} },
  'toku_hojo': { level:'good',  label:'関東盟友',      bonus:'政治+6',        ic:'🌸', statBonus:{se:6} },
  'kita_hosa': { level:'good',  label:'公家武者の誇り', bonus:'知略+5・政治+5', ic:'📜', statBonus:{ch:5,se:5} },
};
function getAffinityKey(a, b) {
  const ids = [a.id, b.id].sort();
  return ids[0] + '_' + ids[1];
}
function getAffinity(fa, mo) {
  if (!fa || !mo) return null;
  return AFFINITY_TABLE[getAffinityKey(fa, mo)] || null;
}
const SKILLS = [
  { id:'mos', nm:'猛将',   ic:'⚔',  ef:'戦闘時 武力+10',        tp:'battle',  st:'bu', bn:10 },
  { id:'gun', nm:'軍師',   ic:'🧠', ef:'戦闘時 知略+10',         tp:'battle',  st:'ch', bn:10 },
  { id:'hao', nm:'覇王',   ic:'👑', ef:'勝利時 名声+20%',        tp:'rep',     st:null, bn:0, rm:1.2 },
  { id:'kyo', nm:'狂戦士', ic:'💀', ef:'勝率↑ 敗北ペナルティ大', tp:'berserk', st:'bu', bn:15 },
  { id:'sei', nm:'聖人',   ic:'🌸', ef:'鍛錬効果+20%',           tp:'train',   st:null, bn:0 },
  { id:'ten', nm:'天才',   ic:'✨', ef:'全ステ成長+5%',           tp:'growth',  st:null, bn:0 },
  { id:'tai', nm:'大将格', ic:'🏯', ef:'戦闘時 統率+10',          tp:'battle',  st:'to', bn:10 },
];
const PERSONALITIES = [
  {
  id:'ino', label:'猪武者', icon:'🐗', cls:'p-ino',
  desc:'突撃を最優先。前線が崩れても怯まず攻め続ける。',
  ai:()=>({ chargePct:.85, distancePct:.10, targetGeneral:false, retreatThreshold:5, skillRate:.4, rallyBonus:5 }),
  },
  {
  id:'chi', label:'智将', icon:'🧠', cls:'p-chi',
  desc:'距離を保ち状況を見極める。士気管理を重視する。',
  ai:()=>({ chargePct:.25, distancePct:.80, targetGeneral:false, retreatThreshold:25, skillRate:.7, rallyBonus:12 }),
  },
  {
  id:'mou', label:'猛将', icon:'⚡', cls:'p-mou',
  desc:'大将を直接狙い一点突破を図る。スキル発動率が高い。',
  ai:()=>({ chargePct:.65, distancePct:.20, targetGeneral:true, retreatThreshold:10, skillRate:.8, rallyBonus:3 }),
  },
  {
  id:'oku', label:'臆病', icon:'🏃', cls:'p-oku',
  desc:'士気低下で早めに撤退判断。ただし温存した力で反撃も。',
  ai:()=>({ chargePct:.30, distancePct:.55, targetGeneral:false, retreatThreshold:40, skillRate:.35, rallyBonus:2 }),
  },
  {
  id:'tou', label:'統率型', icon:'🏯', cls:'p-tou',
  desc:'味方を密集させ組織的に戦う。士気維持能力が高い。',
  ai:()=>({ chargePct:.45, distancePct:.45, targetGeneral:false, retreatThreshold:18, skillRate:.55, rallyBonus:18 }),
  },
];
const BATTLES = [
  {
  n:'桶狭間の戦い', lo:'織田信長', en:'今川義元', er:'永禄3年', startMonth:5,
  rk:'win', allyBase:800, enemyBase:3000,
  units:['前田隊','柴田隊','丹羽隊','佐々隊'],
  enemyUnits:['松平隊','今川本陣','朝比奈隊','鵜殿隊'],
  fi:'天下を揺るがした一戦', rg:35, mg:40,
  },
  {
  n:'長篠の戦い', lo:'織田信長', en:'武田勝頼', er:'天正3年', startMonth:5,
  rk:'win', allyBase:1200, enemyBase:1500,
  units:['鉄砲隊','足軽組','騎馬備','弓隊'],
  enemyUnits:['馬場隊','山県隊','内藤隊','武田本陣'],
  fi:'鉄砲が変えた戦国の様相', rg:28, mg:32,
  },
  {
  n:'川中島の戦い', lo:'上杉謙信', en:'武田信玄', er:'永禄4年', startMonth:8,
  rk:'draw', allyBase:1000, enemyBase:1000,
  units:['車懸り先鋒','上杉本陣','宇佐美隊','甘粕隊'],
  enemyUnits:['典厩隊','啄木鳥隊','武田本陣','真田隊'],
  fi:'伝説の一騎打ちを目の当たりに', rg:22, mg:25,
  },
  {
  n:'関ヶ原の戦い', lo:'徳川家康', en:'石田三成', er:'慶長5年', startMonth:9,
  rk:'win', allyBase:2000, enemyBase:2200,
  units:['本多忠勝隊','福島正則隊','黒田長政隊','東軍本陣'],
  enemyUnits:['宇喜多隊','大谷吉継隊','石田本陣','小早川隊'],
  fi:'天下統一の立役者として名を刻む', rg:42, mg:50,
  },
  {
  n:'大坂夏の陣', lo:'徳川秀忠', en:'豊臣秀頼', er:'慶長20年', startMonth:5,
  rk:'win', allyBase:1500, enemyBase:1000,
  units:['伊達政宗隊','松平忠直隊','水野勝成隊','幕府本陣'],
  enemyUnits:['真田幸村隊','毛利勝永隊','豊臣本陣','後藤又兵衛隊'],
  fi:'戦国の幕を閉じた最後の大戦', rg:38, mg:45,
  },
];
const BOSS_BATTLE = {
  n:'天下への挑戦', lo:'天下人', en:'織田信長', er:'天正10年', startMonth:6,
  rk:'win', boss:1, allyBase:2500, enemyBase:4000,
  units:['精鋭先鋒隊','騎馬先手','鉄砲備','総大将旗本'],
  enemyUnits:['信長親衛隊','滝川一益隊','丹羽長秀隊','信長本陣'],
  fi:'天下に名を轟かせた伝説的一戦', rg:80, mg:100,
};
const EVENTS = [
  { id:'bus',  nm:'武神降臨',   ic:'⚡', ds:'武神が現れ、{n}に天啓を授けた。\n武力が大きく上昇した。',   st:'bu',   gn:15 },
  { id:'ten2', nm:'天才覚醒',   ic:'💡', ds:'深夜の修行中、{n}は閃きを得た。\n知略が大きく上昇した。',   st:'ch',   gn:15 },
  { id:'min',  nm:'民衆の英雄', ic:'🌸', ds:'民草が{n}の武徳を讃えた。\n名声が大きく上昇した。',         st:null,   gn:0, rb:30 },
  { id:'god',  nm:'神刀の伝授', ic:'⚔', ds:'老師が秘剣を{n}に授けた。\n統率と武力が上昇した。',          st:'both', gn:8 },
];
const TRAINING_MENU = [
  {
  id:'mtn', ti:'山岳修行',
  ds:'険しい山中で武を磨く。肉体は強まるが、政には遠ざかる。',
  ef:[{l:'武力＋大',c:'up'},{l:'統率＋小',c:'up'},{l:'政治－小',c:'dn'}],
  ap: (s, m) => ({ bu:f((6+rn(5))*m), ch:f(rn(2)*m), se:-f(2+rn(3)), to:f((2+rn(3))*m) }),
  ev: ['{n}、夜明けより滝に打たれる', '岩を素手で割り、己の限界を超える', '山中の獣と戦い、生死の境を知る'],
  },
  {
  id:'nai', ti:'内政訓練',
  ds:'城下の政務を学ぶ。知と政が伸びるが、武は衰える。',
  ef:[{l:'政治＋大',c:'up'},{l:'知略＋中',c:'up'},{l:'武力－小',c:'dn'}],
  ap: (s, m) => ({ bu:-f(1+rn(3)), ch:f((3+rn(4))*m), se:f((5+rn(5))*m), to:f((1+rn(2))*m) }),
  ev: ['商人との交渉で民の心を知る', '兵法書を三冊読破する', '城の防衛図を独自に改修する'],
  },
  {
  id:'kis', ti:'奇策の探求',
  ds:'成功すれば大きな飛躍。失敗すれば……無念。',
  ef:[{l:'成功：全能＋大',c:'rd'},{l:'失敗：全能－小',c:'rd'}],
  ap: (s, m) => {
  const ok = rnd() < 0.55;
  return ok
  ? { bu:f((4+rn(6))*m), ch:f((4+rn(6))*m), se:f((3+rn(4))*m), to:f((3+rn(5))*m), ok:1 }
  : { bu:-f(1+rn(3)), ch:-f(1+rn(2)), se:-f(1+rn(2)), to:-f(1+rn(2)), ok:0 };
  },
  ev: ['奇策を試みるが…', '夢の中で謎の老師が現れた', '天と地に問いかけ、答えを待つ'],
  },
];
const FIRST_NAMES = ['信','勝','政','元','義','虎','龍','鬼','剛','武','智','仁','忠','雄','猛'];
const LAST_NAMES  = ['之助','郎','衛門','右近','左衛門','兵衛','介','守','斎','丸'];
const EPITHETS    = ['鬼神の如き武将','知略に長けた謀将','義を貫く忠将','天性の武を持つ豪傑','策士にして勇将','乱世を駆けた流星'];
const RANK_TABLE = [
  { m:350, r:'SS', c:'rss', cm:'伝説の将として永く語り継がれる' },
  { m:250, r:'S',  c:'rs',  cm:'天下に名を轟かせた英雄' },
  { m:150, r:'A',  c:'ra',  cm:'稀代の名将として称えられる' },
  { m:80,  r:'B',  c:'rb',  cm:'勇猛なる武将として記録に残る' },
  { m:0,   r:'C',  c:'rc2', cm:'その生涯は静かに幕を閉じた' },
];
const UNIT_LOG_TEMPLATES = {
  charge:   ['{unit}、突撃！', '{unit}が敵陣へ突き進む！', '{unit}、怒涛の前進！', '{unit}が先陣を切る！'],
  rout:     ['{unit}、崩れる！', '{unit}が総崩れ！', '{unit}の旗印が倒れた！', '{unit}が退路を求めて散った！'],
  hold:     ['{unit}、踏みとどまる！', '{unit}が死守！', '{unit}の壁、崩れず！'],
  kill:     ['{unit}が敵将を討ち取る！', '{unit}の一撃、敵大将に届く！'],
  suffer:   ['{unit}に大損害！', '{unit}、甚大な被害！', '{unit}の前線が崩壊寸前！'],
  morale_up:  ['士気回復！兵の目に闘志が戻る！', '鬨の声が戦場に響き渡る！', '逆転の気配、味方士気上昇！'],
  morale_dn:  ['士気が揺らぐ…', '兵の足が止まりかける…', '恐怖が前線に広がる…'],
  reversal: ['まさかの逆転！', '劣勢から大反撃！', '諦めなかった者に女神が微笑む！'],
  general:  ['{n}が先頭に立つ！', '{n}、叱咤激励！', '{n}が決死の突入！'],
};
const MONTHS = ['正月','二月','三月','四月','五月','六月','七月','八月','九月','十月','十一月','十二月'];
let G = { warrior:null, battles:[], trainCnt:0, gen:1, lossStreak:0 };
let selectedFather = null, selectedMother = null;
let battleTimers   = [];
let currentBattle  = null;
let pendingResult  = null;
let battleSim      = null;
let currentTraining = null;
let battleTime = { year:'永禄元年', month:1, era:'永禄元年' };
function goScreen(id) {
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  $el(id).classList.add('active');
  window.scrollTo(0,0);
  if (id === 'screen-gacha')   _initGachaScreen();
  if (id === 'screen-home')    renderHome();
  if (id === 'screen-history') renderHistory();
}
function goBack() { goScreen(G.warrior ? 'screen-home' : 'screen-title'); }
function calcEffectiveBu(isUnderdog) {
  const w = G.warrior; let b = 0;
  if (w.skill && (w.skill.tp==='battle'||w.skill.tp==='berserk') && w.skill.st==='bu') b += w.skill.bn;
  if (w.mut) b += 8;
  b += traitBuBonus(isUnderdog);
  return cl(w.s.bu + b, 1, 120);
}
function calcEffectiveTo() {
  const w = G.warrior; let b = 0;
  if (w.skill?.tp==='battle' && w.skill.st==='to') b += w.skill.bn;
  if (w.mut) b += 5;
  b += traitToBonus();
  return cl(w.s.to + b, 1, 120);
}
function calcEffectiveCh() {
  const w = G.warrior; let b = 0;
  if (w.skill?.tp==='battle' && w.skill.st==='ch') b += w.skill.bn;
  b += traitChBonus();
  return cl(w.s.ch + b, 1, 120);
}
function calcTrainMultiplier() {
  const w = G.warrior; let m = 1.0;
  if (w.skill?.tp==='train')  m = 1.2;
  if (w.skill?.tp==='growth') m = 1.05;
  if (w.mut) m += 0.1;
  m += (traitTrainMul() - 1);
  return m;
}
function traitApply(ctx) {
  const w = G.warrior;
  const r = {};
  const merge = res => { Object.entries(res).forEach(([k,v])=>{ r[k]=(r[k]||0)+v; }); };
  if (w.faTrait?.apply) merge(w.faTrait.apply(w, ctx));
  if (w.moTrait?.apply) merge(w.moTrait.apply(w, ctx));
  return r;
}
function traitBuBonus(isUnderdog) {
  const w = G.warrior;
  let b = traitApply('battle').buBonus || 0;
  if (isUnderdog)       b += traitApply('battle_underdog').buBonus  || 0;
  if (G.lossStreak >= 2) b += traitApply('battle_streak_loss').buBonus || 0;
  return b;
}
function traitToBonus()  { return traitApply('battle').toBonus  || 0; }
function traitChBonus()  { return traitApply('battle').chBonus  || 0; }
function traitMoraleFloor() { return traitApply('battle').moraleFloor || 0; }
function traitTrainMul() { const r=traitApply('train'); return 1 + (r.mul ? r.mul-1 : 0); }
function traitTrainStatBonus(k) {
  const r = traitApply('train');
  let b = r.allBonus || 0;
  if (k==='se') b += r.seBonus || 0;
  if (k==='ch') b += r.chBonus || 0;
  return b;
}
function traitAwakenMul() { return traitApply('awaken').rate || 1; }
function applyRepSkill(rg) {
  let m = 1.0;
  if (G.warrior.skill?.tp==='rep') m *= G.warrior.skill.rm;
  const tr = traitApply('rep_win');
  if (tr.rm) m *= tr.rm;
  return m !== 1.0 ? Math.round(rg * m) : rg;
}
function calcLossPenalty(rg) {
  const base = -f(rg * 0.3) - (G.warrior.skill?.tp==='berserk' ? 10 : 0);
  const tr = traitApply('loss_pen');
  if (tr.noRepLoss) return 0;
  if (tr.reduce)    return Math.round(base * (1 - tr.reduce));
  return base;
}
function _initGachaScreen() {
  selectedFather = selectedMother = null;
  $el('gbtn').disabled = true; $el('gbtn').style.opacity = '.4';
  $el('sinfo').textContent = '';
  renderBloodlineGrid('fg','father'); renderBloodlineGrid('mg','mother');
}
function statToGrade(v) {
  if (v >= 88) return 'SS';
  if (v >= 75) return 'S';
  if (v >= 62) return 'A';
  if (v >= 50) return 'B';
  if (v >= 38) return 'C';
  return 'D';
}
function gradeClass(g) {
  return {SS:'spip-ss',S:'spip-s',A:'spip-a',B:'spip-b',C:'spip-c',D:'spip-d'}[g]||'spip-c';
}
function genStatCap(gen) {
  const caps = [60, 68, 76, 84, 92, 100];
  return caps[Math.min((gen||1) - 1, 5)];
}
function renderBloodlineGrid(gridId, role) {
  const pool = [...BLOODLINES].sort(()=>rnd()-.5).slice(0, 4);
  $el(gridId).innerHTML = pool.map(b => {
  const pips = STAT_KEYS.map(([k, l]) => {
  const g = statToGrade(b.s[k]);
  return `<span class="spip ${gradeClass(g)}">${l[0]} ${g}</span>`;
  }).join('');
  const traitColor = b.trait?.color?.startsWith('var(') ? '#b06bff' : (b.trait?.color||'#888');
  const traitBadge = b.trait
  ? `<span class="btrait" style="color:${traitColor};border-color:${traitColor}">${b.trait.label}</span>`
  : '';
  return `<div class="bcard" onclick="onSelectBloodline('${b.id}','${role}',this)">
  <div class="bnm">${b.name}</div>
  <div class="bdsc">${b.desc}</div>
  <div class="bst">${pips}</div>
  ${traitBadge}
  </div>`;
  }).join('');
}
function onSelectBloodline(id, role, el) {
  el.closest('.bgrid').querySelectorAll('.bcard').forEach(c=>c.classList.remove('sel'));
  el.classList.add('sel');
  const bl = BLOODLINES.find(x=>x.id===id);
  if (role==='father') selectedFather = bl; else selectedMother = bl;
  _updateGachaButton();
}
function _updateGachaButton() {
  const info=$el('sinfo'), btn=$el('gbtn');
  if (selectedFather && selectedMother) {
  info.textContent = `父：${selectedFather.name}の血脈 × 母：${selectedMother.name}の血脈`;
  btn.disabled = false; btn.style.opacity = '1';
  _showAffinityRow(selectedFather, selectedMother);
  } else {
  if (selectedFather) info.textContent = `父：${selectedFather.name}の血脈を選択中`;
  else if (selectedMother) info.textContent = `母：${selectedMother.name}の血脈を選択中`;
  $el('affinity-row').style.display = 'none';
  }
}
function _showAffinityRow(fa, mo) {
  const aff = getAffinity(fa, mo);
  const row = $el('affinity-row');
  const icMap = {great:'⚡',good:'✦',normal:'…',bad:'💀'};
  const clsMap= {great:'aff-great',good:'aff-good',normal:'aff-normal',bad:'aff-bad'};
  if (aff) {
  $el('aff-ic').textContent = aff.ic || icMap[aff.level];
  $el('aff-text').textContent = aff.label;
  $el('aff-text').className = 'affinity-text ' + clsMap[aff.level];
  $el('aff-bonus').textContent = aff.bonus;
  } else {
  $el('aff-ic').textContent = '—';
  $el('aff-text').textContent = '特別な縁なし';
  $el('aff-text').className = 'affinity-text aff-normal';
  $el('aff-bonus').textContent = '';
  }
  row.style.display = 'flex';
}
function doGacha() {
  if (!selectedFather || !selectedMother) return;
  G.warrior = generateWarrior(selectedFather, selectedMother, G.gen, null);
  renderBornScreen(); goScreen('screen-born');
}
function generateWarrior(fa, mo, gen, parentName) {
  const bs = k => cl(Math.round(fa.s[k]*.55 + mo.s[k]*.45 + (rnd()*20-8)), 40, 100);
  const aff = getAffinity(fa, mo);
  const w = {
  name: `${fa.name} ${pick(FIRST_NAMES)}${pick(LAST_NAMES)}`,
  ep: pick(EPITHETS),
  s: {bu:bs('bu'),ch:bs('ch'),se:bs('se'),to:bs('to')},
  rep:0, mer:0, age:15, maxAge:f(50+rnd()*20), btls:0,
  fa:fa.name, mo:mo.name,
  faId:fa.id, moId:mo.id,
  faTrait:fa.trait, moTrait:mo.trait,
  affinity: aff || null,
  skill:rollSkill(), mut:false,
  gen, parentName, personality: pick(PERSONALITIES),
  };
  if (aff && !aff.malus) {
  STAT_KEYS.forEach(([k])=>{
  if (aff.statBonus[k]) w.s[k] = cl(w.s[k] + aff.statBonus[k], 40, 100);
  });
  if (aff.repBonus) w.rep += aff.repBonus;
  } else if (aff?.malus) {
  w.maxAge = Math.max(40, w.maxAge - 5);
  }
  return w;
}
function rollSkill() { return rnd()>.25 ? null : pick(SKILLS); }
function doInherit() {
  const prev = G.warrior; if(!prev) return;
  const mb = f(prev.mer/50); G.gen++;
  const cs = {}; STAT_KEYS.forEach(([k])=>{ cs[k]=cl(Math.round(prev.s[k]*.3+rnd()*20+mb),35,100); });
  G.battles=[]; G.trainCnt=0; G.lossStreak=0;
  const faObj = BLOODLINES.find(b=>b.id===prev.faId) || {name:prev.fa,s:cs,id:prev.faId||'ron'};
  const moObj = BLOODLINES.find(b=>b.id===prev.moId) || {name:prev.mo,s:cs,id:prev.moId||'ron'};
  const fa={...faObj,s:cs}, mo={...moObj,s:cs};
  G.warrior = generateWarrior(fa, mo, G.gen, prev.name);
  G.warrior._inheritText = `${prev.name}の子　（第${G.gen}代）　功績継承ボーナス +${mb}`;
  renderBornScreen();
  goScreen('screen-born');
}
function showTrChoices() {
  $el('tchdr').textContent=`天正${G.trainCnt+1}年　いずれの道で己を磨くか`;
  $el('tcarea').innerHTML = TRAINING_MENU.map(ch=>{
  const tags = ch.ef.map(e=>`<span class="etag e${e.c}">${e.l}</span>`).join('');
  return `<div class="tc" onclick="onSelectTraining('${ch.id}')"><div class="tct">【${ch.ti}】</div><div class="tcd">${ch.ds}</div><div class="tefx">${tags}</div></div>`;
  }).join('');
  goScreen('screen-training-choice');
}
function onSelectTraining(id) {
  currentTraining = TRAINING_MENU.find(c=>c.id===id);
  executeTraining();
}
function executeTraining() {
  goScreen('screen-training');
  const w=G.warrior, ch=currentTraining, mul=calcTrainMultiplier();
  $el('tyr').textContent=`天正${G.trainCnt+1}年`;
  $el('tlog').innerHTML=''; $el('tstats').innerHTML=''; $el('tdbtn').style.display='none';
  const gains=ch.ap(w.s,mul);
  const messages=[...ch.ev];
  if (gains.ok===0) messages.push('しかし結果は思わしくなかった……');
  else if (ch.id==='kis'&&gains.ok) messages.push('閃き！全てがうまくいった！');
  const rareEvent = rnd()<.02 ? pick(EVENTS) : null;
  const logEl=$el('tlog');
  messages.forEach((msg,i)=>{
  setTimeout(()=>{
  const el=document.createElement('div'); el.className='titem';
  el.textContent=msg.replace('{n}',shortName(w)); logEl.appendChild(el);
  logEl.scrollTop=logEl.scrollHeight;
  }, i*800);
  });
  setTimeout(()=>{
  applyTrainingGains(gains); renderTrainingResult(gains);
  if(!checkDeath()){ $el('tdbtn').style.display='block'; if(rareEvent) setTimeout(()=>showEventOverlay(rareEvent),400); }
  }, messages.length*800+600);
}
function applyTrainingGains(gains) {
  const w = G.warrior;
  const cap = genStatCap(w.gen);
  STAT_KEYS.forEach(([k]) => {
  if (k in gains) {
  const tb   = traitTrainStatBonus(k);
  const raw  = gains[k] + tb;
  const cur  = w.s[k];
  const potential = Math.max(
  (BLOODLINES.find(b=>b.id===w.faId)?.s[k]||100),
  (BLOODLINES.find(b=>b.id===w.moId)?.s[k]||100)
  );
  const hardCap = Math.min(cap, potential);
  if (raw <= 0) {
  w.s[k] = cl(cur + raw, 35, 100);
  } else if (cur >= hardCap) {
  w.s[k] = cl(cur + Math.max(1, f(raw * 0.15)), 35, 100);
  } else {
  const headroom = hardCap - cur;
  if (raw <= headroom) {
  w.s[k] = cl(cur + raw, 35, 100);
  } else {
  w.s[k] = cl(hardCap + Math.max(0, f((raw - headroom) * 0.15)), 35, 100);
  }
  }
  }
  });
  w.age++; G.trainCnt++;
}
function renderTrainingResult(gains) {
  const w = G.warrior;
  const cap = genStatCap(w.gen);
  $el('tstats').innerHTML = STAT_KEYS.map(([k,lbl])=>{
  const rawGain = gains[k]||0;
  const tb = traitTrainStatBonus(k);
  const d = rawGain + tb;
  const atCap = w.s[k] >= cap;
  const capNote = atCap ? `<span style="font-size:8px;color:rgba(26,18,8,.35);letter-spacing:.05em">上限${cap}</span>` : '';
  return `<div class="tsi"><div class="tsin">${lbl}</div><div class="tsiv">${w.s[k]}</div><div class="tsid${d<0?' neg':''}">${d>=0?'+':''}${d}</div>${capNote}</div>`;
  }).join('');
}
function finishTr() { renderHome(); goScreen('screen-home'); }
function showEventOverlay(ev) {
  const w=G.warrior, desc=ev.ds.replace('{n}',shortName(w)).replace('\n','<br>');
  const el=document.createElement('div'); el.className='ov'; el.id='rov';
  el.innerHTML=`<div class="ovc rare"><span class="ovic">${ev.ic}</span><div class="ovtag">— 超稀少イベント —</div><div class="ovnm">${ev.nm}</div><div class="ovdsc">${desc}</div><button class="btn-g" onclick="applyEvent('${ev.id}')">受け取る</button></div>`;
  $el('app').appendChild(el);
}
function applyEvent(evId) {
  const ev=EVENTS.find(e=>e.id===evId), w=G.warrior;
  if(!ev){ closeOverlay('rov'); return; }
  if(ev.st==='both'){ w.s.bu=cl(w.s.bu+ev.gn,35,100); w.s.to=cl(w.s.to+ev.gn,35,100); }
  else if(ev.st) w.s[ev.st]=cl(w.s[ev.st]+ev.gn,35,100);
  if(ev.rb) w.rep+=ev.rb;
  closeOverlay('rov'); renderHome();
}
function closeOverlay(id) { const el=$el(id); if(el) el.remove(); }
function tryAwaken() {
  const w=G.warrior;
  const awakenChance = 0.35 * traitAwakenMul();
  if(w.mut || G.lossStreak<2 || rnd()>awakenChance) return false;
  w.mut=true;
  const gain=f(5+rnd()*6);
  STAT_KEYS.forEach(([k])=>{ w.s[k]=cl(w.s[k]+gain,35,100); });
  const el=document.createElement('div'); el.className='ov awbg'; el.id='aov';
  el.innerHTML=`<div class="ovc aw"><span class="ovic aw">✦</span><div class="ovtag aw">— 覚醒 —</div><div class="ovnm aw">${w.name}</div><div class="ovdsc">連敗の闇の中で、${shortName(w)}は眠れる力を目覚めさせた。<br>全ステータスが <strong style="color:var(--aw-l)">+${gain}</strong> 上昇し、<br>「覚醒」状態となった。</div><button class="btn-aw" onclick="closeOverlay('aov');goScreen('screen-home')">力を受け入れる</button></div>`;
  $el('app').appendChild(el);
  return true;
}
function initBattleTime(bd) {
  const m = bd.er.match(/(\d+)年/);
  battleTime = {
  eraName: bd.er.replace(/\d+年/,''),
  year: m ? parseInt(m[1]) : 1,
  month: bd.startMonth || 1,
  baseEra: bd.er,
  };
}
function advanceBattleTime() {
  battleTime.month++;
  if (battleTime.month > 12) { battleTime.month = 1; battleTime.year++; }
  updateTimeDisplay();
}
function updateTimeDisplay() {
  const t = battleTime;
  const yearStr = `${t.eraName}${t.year}年`;
  const monthStr = MONTHS[t.month-1];
  const displayEl = $el('b-time-display');
  if (displayEl) {
  displayEl.style.animation = 'none';
  displayEl.textContent = yearStr;
  requestAnimationFrame(()=>{ displayEl.style.animation = 'timeFlip .4s ease'; });
  }
  const monthEl = $el('b-time-month');
  if (monthEl) monthEl.textContent = monthStr;
}
const MAX_SOLDIERS = 40;
function renderSoldiersInit(allyMax, enemyMax) {
  const total = Math.max(allyMax, enemyMax);
  const allyCount  = Math.round((allyMax  / total) * MAX_SOLDIERS);
  const enemyCount = Math.round((enemyMax / total) * MAX_SOLDIERS);
  renderSoldierGrid('ally-grid',  allyCount,  '🗡', 'charging-r');
  renderSoldierGrid('enemy-grid', enemyCount, '🔴', 'charging-l');
  $el('ally-hp-val').textContent  = allyMax.toLocaleString() + '人';
  $el('enemy-hp-val').textContent = enemyMax.toLocaleString() + '人';
  $el('ally-hp-val').className    = 'army-hp-val';
  $el('enemy-hp-val').className   = 'army-hp-val';
}
function renderSoldierGrid(gridId, count, icon, animClass) {
  const grid = $el(gridId);
  if (!grid) return;
  grid.innerHTML = '';
  for (let i = 0; i < count; i++) {
  const span = document.createElement('span');
  span.className = 'sol ' + animClass;
  span.style.animationDelay = (i * 0.025) + 's';
  span.textContent = icon;
  grid.appendChild(span);
  }
}
function updateSoldiers(allyHP, allyMax, enemyHP, enemyMax, animType) {
  updateSideGrid('ally-grid',  'ally-hp-val',  allyHP,  allyMax,  enemyMax, '🗡', animType, false);
  updateSideGrid('enemy-grid', 'enemy-hp-val', enemyHP, enemyMax, allyMax,  '🔴', animType, true);
}
function updateSideGrid(gridId, hpId, hp, maxHP, totalMax, icon, animType, isEnemy) {
  const grid = $el(gridId), hpEl = $el(hpId);
  if (!grid || !hpEl) return;
  const pct = Math.max(0, hp / Math.max(maxHP, 1));
  const scaledMax = Math.max(maxHP, totalMax, 1);
  const currentCount = grid.querySelectorAll('.sol:not(.dying):not(.retreating-l):not(.retreating-r)').length;
  if (animType === 'rout') {
  grid.querySelectorAll('.sol:not(.dying)').forEach((el, i) => {
  setTimeout(() => {
  el.classList.add(isEnemy ? 'retreating-r' : 'retreating-l');
  setTimeout(() => el.remove(), 500);
  }, i * 18);
  });
  } else {
  const targetCount = Math.round(pct * MAX_SOLDIERS * (maxHP / scaledMax));
  const toRemove = Math.max(0, currentCount - targetCount);
  const alive = Array.from(grid.querySelectorAll('.sol:not(.dying):not(.retreating-l):not(.retreating-r)'));
  for (let i = 0; i < Math.min(toRemove, alive.length); i++) {
  const idx = alive.length - 1 - i;
  if (alive[idx]) {
  alive[idx].classList.add('dying');
  setTimeout(() => alive[idx].remove(), 350);
  }
  }
  if (animType === 'clash') {
  const live = grid.querySelectorAll('.sol:not(.dying)');
  const front = Array.from(live).slice(0, Math.min(5, live.length));
  front.forEach(el => {
  el.classList.add('clashing');
  setTimeout(() => el.classList.remove('clashing'), 400);
  });
  }
  if (animType === 'shake') {
  grid.querySelectorAll('.sol:not(.dying)').forEach(el => {
  el.classList.add('shaking');
  setTimeout(() => el.classList.remove('shaking'), 300);
  });
  }
  }
  hpEl.textContent = hp.toLocaleString() + '人';
  const ratio = hp / Math.max(maxHP, 1);
  hpEl.style.color = ratio < 0.3 ? 'var(--morale-lo)' : ratio < 0.6 ? '#ffb74d' : (isEnemy ? '#ff8a80' : 'var(--morale-hi)');
  if (ratio < 0.25) hpEl.className = 'army-hp-val critical';
  else hpEl.className = 'army-hp-val';
}
function screenFlash(color) {
  const el = $el('bf-flash');
  if (!el) return;
  el.style.background = color==='red' ? 'rgba(200,50,50,.35)' : 'rgba(200,148,26,.25)';
  el.style.animation = 'none';
  requestAnimationFrame(() => {
  el.style.animation = 'screenFlash .5s ease forwards';
  });
}
function updateMoraleBars(am, em) {
  const col = m => m>60?'var(--morale-hi)':m>30?'#ffb74d':'var(--morale-lo)';
  $el('ally-morale-num').textContent  = Math.round(am);
  $el('ally-morale-num').style.color  = col(am);
  $el('ally-morale-fill').style.width = am + '%';
  $el('ally-morale-fill').style.background = col(am);
  $el('enemy-morale-num').textContent  = Math.round(em);
  $el('enemy-morale-num').style.color  = col(em);
  $el('enemy-morale-fill').style.width = em + '%';
  $el('enemy-morale-fill').style.background = col(em);
}
function updateMoraleStatus(am, em) {
  const el = $el('morale-status-row');
  if (!el) return;
  if (am <= 20)      { el.textContent='⚠ 味方士気崩壊寸前'; el.style.color='var(--morale-lo)'; }
  else if (em <= 20) { el.textContent='⚔ 敵軍崩壊寸前！'; el.style.color='#81c784'; }
  else if (am >= 80) { el.textContent='✦ 士気旺盛'; el.style.color='var(--morale-hi)'; }
  else               { el.textContent=''; }
}
function addLog(ic, icCls, text, textCls, sub) {
  const area = $el('battle-log-area');
  if (!area) return;
  const el = document.createElement('div');
  el.className = 'blog-entry';
  el.innerHTML = `<div class="blog-ic ${icCls}">${ic}</div><div><div class="blog-text ${textCls||''}">${text}</div>${sub?`<div class="blog-sub">${sub}</div>`:''}</div>`;
  area.appendChild(el);
  area.scrollTop = area.scrollHeight;
}
function addLogFinal(label, text) {
  const area = $el('battle-log-area');
  if (!area) return;
  const el = document.createElement('div');
  el.className = 'blog-final';
  el.innerHTML = `<div class="blog-final-badge">▶ ${label}</div><div class="blog-final-text">${text}</div>`;
  area.appendChild(el);
  area.scrollTop = area.scrollHeight;
}
function pickUnitLog(type, units, warriorName) {
  const pool = UNIT_LOG_TEMPLATES[type] || [];
  let msg = pick(pool) || '';
  msg = msg.replace('{unit}', pick(units)||'一番組');
  msg = msg.replace('{n}', warriorName);
  return msg;
}
function showRoutOverlay(allyWon) {
  const ov = $el('rout-overlay');
  if (!ov) return;
  ov.innerHTML = `
  <div class="rout-banner-big">
  <span class="rout-kanji ${allyWon?'win-text':'lose-text'}">${allyWon?'敵軍　総崩れ':'味方　退却'}</span>
  <div class="rout-sub-text">${allyWon?'勝利の鬨が戦場を包む':'また刃を交える日を待て'}</div>
  </div>`;
  ov.style.display = 'flex';
  setTimeout(() => { ov.style.display = 'none'; }, 2500);
}
function showReversalOverlay() {
  const bf = $el('battlefield');
  if (!bf) return;
  const el = document.createElement('div');
  el.className = 'reversal-overlay';
  el.innerHTML = `<span class="reversal-text">逆転！</span>`;
  bf.appendChild(el);
  setTimeout(() => el.remove(), 2000);
}
function startBattle() {
  clearBattleTimers();
  const recent = G.battles.slice(-2).map(b=>b.n);
  const filtered = BATTLES.filter(b=>!recent.includes(b.n));
  currentBattle = pick(filtered.length > 0 ? filtered : BATTLES);
  runBattle(currentBattle);
}
function startBossBattle() { clearBattleTimers(); currentBattle=BOSS_BATTLE; runBattle(BOSS_BATTLE); }
function runBattle(bd) {
  const w = G.warrior;
  initBattleTime(bd);
  updateTimeDisplay();
  $el('b-title-row').textContent = bd.n;
  $el('ally-general').textContent = shortName(w);
  $el('enemy-general').textContent = bd.en;
  $el('battle-log-area').innerHTML = '';
  $el('b-next-btn').classList.remove('rdy');
  $el('rout-overlay').style.display = 'none';
  $el('bf-flash').style.opacity = '0';
  const pers = w.personality || PERSONALITIES[0];
  $el('ally-personality-badge').innerHTML = `<span class="personality-inline ${pers.cls}">${pers.icon} ${pers.label}</span>`;
  const to = calcEffectiveTo();
  const armySizeBonus = traitApply('army_size').bonus || 0;
  const allyBase = Math.round(bd.allyBase * (1 + (to-60)*.005) * (1 + armySizeBonus));
  const enemyBase = bd.enemyBase;
  battleSim = {
  allyHP: allyBase, enemyHP: enemyBase,
  allyMax: allyBase, enemyMax: enemyBase,
  allyMorale: 100, enemyMorale: 100,
  phase: 'army', routed: null,
  bu: calcEffectiveBu(), to,
  ch: calcEffectiveCh(),
  moraleFloor: traitMoraleFloor(),
  aiAction: (w.personality||PERSONALITIES[0]).ai(),
  units: bd.units || ['先鋒隊','本陣','右翼','左翼'],
  enemyUnits: bd.enemyUnits || ['敵先鋒','敵本陣','敵右翼','敵左翼'],
  };
  renderSoldiersInit(allyBase, enemyBase);
  updateMoraleBars(100, 100);
  $el('morale-status-row').textContent = '';
  $el('b-rep').textContent  = w.rep;
  $el('b-rep-fill').style.width = Math.min(w.rep/2,100)+'%';
  $el('b-mer').textContent  = w.mer;
  $el('b-mer-fill').style.width = Math.min(w.mer/5,100)+'%';
  goScreen('screen-battle');
  const result = computeFullBattle(bd, w);
  pendingResult = result;
  playBattleAnimation(bd, result, w);
}
function computeFullBattle(bd, w) {
  const sim = JSON.parse(JSON.stringify(battleSim));
  const ai = sim.aiAction;
  const bu = sim.bu;
  const ch = sim.ch || w.s.ch;
  const moraleFloor = sim.moraleFloor || 0;
  let wasLosing = false;
  let reversalTriggered = false;
  let turnCount = 0;
  const maxTurns = 10;
  while (!sim.routed && turnCount < maxTurns) {
  const isUnderdog = sim.allyHP < sim.allyMax * .5 && sim.allyMorale < sim.enemyMorale - 20;
  const effectiveBu = isUnderdog ? calcEffectiveBu(true) : bu;
  const chargeBoost = ai.chargePct > .6 ? 1.2 : 1.0;
  const skillTrigger = rnd() < ai.skillRate;
  let allyAtk  = f((effectiveBu * .4 + rn(20)) * chargeBoost);
  allyAtk += f(ch * .05);
  if (skillTrigger && w.skill?.tp==='battle') allyAtk += w.skill.bn * 2;
  if (ai.targetGeneral) allyAtk = f(allyAtk * 1.3);
  let enemyAtk = f(30 + rn(28));
  const allyLoss  = cl(f(enemyAtk * (100-sim.allyMorale*.3)/100), 1, f(sim.allyHP*.25));
  const enemyLoss = cl(f(allyAtk  * (50+sim.allyMorale*.5)/100),  1, f(sim.enemyHP*.3));
  sim.allyHP  = Math.max(0, sim.allyHP  - allyLoss);
  sim.enemyHP = Math.max(0, sim.enemyHP - enemyLoss);
  const allyM  = calcMoraleDelta2(sim,'ally', allyLoss, enemyLoss, ai);
  const enemyM = calcMoraleDelta2(sim,'enemy',enemyLoss,allyLoss,  null);
  sim.allyMorale  = cl(sim.allyMorale  + allyM,  moraleFloor, 100);
  sim.enemyMorale = cl(sim.enemyMorale + enemyM, 0,           100);
  if (wasLosing && sim.allyMorale > sim.enemyMorale + 20) reversalTriggered = true;
  if (sim.allyMorale < 40 && sim.enemyMorale > 60) wasLosing = true;
  if (sim.enemyMorale <= 15 && sim.enemyHP < sim.enemyMax * .4) { sim.routed = 'enemy'; break; }
  if (sim.allyMorale <= 15 && sim.allyHP < sim.allyMax * .4 && moraleFloor === 0) { sim.routed = 'ally'; break; }
  if (sim.allyHP <= 0 || sim.enemyHP <= 0) { sim.phase='duel'; break; }
  if (ai.retreatThreshold > 35 && sim.allyMorale < ai.retreatThreshold && sim.allyHP < sim.allyMax*.5) {
  sim.routed = 'ally'; break;
  }
  turnCount++;
  }
  if (!sim.routed) {
  if (sim.phase === 'duel') {
  const heroAtk = f(bu * .6 + rn(30));
  const bossAtk = f(50 + rn(40));
  sim.routed = heroAtk > bossAtk ? 'enemy' : 'ally';
  } else {
  const effBu  = calcEffectiveBu();
  const winPct = cl(.4 + (effBu-60)*.008, .15, .92);
  sim.routed   = (bd.rk==='draw' ? true : bd.rk==='win' ? rnd()<winPct : false) ? 'enemy' : 'ally';
  }
  }
  const won = sim.routed === 'enemy';
  const rk  = bd.rk==='draw' ? 'draw' : (won ? 'win' : 'loss');
  let rg = bd.rg, mg = bd.mg;
  if (!won && bd.rk!=='draw') { rg=calcLossPenalty(bd.rg); mg=f(bd.mg*.2); }
  if (won) rg = applyRepSkill(rg);
  return {
  won, rk, rg, mg,
  allyFinal:   sim.allyHP,
  enemyFinal:  sim.enemyHP,
  allyMax:     sim.allyMax,
  enemyMax:    sim.enemyMax,
  allyMorale:  sim.allyMorale,
  enemyMorale: sim.enemyMorale,
  reversalTriggered,
  allyTurns: turnCount,
  };
}
function calcMoraleDelta2(sim, side, ownLoss, oppLoss, ai) {
  const maxHP = side==='ally' ? sim.allyMax : sim.enemyMax;
  let d = -f((ownLoss/maxHP)*80);
  if (oppLoss > ownLoss*1.5) d += f((oppLoss/(sim.enemyMax||1))*40);
  if (ai) d += f(ai.rallyBonus * rnd());
  const ratio = side==='ally' ? sim.allyHP/sim.allyMax : sim.enemyHP/sim.enemyMax;
  if (ratio < .3) d -= 8;
  return cl(d, -25, 20);
}
function playBattleAnimation(bd, result, w) {
  const sim = JSON.parse(JSON.stringify(battleSim));
  const ai = sim.aiAction;
  const units = bd.units || ['一番組','二番組','三番組'];
  const eu    = bd.enemyUnits || ['敵先鋒','敵本陣','敵右翼'];
  const wn    = shortName(w);
  let delay   = 500;
  const T_TURN  = 1400;
  const T_LOG   = 600;
  const TURN_COUNT = 6;
  for (let t = 0; t < TURN_COUNT; t++) {
  const ti = t;
  battleTimers.push(setTimeout(() => {
  if (!sim || sim.routed) return;
  advanceBattleTime();
  const isFinalTurn = (ti === TURN_COUNT - 1);
  let allyAtk, enemyAtk, allyLoss, enemyLoss;
  if (isFinalTurn) {
  allyLoss  = Math.max(0, sim.allyHP  - result.allyFinal);
  enemyLoss = Math.max(0, sim.enemyHP - result.enemyFinal);
  sim.allyHP     = result.allyFinal;
  sim.enemyHP    = result.enemyFinal;
  sim.allyMorale = result.allyMorale;
  sim.enemyMorale= result.enemyMorale;
  } else {
  const chargeBoost = ai.chargePct > .6 ? 1.2 : 1.0;
  allyAtk  = f((sim.bu * .4 + rn(20)) * chargeBoost);
  enemyAtk = f(30 + rn(28));
  allyLoss  = cl(f(enemyAtk*(100-sim.allyMorale*.3)/100),1,f(sim.allyHP*.25));
  enemyLoss = cl(f(allyAtk *(50+sim.allyMorale*.5)/100), 1,f(sim.enemyHP*.3));
  sim.allyHP  = Math.max(0, sim.allyHP  - allyLoss);
  sim.enemyHP = Math.max(0, sim.enemyHP - enemyLoss);
  const allyMd  = calcMoraleDelta2(sim,'ally', allyLoss, enemyLoss, ai);
  const enemyMd = calcMoraleDelta2(sim,'enemy',enemyLoss,allyLoss,  null);
  sim.allyMorale  = cl(sim.allyMorale  + allyMd,  0, 100);
  sim.enemyMorale = cl(sim.enemyMorale + enemyMd, 0, 100);
  }
  const animType = (allyLoss||0) > sim.allyMax * .1 ? 'shake' : 'clash';
  updateSoldiers(sim.allyHP, sim.allyMax, sim.enemyHP, sim.enemyMax, animType);
  updateMoraleBars(sim.allyMorale, sim.enemyMorale);
  updateMoraleStatus(sim.allyMorale, sim.enemyMorale);
  if ((allyLoss||0) > sim.allyMax * .1) screenFlash('red');
  else if ((enemyLoss||0) > sim.enemyMax * .1) screenFlash('gold');
  if (rnd() < ai.chargePct) {
  const u = pick(units);
  addLog('⚔', 'ally-ic', pickUnitLog('charge', units, wn), 'bold', `${u}が前進`);
  }
  if ((allyLoss||0) > sim.allyMax * .12) {
  addLog('💀', 'enemy-ic', pickUnitLog('suffer', units, wn), 'rout-text', `損害 -${allyLoss||0}人`);
  } else if ((enemyLoss||0) > sim.enemyMax * .12) {
  addLog('💥', 'neutral', pickUnitLog('rout', eu, wn), 'gold-text', `敵損害 -${enemyLoss||0}人`);
  } else {
  addLog('⚔', 'neutral',
  `${pick(units)}と${pick(eu)}が激突`, '',
  `味方-${allyLoss||0} / 敵-${enemyLoss||0}人`);
  }
  if (sim.allyMorale <= 10) {
  addLog('📉', 'neutral', pickUnitLog('morale_dn', units, wn), '', `士気 ${Math.round(sim.allyMorale)}`);
  } else if (isFinalTurn && result.won) {
  addLog('📈', 'ally-ic', pickUnitLog('morale_up', units, wn), 'gold-text', `士気 ${Math.round(sim.allyMorale)}`);
  }
  if (ti % 2 === 1) {
  addLog('⚡', 'drama-ic', pickUnitLog('general', units, wn), 'bold', '');
  }
  if (rnd() < ai.skillRate * .5 && w.skill) {
  addLog(w.skill.ic, 'drama-ic', `${wn}の「${w.skill.nm}」発動！`, 'gold-text', w.skill.ef);
  }
  if (sim.enemyMorale <= 20 && sim.enemyHP < sim.enemyMax*.5) {
  sim.routed = 'enemy';
  } else if (sim.allyMorale <= 20 && sim.allyHP < sim.allyMax*.5) {
  sim.routed = 'ally';
  }
  }, delay + t * T_TURN));
  }
  delay += TURN_COUNT * T_TURN + 400;
  if (result.reversalTriggered) {
  battleTimers.push(setTimeout(() => {
  showReversalOverlay();
  addLog('🌟', 'drama-ic', pickUnitLog('reversal', units, wn), 'gold-text', '奇跡的な反攻！');
  screenFlash('gold');
  }, delay));
  delay += 1800;
  }
  if (result.allyFinal <= 0 || result.enemyFinal <= 0 || result.allyMorale <= 20) {
  battleTimers.push(setTimeout(() => {
  addLog('⚡', 'drama-ic', `両軍消耗！${wn} vs ${bd.en}、大将同士の対決へ！`, 'bold', '一騎討ち');
  }, delay));
  delay += T_LOG * 2;
  battleTimers.push(setTimeout(() => {
  const won = result.won;
  addLog(won ? '🌟' : '🩸', won ? 'drama-ic' : 'enemy-ic',
  won ? `${wn}、${bd.en}を撃破！` : `${bd.en}の猛攻に押される…`,
  won ? 'gold-text' : 'rout-text', '一騎討ちの結末');
  }, delay));
  delay += T_LOG * 2;
  }
  battleTimers.push(setTimeout(() => {
  const won = result.won;
  updateSoldiers(
  won ? result.allyFinal : 0,
  result.allyMax,
  won ? 0 : result.enemyFinal,
  result.enemyMax,
  'rout'
  );
  updateMoraleBars(result.allyMorale, result.enemyMorale);
  screenFlash(won ? 'gold' : 'red');
  showRoutOverlay(won);
  if (result.rk !== 'draw') {
  addLog(won ? '💥' : '🏳', won ? 'drama-ic' : 'rout-ic',
  won ? pickUnitLog('rout', eu, wn) : '味方、退却を決断…',
  won ? 'gold-text' : 'rout-text',
  won ? '敵軍完全崩壊' : '兵を収め陣を退く');
  }
  }, delay));
  delay += 2000;
  battleTimers.push(setTimeout(() => {
  const label = result.rk==='win'?'勝利':result.rk==='draw'?'引き分け':'敗戦';
  addLog(result.won?'🏆':'📜', 'neutral', bd.fi, result.won?'gold-text':'', '');
  addLogFinal(label, result.won ? '武名、さらに轟く' : 'また刃を交える日を待て');
  const repNow = G.warrior.rep;
  const repNew = Math.min(999, Math.max(0, repNow + result.rg));
  const repMax = Math.max(200, Math.max(repNow, repNew) + 20);
  animGauge('b-rep','b-rep-fill', repNow, repNew, repMax);
  animGauge('b-mer','b-mer-fill', G.warrior.mer, G.warrior.mer+result.mg, Math.max(500, G.warrior.mer+result.mg+20));
  $el('b-next-btn').classList.add('rdy');
  }, delay));
}
function skipBattle() {
  clearBattleTimers();
  if (!currentBattle || !pendingResult) return;
  const result = pendingResult;
  const w = G.warrior;
  const bd = currentBattle;
  $el('battle-log-area').innerHTML = '';
  updateSoldiers(
  result.won ? result.allyFinal : 0,
  result.allyMax || 1000,
  result.won ? 0 : result.enemyFinal,
  result.enemyMax || 1000,
  'normal'
  );
  updateMoraleBars(result.allyMorale, result.enemyMorale);
  addLog('⚔','neutral','激戦の末…','','全軍が奮戦した');
  if (result.rk !== 'draw') {
  addLog(result.won?'💥':'🏳', result.won?'drama-ic':'rout-ic',
  result.won ? '敵軍、総崩れ！' : '味方、退却…',
  result.won?'gold-text':'rout-text','');
  }
  const label = result.rk==='win'?'勝利':result.rk==='draw'?'引き分け':'敗戦';
  addLogFinal(label, bd.fi);
  const repNow = w.rep;
  const repNew = Math.min(999, Math.max(0, repNow + result.rg));
  const repMax = Math.max(200, Math.max(repNow, repNew) + 20);
  animGauge('b-rep','b-rep-fill', repNow, repNew, repMax);
  animGauge('b-mer','b-mer-fill', w.mer, w.mer+result.mg, Math.max(500, w.mer+result.mg+20));
  $el('b-next-btn').classList.add('rdy');
}
function afterBattle() {
  if (!currentBattle || !pendingResult) return;
  const w = G.warrior;
  const { won, rk, rg, mg } = pendingResult;
  w.rep  = Math.min(999, Math.max(0, w.rep + rg));
  w.mer += mg;
  w.age += 1 + rn(2);
  w.btls++;
  if (!won && rk==='loss') G.lossStreak++; else G.lossStreak=0;
  if (w.btls === 1) {
  const fb = traitApply('first_battle');
  if (fb.repBonus) w.rep = Math.min(999, w.rep + fb.repBonus);
  }
  G.battles.push({
  n:currentBattle.n, er:currentBattle.er,
  lo:currentBattle.lo, en:currentBattle.en,
  res:rk, fi:currentBattle.fi, rg, mg,
  boss:currentBattle.boss||0,
  allyFinal:pendingResult.allyFinal,
  enemyFinal:pendingResult.enemyFinal,
  personality:w.personality?.label||'—',
  });
  pendingResult=null; currentBattle=null; battleSim=null;
  if (checkDeath()) return;
  if (!won && rk==='loss' && G.lossStreak>=2 && tryAwaken()) return;
  renderHome();
  goScreen('screen-home');
}
function clearBattleTimers() { battleTimers.forEach(clearTimeout); battleTimers=[]; }
function animGauge(valId, fillId, from, to, maxVal) {
  const vEl=$el(valId), fEl=$el(fillId);
  if (!vEl || !fEl) return;
  let step=0;
  const timerId=setInterval(()=>{
  step++;
  const cur=Math.round(from+(to-from)*(step/30));
  vEl.textContent=cur;
  fEl.style.width=Math.min(Math.max(cur/maxVal*100,0),100)+'%';
  if(step>=30) clearInterval(timerId);
  },40);
}
function renderBornScreen() {
  const w=G.warrior;
  $el('bnm').textContent=w.name; $el('bep').textContent=w.ep;
  $el('bheri').textContent = w._inheritText
  ? w._inheritText
  : `父：${w.fa}の血 × 母：${w.mo}の血　（第${w.gen}代）`;
  $el('bstats').innerHTML=STAT_KEYS.map(([k,lbl])=>`
  <div class="scell"><div class="snm">${lbl}</div><div class="sv">${w.s[k]}</div>
  <div class="sbar"><div class="sbf" data-t="${w.s[k]}%" style="width:0"></div></div></div>`).join('');
  $el('bskill').innerHTML=renderSkillBlock(w);
  let traitHtml = '';
  const tc = (t,label) => t ? `<span class="btrait" style="margin:2px 4px;color:${t.color?.startsWith('var(')?'#b06bff':(t.color||'#888')};border-color:${t.color?.startsWith('var(')?'#b06bff':(t.color||'#888')}">${label}：${t.label}</span>` : '';
  traitHtml += tc(w.faTrait,'父');
  traitHtml += tc(w.moTrait,'母');
  if (w.affinity && !w.affinity.malus) {
  const clr = w.affinity.level==='great'?'#e65100':'#c8941a';
  traitHtml += `<span class="btrait" style="color:${clr};border-color:${clr}">${w.affinity.ic} ${w.affinity.label}</span>`;
  } else if (w.affinity?.malus) {
  traitHtml += `<span class="btrait" style="color:#78909c;border-color:#78909c">💀 ${w.affinity.label}</span>`;
  }
  if (traitHtml) {
  $el('bskill').innerHTML += `<div style="padding:4px 20px 8px;display:flex;flex-wrap:wrap;gap:4px;justify-content:center">${traitHtml}</div>`;
  }
  const pers=w.personality||PERSONALITIES[0];
  $el('bpersonality').innerHTML=`<span class="personality-badge ${pers.cls}" style="opacity:0;animation:personalityBadge .6s .3s cubic-bezier(.22,1,.36,1) forwards">${pers.icon} ${pers.label}　<span style="font-weight:400;opacity:.7">${pers.desc}</span></span>`;
  setTimeout(()=>{ $el('bstats').querySelectorAll('.sbf').forEach(e=>e.style.width=e.dataset.t); },300);
}
function renderHome() {
  const w=G.warrior; if(!w) return;
  $el('hpanel').className='hpanel'+(w.mut?' mut':'');
  $el('hnm').textContent=w.name; $el('hep').textContent=w.ep;
  $el('hskill').innerHTML=renderSkillBadges(w);
  $el('hrep').textContent=w.rep;
  $el('hrepf').style.width=Math.min(w.rep/2,100)+'%';
  renderLifespanGauge(w);
  $el('hage').textContent=w.age; $el('hbtl').textContent=w.btls; $el('hmer').textContent=w.mer;
  renderBossMenuItem(w);
}
function renderLifespanGauge(w) {
  const rem=Math.max(0,w.maxAge-w.age), range=Math.max(1,w.maxAge-15);
  const ratio=Math.max(0,rem/range);
  $el('hlife').textContent=rem>0?`残り約${rem}年`:'余命僅か';
  $el('hlifef').style.width=Math.min(ratio*100,100)+'%';
  $el('hlifef').className='lf'+(ratio<.25?' danger':'');
}
function renderBossMenuItem(w) {
  const menu=$el('hmenu'); const old=$el('boss-mi'); if(old) old.remove();
  if(w.rep>=150){
  const el=document.createElement('div'); el.id='boss-mi'; el.className='mi boss';
  el.innerHTML=`<div class="miic" style="background:linear-gradient(135deg,#8b1a1a,#c0392b)">👑</div><div><div class="mit" style="color:var(--red-l)">天下への挑戦</div><div class="mid">信長が待ち受ける、最後の戦い</div></div><div class="mia">›</div>`;
  el.onclick=startBossBattle; menu.appendChild(el);
  }
}
function viewStatus() {
  const w=G.warrior; if(!w) return;
  const pers=w.personality||PERSONALITIES[0];
  const sg=STAT_KEYS.map(([k,lbl])=>`<div class="scell"><div class="snm">${lbl}</div><div class="sv">${w.s[k]}</div><div class="sbar"><div class="sbf" style="width:${w.s[k]}%"></div></div></div>`).join('');
  const mb=w.mut?`<div class="skd mut" style="margin-top:0"><span class="skic">✦</span><div><div class="sknm">覚醒状態</div><div class="skef">全ステ+8、鍛錬効果+10% 補正中</div></div></div>`:'';
  let traitSection = '';
  const tc2 = (t,label) => t ? `<div style="display:flex;align-items:center;gap:6px;padding:6px 0;border-bottom:1px solid var(--border)"><span style="font-size:10px;opacity:.45;width:2em">${label}</span><span class="btrait" style="color:${t.color?.startsWith('var(')?'#b06bff':(t.color||'#888')};border-color:${t.color?.startsWith('var(')?'#b06bff':(t.color||'#888')}">${t.label}</span><span style="font-size:10px;opacity:.55;margin-left:4px">${t.desc}</span></div>` : '';
  traitSection += tc2(w.faTrait,'父');
  traitSection += tc2(w.moTrait,'母');
  if (w.affinity) {
  const clr = w.affinity.malus ? '#78909c' : (w.affinity.level==='great'?'#e65100':'#c8941a');
  traitSection += `<div style="display:flex;align-items:center;gap:6px;padding:6px 0"><span style="font-size:10px;opacity:.45;width:2em">相性</span><span class="btrait" style="color:${clr};border-color:${clr}">${w.affinity.ic} ${w.affinity.label}</span><span style="font-size:10px;opacity:.55;margin-left:4px">${w.affinity.bonus}</span></div>`;
  }
  const traitBlock = traitSection ? `<div style="padding:8px 20px 4px;border-top:1px solid var(--border)">${traitSection}</div>` : '';
  $el('scontent').innerHTML=`
  <div class="rc" style="margin:20px"><div class="rch"><div class="wnm">${w.name}</div><div class="wep">${w.ep}</div></div><div class="sgrid">${sg}</div></div>
  ${renderSkillBlock(w)}${mb}
  ${traitBlock}
  <div style="padding:12px 20px;text-align:center"><span class="personality-badge ${pers.cls}">${pers.icon} ${pers.label}　<span style="font-weight:400;opacity:.75">${pers.desc}</span></span></div>
  <div style="padding:8px 20px;font-size:12px;color:rgba(26,18,8,.5);letter-spacing:.08em;line-height:2.2">
  <div>父：${w.fa}　母：${w.mo}</div><div>年齢：${w.age}歳　寿命：${w.maxAge}歳まで</div>
  <div>名声：${w.rep}　功績：${w.mer}</div><div>出陣：${w.btls}回</div>
  <div>第${w.gen||1}代${w.parentName?'（'+w.parentName+'の子）':''}</div>
  <div>血統上限：${genStatCap(w.gen)}　${w.gen>=6?'【完全解放】':w.gen>=5?'【解放済】':'（第5代で92、第6代で完全解放）'}</div>
  </div>`;
  goScreen('screen-status');
}
function renderHistory() {
  const list=$el('hlist');
  if(!G.battles.length){
  list.innerHTML=`<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px 20px;gap:12px;text-align:center;opacity:.5"><div style="font-size:48px">📜</div><div style="font-size:14px;letter-spacing:.1em">まだ合戦の記録はありません</div></div>`;
  return;
  }
  list.innerHTML=[...G.battles].reverse().map(b=>`
  <div class="hcard">
  <div class="hch"><div class="hcn">${b.boss?'👑 ':''}${b.n}</div><div class="hbadge ${b.res==='win'?'bw':b.res==='draw'?'bd':'bl'}">${b.res==='win'?'勝':b.res==='loss'?'敗':'分'}</div></div>
  <div class="hcb">
  <div class="hst"><div class="hsl">時代</div><div class="hsv" style="font-size:11px">${b.er}</div></div>
  <div class="hst"><div class="hsl">名声</div><div class="hsv" style="${b.rg<0?'color:var(--red-l)':''}">${b.rg>=0?'+':''}${b.rg}</div></div>
  <div class="hst"><div class="hsl">功績</div><div class="hsv">+${b.mg}</div></div>
  </div>
  ${b.personality?`<div style="padding:0 14px 4px;font-size:10px;color:rgba(26,18,8,.4)">性格：${b.personality} / 残兵 ${(b.allyFinal||0).toLocaleString()}人</div>`:''}
  <div style="padding:0 14px 10px;font-size:11px;color:rgba(26,18,8,.45)">▶ ${b.fi}</div>
  </div>`).join('');
}
function checkDeath() {
  const w=G.warrior; if(!w||w.age<w.maxAge) return false;
  const score=w.rep+f(w.mer/2)+w.btls*5;
  const rank=RANK_TABLE.find(r=>score>=r.m)||RANK_TABLE[RANK_TABLE.length-1];
  $el('dnm').textContent=w.name; $el('dep').textContent=w.ep; $el('dage').textContent=`享年 ${w.age} 歳`;
  const rv=$el('drank'); rv.textContent=rank.r; rv.className='rv '+rank.c;
  $el('drcmt').textContent=rank.cm;
  const wins=G.battles.filter(b=>b.res==='win').length, losses=G.battles.filter(b=>b.res==='loss').length;
  $el('dsum').innerHTML=[
  ['最終名声',w.rep],['総功績',w.mer],['出陣回数',w.btls],
  ['勝利数',wins],['敗北数',losses],['鍛錬回数',G.trainCnt],
  ['スコア',score],['世代',`第${w.gen||1}代`],['性格',w.personality?.label||'—'],
  ].map(([l,v])=>`<div class="dsi"><span class="dsl">${l}</span><span class="dsv">${v}</span></div>`).join('');
  goScreen('screen-death'); return true;
}
function renderSkillBlock(w) {
  if(!w.skill) return '';
  return `<div class="skd${w.mut?' mut':''}"><span class="skic">${w.skill.ic}</span><div><div class="sknm">${w.skill.nm}</div><div class="skef">${w.skill.ef}</div></div></div>`;
}
function renderSkillBadges(w) {
  let h='';
  if(w.personality) h+=`<span class="skb ${w.personality.cls}" style="margin-right:4px">${w.personality.icon} ${w.personality.label}</span>`;
  if(w.skill) h+=`<span class="skb">${w.skill.ic} ${w.skill.nm}</span>`;
  if(w.mut)   h+=`<span class="skb mut">✦ 覚醒</span>`;
  return h;
}</script>
</body>
</html>
