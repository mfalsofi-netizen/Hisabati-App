from pathlib import Path
import re

app = next(Path("appsrc").rglob("package.json")).parent
hp = app / "www" / "index.html"
jp = app / "www" / "app.js"
h = hp.read_text(encoding="utf-8")
s = jp.read_text(encoding="utf-8")

css = r"""
/* Approved unified visual system for the New Order screen */
:root{
  --ho-blue:#1769c2;--ho-blue-dark:#10539e;--ho-blue-soft:#eaf3ff;
  --ho-border:#d7e5f8;--ho-text:#1e293b;--ho-muted:#64748b;
  --ho-shadow:0 5px 18px rgba(28,76,132,.07);
}
body{background:#f5f8fd!important;color:var(--ho-text)}
.new-order-screen{max-width:760px;margin-inline:auto;padding:12px 12px 24px!important}
.new-order-screen .panel,
.new-order-screen .customer-card,
.new-order-screen .items-card,
.new-order-screen .shipping-card,
.new-order-screen .payment-card,
.new-order-screen .summary-card{
  background:#fff!important;border:1px solid var(--ho-border)!important;
  border-radius:17px!important;box-shadow:var(--ho-shadow)!important;
  padding:13px!important;margin:0 0 13px!important;
}
.new-order-screen label{display:block;color:#334155!important;font-size:13px!important;font-weight:700!important;margin:0 0 6px!important}
.new-order-screen input:not([type=checkbox]),.new-order-screen select,.new-order-screen textarea{
  width:100%;min-width:0;box-sizing:border-box;border:1px solid #d6dfec!important;
  border-radius:11px!important;background:#fff!important;color:#172033!important;
  min-height:43px!important;padding:9px 11px!important;font-size:14px!important;
  box-shadow:inset 0 1px 2px rgba(15,23,42,.025)!important;
}
.new-order-screen input:focus,.new-order-screen select:focus,.new-order-screen textarea:focus{
  outline:none!important;border-color:#70a8eb!important;box-shadow:0 0 0 3px rgba(23,105,194,.10)!important
}
.new-order-screen .customer-card{
  display:grid!important;grid-template-columns:minmax(0,1fr) minmax(0,1fr)!important;
  gap:12px!important;align-items:end!important
}
.new-order-screen .customer-card>div{min-width:0}
.new-order-screen #customerName,.new-order-screen #customerPhone{font-weight:600}
.new-order-screen #pickContact{
  margin-top:7px!important;min-height:38px!important;padding:7px 11px!important;
  border-radius:10px!important;background:var(--ho-blue-soft)!important;
  color:var(--ho-blue-dark)!important;border:1px solid #c9def8!important;
  font-size:12px!important;font-weight:700!important
}
.new-order-screen .items-card{padding:0!important;overflow:hidden!important}
.new-order-screen .items-card .section-heading,
.new-order-screen .items-card h3,
.new-order-screen .items-card h2{
  background:linear-gradient(100deg,#edf5ff,#dcecff)!important;color:#174f91!important;
  padding:12px 14px!important;margin:0!important;font-size:16px!important;font-weight:800!important;
  border-bottom:1px solid #d9e8fb!important
}
.new-order-screen #items{padding:9px 10px 11px!important;overflow-x:auto!important}
.new-order-screen .itemline{
  display:grid!important;grid-template-columns:minmax(105px,1.7fr) 48px 72px 72px 72px 30px!important;
  gap:5px!important;min-width:390px!important;align-items:center!important;margin:6px 0!important
}
.new-order-screen .itemline-head{font-size:11px!important;color:#405875!important;font-weight:800!important}
.new-order-screen .itemline input{min-height:39px!important;padding:6px 5px!important;border-radius:9px!important;font-size:12px!important}
.new-order-screen .itemline .iname{text-align:right!important;font-size:12px!important}
.new-order-screen .itemline .lineTotal{min-height:39px!important;display:flex!important;align-items:center!important;justify-content:center!important;
  border:1px solid #d6e6fa!important;border-radius:9px!important;background:#edf5ff!important;color:#1559a6!important;
  font-size:11px!important;font-weight:800!important;white-space:nowrap!important}
.new-order-screen #addItem{margin:9px 11px 2px!important;min-height:38px!important;border-radius:10px!important;
  background:var(--ho-blue)!important;color:#fff!important;font-weight:700!important;padding:8px 13px!important}
.new-order-screen .shipping-card{
  display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:11px!important;align-items:end!important
}
.new-order-screen .shipping-card>div{min-width:0}
.new-order-screen .shipping-card input,
.new-order-screen #receivedAmountWrap input,
.new-order-screen #shippingCost,.new-order-screen #shippingCharge{
  height:40px!important;min-height:40px!important;padding:7px 9px!important;font-size:13px!important
}
.new-order-screen .payment-card{
  display:grid!important;grid-template-columns:minmax(0,1fr) minmax(0,1fr)!important;gap:11px!important;align-items:end!important
}
.new-order-screen #receivedAmountWrap{display:block!important;min-width:0!important;max-width:none!important;width:100%!important;flex:none!important}
.new-order-screen #paymentStatus{font-weight:700!important}
.new-order-screen #orderSummary{
  border:1px solid #f0dfaa!important;border-radius:16px!important;background:#fff9e8!important;
  padding:12px!important;margin:0!important
}
.new-order-screen .summary-card{padding:0!important;overflow:hidden!important}
.new-order-screen .summary-card #orderSummary{border:0!important;box-shadow:none!important}
.new-order-screen .sum-grid{display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:8px!important}
.new-order-screen .sum-item{border:1px solid #f0e5c5!important;border-radius:11px!important;background:#fffdf7!important;padding:10px!important;min-width:0!important}
.new-order-screen .sum-item small{font-size:11px!important;color:#64748b!important}
.new-order-screen .sum-item b{font-size:15px!important;font-weight:800!important;direction:ltr!important;text-align:left!important}
.new-order-screen .sum-due{background:#fff0d5!important;border-color:#f5d7a2!important}
.new-order-screen .sum-profit{background:#effaf3!important;border-color:#ccebd8!important}
.new-order-screen .actions,.new-order-screen .form-actions{
  display:flex!important;gap:9px!important;align-items:center!important
}
.new-order-screen #reviewOrder,.new-order-screen #confirmSave{
  background:linear-gradient(110deg,#1769c2,#1057a8)!important;color:#fff!important;
  border:0!important;border-radius:13px!important;min-height:49px!important;font-weight:800!important
}
.new-order-screen #clearForm{
  background:#fff!important;color:#475569!important;border:1px solid #cbd5e1!important;
  border-radius:13px!important;min-height:49px!important;font-weight:700!important
}
.new-order-screen input[type=number]{
  direction:ltr!important;text-align:left!important;font-variant-numeric:lining-nums tabular-nums!important;
  font-feature-settings:"lnum" 1,"tnum" 1!important
}
.new-order-screen .itemline input[type=number]{text-align:center!important}
@media(max-width:430px){
 .new-order-screen{padding:9px 9px 18px!important}
 .new-order-screen .customer-card,.new-order-screen .payment-card{gap:8px!important;padding:10px!important}
 .new-order-screen .customer-card input{font-size:13px!important}
 .new-order-screen .shipping-card{gap:8px!important;padding:10px!important}
 .new-order-screen .shipping-card label,.new-order-screen .payment-card label{font-size:11px!important}
 .new-order-screen .sum-grid{gap:6px!important}
 .new-order-screen .sum-item{padding:8px!important}
 .new-order-screen .sum-item b{font-size:13px!important}
}
"""

