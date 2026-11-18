from pathlib import Path
import re

app = next(Path("appsrc").rglob("package.json")).parent
hp = app / "www" / "index.html"
jp = app / "www" / "app.js"
h = hp.read_text(encoding="utf-8")
s = jp.read_text(encoding="utf-8")

# Compact the three money inputs without making their values hard to read.
css = r"""
/* Compact money fields approved in the UI review */
#receivedAmountWrap{flex:0 1 46%;max-width:46%;min-width:138px}
#receivedAmountWrap input,
#shippingCost,#shippingCharge{
  min-height:36px!important;height:38px!important;padding:7px 9px!important;
  font-size:14px!important;line-height:1.25!important;font-variant-numeric:tabular-nums
}
#shippingCost,#shippingCharge{width:100%;box-sizing:border-box}
#shippingCost,#shippingCharge{direction:ltr!important;text-align:left!important}
#receivedAmount{direction:ltr!important;text-align:left!important}
@media(max-width:420px){
 #receivedAmountWrap{min-width:0;flex-basis:48%;max-width:48%}
 #receivedAmountWrap input,#shippingCost,#shippingCharge{font-size:13px!important;padding:6px 7px!important}
}
input[type=number]{direction:ltr!important;text-align:left!important;font-variant-numeric:tabular-nums}
#saveSuccessOverlay{position:fixed;inset:0;z-index:100000;background:rgba(15,23,42,.48);display:flex;align-items:center;justify-content:center;padding:16px;box-sizing:border-box}
#saveSuccessCard{width:min(440px,100%);max-height:88vh;overflow:auto;background:#fff;border-radius:18px;box-shadow:0 18px 55px rgba(0,0,0,.24);padding:18px;direction:rtl;color:#172033;font-family:inherit}
#saveSuccessCard .ss-head{display:flex;align-items:center;gap:10px;margin-bottom:12px}
#saveSuccessCard .ss-check{width:38px;height:38px;border-radius:50%;background:#e8f7ef;color:#16834b;display:grid;place-items:center;font-size:23px;font-weight:bold;flex:none}
#saveSuccessCard h3{font-size:17px;margin:0}
#saveSuccessCard .ss-sub{font-size:12px;color:#64748b;margin-top:3px}
#saveSuccessCard .ss-meta{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0}
#saveSuccessCard .ss-meta div,#saveSuccessCard .ss-row{background:#f7f9fc;border-radius:10px;padding:9px}
#saveSuccessCard small{display:block;color:#64748b;font-size:11px;margin-bottom:4px}
#saveSuccessCard b,#saveSuccessCard strong{font-variant-numeric:tabular-nums}
#saveSuccessCard .ss-items{border:1px solid #e5eaf1;border-radius:10px;padding:9px;margin:10px 0}
#saveSuccessCard .ss-item{display:grid;grid-template-columns:minmax(0,1fr) auto auto;gap:8px;padding:6px 0;border-bottom:1px solid #edf0f4;font-size:12px}
#saveSuccessCard .ss-item:last-child{border-bottom:0}
#saveSuccessCard .ss-num{direction:ltr;text-align:left;white-space:nowrap;font-weight:700}
#saveSuccessCard .ss-money{display:grid;gap:7px}
#saveSuccessCard .ss-row{display:flex;justify-content:space-between;align-items:center;gap:10px;font-size:12px}
#saveSuccessCard .ss-row .ss-num{font-size:13px}
#saveSuccessCard .ss-sale .ss-num{color:#2878d0}
#saveSuccessCard .ss-due .ss-num{color:#d97706;font-weight:800}
#saveSuccessCard .ss-received .ss-num{color:#20a464}
#saveSuccessCard .ss-remaining .ss-num{color:#dc4545}
#saveSuccessCard .ss-currency{display:flex;align-items:center;justify-content:space-between;margin:12px 0;font-size:13px}
#saveSuccessCard .ss-currency strong{font-size:17px}
#saveSuccessCard .ss-close{width:100%;border:0;border-radius:11px;background:#1877c9;color:#fff;padding:12px;font-weight:700;font-size:14px}
"""
if "</style></head>" in h:
    h = h.replace("</style></head>", css + "\n</style></head>", 1)
elif "</head>" in h:
    h = h.replace("</head>", "<style>" + css + "</style></head>", 1)
else:
    raise SystemExit("Could not find HTML head to add approved styles")

# Native number controls use the device/browser locale; remove earlier forced English locale.
s = s.replace("x.lang='en';", "x.lang=(navigator.language||document.documentElement.lang||'ar');")
s = s.replace("a.lang='en';", "a.lang=(navigator.language||document.documentElement.lang||'ar');")
s = s.replace("$('amountReceived').lang='en';", "$('amountReceived').lang=(navigator.language||document.documentElement.lang||'ar');")
s = s.replace('lang="en"', 'lang=""')
# Ensure all existing and dynamically-created numeric inputs inherit the device locale.
locale_logic = r"""
function applyDeviceNumberLocale(root=document){
  const locale=(navigator.languages&&navigator.languages[0])||navigator.language||document.documentElement.lang||'ar';
  root.querySelectorAll('input[type="number"]').forEach(el=>{el.lang=locale;el.style.direction='ltr';el.style.textAlign='left';});
}
document.addEventListener('DOMContentLoaded',()=>applyDeviceNumberLocale());
"""
if "function applyDeviceNumberLocale(root=document)" not in s:
    s += "\n" + locale_logic + "\n"
