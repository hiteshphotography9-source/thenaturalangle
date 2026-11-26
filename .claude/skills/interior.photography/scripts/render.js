const {chromium}=require('playwright');
(async()=>{const dir=process.argv[2],ids=process.argv[3].split(',');
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:1500}});
await p.goto('file://'+dir+'/slides.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(2500);
for(const id of ids){await p.locator('#'+id).screenshot({path:dir+'/'+id+'.png'});}
await b.close();})();