if "</style></head>" in h:
    h = h.replace("</style></head>", css + "\n</style></head>", 1)
elif "</head>" in h:
    h = h.replace("</head>", "<style>" + css + "</style></head>", 1)
else:
    raise SystemExit("Could not locate HTML head for the approved screen styles")

# Add semantic classes to existing form groups without moving controls or changing their IDs.
decorator = r"""
function applyApprovedNewOrderLayout(){
 const $id=id=>document.getElementById(id);
 const name=$id('customerName'),phone=$id('customerPhone'),items=$id('items');
 const shipping=$id('shippingCost'),charge=$id('shippingCharge'),received=$id('receivedAmountWrap');
 const payment=$id('paymentStatus'),summary=$id('orderSummary');
 const page=(name&&name.closest('.page'))||(items&&items.closest('.page'))||
   (name&&name.closest('main'))||(items&&items.closest('main'));
 if(page)page.classList.add('new-order-screen');
 const mark=(el,cls,selector)=>{if(!el)return null;let p=el.closest(selector||'.row')||el.parentElement;if(p)p.classList.add(cls);return p;};
 const customer=mark(name,'customer-card','.row');
 if(phone){let p=phone.closest('.row');if(p&&customer&&p!==customer)p.classList.add('customer-card');}
 if(items){
   let p=items.closest('.panel')||items.parentElement;
   if(p)p.classList.add('items-card');
   const add=$id('addItem');if(add&&p&&!p.contains(add))p.insertBefore(add,items);
 }
 if(shipping){
   let a=shipping.closest('.row')||shipping.parentElement;
   let b=charge&&(charge.closest('.row')||charge.parentElement);
   const card=(a&&b&&a===b)?a:(a&&a.parentElement&&a.parentElement===b?.parentElement?a.parentElement:(a||b));
   if(card)card.classList.add('shipping-card');
 }
 if(payment||received){
   let a=payment&&(payment.closest('.row')||payment.parentElement);
   let b=received&&(received.closest('.row')||received.parentElement);
   const card=(a&&b&&a===b)?a:(a&&b&&a.parentElement===b.parentElement?a.parentElement:(a||b));
   if(card)card.classList.add('payment-card');
 }
 if(summary){
   let p=summary.closest('.panel')||summary.parentElement;
   if(p)p.classList.add('summary-card');
 }
 // Keep all number controls and formatted totals in English numerals, independent of device language.
 const setEnglishNumbers=root=>{
   (root||document).querySelectorAll('input[type="number"]').forEach(el=>{
     el.lang='en-US';el.style.direction='ltr';el.style.textAlign='left';
     el.style.fontVariantNumeric='lining-nums tabular-nums';
   });
 };
 setEnglishNumbers(document);
 if(!window.__hisabatiEnglishNumbersObserver){
   window.__hisabatiEnglishNumbersObserver=new MutationObserver(records=>{
     records.forEach(rec=>rec.addedNodes.forEach(node=>{
       if(node.nodeType===1){if(node.matches&&node.matches('input[type="number"]')){node.lang='en-US';node.style.direction='ltr';node.style.textAlign='left';}setEnglishNumbers(node);}
     }));
   });
   window.__hisabatiEnglishNumbersObserver.observe(document.body,{childList:true,subtree:true});
 }
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',applyApprovedNewOrderLayout);
else applyApprovedNewOrderLayout();
window.addEventListener('load',applyApprovedNewOrderLayout);
"""
if "function applyApprovedNewOrderLayout()" not in s:
    s += "\n" + decorator + "\n"

# Force English digits in the save-success dialog and any locale-sensitive number formatter.
s = s.replace(
 "const locale=(navigator.languages&&navigator.languages[0])||navigator.language||document.documentElement.lang||'ar';",
 "const locale='en-US';"
)
s = s.replace(".toLocaleString()", ".toLocaleString('en-US')")
s = s.replace("new Intl.NumberFormat(locale,", "new Intl.NumberFormat('en-US',")
s = s.replace("function applyDeviceNumberLocale(root=document){", "function applyDeviceNumberLocale(root=document){")
s = s.replace("const locale=(navigator.languages&&navigator.languages[0])||navigator.language||document.documentElement.lang||'ar';\n  root.querySelectorAll('input[type=\"number\"]').forEach(el=>{el.lang=locale;", "const locale='en-US';\n  root.querySelectorAll('input[type=\"number\"]').forEach(el=>{el.lang=locale;")

hp.write_text(h, encoding="utf-8")
jp.write_text(s, encoding="utf-8")
print("Approved New Order visual layout and English numeral policy applied")
