(self.webpackChunk_retrolab_lab_extension=self.webpackChunk_retrolab_lab_extension||[]).push([[568],{568:(e,a,t)=>{"use strict";t.r(a),t.d(a,{default:()=>s});var o,r=t(770),n=t(148),l=t(77),c=t(337),d=t(125),i=t(456),m=t(706),b=t(714);!function(e){e.launchRetroTree="retrolab:launch-tree",e.openRetro="retrolab:open-retro",e.openClassic="retrolab:open-classic",e.openLab="retrolab:open-lab"}(o||(o={}));const u={id:"@retrolab/lab-extension:interface-switcher",autoStart:!0,requires:[i.ITranslator],optional:[d.INotebookTracker,n.ICommandPalette,c.IMainMenu,b.IRetroShell,r.ILabShell],activate:(e,a,t,o,r,n,c)=>{if(!t)return;const{commands:d,shell:i}=e,b=l.PageConfig.getBaseUrl(),u=a.load("retrolab"),s=new m.MenuBar,p=new m.Menu({commands:d});p.title.label=u.__("Interface"),s.addMenu(p);const h=()=>null!==t.currentWidget&&t.currentWidget===i.currentWidget,_=e=>{const{command:a,commandLabel:n,urlPrefix:l}=e;d.addCommand(a,{label:e=>e.noLabel?"":n,caption:n,execute:()=>{const e=t.currentWidget;e&&window.open(`${l}${e.context.path}`)},isEnabled:h}),o&&o.addItem({command:a,category:"Other"}),r&&r.viewMenu.addGroup([{command:a}],1),p.addItem({command:a})};_({command:"retrolab:open-classic",commandLabel:u.__("Open With %1","Classic Notebook"),buttonLabel:"openClassic",urlPrefix:`${b}tree/`}),n||_({command:"retrolab:open-retro",commandLabel:u.__("Open With %1","RetroLab"),buttonLabel:"openRetro",urlPrefix:`${b}retro/tree/`}),c||_({command:"retrolab:open-lab",commandLabel:u.__("Open With %1","JupyterLab"),buttonLabel:"openLab",urlPrefix:`${b}doc/tree/`}),t.widgetAdded.connect((async(e,a)=>{a.toolbar.insertBefore("kernelName","interface-switcher",s),await a.context.ready,d.notifyCommandChanged()}))}},s=[{id:"@retrolab/lab-extension:launch-retrotree",autoStart:!0,requires:[i.ITranslator],optional:[c.IMainMenu,n.ICommandPalette],activate:(e,a,t,r)=>{const{commands:n}=e,c=a.load("retrolab"),d=c.__("Help");n.addCommand(o.launchRetroTree,{label:c.__("Launch RetroLab File Browser"),execute:()=>{window.open(l.PageConfig.getBaseUrl()+"retro/tree")}}),t&&t.helpMenu.addGroup([{command:o.launchRetroTree}],1),r&&r.addItem({command:o.launchRetroTree,category:d})}},u]}}]);