# Re-apply locale to new item inputs after rows are created.
s = s.replace("updateLineTotal(d);calcSummary();\n}", "updateLineTotal(d);applyDeviceNumberLocale(d);calcSummary();\n}", 1)

# Replace the save handler with a post-save, centered confirmation containing real saved values.
success_logic = r"""
function successCurrency(code){
 const m={SAR:'🇸🇦 SAR',USD:'🇺🇸 USD',YER:'🇾🇪 YER'};
 return m[code]||code||'';
}
function successNumber(value,code){
 const locale=(navigator.languages&&navigator.languages[0])||navigator.language||document.documentElement.lang||'ar';
 try{return new Intl.NumberFormat(locale,{minimumFractionDigits:2,maximumFractionDigits:2,useGrouping:true}).format(Number(value||0));}
 catch(e){return Number(value||0).toFixed(2);}
}
function showSavedOrderSummary(o){
 const t=totals(o),received=Number(o.amountReceived||0),remaining=Math.max(0,t.due-received);
 const escv=v=>esc(String(v??''));
 const itemRows=(o.items||[]).map(x=>'<div class="ss-item"><span>'+escv(x.name)+'</span><span class="ss-num">'+successNumber(x.qty,o.currency)+' × '+successNumber(x.price,o.currency)+'</span><strong class="ss-num">'+successNumber(Number(x.qty||0)*Number(x.price||0),o.currency)+'</strong></div>').join('');
 const old=document.getElementById('saveSuccessOverlay');if(old)old.remove();
 const overlay=document.createElement('div');overlay.id='saveSuccessOverlay';overlay.setAttribute('role','dialog');overlay.setAttribute('aria-modal','true');overlay.setAttribute('aria-label','تم حفظ الطلب بنجاح');
 overlay.innerHTML='<section id="saveSuccessCard"><div class="ss-head"><div class="ss-check">✓</div><div><h3>تم حفظ الطلب بنجاح</h3><div class="ss-sub">ملخص بيانات الطلب المحفوظ</div></div></div><div class="ss-meta"><div><small>رقم الطلب</small><b>'+escv(o.id)+'</b></div><div><small>اسم العميل</small><b>'+escv(o.customerName)+'</b></div><div><small>عدد الأصناف</small><b>'+successNumber((o.items||[]).length,o.currency)+' صنف</b></div><div><small>حالة الدفع</small><b>'+escv(o.paymentStatus||'بانتظار الدفع')+'</b></div></div><div class="ss-items">'+(itemRows||'<div class="ss-sub">لا توجد أصناف</div>')+'</div><div class="ss-money"><div class="ss-row"><span>إجمالي تكلفة البضاعة</span><strong class="ss-num">'+successNumber(t.cost,o.currency)+'</strong></div><div class="ss-row ss-sale"><span>إجمالي بيع البضاعة</span><strong class="ss-num">'+successNumber(t.sale,o.currency)+'</strong></div><div class="ss-row"><span>تكلفة الشحن الفعلية</span><strong class="ss-num">'+successNumber(o.shippingCost,o.currency)+'</strong></div><div class="ss-row"><span>تكلفة الشحن على العميل</span><strong class="ss-num">'+successNumber(o.shippingCharge,o.currency)+'</strong></div><div class="ss-row ss-due"><b>المطلوب من العميل</b><strong class="ss-num">'+successNumber(t.due,o.currency)+'</strong></div><div class="ss-row ss-received"><span>المبلغ المستلم</span><strong class="ss-num">'+successNumber(received,o.currency)+'</strong></div><div class="ss-row ss-remaining"><span>المبلغ المتبقي</span><strong class="ss-num">'+successNumber(remaining,o.currency)+'</strong></div></div><div class="ss-currency"><span>العملة</span><strong>'+successCurrency(o.currency)+'</strong></div><button type="button" class="ss-close" id="closeSavedOrderSummary">حسناً</button></section>';
 document.body.appendChild(overlay);
 const close=()=>overlay.remove();
 overlay.querySelector('#closeSavedOrderSummary').addEventListener('click',close);
 overlay.addEventListener('click',e=>{if(e.target===overlay)close();});
}
async function confirmSaveOrder(){
 const o=formData(),error=validate(o);if(error){alert(error);$('modal').classList.add('hidden');return;}
 const idx=orders.findIndex(x=>x.id===o.id);if(idx>=0)orders[idx]=o;else orders.unshift(o);
 await saveAll();
 $('modal').classList.add('hidden');
 clearForm();
 showPage('orders');
 showSavedOrderSummary(o);
}
"""
# Keep the existing listener; function declarations resolve to this latest definition.
if "function showSavedOrderSummary(o)" not in s:
    s += "\n" + success_logic + "\n"

hp.write_text(h, encoding="utf-8")
jp.write_text(s, encoding="utf-8")
print("Applied compact fields, device-locale number display, and centered saved-order summary")
